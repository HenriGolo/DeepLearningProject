import cv2
import os
from ultralytics import YOLO

IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".jfif"]
DOSSIER = "./TEST"

model = YOLO("../runs/detect/pfc_model2/weights/best.pt")
#results = model("./TEST/IMG_20260217_134055.jpg", save=True)

for file in os.listdir(DOSSIER):
    for ext in IMAGE_EXTS:
        if file.endswith(ext):
            img_path = os.path.join(DOSSIER, file)
            results = model(img_path, save=True)

"""annotated = results[0].plot()

cv2.imshow("Result", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()"""

#PS : enristrement des prediction dans runs/detect/predict/