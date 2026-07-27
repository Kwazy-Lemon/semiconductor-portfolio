# Understanding FAST-LIO

> **Engineering Learning Note #08**

**Date:** July 2026

---

# Background

After learning LiDAR point clouds, RGB-D perception, Dense/Semi-Dense/Sparse methods, and feature extraction algorithms, I began studying a practical LiDAR SLAM framework widely used in robotics:

> **FAST-LIO (Fast LiDAR-Inertial Odometry)**

Unlike Livox Viewer, which only visualizes point cloud data, FAST-LIO performs real-time localization by combining LiDAR measurements with IMU data.

Today's learning focused on understanding the overall architecture of FAST-LIO and why it has become one of the most popular LiDAR SLAM algorithms in modern robotic systems.

---

# What is FAST-LIO?

FAST-LIO stands for

> **Fast LiDAR-Inertial Odometry**

It is a real-time LiDAR SLAM framework that tightly fuses

- LiDAR
- IMU (Inertial Measurement Unit)

to estimate the robot's pose.

Instead of simply displaying point clouds,

FAST-LIO continuously estimates

- Position
- Orientation
- Velocity

while simultaneously building a map of the environment.

---

# Why IMU?

One question I had was:

> Why is LiDAR alone not enough?

LiDAR scans the environment relatively slowly compared with the robot's motion.

If the robot moves while the LiDAR is scanning,

motion distortion may occur.

An IMU provides

- Angular velocity
- Linear acceleration

at a much higher frequency.

By combining these measurements,

FAST-LIO can compensate for motion distortion and improve localization accuracy.

---

# Overall Workflow

```
LiDAR Scan
        │
        ▼
IMU Measurements
        │
        ▼
Motion Compensation
        │
        ▼
State Estimation
        │
        ▼
Scan Matching
        │
        ▼
Map Update
        │
        ▼
Robot Localization
```

FAST-LIO continuously repeats this process as the robot moves.

---

# Relationship with Previous Notes

Through previous learning,

I gradually understood the following perception pipeline.

```
Livox MID360

↓

Point Cloud

↓

Point Cloud Filtering

↓

FAST-LIO

↓

Robot Pose Estimation

↓

Map Building

↓

Navigation
```

This helped me realize that point cloud visualization is only the beginning.

The real objective is to estimate the robot's position while constructing an accurate map.

---

# Engineering Perspective

Unlike traditional LiDAR visualization software,

FAST-LIO is designed for autonomous robotic systems.

Its purpose is not to display point clouds,

but to estimate robot motion in real time.

This makes FAST-LIO suitable for

- Autonomous robots
- Mobile platforms
- Robocon robots
- Autonomous vehicles
- UAVs

where accurate localization is essential.

---

# Reflection

Before today's learning,

I regarded LiDAR primarily as a sensor for collecting point clouds.

Learning about FAST-LIO changed this understanding.

I realized that point clouds themselves do not directly solve robotic localization.

Instead,

algorithms such as FAST-LIO transform raw sensor measurements into meaningful robot poses.

This shifted my perspective from "collecting data" to "using data for autonomous perception."

---

# Questions

Several questions remain for future investigation.

- How does FAST-LIO fuse LiDAR and IMU measurements?
- Why is the IMU frequency much higher than the LiDAR frequency?
- What is motion compensation?
- How is scan matching performed?
- Why is FAST-LIO faster than many traditional LiDAR SLAM methods?

---

# Next Steps

- [x] Learn Point Cloud
- [x] Understand Localization Error
- [x] Environment Adaptation
- [x] Dense vs Sparse
- [x] Semi-Dense SLAM
- [x] Compare RGB-D and LiDAR
- [x] Feature Extraction
- [x] Understand FAST-LIO
- [ ] Deploy FAST-LIO
- [ ] Learn ROS2 Topics
- [ ] Visualize FAST-LIO in RViz
- [ ] Analyze localization accuracy

---

# Key Takeaway

Today's biggest takeaway is that LiDAR point clouds alone cannot provide robot localization.

FAST-LIO combines LiDAR and IMU measurements to estimate the robot's motion while simultaneously building a map.

Understanding FAST-LIO helped me connect the knowledge learned in previous notes—including point clouds, localization, and perception algorithms—into a complete robotic perception pipeline.

---

# References

- FAST-LIO: A Fast, Robust LiDAR-Inertial Odometry Package by Tightly-Coupled Iterated Kalman Filter
- FAST-LIO2 Paper
- Livox MID360 Documentation
- ROS2 Documentation
