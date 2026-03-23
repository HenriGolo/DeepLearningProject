import os

# Extensions d'image possibles
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".bmp"]
DATA_TYPE = "TRAIN" #TEST
LABELISER_CLASS_PATH = os.path.join(os.path.dirname(__file__), 'labelizer', 'labelImg-master', 'data', 'predefined_classes.txt') # fichier class du labeliseur
DICO_CLASS = {}
DICO_CLASS_NUMBER = {}
def find_image(base_path, name):
    for ext in IMAGE_EXTS:
        img_path = os.path.join(base_path, name + ext)
        if os.path.exists(img_path):
            return img_path
    return None

def yolo_to_bbox(x_center, y_center, w, h, img_w, img_h):
    xmin = (x_center - w / 2) * img_w
    ymin = (y_center - h / 2) * img_h
    xmax = (x_center + w / 2) * img_w
    ymax = (y_center + h / 2) * img_h
    return xmin, ymin, xmax, ymax

def get_classes():
    global LABELISER_CLASS_PATH
    global DICO_CLASS
    with open(LABELISER_CLASS_PATH, "r") as f:
        for idx, line in enumerate(f, start=0):
            DICO_CLASS[idx] = line[:-1]
            DICO_CLASS_NUMBER[line[:-1]] = 0

def process_folder(folder_path, output_file):
    global DICO_CLASS
    with open(output_file, "w") as out:
        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                txt_path = os.path.join(folder_path, file)
                base_name = os.path.splitext(file)[0]

                img_path = find_image(folder_path, base_name)
                if img_path is None:
                    print(f"Image non trouvée pour {file}")
                    continue

                # Lire annotations
                with open(txt_path, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) != 5:
                            continue

                        # Format YOLO direct (normalisé)
                        cls, x, y, w, h = parts
                        DICO_CLASS_NUMBER[DICO_CLASS[int(cls)]]+=1
                        out.write(
                            f"{DATA_TYPE}\t{DICO_CLASS[int(cls)]}\t{img_path}\t{x}\t{y}\t{w}\t{h}\n"
                        )

if __name__ == "__main__":
    dossier ="./DB_images" #input("Chemin du dossier : ") #./DB_images
    output = "labels_formates.txt"
    get_classes()
    process_folder(dossier, output)
    print("Fichier généré !")
    print(DICO_CLASS_NUMBER)