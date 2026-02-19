import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget, QRadioButton, QGroupBox
)
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QPoint


ANNOTATION_FILE = "annotation.txt"
SIZE_MIN = 10

CLASSES = {
    "chat": 0,
    "chien": 1,
    "voiture": 2
}


# ==========================================================
# ===================== IMAGE LABEL =========================
# ==========================================================

class ImageLabel(QLabel):
    HANDLE_SIZE = 8

    def __init__(self, main_window):
        super().__init__()
        # Permet de recevoir les événements clavier même si le focus est sur un autre widget
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

        self.main_window = main_window

        self.start_point = None
        self.current_rect = None

        # Boxes stockées en pixels IMAGE
        # {"x":..., "y":..., "w":..., "h":..., "class_id":...}
        self.boxes = []

        # Index de la box sélectionnée ou None
        self.selected_index = None

        self.resizing = False
        self.resize_corner = None
        

    # ------------------------------------------------------
    # OFFSET IMAGE DANS LABEL
    # ------------------------------------------------------

    def get_image_offset(self):
        pixmap = self.pixmap()
        if not pixmap:
            return 0, 0

        label_w = self.width()
        label_h = self.height()

        img_w = pixmap.width()
        img_h = pixmap.height()

        offset_x = (label_w - img_w) // 2
        offset_y = (label_h - img_h) // 2

        return offset_x, offset_y

    # ------------------------------------------------------
    # MOUSE EVENTS
    # ------------------------------------------------------

    def mousePressEvent(self, event):
        self.setFocus()
        self.main_window.update_class_selection()

        pos = event.pos()
        offset_x, offset_y = self.get_image_offset()

        # Vérifier clic sur box existante
        for i, box in enumerate(self.boxes):
            rect = QRect(
                int(box["x"] + offset_x),
                int(box["y"] + offset_y),
                int(box["w"]),
                int(box["h"])
            )

            # Selection d'une box
            if rect.contains(pos):
                self.selected_index = i
                # Met à jour les boutons radio de classe pour la box sélectionnée
                self.main_window.update_class_selection()
                
                # Vérifier si clic sur poignée de redimensionnement
                corner = self.get_corner(rect, pos)
                if corner:
                    self.resizing = True
                    self.resize_corner = corner

                self.update()
                return

        self.selected_index = None
        # Sinon création nouvelle box
        self.start_point = pos
        self.current_rect = QRect(pos, pos)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        offset_x, offset_y = self.get_image_offset()

        # Resize
        if self.resizing and self.selected_index is not None:
            box = self.boxes[self.selected_index]

            rect = QRect(
                # Passage en coordonnées absolues
                int(box["x"] + offset_x),
                int(box["y"] + offset_y),
                int(box["w"]),
                int(box["h"])
            )

            if self.resize_corner == "br":
                rect.setBottomRight(pos)
            elif self.resize_corner == "tl":
                rect.setTopLeft(pos)

            rect = rect.normalized()

            # Passage en coordonnées de l'image (relatives)
            box["x"] = rect.x() - offset_x
            box["y"] = rect.y() - offset_y
            box["w"] = rect.width()
            box["h"] = rect.height()

            self.update()
            return

        # Création en cours
        if self.start_point:
            self.current_rect = QRect(self.start_point, pos)
            self.update()

    def mouseReleaseEvent(self, event):
        offset_x, offset_y = self.get_image_offset()

        # Fin resize
        if self.resizing:
            box = self.boxes[self.selected_index]
            if box["w"] < SIZE_MIN or box["h"] < SIZE_MIN:
                del self.boxes[self.selected_index]
                self.selected_index = None

            self.resizing = False
            self.resize_corner = None
            self.update()
            return

        # Fin création
        if self.current_rect:
            rect = self.current_rect.normalized()

            if rect.width() >= SIZE_MIN and rect.height() >= SIZE_MIN:
                x_img = rect.x() - offset_x
                y_img = rect.y() - offset_y

                self.boxes.append({
                    "x": x_img,
                    "y": y_img,
                    "w": rect.width(),
                    "h": rect.height(),
                    "class_id": 0
                })

            self.current_rect = None
            self.start_point = None
            self.update()

    # ------------------------------------------------------
    # DRAWING
    # ------------------------------------------------------

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        offset_x, offset_y = self.get_image_offset()

        for i, box in enumerate(self.boxes):
            rect = QRect(
                int(box["x"] + offset_x),
                int(box["y"] + offset_y),
                int(box["w"]),
                int(box["h"])
            )

            if i == self.selected_index:
                pen = QPen(Qt.red, 2)
            else:
                pen = QPen(Qt.green, 2)

            painter.setPen(pen)
            painter.drawRect(rect)

            # poignées
            painter.fillRect(
                rect.right() - self.HANDLE_SIZE,
                rect.bottom() - self.HANDLE_SIZE,
                self.HANDLE_SIZE,
                self.HANDLE_SIZE,
                Qt.blue
            )

            painter.fillRect(
                rect.left(),
                rect.top(),
                self.HANDLE_SIZE,
                self.HANDLE_SIZE,
                Qt.blue
            )

        # dessin en cours
        if self.current_rect:
            painter.setPen(QPen(Qt.green, 2))
            painter.drawRect(self.current_rect.normalized())

    # ------------------------------------------------------

    def get_corner(self, rect, pos):
        br = QPoint(rect.right(), rect.bottom())
        if (abs(pos.x() - br.x()) < self.HANDLE_SIZE and
                abs(pos.y() - br.y()) < self.HANDLE_SIZE):
            return "br"

        tl = QPoint(rect.left(), rect.top())
        if (abs(pos.x() - tl.x()) < self.HANDLE_SIZE and
                abs(pos.y() - tl.y()) < self.HANDLE_SIZE):
            return "tl"

        return None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.selected_index is not None:
            del self.boxes[self.selected_index]
            self.selected_index = None
            self.update()


# ==========================================================
# ===================== MAIN WINDOW ========================
# ==========================================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.image_files = [
            f for f in os.listdir(".") if f.lower().endswith(".jpg")
        ]
        self.index = 0

        self.label = ImageLabel(self)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_image)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.next_button)

        # Classes
        self.class_group = QGroupBox("Classes")
        self.class_layout = QVBoxLayout()
        self.radio_buttons = []

        for name in CLASSES.keys():
            rb = QRadioButton(name)
            rb.toggled.connect(self.change_class)
            self.class_layout.addWidget(rb)
            self.radio_buttons.append(rb)

        self.class_group.setLayout(self.class_layout)
        layout.addWidget(self.class_group)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        if self.image_files:
            self.load_image()

    # ------------------------------------------------------

    def load_image(self):
        image_path = self.image_files[self.index]
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)

        # Reset des paramètre de l'image (rien de selectionné, pas de box en cours de création...)
        self.label.boxes = []
        self.label.selected_index = None
        self.label.current_rect = None
        self.label.start_point = None

        self.label.boxes = []
        self.load_annotations(image_path)

    def save_annotations(self):
        image_name = self.image_files[self.index]
        pixmap = self.label.pixmap()
        w = pixmap.width()
        h = pixmap.height()

        lines = []
        if os.path.exists(ANNOTATION_FILE):
            with open(ANNOTATION_FILE, "r") as f:
                lines = f.readlines()

        lines = [l for l in lines if not l.startswith(image_name)]

        for box in self.label.boxes:
            x = box["x"]
            y = box["y"]
            bw = box["w"]
            bh = box["h"]
            class_id = box["class_id"]

            x_center = (x + bw/2) / w
            y_center = (y + bh/2) / h
            width = bw / w
            height = bh / h

            lines.append(
                f"{image_name} {class_id} {x_center} {y_center} {width} {height}\n"
            )

        with open(ANNOTATION_FILE, "w") as f:
            f.writelines(lines)

    def load_annotations(self, image_name):
        if not os.path.exists(ANNOTATION_FILE):
            return

        pixmap = self.label.pixmap()
        w = pixmap.width()
        h = pixmap.height()

        with open(ANNOTATION_FILE, "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts[0] == image_name:
                    _, cls, xc, yc, bw, bh = parts
                    xc, yc, bw, bh = map(float, (xc, yc, bw, bh))

                    rect_w = bw * w
                    rect_h = bh * h
                    x = xc * w - rect_w/2
                    y = yc * h - rect_h/2

                    self.label.boxes.append({
                        "x": x,
                        "y": y,
                        "w": rect_w,
                        "h": rect_h,
                        "class_id": int(cls)
                    })

    def next_image(self):
        self.save_annotations()
        self.index += 1
        if self.index >= len(self.image_files):
            self.index = 0
        self.load_image()

    def change_class(self):
        idx = self.label.selected_index
        if idx is None:
            return

        for i, rb in enumerate(self.radio_buttons):
            if rb.isChecked():
                self.label.boxes[idx]["class_id"] = i
                self.label.update()

    def update_class_selection(self):
        idx = self.label.selected_index
        if idx is None:
            return

        class_id = self.label.boxes[idx]["class_id"]
        self.radio_buttons[class_id].setChecked(True)


# ==========================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 800)
    window.show()
    sys.exit(app.exec_())
