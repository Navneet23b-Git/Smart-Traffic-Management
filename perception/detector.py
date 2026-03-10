# perception/detector.py
from models.yolo import YOLODetector

# COCO class IDs for common vehicles in YOLOv8
COCO_VEHICLE_IDS = {
    "bike": 3,         # motorcycle
    "car": 2,          # car
    "bus": 5,          # bus
    "truck": 7         # truck
}

class VehicleDetector:
    def __init__(self, model_path="yolov8n.pt", conf=0.4, imgsz=640):
        self.detector = YOLODetector(model_path=model_path, conf=conf, imgsz=imgsz)

    def detect_counts(self, frame):
        """
        Returns counts per class and raw results.
        """
        results = self.detector.infer(frame)
        counts = {"bike": 0, "car": 0, "bus": 0, "truck": 0, "emergency": 0}

        if results and results[0].boxes is not None:
            classes = results[0].boxes.cls.cpu().numpy().astype(int)
            for cid in classes:
                for name, coco_id in COCO_VEHICLE_IDS.items():
                    if cid == coco_id:
                        counts[name] += 1

        counts["emergency"] = 0  # placeholder
        return counts, results

    def detect_counts_by_roi(self, frame, rois: dict):
        """
        Split detections into entry/box/exit using ROIs.
        """
        results = self.detector.infer(frame)

        counts = {
            "entry": {"bike": 0, "car": 0, "bus": 0, "truck": 0, "emergency": 0},
            "box":   {"bike": 0, "car": 0, "bus": 0, "truck": 0, "emergency": 0},
            "exit":  {"bike": 0, "car": 0, "bus": 0, "truck": 0, "emergency": 0},
        }

        if results and results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            classes = results[0].boxes.cls.cpu().numpy().astype(int)

            for (x1, y1, x2, y2), cid in zip(boxes, classes):
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2

                for zone, (rx1, ry1, rx2, ry2) in rois.items():
                    if rx1 <= cx <= rx2 and ry1 <= cy <= ry2:
                        for name, coco_id in COCO_VEHICLE_IDS.items():
                            if cid == coco_id:
                                counts[zone][name] += 1

        return counts, results
