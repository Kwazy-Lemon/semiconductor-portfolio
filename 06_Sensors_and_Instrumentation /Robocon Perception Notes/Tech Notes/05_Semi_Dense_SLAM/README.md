# Understanding Semi-Dense SLAM

> **Technical Learning Note #04**

**Date:** July 8, 2026

---

# Background

After learning the differences between Dense and Sparse RGB-D perception methods, I naturally encountered another question:

> If Dense methods use almost every pixel and Sparse methods use only feature points, is there a compromise between the two?

Today's discussion introduced the concept of **Semi-Dense SLAM**, which attempts to balance computational efficiency and environmental information.

Rather than representing another independent algorithm, Semi-Dense SLAM reflects an engineering trade-off between accuracy and real-time performance.

---

# Why Semi-Dense?

Dense methods process almost every valid pixel in an image.

Although they preserve abundant geometric information, they require high computational resources and memory.

Sparse methods only extract a limited number of feature points, making them computationally efficient but losing a significant amount of environmental information.

Semi-Dense methods lie between these two extremes.

Instead of processing every pixel, they only retain pixels with strong image gradients, such as object edges and textured regions.

This allows the algorithm to preserve important structural information while reducing computational cost.

---

# Dense vs Semi-Dense vs Sparse

| Method | Pixels Used | Computational Cost | Information Preserved | Typical Characteristic |
|---------|-------------|-------------------|------------------------|------------------------|
| Dense | Nearly all pixels | High | Richest | High-quality reconstruction |
| Semi-Dense | High-gradient pixels | Medium | Moderate | Balance between accuracy and efficiency |
| Sparse | Feature points only | Low | Limited | Fast real-time performance |

---

# Why High-Gradient Pixels?

One question I had today was:

> Why doesn't Semi-Dense simply select random pixels?

The answer is that pixels located on object boundaries usually contain much more geometric information than pixels inside flat surfaces.

For example,

```
Wall
██████████████

Edge
||||||||||||||

Door
□□□□□□□□□□□□
```

The boundary between the wall and the door provides much stronger visual constraints than the middle of either surface.

Therefore, Semi-Dense methods mainly preserve pixels around edges and regions with significant intensity changes.

---

# Engineering Perspective

Today's discussion helped me understand that robotic perception is not simply about using as much data as possible.

Instead, engineers must carefully determine which information is valuable enough to justify the computational cost.

Semi-Dense SLAM represents an engineering compromise.

Compared with Dense methods,

- it significantly reduces computational complexity,

while compared with Sparse methods,

- it preserves more environmental structure.

This balance makes Semi-Dense methods attractive for robotic systems with limited computing resources.

---

# Reflection

Before today's discussion, I assumed that SLAM algorithms could simply be divided into Dense and Sparse categories.

However, learning about Semi-Dense SLAM changed this understanding.

Instead of viewing these methods as competing approaches, I now see them as different design choices under different engineering constraints.

The objective is not always to maximize accuracy, but rather to achieve an appropriate balance among computational efficiency, robustness, and environmental representation.

This engineering perspective is one of the most valuable ideas I learned today.

---

# Questions

Several questions remain for future investigation.

- How are high-gradient pixels selected?
- How does Semi-Dense SLAM perform in low-texture environments?
- Why are algorithms such as LSD-SLAM and DSO classified as Semi-Dense methods?
- Can Semi-Dense methods be combined with LiDAR perception?
- Why do many modern robotic systems still choose Sparse methods?

---

# Next Steps

- [x] Understand RGB-D sensors
- [x] Learn Dense methods
- [x] Learn Sparse methods
- [x] Understand Semi-Dense SLAM
- [ ] Compare RGB-D and LiDAR perception
- [ ] Learn feature extraction algorithms (ORB, FAST, etc.)

---

# Key Takeaway

Today's biggest takeaway is that Semi-Dense SLAM is not simply a compromise between Dense and Sparse methods.

Instead, it reflects an engineering philosophy:

> Use only the information that contributes most to localization and mapping while avoiding unnecessary computational overhead.

Understanding this balance helped me realize that designing robotic perception systems is not only about improving accuracy, but also about making practical engineering decisions under real-world constraints.

---

# References

- LSD-SLAM
- Direct Sparse Odometry (DSO)
- RGB-D SLAM Literature
