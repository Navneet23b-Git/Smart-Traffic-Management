# perception/video_ingest.py
import cv2

class VideoIngestor:
    def __init__(self, sources: dict):
        """
        sources: dict mapping camera name -> video path
        Example:
        {
            "north_entry": "data/north_entry.mp4",
            "east_entry": "data/east_entry.mp4",
            ...
        }
        """
        self.sources = sources
        self.captures = {}

        for name, path in sources.items():
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                raise RuntimeError(f"Could not open video source: {path}")
            self.captures[name] = cap

    def read(self):
        """
        Read one frame from each source.
        Returns:
            frames: dict mapping name -> frame (or None if ended)
        """
        frames = {}
        for name, cap in self.captures.items():
            ok, frame = cap.read()
            if not ok:
                frames[name] = None
            else:
                frames[name] = frame
        return frames

    def release(self):
        for cap in self.captures.values():
            cap.release()
