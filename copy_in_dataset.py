import os
import shutil
import tkinter as tk
from tkinter import messagebox

def confirmer_action():
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale
    return messagebox.askyesno(
        "Confirmation",
        "⚠️ Attention ! Le contenu du dossier B va être supprimé.\n\nÊtes-vous sûr de vouloir continuer ?"
    )

def vider_dossier(dossier):
    if os.path.exists(dossier):
        for fichier in os.listdir(dossier):
            chemin = os.path.join(dossier, fichier)
            try:
                if os.path.isfile(chemin) or os.path.islink(chemin):
                    os.unlink(chemin)
                elif os.path.isdir(chemin):
                    shutil.rmtree(chemin)
            except Exception as e:
                print(f"Erreur lors de la suppression de {chemin} : {e}")

def copier_dossier(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)

def main():
    dossier_A = r".\TRAIN"
    dossier_B = r".\dataset\train\images"

    if not os.path.exists(dossier_A):
        print("Le dossier A n'existe pas.")
        return

    if confirmer_action():
        print("Suppression du contenu du dossier B...")
        vider_dossier(dossier_B)

        print("Copie en cours...")
        copier_dossier(dossier_A, dossier_B)

        print("Opération terminée.")
    else:
        print("Opération annulée.")

if __name__ == "__main__":
    main()