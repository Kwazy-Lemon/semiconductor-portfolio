# Sensors and Instrumentation

> This section documents my learning journey in robotic perception, sensing technologies, and autonomous navigation during my robotics research and Robocon project.

---

# Overview

Robotic perception is one of the core components of autonomous systems.

Before a robot can navigate, localize itself, or perform autonomous tasks, it must first perceive its surrounding environment through different sensors.

This module summarizes my learning process on robotic sensing technologies, including LiDAR, RGB-D cameras, SLAM, localization, and perception frameworks.

The notes combine theoretical understanding with engineering observations obtained during practical learning and Robocon project discussions.

---

# Repository Structure

```text
06_Sensors_and_Instrumentation
│
├── Livox MID360
|
│
├── Robocon Perception Notes
│      ├── 01_Point_Cloud
│      ├── 02_Localization_Error
│      ├── 03_Environment_Adaptation
│      ├── 04_Dense_vs_Sparse
│      ├── 05_Semi_Dense_SLAM
│      ├── 06_RGBD_vs_LiDAR
│      ├── 07_Feature_Extraction
│      ├── 08_FAST_LIO
│      ├── 09_Localization
│      └── 10_ROS2
│
└── README.md
```

---

# Learning Roadmap

The learning notes follow a gradual progression from understanding sensors to complete robotic perception systems.

```
Sensors

↓

Point Cloud

↓

Perception Algorithms

↓

SLAM

↓

Localization

↓

Robot Navigation
```

The corresponding learning sequence is

- Point Cloud
- Localization Error
- Environment Adaptation
- Dense vs Sparse Methods
- Semi-Dense SLAM
- RGB-D vs LiDAR
- Feature Extraction
- FAST-LIO
- Localization
- ROS2 for Robot Perception

---

# Topics Covered

## LiDAR

- Livox MID360
- Point Cloud
- Sensor Characteristics
- Point Cloud Processing

---

## Visual Perception

- RGB-D Sensors
- Dense Methods
- Sparse Methods
- Semi-Dense SLAM
- Feature Extraction

---

## Robot Localization

- FAST-LIO
- Localization
- Environment Adaptation
- Localization Error Analysis

---

## Robotic Software

- ROS2
- RViz
- Robotic Perception Pipeline

---

# Engineering Perspective

Rather than simply introducing individual algorithms,

these notes focus on understanding how different sensing technologies are integrated into practical robotic systems.

During the Robocon project,

many engineering problems—including localization errors, environmental adaptation, and point cloud preprocessing—provided valuable opportunities to connect theoretical knowledge with practical robotic applications.

---

# Future Learning Plan

- Sensor Fusion
- Visual-Inertial SLAM
- Loop Closure
- ICP Registration
- Point Cloud Filtering
- Multi-Sensor Calibration
- Navigation Stack

---

# Related Resources

- Livox MID360 Documentation
- ROS2 Documentation
- FAST-LIO
- ORB-SLAM
- OpenCV
