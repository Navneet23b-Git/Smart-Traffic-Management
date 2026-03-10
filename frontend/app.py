# frontend/app.py
import streamlit as st
import time
import json
import os
import cv2

from frontend.components import lane_panel, deadlock_panel

STATE_FILE = "outputs/metrics.json"
FRAMES_DIR = "outputs/frames"

st.set_page_config(page_title="Smart Traffic AI", layout="wide")
st.title("🚦 Smart Traffic Management Dashboard (Live YOLO)")

placeholder = st.empty()

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return None

def load_frame(lane):
    path = os.path.join(FRAMES_DIR, f"{lane}.jpg")
    if not os.path.exists(path):
        return None

    img = cv2.imread(path)
    if img is None or img.size == 0:
        return None

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

while True:
    with placeholder.container():
        state = load_state()

        cols_vid = st.columns(4)
        for i, lane in enumerate(["N", "E", "S", "W"]):
            with cols_vid[i]:
                st.subheader(f"{lane} View")
                frame = load_frame(lane)
                if frame is not None:
                    st.image(frame, channels="RGB", width="stretch")
                else:
                    st.info("Waiting for frames from backend...")

        st.divider()

        if not state:
            st.info("Waiting for backend state...")
        else:
            st.subheader(
                f"Phase: {state.get('phase','GREEN')} | "
                f"Mode: {state['mode']} | "
                f"GREEN: {state['current_green']} | "
                f"Next: {state.get('next_green')}"
            )

            cols = st.columns(4)
            for i, (lane, data) in enumerate(state["lanes"].items()):
                with cols[i]:
                    lane_panel(lane, data, green=(lane == state["current_green"]))

            deadlock_panel(state["mode"], state.get("passable"))

    time.sleep(1)
