import os
import random
import cv2
import albumentations as A

IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".jfif"]
TRAIN_DIR = "./../TRAIN"
NUM_AUG = 300

"""A.Rotate(limit=30, border_mode=cv2.BORDER_REFLECT_101, p=0.7),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.HueSaturationValue(p=0.4),
    A.GaussianBlur(blur_limit=(3, 7), p=0.3),
    A.RandomScale(scale_limit=0.2, p=0.3),"""
transform = A.Compose([
    A.MotionBlur(blur_limit=(3, 9), p=0.3),   # flou de mouvement (réaliste pour webcam)
    A.ImageCompression(quality_lower=60, p=0.3),  # simule compression JPEG basse qualité
    A.RandomShadow(p=0.2),                     # ombres portées sur la main
    A.CoarseDropout(max_holes=4, max_height=30, max_width=30, p=0.3),  # occlusions partielles
], bbox_params=A.BboxParams(
    format="yolo",
    label_fields=["class_labels"],
    min_visibility=0.3,
))


def read_yolo_labels(label_path):
    bboxes, class_labels = [], []
    if not os.path.exists(label_path):
        return bboxes, class_labels
    with open(label_path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 5:
                class_labels.append(int(parts[0]))
                bboxes.append([float(x) for x in parts[1:]])
    return bboxes, class_labels


def write_yolo_labels(label_path, bboxes, class_labels):
    with open(label_path, "w") as f:
        for cls, box in zip(class_labels, bboxes):
            f.write(f"{int(cls)} {box[0]:.6f} {box[1]:.6f} {box[2]:.6f} {box[3]:.6f}\n")

all_img_paths = [
    os.path.join(TRAIN_DIR, f)
    for f in os.listdir(TRAIN_DIR)
    if any(f.lower().endswith(ext) for ext in IMAGE_EXTS)
    and "_aug_" not in f
]

if not all_img_paths:
    print("Aucune image trouvée dans", TRAIN_DIR)
    exit(1)

print(f"{len(all_img_paths)} images sources. Génération de {NUM_AUG} images augmentées...")

generated = 0
while generated < NUM_AUG:
    src_path = random.choice(all_img_paths)
    img = cv2.imread(src_path)
    if img is None:
        continue
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    base = os.path.splitext(src_path)[0]
    bboxes, class_labels = read_yolo_labels(base + ".txt")

    result = transform(image=img, bboxes=bboxes, class_labels=class_labels)

    src_name = os.path.splitext(os.path.basename(src_path))[0]
    out_name = f"{src_name}_aug_{generated}"
    out_img = os.path.join(TRAIN_DIR, out_name + ".jpg")
    out_lbl = os.path.join(TRAIN_DIR, out_name + ".txt")

    cv2.imwrite(out_img, cv2.cvtColor(result["image"], cv2.COLOR_RGB2BGR))
    write_yolo_labels(out_lbl, result["bboxes"], result["class_labels"])
    generated += 1

print(f"Done : {generated} images augmentées dans {TRAIN_DIR}")
