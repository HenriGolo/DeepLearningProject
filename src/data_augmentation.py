import os
import cv2
import random
import numpy as np
import shutil


IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".jfif"]
DOSSIER = "./TRAIN"
NEW_DOSSIER = "./TRAIN_AUG"
all_img_path = []
number_aug_img = 100

for file in os.listdir(DOSSIER):
    for ext in IMAGE_EXTS:
        if file.endswith(ext):
            img_path = os.path.join(DOSSIER, file)
            all_img_path.append(img_path)

for i in range (0, number_aug_img):

    img_path = all_img_path[random.randint(0, len(all_img_path)-1)]

    #randomly apply rotation, color filter and blur
    (rot, col, blu) = (random.randint(0, 1),
                               random.randint(0, 1),
                               random.randint(0, 1))
            
    img = cv2.imread(img_path)
    height, width = img.shape[:2]

    #rotation parameters
    if (rot==1):
        center = (width // 2, height // 2)
        angle = random.randint(1, 359)
        scale = 1.0

        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        img = cv2.warpAffine(img, rotation_matrix, (width, height))


        if (col==1):
            color_filter  = np.full((height,width,3), (random.randint(0, 255),
                                                           random.randint(0, 255),
                                                           random.randint(0, 255)),
                                                           np.uint8)
            img  = cv2.addWeighted(img, 0.8, color_filter, 0.2, 0)
        if (blu==1):
            ksize = random.randint(1, 10)
            img = cv2.blur(img,(ksize,ksize))
        
        #path without file extension
        update_path = img_path.split(".")
        print(update_path)
        only_img_name = update_path[1].split("/")

        new_path = "/" + only_img_name[2] + "_aug_" + str(rot) + "_" + str(col) + "_" + "_" + str(blu) + "_" + str(i)

        if (rot == 1):
            # A MODIFIER POUR CHANGER LES BOUNDINGS BOXS
            shutil.copy("." + update_path[1] + ".txt", NEW_DOSSIER + new_path + ".txt")
        else:
            shutil.copy("." + update_path[1] + ".txt", NEW_DOSSIER + new_path + ".txt")

        #save image
        
        cv2.imwrite(new_path + ".jpg", img)

        










