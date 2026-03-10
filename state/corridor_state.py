# state/corridor_state.py
import time

class CorridorState:
    def __init__(self):
        # Store latest known state of neighboring intersections
        # key: intersection_id -> state snapshot
        self.neighbors = {}
        self.last_update_ts = time.time()

    def update_neighbor(self, intersection_id, snapshot):
        """
        snapshot: state snapshot from neighbor intersection
        """
        self.neighbors[intersection_id] = {
            "snapshot": snapshot,
            "ts": time.time()
        }
        self.last_update_ts = time.time()

    def get_neighbor(self, intersection_id):
        return self.neighbors.get(intersection_id)

    def all_neighbors(self):
        return self.neighbors

    def prune_stale(self, max_age_sec=10.0):
        """
        Remove neighbors that haven't updated recently.
        """
        now = time.time()
        stale = [k for k, v in self.neighbors.items() if now - v["ts"] > max_age_sec]
        for k in stale:
            del self.neighbors[k]
