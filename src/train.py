from ultralytics import YOLO

def train_model():
    # Charge modèle pré-entraîné 
    model = YOLO("yolov8s.pt")  #yolov8s.pt

    results = model.train(
        data="data.yaml",
        epochs=150,
        patience=25,
        imgsz=640,
        batch=16,
        name="first_train_50_epoch",
        device="0",
        # meilleurs hyperparamètres trouvés par tune()
        lr0=0.004,
        lrf=0.01289,
        momentum=0.96157,
        weight_decay=0.00038,
        warmup_epochs=3.83887,
        warmup_momentum=0.7684,
        box=5.0347,
        cls=0.39708,
        dfl=1.06117,
        hsv_h=0.02894,
        hsv_s=0.69035,
        hsv_v=0.43702,
        translate=0.06782,
        scale=0.48774,
        flipud=0.00742,
        fliplr=0.52641,
        mosaic=1.0,
        mixup=0.00173,
        close_mosaic=9, #9
        degrees=0.0,
    )

if __name__ == "__main__":
    train_model()