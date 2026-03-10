# models/yolo.py
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path="yolov8n.pt", conf=0.4, imgsz=640):
        self.model = YOLO(model_path)
        self.conf = conf
        self.imgsz = imgsz

    def infer(self, frame):
        """
        Run YOLO inference on a single frame.
        Returns YOLO results object.
        """
        results = self.model(frame, conf=self.conf, imgsz=self.imgsz, verbose=False)
        return results
