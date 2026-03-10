# main.py
import time
import json
import os
import yaml
import cv2

from perception.video_ingest import VideoIngestor
from perception.detector import VehicleDetector
from perception.fusion import fuse_lane_views
from perception.roi import ROIS
from state.traffic_state import TrafficState
from control.scheduler import FairScheduler
from control.deadlock import DeadlockDetector
from control.recovery import DeadlockRecovery
from control.emergency import EmergencyPrioritizer

with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

OUTPUTS_DIR = "outputs"
STATE_FILE = os.path.join(OUTPUTS_DIR, "metrics.json")
FRAMES_DIR = os.path.join(OUTPUTS_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

SOURCES = {
    "N": "data/north.mp4",
    "E": "data/east.mp4",
    "S": "data/south.mp4",
    "W": "data/west.mp4",
}

LANES = ["N", "E", "S", "W"]

def draw_boxes(frame, results):
    if results and results[0].boxes is not None:
        for box in results[0].boxes.xyxy.cpu().numpy():
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

def main_loop():
    ingestor = VideoIngestor(SOURCES)

    detector = VehicleDetector(
        model_path=CONFIG["yolo"]["model_path"],
        conf=CONFIG["yolo"]["conf"],
        imgsz=CONFIG["yolo"]["imgsz"],
    )

    traffic_state = TrafficState(lanes=LANES)
    scheduler = FairScheduler(CONFIG)
    deadlock_detector = DeadlockDetector(CONFIG)
    recovery = DeadlockRecovery(CONFIG)
    emergency = EmergencyPrioritizer(max_override_sec=20)

    yellow_time = CONFIG.get("yellow_time", 3)

    last_switch_ts = 0
    yellow_start_ts = 0
    green_time_left = 0

    while True:
        frames = ingestor.read()
        now = time.time()

        for lane in LANES:
            frame = frames.get(lane)
            if frame is None:
                continue

            counts_by_zone, results = detector.detect_counts_by_roi(frame, ROIS[lane])
            fused = fuse_lane_views(
                counts_by_zone["entry"],
                counts_by_zone["box"],
                counts_by_zone["exit"],
                CONFIG
            )
            traffic_state.update_lane(lane, fused)

            vis = draw_boxes(frame.copy(), results)
            for zone, (x1, y1, x2, y2) in ROIS[lane].items():
                cv2.rectangle(vis, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(vis, zone, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            cv2.imwrite(os.path.join(FRAMES_DIR, f"{lane}.jpg"), vis)

        traffic_state.tick()

        is_deadlock = deadlock_detector.check(traffic_state)
        ev_lane = emergency.detect_emergency(traffic_state, now)

        if traffic_state.current_green is None:
            lane, green_time_left = scheduler.choose_lane(traffic_state)
            traffic_state.set_mode("NORMAL")
            traffic_state.set_green(lane)
            last_switch_ts = now

        elif traffic_state.phase == "GREEN" and now - last_switch_ts >= green_time_left:
            if emergency.is_override_active(now):
                next_lane = emergency.get_active_lane(now)
                traffic_state.set_mode("EMERGENCY")
            elif ev_lane:
                emergency.activate_override(ev_lane, now)
                next_lane = ev_lane
                traffic_state.set_mode("EMERGENCY")
            elif is_deadlock:
                next_lane, _ = recovery.next_recovery_lane(traffic_state)
                traffic_state.set_mode("DEADLOCK_RECOVERY")
            else:
                next_lane, _ = scheduler.choose_lane(traffic_state)
                traffic_state.set_mode("NORMAL")

            traffic_state.set_yellow(next_lane)
            yellow_start_ts = now

        elif traffic_state.phase == "YELLOW" and now - yellow_start_ts >= yellow_time:
            traffic_state.apply_next_green()
            last_switch_ts = now

            if traffic_state.mode == "EMERGENCY":
                green_time_left = emergency.max_override_sec
            elif traffic_state.mode == "DEADLOCK_RECOVERY":
                green_time_left = CONFIG["recovery_window"]
            else:
                _, green_time_left = scheduler.choose_lane(traffic_state)

        snapshot = traffic_state.snapshot()
        snapshot["green_time_left"] = max(0, int(green_time_left - (now - last_switch_ts)))

        if traffic_state.mode == "DEADLOCK_RECOVERY" and traffic_state.current_green:
            counts = traffic_state.lanes[traffic_state.current_green]["counts"]["box"]
            snapshot["passable"] = {
                "bike": counts["bike"],
                "car": counts["car"],
                "truck": counts["truck"],
            }

        with open(STATE_FILE, "w") as f:
            json.dump(snapshot, f, indent=2)

        time.sleep(1)

if __name__ == "__main__":
    main_loop()