# frontend/components.py
import streamlit as st

def lane_panel(lane, data, green=False):
    st.markdown(f"### Lane {lane} {'🟢' if green else '🔴'}")
    st.write(f"Density: {data['density']:.2f}")
    st.write(f"Wait time: ⏳ {int(data['wait_time'])} sec")
    st.write("Counts (Box):")
    st.json(data["counts"]["box"])

def deadlock_panel(mode, passable=None):
    if mode == "DEADLOCK_RECOVERY" and passable:
        st.warning("⚠ Deadlock recovery active")
        st.write("Passable vehicles from box:")
        st.json(passable)