# control/scheduler.py
class FairScheduler:
    def __init__(self, config):
        self.min_green = config.get("min_green", 8)
        self.max_green = config.get("max_green", 40)
        self.max_wait = config.get("max_wait", 60)
        self.weights = config.get("weights", {"density": 0.6, "wait": 0.3, "exit_free": 0.1})
        self.density_delta = config.get("density_delta", 0.25)

    def choose_lane(self, traffic_state):
        """
        Choose next green lane based on fairness + thresholds.
        """
        lanes = traffic_state.lanes

        # Anti-starvation: serve any lane waiting too long
        for lane, data in lanes.items():
            if data["wait_time"] >= self.max_wait and data["exit_free"]:
                return lane, self.min_green

        # Compute normalized scores
        max_density = max(d["density"] for d in lanes.values()) or 1.0
        max_wait = max(d["wait_time"] for d in lanes.values()) or 1.0

        scores = {}
        for lane, data in lanes.items():
            norm_density = data["density"] / max_density
            norm_wait = data["wait_time"] / max_wait
            exit_bonus = 1.0 if data["exit_free"] else 0.0

            score = (
                self.weights["density"] * norm_density +
                self.weights["wait"] * norm_wait +
                self.weights["exit_free"] * exit_bonus
            )
            scores[lane] = score

        chosen = max(scores, key=scores.get)

        # Green time proportional to density but capped
        density = lanes[chosen]["density"]
        green_time = int(self.min_green + density)
        green_time = max(self.min_green, min(self.max_green, green_time))

        return chosen, green_time
