# Comparing RGB-D and LiDAR Perception

> **Engineering Learning Note #06**

---

# Background

After learning RGB-D perception algorithms (Dense, Semi-Dense and Sparse methods) and gaining hands-on experience with the Livox MID360 LiDAR, I became interested in another question:

> **How does RGB-D perception differ from LiDAR perception?**

Although both sensors provide depth information, they acquire environmental information in fundamentally different ways and are suitable for different robotic applications.

Today's discussion helped me compare these two perception systems from both theoretical and engineering perspectives.

---

# What is RGB-D?

An RGB-D camera simultaneously captures

- RGB images
- Depth images

The RGB image provides texture and color information, while the depth image records the distance between the camera and surrounding objects.

Each pixel therefore contains both visual appearance and geometric information.

Typical RGB-D sensors include:

- Intel RealSense
- Microsoft Kinect
- Orbbec Astra

---

# What is LiDAR?

A LiDAR actively emits laser beams and measures the time required for the reflected laser to return.

Each laser return becomes a three-dimensional point.

Thousands of measurements together form a point cloud.

Unlike RGB-D cameras, LiDAR does not depend on image texture.

Typical robotic LiDAR sensors include:

- Livox MID360
- Velodyne VLP Series
- Ouster Series

---

# Working Principle

## RGB-D

```
Scene

↓

RGB Camera

+

Depth Camera

↓

RGB Image + Depth Image

↓

3D Perception
```

RGB-D relies on optical imaging together with depth sensing.

Every pixel has a corresponding depth value.

---

## LiDAR

```
Laser Pulse

↓

Object Surface

↓

Laser Reflection

↓

Distance Measurement

↓

Point Cloud
```

LiDAR directly measures the distance between the sensor and surrounding objects using laser pulses.

The output is a three-dimensional point cloud rather than an image.

---

# Comparison

| Aspect | RGB-D | LiDAR |
|---------|--------|--------|
| Output | RGB Image + Depth Map | Point Cloud |
| Measurement Principle | Camera + Depth Sensor | Laser Time-of-Flight |
| Environmental Information | Texture + Geometry | Geometry Only |
| Outdoor Performance | Limited by sunlight | Better outdoor robustness |
| Long Distance | Limited | Excellent |
| Computational Requirement | Moderate | Moderate |
| Typical Applications | Indoor Robotics, AR, RGB-D SLAM | Autonomous Driving, Mobile Robots, LiDAR SLAM |

---

# Advantages

## RGB-D

Advantages:

- Rich texture information
- Dense depth measurements
- Suitable for object recognition
- Easy visualization

Limitations:

- Sensitive to lighting conditions
- Limited sensing range
- Depth quality decreases outdoors

---

## LiDAR

Advantages:

- Accurate geometric measurement
- Long sensing distance
- Less affected by illumination
- High localization accuracy

Limitations:

- No color information
- Point cloud is relatively sparse compared with images
- Higher hardware cost

---

# Engineering Perspective

One important lesson from today's discussion is that neither RGB-D nor LiDAR is universally superior.

Instead, the choice depends on the application.

For example,

RGB-D cameras are often preferred for indoor robotic perception because they provide both appearance and depth information.

LiDAR systems are commonly selected for autonomous navigation because they offer robust geometric measurements over long distances.

In many practical robotic systems,

both sensors are combined to complement each other's strengths.

---

# Reflection

Before learning robotic perception, I tended to think that RGB-D and LiDAR were simply two different ways of measuring distance.

Today's discussion helped me understand that they represent two fundamentally different perception paradigms.

RGB-D focuses on combining visual appearance with depth estimation.

LiDAR focuses on obtaining accurate three-dimensional geometry directly from laser measurements.

The comparison also helped me realize that perception system design is driven by engineering requirements rather than individual sensor performance.

Selecting the appropriate sensor depends on the operating environment, computational resources and application objectives.

---

# Questions

Several questions remain for future investigation.

- How are RGB-D and LiDAR fused in modern robotic systems?
- Why do many autonomous robots use both cameras and LiDAR?
- How does sensor fusion improve localization robustness?
- Which perception system is more suitable for Robocon robots?
- What are the advantages of visual-inertial-LiDAR fusion?

---

# Next Steps

- [x] Learn Point Cloud
- [x] Location Error
- [x] Environment Adaption
- [x] Learn the difference between Dense and Sparse methods
- [x] Study Semi-Dense SLAM
- [x] Compare RGB-D and LiDAR perception
- [ ] Learn feature extraction algorithms (ORB, FAST, etc.)
- [ ] FAST-LIO
- [ ] ROS2 Topics
- [ ] RViz
- [ ] Localization
- [ ] Learn Point Cloud
- [ ] Location Error
- [ ] Environment Adaption


---

# Key Takeaway

Today's biggest takeaway is that RGB-D and LiDAR are not competing technologies but complementary perception systems.

RGB-D provides rich visual and depth information for understanding the environment, while LiDAR delivers highly accurate geometric measurements for localization and mapping.

Modern robotic perception increasingly relies on combining multiple sensors rather than depending on a single sensing modality.

---

# References

- Intel RealSense Documentation
- Livox MID360 Documentation
- RGB-D SLAM Literature
- LiDAR SLAM Literature
