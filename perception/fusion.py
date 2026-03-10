# perception/fusion.py

def fuse_lane_views(entry_counts, box_counts, exit_counts, config=None):
    """
    Fuse counts from entry, box, and exit views into a lane state.

    entry_counts, box_counts, exit_counts: dicts like:
    {
        "bike": int, "car": int, "bus": int, "truck": int, "emergency": int
    }

    Returns:
        fused: dict with lane density, box occupancy, exit_free, class-wise counts
    """
    # weights (can be tuned via config)
    w_entry = 0.6
    w_box = 0.4

    if config:
        w_entry = config.get("w_entry", w_entry)
        w_box = config.get("w_box", w_box)

    # total vehicles in views
    total_entry = sum(entry_counts.values())
    total_box = sum(box_counts.values())
    total_exit = sum(exit_counts.values())

    # density estimation (entry + box)
    density = w_entry * total_entry + w_box * total_box

    # exit availability (simple threshold)
    exit_block_threshold = 5
    if config:
        exit_block_threshold = config.get("exit_block_threshold", exit_block_threshold)

    exit_free = total_exit < exit_block_threshold

    fused = {
        "density": density,
        "box_occupancy": total_box,
        "exit_free": exit_free,
        "counts": {
            "entry": entry_counts,
            "box": box_counts,
            "exit": exit_counts
        }
    }

    return fused
