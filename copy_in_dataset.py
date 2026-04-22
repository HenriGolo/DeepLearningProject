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

def synchroniser_fichiers(source, destination, extensions_voulues=None, extensions_non_voulues=None):
    """
    Synchronise les fichiers entre source (A) et destination (B)

    Paramètres :
    - extensions_voulues : liste ou string (ex: ".jpg" ou [".jpg", ".png"])
    - extensions_non_voulues : liste ou string (ex: ".txt")

    Règles :
    - Si extensions_voulues est défini → on prend uniquement celles-ci
    - Sinon → on prend tout sauf extensions_non_voulues
    """

    def normaliser_ext(ext):
        if isinstance(ext, str):
            ext = [ext]
        return {e.lower() if e.startswith('.') else f".{e.lower()}" for e in ext} if ext else set()

    ext_ok = normaliser_ext(extensions_voulues)
    ext_ko = normaliser_ext(extensions_non_voulues)

    def fichier_valide(fichier):
        _, ext = os.path.splitext(fichier)
        ext = ext.lower()

        if ext_ok:
            return ext in ext_ok
        else:
            return ext not in ext_ko

    if not os.path.exists(source):
        print("Le dossier source n'existe pas.")
        return

    if not os.path.exists(destination):
        os.makedirs(destination)

    fichiers_A = {f for f in os.listdir(source) if fichier_valide(f)}
    fichiers_B = {f for f in os.listdir(destination) if fichier_valide(f)}

    a_supprimer = fichiers_B - fichiers_A
    a_copier = fichiers_A - fichiers_B

    # Suppression
    for fichier in a_supprimer:
        chemin = os.path.join(destination, fichier)
        try:
            os.remove(chemin)
            print(f"Supprimé : {fichier}")
        except Exception as e:
            print(f"Erreur suppression {fichier} : {e}")

    # Copie
    for fichier in a_copier:
        src_path = os.path.join(source, fichier)
        dst_path = os.path.join(destination, fichier)
        try:
            shutil.copy2(src_path, dst_path)
            print(f"Copié : {fichier}")
        except Exception as e:
            print(f"Erreur copie {fichier} : {e}")

    print("Synchronisation terminée.")

def override_dossier(source, destination, extensions_voulues=None, extensions_non_voulues=None, exclusions=None):
    if not os.path.exists(source):
        print("Le dossier source n'existe pas.")
        return

    if not os.path.exists(destination):
        os.makedirs(destination)

    exclusions = set(exclusions or [])

    def normaliser_ext(ext):
        if isinstance(ext, str):
            ext = [ext]
        return {e.lower() if e.startswith('.') else f".{e.lower()}" for e in ext} if ext else set()

    ext_ok = normaliser_ext(extensions_voulues)
    ext_ko = normaliser_ext(extensions_non_voulues)

    def fichier_valide(fichier):
        if fichier in exclusions:
            return False

        _, ext = os.path.splitext(fichier)
        ext = ext.lower()

        if ext_ok:
            return ext in ext_ok
        else:
            return ext not in ext_ko

    # 🔥 Suppression complète du dossier B
    for fichier in os.listdir(destination):
        chemin = os.path.join(destination, fichier)
        try:
            if os.path.isfile(chemin) or os.path.islink(chemin):
                os.remove(chemin)
            else:
                shutil.rmtree(chemin)
        except Exception as e:
            print(f"Erreur suppression {fichier} : {e}")

    # 📥 Copie depuis A
    for fichier in os.listdir(source):
        if not fichier_valide(fichier):
            continue

        src_path = os.path.join(source, fichier)
        dst_path = os.path.join(destination, fichier)

        try:
            shutil.copy2(src_path, dst_path)
            print(f"Copié : {fichier}")
        except Exception as e:
            print(f"Erreur copie {fichier} : {e}")

    print("Override terminé.")

def main():
    transferts = [
        (r".\TRAIN", r".\dataset\images\train", [], [".txt"], [], "synchronize"),
        (r".\TEST", r".\dataset\images\test", [], [".txt"], [], "synchronize"),
        (r".\VALIDATION", r".\dataset\images\val", [], [".txt"], [], "synchronize"),

        (r".\TRAIN", r".\dataset\labels\train", [".txt"], [], ["classes.txt"], "override"),
        (r".\TEST", r".\dataset\labels\test", [".txt"], [], ["classes.txt"], "override"),
        (r".\VALIDATION", r".\dataset\labels\val", [".txt"], [], ["classes.txt"], "override"),
    ]

    if not confirmer_action():
        print("Opération annulée.")
        return

    for source, destination, ext_ok, ext_ko, exclusions, mode in transferts:
        print(f"\n--- Traitement : {source} → {destination} ({mode}) ---")

        if mode == "synchronize":
            synchroniser_fichiers(source, destination, ext_ok, ext_ko)

        elif mode == "override":
            override_dossier(source, destination, ext_ok, ext_ko, exclusions)

        else:
            print(f"Mode inconnu : {mode}")

if __name__ == "__main__":
    main()