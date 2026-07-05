# Livox MID360

> Learning notes on the Livox MID360 LiDAR sensor used in autonomous robotic perception systems.

---

# Overview

The Livox MID360 is a compact 360° LiDAR designed for robotics, autonomous navigation, mapping, and perception. Unlike conventional mechanical spinning LiDARs, the MID360 integrates laser ranging, inertial sensing, and a wide field of view into a lightweight sensor, making it suitable for mobile robots operating in indoor and outdoor environments.

In many autonomous robot systems, the MID360 serves as the primary perception sensor by continuously generating three-dimensional point clouds that are subsequently used for localization, mapping, obstacle detection, and navigation.

---

# Why MID360?

Compared with traditional rotating LiDARs, the MID360 provides several advantages for mobile robotic applications.

- 360° horizontal field of view
- Integrated IMU
- Compact and lightweight design
- High point cloud density
- Suitable for SLAM applications
- Compatible with ROS2 ecosystem

These characteristics make it a common choice for autonomous mobile robots participating in robotics competitions and research projects.

---

# Working Principle

The MID360 continuously emits laser pulses into the surrounding environment.

For each emitted laser beam,

1. A laser pulse is transmitted.
2. The pulse reflects from surrounding objects.
3. The reflected signal returns to the receiver.
4. The sensor measures the time of flight (ToF).
5. The distance is calculated.
6. Combined with the scanning angle, a three-dimensional point is generated.

Repeating this process thousands of times every second produces a dense 3D point cloud representing the surrounding environment.

---

# Sensor Outputs

The MID360 provides multiple types of information simultaneously.

| Data | Description |
|-------|-------------|
| Point Cloud | 3D spatial measurements |
| IMU | Acceleration and angular velocity |
| Timestamp | Precise synchronization |
| Intensity | Reflection strength |

These outputs can be fused by localization algorithms such as FAST-LIO.

---

# Role in the Robotics Pipeline

A typical perception pipeline is

```text
Livox MID360
        │
        ▼
Livox Driver
        │
        ▼
ROS2 Topics
        │
        ▼
Point Cloud
        │
        ▼
FAST-LIO
        │
        ▼
Robot Pose
        │
        ▼
RViz Visualization
```

The LiDAR itself does not determine the robot position.

Instead, it continuously provides raw environmental measurements that are processed by localization algorithms to estimate the robot pose.

---

# Applications

Typical applications include

- Autonomous Mobile Robots (AMR)
- SLAM
- Autonomous Navigation
- Robocon
- Warehouse Robotics
- Service Robots
- Environment Mapping

---

# Learning Progress

- [ ] Hardware architecture
- [ ] Communication protocol
- [ ] Livox SDK
- [ ] ROS2 Driver
- [ ] Point Cloud Visualization
- [ ] Coordinate Systems
- [ ] Sensor Calibration
- [ ] FAST-LIO Integration

---

# References

- Livox Official Documentation
- Livox SDK2
- ROS2 Documentation
- FAST-LIO
