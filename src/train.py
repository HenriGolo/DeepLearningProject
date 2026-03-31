from ultralytics import YOLO

def train_model():
    # Charger un modèle pré-entraîné (recommandé)
    model = YOLO("yolov8s.pt")  # ou yolov8n.pt pour plus léger

    # Lancer l'entraînement
    results = model.train(
        data="data.yaml",   # chemin vers ton fichier yaml
        epochs=50,          # nombre d'epochs
        imgsz=640,          # taille des images
        batch=16,           # adapte selon ton GPU
        name="pfc_model",   # nom de l'expérience
        device=0            # 0 = GPU, "cpu" sinon
    )

if __name__ == "__main__":
    train_model()