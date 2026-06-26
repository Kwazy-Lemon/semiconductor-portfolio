# Columbia University - MOS Transistors

## Course Information

- Institution: Columbia University
- Instructor: Yannis Tsividis
- Platform: Coursera
- Duration: ~20 hours
- Modules: 12
- Status: completed
---

## Overview

This repository documents my learning progress in MOS transistor physics and semiconductor device fundamentals through the Columbia University course.

---

## Topics Covered

- MOS Capacitors
- MOS Transistors
- Device Physics
- Threshold Voltage
- Current-Voltage Characteristics
- Short-Channel Effects

---

## Learning Progress

### Module 1 - Course Introduction and MOS Transistor Overview
#### Key Concepts
- Course objectives and learning roadmap
- Fundamentals of MOS transistor operation
- MOS capacitor and transistor structure
- Formation of the inversion layer
- Roles of gate voltage (VGS) and drain voltage (VDS)
- Weak, moderate, and strong inversion
- Linear region and saturation region
- Importance of compact MOSFET models in circuit design

#### Summary
This module will explain the general goals of the course and provide some insight about the behavior of the MOS transistor. In particular, it discusses how the gate voltage can control the number of carriers at the semiconductor surface to create a conductive channel between the source and drain. Various regimes of inversion and the current-voltage characteristics of the transistor are introduced here.

#### Reflection
The physical insight into MOS transistors is taught in this module. The knowledge about channel formation, channel inversion, and current flow in the transistor becomes very important while learning about compact modeling, parameter extraction, and semiconductor devices.

#### Connection to My Research
These topics taught in this module have direct connections to MOSFET parameter extraction and compact modeling. The knowledge about the threshold voltage, channel formation, and MOSFET working principle is helpful in interpreting the I-V curves obtained during experimentation.


### Module 2

#### Part 1 – CMOS Manufacturing Process
##### Key Concepts
- CMOS technology integrates both NMOS and PMOS transistors.
- NMOS devices are fabricated in p-type regions, while PMOS devices are fabricated in n-wells.
- LOCOS (Local Oxidation of Silicon) was an early isolation technology.
- Modern fabrication mainly uses Shallow Trench Isolation (STI).
- Source/drain extension regions reduce electric field concentration.
- Silicide layers lower contact resistance.
- Metal contacts connect devices to upper interconnect layers.
- Strain engineering improves carrier mobility in advanced CMOS technologies.


#### Part 2 - Semiconductor Fundamentals
##### Key Concepts
###### Semiconductor Equilibrium
- Semiconductor analysis begins under thermal equilibrium conditions.
- No external electric field, illumination, or current is assumed.
- The Fermi level remains constant throughout the material.

###### Intrinsic Semiconductor
- Pure silicon contains equal concentrations of electrons and holes.
- Thermal energy excites electrons from the valence band into the conduction band.
- Every generated electron leaves behind a corresponding hole.

###### Extrinsic Semiconductor
- N-type silicon is created by donor impurities (e.g., phosphorus).
- P-type silicon is created by acceptor impurities (e.g., boron).
- Electrons are majority carriers in n-type materials.
- Holes are majority carriers in p-type materials.
- Carrier concentrations satisfy the mass-action law:
  np = ni²

###### Energy Band Model
- Electron transport is described using the conduction band and valence band.
- Doping shifts the Fermi level toward either the conduction or valence band.
- Band diagrams provide a physical interpretation of carrier behavior.

###### Carrier Statistics
- Carrier concentrations follow Fermi–Dirac statistics.
- Under normal operating conditions, Maxwell–Boltzmann approximation is usually sufficient.
- The thermal voltage (VT) simplifies carrier concentration equations.

###### Electrostatics
- Charge density determines the electric field.
- Electric potential is obtained from the electric field.
- Poisson's equation connects charge density and electrostatic potential.

###### Non-equilibrium Conditions
- Current flow introduces non-equilibrium conditions.
- Separate quasi-Fermi levels are used for electrons and holes.
- These concepts are essential for PN junctions and MOS transistor operation.


#### Part 3 - Conduction
##### Key Concepts
###### Carrier Transport Mechanisms
Semiconductor current consists of two fundamental transport mechanisms:
- Drift
- Diffusion
The total current is the sum of both components.

###### Drift Current
- Drift is caused by an external electric field.
- Carrier drift velocity is proportional to the electric field under low-field conditions.
v_d = μE
where:
- μ is the carrier mobility.
- E is the electric field.
At high electric fields, carrier velocity approaches saturation due to lattice scattering.

###### Diffusion Current
- Diffusion results from carrier concentration gradients.
- Carriers naturally move from regions of high concentration to low concentration.
- Diffusion is a statistical transport process driven by thermal motion.
The diffusion current is proportional to the carrier concentration gradient.

###### Einstein Relation
Carrier mobility and diffusion coefficient are related by
D = μVT
where VT is the thermal voltage.

###### Total Current
Both electrons and holes contribute to current through drift and diffusion.
Total current consists of:
- Electron drift current
- Electron diffusion current
- Hole drift current
- Hole diffusion current

#### Part 4 - Contact Potentials & PN Junctions
##### Key Concepts
###### Contact Potential
- Different materials possess different work functions.
- When two materials are brought into contact, electrons move from the material with a lower work function to the one with a higher work function.
- Electron diffusion continues until thermal equilibrium is reached.
- At equilibrium, the Fermi levels of both materials become aligned.
- The resulting electric field creates a built-in contact potential.

###### Work Function
- The work function represents the energy required to remove an electron from the Fermi level to the vacuum level.
- Differences in work function determine the magnitude of the contact potential.

###### PN Junction at Equilibrium
- Carrier diffusion forms a depletion region.
- Ionized donors and acceptors generate an internal electric field.
- A built-in potential opposes further carrier diffusion.
- The Fermi level remains constant across the junction.

###### Forward Bias
- Applying a forward bias lowers the built-in potential barrier.
- The depletion region becomes narrower.
- Carrier injection increases dramatically.
- The diode current increases approximately exponentially.

###### Quasi-Fermi Levels
- Under non-equilibrium conditions, electrons and holes are described by separate quasi-Fermi levels.
- Quasi-Fermi levels explain carrier transport under applied bias.

#### Part 5 - PN Junctions(Reverse Bias)
##### Key Concepts
###### Reverse-Biased PN Junction
- Applying a reverse bias increases the built-in potential barrier.
- The depletion region widens as the reverse voltage increases.
- Carrier diffusion is strongly suppressed.
- The maximum electric field occurs near the metallurgical junction.

###### Charge Distribution
- Fixed ionized donors and acceptors remain inside the depletion region.
- Charge density is approximately constant within each side of the depletion region.
- Electric field and potential are obtained by integrating the charge distribution.

###### One-Sided Junction Approximation
- For highly asymmetric doping (N⁺/P junction), the depletion region mainly extends into the lightly doped side.
- Depletion width depends on:
  - Doping concentration
  - Dielectric constant
  - Built-in potential
  - Applied reverse voltage
 
###### Junction Capacitance
- A reverse-biased PN junction behaves like a voltage-dependent capacitor.
- Junction capacitance is defined as
  Cj = dQ / dV
- Increasing reverse bias widens the depletion region and decreases junction capacitance.

###### Dynamic Performance
- Junction capacitance limits the switching speed of semiconductor devices.
- Lower junction capacitance enables faster circuit operation.

#### Module Summary
This unit builds the semiconductor physics that are needed to understand the functioning of MOS transistors. The CMOS process technology, semiconductor physics, carrier transport, PN junction electrostatics, and junction capacitance concepts all form the physical basis of MOS transistor modeling.

#### What I Learned
In this module, I acquired an organized knowledge about the physics behind semiconductor devices. This included the fabrication process of modern CMOS transistors, the factors that affect semiconductors through carrier concentration and energy band structures, and carrier transport under the influence of drift and diffusion. Furthermore, I became proficient in the concept of PN junction electrostatics such as built-in voltage, depletion layers, reverse bias conditions, and junction capacitance. This forms the basis of study for MOS capacitors, MOS transistors, and MOSFET models in upcoming modules.

#### Research Connection
The topics covered in this module form the basis of MOSFET compact modeling and parameter extraction. Knowledge of carrier transport, electrostatics, PN junction, and junction capacitance is necessary to understand the MOSFET I-V behavior and develop the physics-based compact model.

### Module 3
Coming soon.

### Module 4
Coming soon.

---

## Skills Acquired

- MOS Device Physics
- Semiconductor Fundamentals
- Device Modeling
- Analytical Thinking

---

## Reflection

This course strengthens my understanding of MOS transistor operation and semiconductor device physics, providing theoretical foundations for my research on MOSFET modeling and parameter extraction.
