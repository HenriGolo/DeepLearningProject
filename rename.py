import os
BEGINING = 20

dossier = os.path.join(os.path.dirname(__file__), 'Images_Internet')

extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")

fichiers = [f for f in os.listdir(dossier) if f.lower().endswith(extensions)]

fichiers.sort()

# Renommage
for i, fichier in enumerate(fichiers, start=1):
    ancienne_path = os.path.join(dossier, fichier)
    extension = os.path.splitext(fichier)[1]
    nouveau_nom = f"internet{i+BEGINING}{extension}"
    nouvelle_path = os.path.join(dossier, nouveau_nom)

    os.rename(ancienne_path, nouvelle_path)

print("Renommage terminé !")