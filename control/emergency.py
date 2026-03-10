# control/emergency.py
class EmergencyPrioritizer:
    def __init__(self, max_override_sec=20):
        # Maximum time emergency can override normal control
        self.max_override_sec = max_override_sec
        self._active_lane = None
        self._override_until_ts = 0.0

    def detect_emergency(self, traffic_state, now_ts):
        """
        Check if any lane has emergency vehicles waiting.
        Returns the lane with highest emergency count, else None.
        """
        ev_counts = {
            lane: data["counts"]["entry"].get("emergency", 0)
            for lane, data in traffic_state.lanes.items()
        }
        lane = max(ev_counts, key=ev_counts.get)
        return lane if ev_counts[lane] > 0 else None

    def activate_override(self, lane, now_ts):
        self._active_lane = lane
        self._override_until_ts = now_ts + self.max_override_sec

    def is_override_active(self, now_ts):
        return self._active_lane is not None and now_ts <= self._override_until_ts

    def get_active_lane(self, now_ts):
        if self.is_override_active(now_ts):
            return self._active_lane
        # reset after expiry
        self._active_lane = None
        return None
