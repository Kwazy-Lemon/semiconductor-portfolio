# Robocon 2026 – Autonomous Robotics Learning Portfolio

> Independent study and technical documentation of autonomous robotics technologies based on the 25th China University Robocon Competition.

---

## Overview

This repository documents my independent learning of autonomous robotics through the 25th China University Robocon Competition (Robocon 2026).

The primary objective is not to reproduce the competition itself, but to understand the engineering principles behind an autonomous competition robot, including perception, localization, software architecture, system integration, and robot cooperation.

Throughout this learning process, I study both the official competition rules and the technical implementation used by the robotics team, while organizing my understanding into a structured engineering knowledge base.

---

# Competition Background

The 25th China University Robocon Competition adopts the theme

> **Martial Arts Exploration (武林探秘)**

Inspired by traditional Chinese martial arts culture, two cooperative robots must complete a sequence of tasks including weapon assembly, autonomous exploration, secret manual collection, and strategic confrontation. The competition combines traditional cultural elements with modern robotics technologies such as autonomous navigation, perception, localization, and multi-robot cooperation. 
<img width="629" height="500" alt="image" src="https://github.com/user-attachments/assets/2e124995-9d1a-4be7-bded-bfe2667fed67" />

---

# Competition Structure

Each team is allowed to use **two robots**.

## R1

Manual / Semi-autonomous Robot

Main responsibilities include

- Weapon assembly
- Transportation
- Collecting R1 secret manuals
- Nine-grid confrontation
- Cooperation with R2
<img width="677" height="206" alt="image" src="https://github.com/user-attachments/assets/12c25bdc-8370-4f3a-8c0a-71fa722ba858" />

---

## R2

Fully Autonomous Robot

Main responsibilities include

- Autonomous navigation
- LiDAR perception
- Localization
- Secret manual recognition
- Collecting R2 secret manuals
- Multi-stage decision making
- Cooperation with R1

According to the official rules, **R2 must operate as a fully autonomous robot without manual intervention.** :contentReference[oaicite:1]{index=1}
<img width="604" height="311" alt="image" src="https://github.com/user-attachments/assets/a1b51309-1c43-4111-b4ef-e0bd26e651e8" />

---

# Engineering Topics

Instead of concentrating only on the competition rules, this repository focuses on the engineering technologies required for building an autonomous competition robot.

Current learning topics include

- Robot System Architecture
- Ubuntu
- Linux
- ROS2
- RViz
- Livox MID360
- LiDAR Fundamentals
- Point Cloud Processing
- FAST-LIO
- Robot Localization
- Coordinate Systems (TF)
- Robot Perception
- Autonomous Navigation
- Multi-Robot Cooperation

---

# Learning Objectives

The goal of this project is to understand

- how an autonomous robot is designed;
- how perception information flows through the software stack;
- how LiDAR and IMU are integrated for localization;
- how autonomous robots cooperate to accomplish complex tasks;
- how robotic software systems are organized in practice.

---

# Technical Knowledge Base

The detailed learning notes are maintained in independent repositories.

| Topic | Status |
|-------|--------|
| Robot System Architecture | 🚧 |
| Ubuntu & Linux | 🚧 |
| ROS2 | 🚧 |
| RViz | 🚧 |
| Livox MID360 | 🚧 |
| LiDAR Fundamentals | 🚧 |
| Point Cloud Processing | 🚧 |
| FAST-LIO | 🚧 |
| Robot Localization | 🚧 |
| Navigation | 🚧 |

---

# Learning Outcome

This repository records the complete learning process of autonomous robotics, including

- technical notes
- architecture diagrams
- software workflow
- perception pipeline
- engineering observations
- competition analysis
- implementation summaries

The repository will continue to evolve as new topics are studied.

---

# References

- Official Robocon 2026 Rulebook
- ROS2 Documentation
- Livox Documentation
- FAST-LIO
- Related research papers
