# **Computer Vision Based Automated Traffic Management System**

Traffic congestion is a major problem in modern cities, leading to **increased travel time**, **fuel consumption**, **air pollution**, and **delayed emergency services**. Traditional traffic control systems operate on **predefined signal timings**, which do not adapt to fluctuating traffic conditions and often cause **intersection gridlocks (deadlocks)**.

Recent advances in **Artificial Intelligence (AI)** and **Computer Vision (CV)** enable accurate real-time traffic monitoring using camera systems. However, AI-only systems lack the ability to **control real-world traffic infrastructure such as traffic lights**, making them difficult to deploy in practical environments.

To address these limitations, this project proposes a **hybrid AI \+ IoT based automated traffic management system** where:

* **AI performs intelligent traffic analysis using computer vision**  
* **IoT enables communication and control of traffic signal systems**  
* **Deadlock detection and recovery prevent intersection gridlocks**  
* **Adaptive scheduling optimizes traffic signal timing**

This system bridges the gap between **AI-based traffic analysis** and **physical actuation of traffic signals**, making it suitable for **smart city deployments**.

---

# **System Overview**

The system analyzes **multi-direction traffic video feeds (North, South, East, West)** and uses a **YOLO-based object detection model** to detect and classify vehicles.

Detected vehicles are mapped into traffic zones:

* Entry lane  
* Intersection box  
* Exit lane

Using these observations, the system calculates:

* Lane-wise traffic density  
* Intersection occupancy  
* Deadlock conditions  
* Emergency vehicle presence

An intelligent **decision engine** then determines optimal signal timing and communicates commands to traffic lights using an **IoT communication layer**.

---

# **It Includes (Updated Modules)**

## **Perception Layer**

* `perception/video_ingest.py` – Multi-camera traffic video ingestion  
* `perception/detector.py` – YOLO-based vehicle detection  
* `perception/roi.py` – Entry / Box / Exit lane zone mapping  
* `perception/fusion.py` – Multi-camera fusion and lane aggregation

## **Control Layer**

* `control/scheduler.py` – Adaptive traffic signal scheduling  
* `control/deadlock.py` – Intersection deadlock detection logic  
* `control/recovery.py` – Deadlock recovery strategy  
* `control/emergency.py` – Emergency vehicle prioritization  
* `control/corridor.py` – Intersection synchronization (green wave)

## **State Management**

* `state/traffic_state.py` – Lane and signal state management  
* `state/corridor_state.py` – Multi-intersection corridor coordination

## **Communication Layer**

* `comms/mqtt_client.py` – MQTT communication  
* `comms/rest_api.py` – REST API communication

## **Frontend**

* `frontend/app.py` – Streamlit dashboard  
* `frontend/components.py` – UI components

## **Model Layer**

* `models/yolo.py` – YOLO detection wrapper

## **System Execution**

* `main.py` – End-to-end system pipeline  
* `config.yaml` – System configuration

## **Data & Outputs**

* `data/` – Traffic videos   
* `outputs/frames/` – Extracted frames  
* `outputs/annotated/` – YOLO annotated frames  
* `outputs/metrics.json` – Live dashboard metrics

---

# **Model Architecture**

```python
Traffic Cameras (N, S, E, W)  
       ↓  
AI Computer Vision Module (YOLO)  
       ↓  
Traffic Density & Intersection Analysis  
       ↓  
Deadlock Detection Module  
       ↓  
Adaptive Decision Engine  
       ↓  
IoT Communication Layer (MQTT / REST)  
       ↓  
Traffic Signal Controller  
       ↓  
Traffic Lights  
```
---

# **System Architecture Diagram**
```python
                Traffic Cameras  
              (North, South, East, West)  
                        │  
                        ▼  
              Computer Vision Layer  
               (YOLO Vehicle Detection)  
                        │  
                        ▼  
             Traffic Analysis Layer  
       (Lane Density + Box Occupancy Estimation)  
                        │  
                        ▼  
               Deadlock Detection  
                        │  
                        ▼  
               Decision Engine  
    (Adaptive Scheduling + Emergency Priority)  
                        │  
                        ▼  
             Intersection Synchronization  
                  (Green Wave Logic)  
                        │  
                        ▼  
            IoT Communication Layer  
               (MQTT / REST API)  
                        │  
                        ▼  
           Traffic Signal Controller  
                        │  
                        ▼  
                   Traffic Lights  
```

# **Key Components**

## **AI Computer Vision Module**

* YOLO-based deep learning object detection  
* Detects vehicles such as **cars, bikes, buses, and trucks**  
* Works in real time using traffic camera feeds  
* Designed to be trained for **Indian traffic conditions**

---

## **Traffic Density Analyzer**

Lane congestion is estimated using vehicle counts.

```python
Density = Number of Vehicles / Lane Length
```

This allows dynamic allocation of **traffic signal timings**.

---

## **Deadlock Detection and Recovery**

A **deadlock (gridlock)** occurs when vehicles from multiple directions enter the intersection and block each other.

Deadlock is detected when:
```python
Box Occupancy > Threshold  
AND  
Exit Lanes Blocked  
AND  
Vehicles stationary for time T
```
Recovery strategy:

* Temporarily stop entry lanes  
* Clear one direction at a time  
* Resume normal scheduling once cleared

---

## **Emergency Vehicle Prioritization**

Emergency vehicles such as **ambulances or fire trucks** are detected using computer vision.

When detected:

* Signals dynamically change  
* Emergency path is cleared  
* Other lanes are temporarily paused

---

## **Intersection Synchronization**

Multiple intersections can be coordinated using **green wave synchronization**.

```python
Offset(j) = Offset(i) + TravelTime(i → j) mod CycleTime
```
This allows vehicles to pass multiple signals without stopping.

---

# **Working Methodology**

### **Step 1: Vehicle Detection**

* Traffic videos are processed frame-by-frame  
* YOLO detects and classifies vehicles  
* Vehicles are mapped to entry lanes

---

### **Step 2: Traffic Analysis**

The system estimates:

* Lane-wise density  
* Intersection occupancy  
* Exit lane availability

---

### **Step 3: Decision Engine**

Based on analysis:

* Signal timing is dynamically adjusted  
* Deadlocks are detected and resolved  
* Emergency vehicles are prioritized

---

### **Step 4: IoT-Based Control**

Example AI output:
```python
lane-1-density : 50  
lane-2-density : 30  
lane-3-density : 60  
deadlock           : false  
emergency          : false
```
Traffic controller receives the command and updates signal states.

---

# **Example YOLO Detection Output**

Example vehicle detection:
```python
Detected Objects  
-----------------  
Car   : 18  
Bike  : 12  
Bus   : 2  
Truck : 3
```
These detections help compute:

* Lane density  
* Intersection occupancy  
* Emergency vehicle presence

---

# **Visualization Dashboard**

A **Streamlit dashboard** visualizes the system in real time.

The dashboard shows:

* Live traffic video  
* YOLO detection boxes  
* Lane-wise vehicle counts  
* Traffic signal timers  
* Deadlock alerts  
* Emergency vehicle notifications

---

# **Features**

* Real-time traffic analysis using computer vision  
* Dynamic traffic signal scheduling  
* Deadlock detection and recovery  
* Emergency vehicle prioritization  
* Multi-intersection synchronization  
* IoT-based signal control  
* Streamlit visualization dashboard

---

# **Deployment Modes**

## **Simulation Mode**

* Recorded traffic videos  
* Virtual traffic lights  
* Streamlit dashboard

---

## **Real-World Deployment**

* CCTV cameras  
* Edge device (Raspberry Pi / Mini PC)  
* IoT signal controller (ESP32)

The architecture is designed to scale from **prototype to smart city deployment**.

---

# **Requirements**

## **Software Requirements**

* Python **3.8+**  
* Windows / Linux / macOS

---

## **Python Dependencies**
```python
ultralytics  
opencv-python  
numpy  
pandas  
torch  
torchvision  
paho-mqtt  
streamlit  
matplotlib  
pyyaml  
```
---

# **Project Structure**

```python
Automated-Traffic-Management/  
│  
├── perception/  
│   ├── video-ingest.py  
│   ├── detector.py  
│   ├── roi.py  
│   └── fusion.py  
│  
├── control/  
│   ├── scheduler.py  
│   ├── deadlock.py  
│   ├── recovery.py  
│   ├── emergency.py  
│   └── corridor.py  
│  
├── state/  
│   ├── traffic-state.py  
│   └── corridor-state.py  
│  
├── comms/  
│   ├── mqtt-client.py  
│   └── rest-api.py  
│  
├── frontend/  
│   ├── app.py  
│   └── components.py  
│  
├── models/  
│   └── yolo.py  
│  
├── data/  
│   ├── north.mp4  
│   ├── south.mp4  
│   ├── east.mp4  
│   └── west.mp4  
│  
├── outputs/  
│   ├── frames/  
│   ├── annotated/  
│   └── metrics.json  
│  
├── config.yaml  
├── main.py  
├── requirements.txt  
└── README.md  
```
---

# **Future Improvements**

Future work will focus on:

* Training YOLO for **Indian traffic datasets**  
* Improving lane detection and segmentation  
* Integrating real **IoT traffic signal controllers**  
* Expanding to **multi-intersection smart traffic networks**

---

# **References**

1. **ISSN: 2456-3315**  
   [https://ijrti.org/papers/IJRTI2305036.pdf](https://ijrti.org/papers/IJRTI2305036.pdf)  
2. **YOLO: Real-Time Object Detection**  
   [https://www.aijfr.com/papers/2025/4/1053.pdf](https://www.aijfr.com/papers/2025/4/1053.pdf)

