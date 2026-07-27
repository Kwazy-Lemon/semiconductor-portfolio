# Understanding Dense and Sparse Methods in RGB-D Perception

> **Technical Learning Note #03**


---

# Background

Today I participated in a technical discussion about RGB-D perception algorithms.

The discussion focused on two different ways of utilizing RGB-D information:

- Dense methods
- Sparse methods

Although both approaches estimate the robot's motion using RGB-D data, they differ significantly in how visual information is extracted and processed.

---

# What is RGB-D?

An RGB-D camera provides two types of information simultaneously.

- RGB image
- Depth image

Unlike a traditional camera, every pixel also contains distance information.

This allows the robot to recover the three-dimensional structure of the surrounding environment.

---

# Dense Methods

Dense methods attempt to use almost every valid pixel in the image.

Instead of selecting only feature points, they directly utilize the complete depth map to reconstruct the environment.

Advantages:

- Rich environmental information
- Dense map reconstruction
- High geometric accuracy

Disadvantages:

- High computational cost
- Large memory consumption
- Difficult to achieve real-time performance on embedded platforms

Typical applications include:

- KinectFusion
- Dense RGB-D Mapping

---

# Sparse Methods

Sparse methods only extract distinctive feature points from an image.

Typical features include corners and high-texture regions.

Only these representative points are used for pose estimation and mapping.

Advantages:

- Lower computational complexity
- Faster processing speed
- Better real-time performance

Disadvantages:

- Map contains fewer points
- Performance depends on feature quality
- Less suitable for textureless environments

Typical applications include:

- ORB-SLAM
- Feature-based Visual SLAM

---

# Comparison

| Aspect | Dense | Sparse |
|---------|--------|---------|
| Data Used | Almost every pixel | Feature points only |
| Computation | High | Low |
| Memory | Large | Small |
| Mapping | Dense map | Sparse map |
| Speed | Slower | Faster |
| Real-Time Performance | More difficult | Better |

---

# Engineering Perspective

One important idea I learned today is that choosing an algorithm is not simply about accuracy.

In robotic systems, computational resources are limited.

An algorithm that performs well offline may not be suitable for real-time applications.

Therefore, engineers often need to balance:

- Accuracy
- Robustness
- Computational cost
- Real-time performance

This engineering trade-off is one of the key considerations when selecting a perception algorithm.

---

# Reflection

Before today's discussion, I assumed that using more data would always produce better perception results.

However, I realized that this is not necessarily true.

Dense methods preserve more environmental information but require much higher computational resources.

Sparse methods intentionally discard a large amount of information while retaining only the most informative features.

Although less information is used, the system can often achieve faster and more robust real-time performance.

This helped me understand that perception algorithms are designed by balancing efficiency and accuracy rather than maximizing the amount of processed data.

---

# Questions

After today's discussion, I would like to further investigate:

- What is Semi-Dense SLAM?
- Why do many modern SLAM systems adopt sparse or semi-dense approaches?
- How are LiDAR and RGB-D perception combined?
- Which approach is more suitable for Robocon robots?

---

# Next Steps

- [x] Learn Point Cloud
- [x] Location Error
- [x] Environment Adaption
- [x] Learn the difference between Dense and Sparse methods
- [ ] Study Semi-Dense SLAM
- [ ] Compare RGB-D and LiDAR perception
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

Today's biggest takeaway is that perception algorithms are designed around engineering trade-offs.

Dense methods aim to maximize environmental information, while sparse methods prioritize computational efficiency and real-time performance.

Selecting the appropriate method depends on the requirements and constraints of the robotic system rather than simply choosing the algorithm that uses the most data.

---

# References

- ORB-SLAM Series
- KinectFusion
- RGB-D SLAM Literature
