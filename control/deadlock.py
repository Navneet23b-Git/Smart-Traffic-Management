# control/deadlock.py
class DeadlockDetector:
    def __init__(self, config):
        self.box_occupancy_threshold = config.get("box_occupancy_threshold", 5)
        self.exit_block_threshold = config.get("exit_block_threshold", 5)
        self.stagnation_cycles = config.get("stagnation_cycles", 3)

        self._stagnation_counter = 0

    def check(self, traffic_state):
        """
        Deadlock if:
        - Vehicles are in the box
        - AND exits are blocked
        - AND this persists for N cycles (stagnation)
        """
        box_total = sum(data["box_occupancy"] for data in traffic_state.lanes.values())
        exits_blocked = all(not data["exit_free"] for data in traffic_state.lanes.values())

        if box_total >= self.box_occupancy_threshold and exits_blocked:
            self._stagnation_counter += 1
        else:
            self._stagnation_counter = 0

        return self._stagnation_counter >= self.stagnation_cycles
