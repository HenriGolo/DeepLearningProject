from ultralytics import YOLO

def tune_model():
    model = YOLO("yolov8s.pt")

    model.tune(
        data="data.yaml",
        epochs=50,
        iterations=30,
        device="0",
        plots=True,
        save=True,
        name="pfc_tune",
    )

if __name__ == "__main__":
    tune_model()
