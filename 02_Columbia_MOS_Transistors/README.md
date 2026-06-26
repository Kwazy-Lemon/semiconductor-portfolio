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

---

### Module 2 - Priliminaries and Background

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

#### Summary
This unit builds the semiconductor physics that are needed to understand the functioning of MOS transistors. The CMOS process technology, semiconductor physics, carrier transport, PN junction electrostatics, and junction capacitance concepts all form the physical basis of MOS transistor modeling.

#### Reflection
In this module, I acquired an organized knowledge about the physics behind semiconductor devices. This included the fabrication process of modern CMOS transistors, the factors that affect semiconductors through carrier concentration and energy band structures, and carrier transport under the influence of drift and diffusion. Furthermore, I became proficient in the concept of PN junction electrostatics such as built-in voltage, depletion layers, reverse bias conditions, and junction capacitance. This forms the basis of study for MOS capacitors, MOS transistors, and MOSFET models in upcoming modules.

#### Connection to My Research
The topics covered in this module form the basis of MOSFET compact modeling and parameter extraction. Knowledge of carrier transport, electrostatics, PN junction, and junction capacitance is necessary to understand the MOSFET I-V behavior and develop the physics-based compact model.

---

### Module 3 - The Two-Terminal and Three-Terminal MOS Structures
#### Part 1 – Flatband Voltage and Surface Condition
##### Key Concepts
- The two-terminal structure of the MOS device is the basis of analysis of MOS transistor operation.
- The voltage at which the semiconductor energy bands become flat is known as flatband voltage (VFB).
- Flatband voltage is defined by the work-function difference and interface charge.
- Gate voltage regulates the state of the semiconductor surface through accumulation, depletion, and inversion states.
- The surface potential determines the bending of energy band and carrier concentration at the semiconductor surface.
- Inversion happens when there are enough minority carriers to create an inversion layer.

#### Part 2 - General Analysis, Inversion, and Strong Inversion
##### Key Concepts
- Formulated an analysis framework of the MOS structure for accumulation, depletion, and inversion regions.
- Surface potential (ψs) is derived as a function of the gate bias voltage (VGB) based on charge and potential balance considerations.
- The net charge on the semiconductor side of the oxide layer is comprised of depletion charge and inversion charge.
- Weak, moderate, and strong inversion describe different regimes of correlation between surface potential and the inversion charge.
- Strong inversion means that surface potential remains essentially constant, while the inversion charge grows almost linearly with gate voltage.
- Threshold voltage (VT0) is defined as a parameter of the strong inversion regime and serves as a foundation for MOSFET modeling.

#### Part 3 - Weak Inversion and Small-Signal Capacitance
##### Key Concepts
- Weak inversion is described by an exponential relation between the inversion charge and the gate voltage.
- Different mathematical models need to be considered in the case of weak, moderate, and strong inversion, since a single equation will not represent all regions appropriately.
- The small-signal model considers the change in charge and voltage incrementally in the model of MOSFET.
- The gate-body capacitance CGB is defined as a serial connection of the oxide capacitance and semiconductor capacitance.
- The semiconductor capacitance includes depletion capacitance and inversion capacitance.
- The measured value of gate capacitance varies with respect to signal frequency due to inversion charge carriers.

#### Part 4 - The Three-Terminal MOS Structure
##### Key Concepts
- A third terminal introduces an effect on the carrier concentration in the inversion layer in relation to the body-to-channel voltage (VCB).
- Reverse body bias lowers the inversion charge and raises the inversion onset point gate voltage.
- The body effect is responsible for the rise in threshold voltage when the body bias becomes high.
- The body effect coefficient (γ) is used to measure the sensitivity of the threshold voltage to body bias.
- Strong and weak inversion formulas can be adapted from the two terminal MOS by including the body bias.
- The pinch-off voltage is the body bias where the strong inversion model assumes zero inversion charge.

#### Summary
In this module, the study of the MOS capacitor is continued beyond electrostatic analysis to its real life application. Flatband voltage, surface characteristics, inversion phenomena, small signal capacitance, and the structure of the MOS device with three terminals will be discussed in this module. This module will also discuss how body bias affects the inversion charge and threshold voltage.

#### Reflection
In this module, I was able to develop an understanding of the electrostatics and inversion physics of the MOS structure. This included gaining knowledge on how the gate voltage controls the state of the semiconductor at its surface, how the concept of inversion is built up from weak to strong inversion, and how the carrier density affects the behavior of the structure.

#### Connection to My Research
These concepts that have been learned in this module are actually very relevant to compact MOSFET modeling and parameter extraction. Some of the parameters that are very important in compact MOSFET models like EKV and BSIM include surface potential, inversion charge, threshold voltage, body effect, and small signal capacitance. Knowledge about these physical phenomena gives the basis for the successful modeling of MOSFET behavior and parameter extraction.

---

### Module 4 - The Long-Channel MOS Transistor 1
#### Part 1 – Introduction to the Long-Channel MOS Transistor
##### Key Concepts
- Assumptions and structure of long-channel MOSFETs.
- Operation of four-terminal MOSFETs with various biases.
- Formation of channel and current flow at strong inversion.
- IDS-VDS behavior and inversion zones.
- Basic physical model of MOSFET compact modeling.

#### Part 2 – Complete All-Region Model and Simplified All-Region Models
##### Key Concepts
- The all-region model represents the behavior of the MOSFET through the regions of weak, moderate, and strong inversion.
- The channel current includes drift and diffusion terms.
- The drift term plays the dominant role during strong inversion, and the diffusion term becomes dominant during weak inversion.
- Surface potential is the main parameter in finding the drain current.
- All-region simplified models enhance computational efficiency without decreasing accuracy.
- They form the basis for advanced MOSFET models like PSP, EKV, and HiSIM.

#### Part 3 – Strong Inversion Models I
##### Key Concepts
- The inversion flow in a strong inversion regime involves drifting and neglects diffusing.
- Models for strong inversions offer explicit expressions for drain currents in terms of voltage across terminals.
- The non-saturation mode is based on strong inversions over the whole channel.
- Transition to the saturation mode takes place when the inversion charges at the drain end become zero.
- The saturation flow in long-channel devices is considered nearly constant.
- Simple models for strong inversions help enhance computational performance without sacrificing accuracy.

#### Summary
The operation of the long-channel MOSFET was discussed and models of currents were developed for various regions of inversion. The derivation of the simplified models of currents in the case of strong inversion was done from the all-regions model, which was used to describe the switching from linear to saturation modes of operation of MOSFETs.

#### Reflection
In this module, I came to know about how semiconductor physics is applied to build models of transistor currents. Drift current dominance during strong inversion became clear, along with the need for different models according to the different operating regions.

#### Connection to my Research
The modeling tools currently covered in this module are highly relevant to the work I am doing on MOSFET compact modeling and parameter extraction, which involves establishing the link between inversion charge, threshold voltage, and drain current as the physical foundation for model validation and parameter extraction.


---

### Module 5 - The Long-Channel MOS Transistor 2
#### Part 1 – Strong Inversion Models II
##### Key Concepts

#### Part 2 – Weak Inversion Models and Source Reference vs. Body Reference
##### Key Concepts

#### Part 3 – Effective Mobility
##### Key Concepts

#### Part 4 – Additional Topics
##### Key Concepts

#### Summary
#### Reflection
#### Connection to my Research
---

### Module 6 - Small - Dimension Effect 1
#### Part 1 – Velocity Saturation
##### Key Concepts

#### Part 2 – Channel Length Modulation
##### Key Concepts

#### Part 3 – Charge Sharing
##### Key Concepts

#### Part 4 – Drain-Induced Barrier Lowering and Combining Several Effects Into One Model
##### Key Concepts

#### Part 5 – Hot Carrier Effects and Velocity Overshoot and Ballistic Operation
##### Key Concepts

#### Part 6 – Polysilicon Depletion
##### Key Concepts

#### Summary
#### Reflection
#### Connection to my Research

---

### Module 7 - Small - Dimension Effect 2 & Modelling for Circuits Simulation
#### Part 1 – Quantum-Mechanical Effects; Gate Curren, Junction Leakage, and Scaling and New Technologies
##### Key Concepts

#### Part 2 – Approaches and Properties of Good Models and Model Formulation Considerations
##### Key Concepts

#### Part 3 – Parameter Extraction
##### Key Concepts

#### Part 4 – Representative Compact Models and Benchmark Tests
##### Key Concepts

#### Summary
#### Reflection
#### Connection to my Research

---

### Module 8 - Large - Signal Dynamic Operation
#### Part 1 – Quasi-Static Operation, Terminal Currents in QS Operation, amd Charging Currents in QS Operation
##### Key Concepts

#### Part 2 – Evaluation of Charges, Transit Time, and Transient Response Using QS Modeling
##### Key Concepts
#### Part 3 – Non-Quasi-Static Operation and Extrinsic Parasitics
##### Key Concepts

#### Summary
#### Reflection
#### Connection to my Research


---

### Module 9 - Small-Signal Modeling 1
#### Part 1 – Conductance Parameters
##### Key Concepts

#### Part 2 – Transconductance
##### Key Concepts

#### Part 3 – Source-Drain and Output Conductance and Capacitance Definitions and Equivalent Circuits
##### Key Concepts

#### Part 4 – Capacitance Evaluation and Properties
##### Key Concepts

#### Summary
#### Reflection
#### Connection to my Research

---

### Module 10 - Small-Signal Modeling 2
#### Part 1 – Complete Capacitance Parameter Set and Complete Quasi-Static Model
##### Key Concepts

#### Part 2 – y-Parameter Model and Non-Quasi-Static Model
##### Key Concepts

#### Part 3 – Model Comparison and RF Models
##### Key Concepts

#### Summary
#### Reflection
#### Connection to my Research

---

### Module 11&12 - Final Exam & End of Course



---
## Skills Acquired

- MOS Device Physics
- Semiconductor Fundamentals
- Device Modeling
- Analytical Thinking

---

## Reflection

This course strengthens my understanding of MOS transistor operation and semiconductor device physics, providing theoretical foundations for my research on MOSFET modeling and parameter extraction.
