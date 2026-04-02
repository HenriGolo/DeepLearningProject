import cv2
from ultralytics import YOLO

model = YOLO("../runs/detect/pfc_model2/weights/best.pt")
results = model("./TEST/IMG_20260217_134055.jpg", save=True)
"""annotated = results[0].plot()

cv2.imshow("Result", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()"""

#PS : enristrement des prediction dans runs/detect/predict/