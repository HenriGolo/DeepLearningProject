import os

TRAIN_DIR = "./TRAIN"

deleted = 0
for f in os.listdir(TRAIN_DIR):
    if "_aug_" in f:
        os.remove(os.path.join(TRAIN_DIR, f))
        deleted += 1

print(f"{deleted} fichiers supprimés.")
