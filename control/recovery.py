# control/recovery.py
from collections import deque

class DeadlockRecovery:
    def __init__(self, config, order=("E", "N", "W", "S")):
        self.recovery_window = config.get("recovery_window", 12)
        self.order = deque(order)

    def next_recovery_lane(self, traffic_state):
        """
        Rotate recovery priority to avoid starving any direction.
        Choose a lane whose exit is free, if possible.
        """
        for _ in range(len(self.order)):
            lane = self.order[0]
            self.order.rotate(-1)

            if traffic_state.lanes[lane]["exit_free"]:
                return lane, self.recovery_window

        # Fallback: no exits free, pick next in rotation (still bounded)
        lane = self.order[0]
        self.order.rotate(-1)
        return lane, self.recovery_window
