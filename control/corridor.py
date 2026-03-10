# control/corridor.py
class CorridorCoordinator:
    def __init__(self, config):
        self.max_downstream_queue = config.get("max_downstream_queue", 15)
        self.green_wave_bonus = config.get("green_wave_bonus", 1.2)

    def adjust_for_corridor(self, traffic_state, corridor_state, candidate_lane):
        """
        Adjust decision based on downstream state.
        If downstream is congested, penalize feeding that direction.
        If downstream is free, slightly boost (green wave).
        """
        neighbor = corridor_state.get_neighbor(candidate_lane)
        if not neighbor:
            return candidate_lane

        snapshot = neighbor["snapshot"]
        lanes = snapshot.get("lanes", {})
        downstream_lane = lanes.get(candidate_lane)

        if not downstream_lane:
            return candidate_lane

        # If downstream exit is blocked or queue too large, discourage feeding
        if not downstream_lane.get("exit_free", True) or downstream_lane.get("density", 0) > self.max_downstream_queue:
            return None  # let scheduler pick alternative

        # Downstream is free: green wave possible (keep same lane)
        return candidate_lane
