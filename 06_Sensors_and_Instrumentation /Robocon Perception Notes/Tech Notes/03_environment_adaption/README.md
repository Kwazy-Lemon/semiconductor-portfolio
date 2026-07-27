# Adapting LiDAR Perception to Different Competition Environments

> **Engineering Learning Note #3**

**Date:** July 7, 2026

---

# Background

Today's discussion focused on a practical engineering problem encountered during Robocon preparation.

Unlike laboratory environments, the official competition venue has significantly different structural characteristics.

This raised an important question:

> **Can a LiDAR configuration optimized in the training venue still perform well in the competition venue?**

Instead of directly modifying the localization algorithm, the team first investigated how differences in the environment influence point cloud quality.

---

# Engineering Problem

The training venue has a relatively low ceiling (approximately 5–6 meters).

Since the ceiling is close to the robot, the Livox MID360 can obtain dense and stable point cloud returns from the ceiling.

These points provide rich geometric information for localization.

However, the official competition venue is a large sports hall with a ceiling height of approximately 20 meters.

At such distances,

- fewer laser beams reach the ceiling,
- returned signals become weaker,
- point density decreases,
- and the ceiling may no longer provide reliable geometric features.

Therefore, the point cloud collected in the competition venue may be significantly different from the one collected during training.

---

# Engineering Question

The main question discussed today was:

> **Should the localization system rely on ceiling points that may disappear in the competition venue?**

If localization depends heavily on those points,

the robot may perform well during testing but degrade significantly during the actual competition.

---

# Experimental Design

To investigate this issue, the team proposed a simple experiment.

Instead of using all point cloud data,

a height threshold is introduced.

For example,

```
Keep only points below 3 meters.
Discard points above 3 meters.
```

The idea is to intentionally ignore ceiling points during training.

If both the training venue and the competition venue use exactly the same height limitation,

the localization system may become more robust because it always receives similar input data.

The goal is not to maximize point cloud density,

but to improve consistency between different environments.

---

# Experimental Observation

After applying the height threshold,

the point cloud became noticeably less informative.

Removing all points above 3 meters also removed many useful geometric features.

As a result,

the localization quality became worse during testing.

This indicates an engineering trade-off.

- Keeping ceiling points provides richer environmental information.
- Removing ceiling points increases consistency between different venues.
- However, excessive filtering may reduce localization accuracy.

Finding the appropriate balance therefore becomes an important engineering problem.

---

# What I Learned

Today's discussion helped me realize that robotic perception is not simply about collecting as many points as possible.

More data does not always lead to better performance.

Sometimes,

removing part of the data can improve the robustness of the system when operating in different environments.

The challenge is determining which information is useful and which information may reduce generalization.

This is essentially an engineering optimization problem rather than a hardware problem.

---

# Reflection

Before today, I tended to think that a better LiDAR system should always preserve as much information as possible.

However, today's discussion changed my understanding.

A localization algorithm should not only perform well in one environment.

It should also remain stable after the environment changes.

This means the quality of a perception system depends not only on sensor capability,

but also on how the sensor data are selected and utilized.

The concept of **consistency across environments** was one of the most important ideas I learned today.

---

# Questions

Several questions remain for future investigation.

- What is the optimal height threshold?
- Is a fixed threshold sufficient for all environments?
- Can the robot automatically identify unreliable points?
- Would adaptive point cloud filtering perform better?
- How do state-of-the-art SLAM systems handle large indoor environments with different ceiling heights?

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

Today's biggest takeaway was that robotic perception is not only determined by sensor performance.

The same LiDAR may produce very different localization results under different environmental conditions.

Designing a perception system that remains stable across multiple environments requires careful preprocessing of point cloud data and thoughtful engineering trade-offs.

---
