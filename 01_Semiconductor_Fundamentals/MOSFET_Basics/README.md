# MOSFET Basics

The Metal–Oxide–Semiconductor Field-Effect Transistor (MOSFET) is the most widely used semiconductor device in modern integrated circuits. It operates by controlling the formation of a conductive channel through an electric field applied at the gate terminal.

This page introduces the basic structure, operating principles, electrical characteristics, and applications of MOSFETs. The concepts presented here provide the foundation for the device characterization and parameter extraction projects included in this portfolio.

---

## Overview

A MOSFET is a voltage-controlled semiconductor device consisting of four terminals: gate, source, drain, and body (substrate). By applying a gate voltage, the conductivity of the semiconductor surface can be controlled, allowing current to flow between the source and drain.

Compared with bipolar junction transistors (BJTs), MOSFETs offer high input impedance, low power consumption, and excellent scalability, making them the dominant device in modern CMOS technology.

---

## Device Structure

A typical n-channel MOSFET consists of:

- **Gate** – Controls channel formation through the applied gate voltage.
- **Gate Oxide** – A thin insulating layer that separates the gate from the semiconductor.
- **Source** – Supplies electrons to the channel.
- **Drain** – Collects electrons from the channel.
- **Body (Substrate)** – Usually p-type silicon.

<img width="760" height="514" alt="image" src="https://github.com/user-attachments/assets/1946dccc-92e7-44b9-8a33-e27cd44a975a" />


---

## Operating Principle

When no gate voltage is applied, no conductive channel exists between the source and drain.

As the gate voltage increases, electrons accumulate near the oxide-semiconductor interface. Once the gate voltage exceeds the threshold voltage, an inversion channel is formed, allowing current to flow from drain to source.

<img width="795" height="526" alt="image" src="https://github.com/user-attachments/assets/a4b1e1dd-3cf1-41b7-9de1-594fce514d99" />


---

## Operating Regions

### Cutoff Region

When the gate voltage is below the threshold voltage,

- No inversion channel exists.
- Drain current is approximately zero.

---

### Linear Region

When the gate voltage exceeds the threshold voltage and the drain voltage remains relatively small,

- A conductive channel forms.
- Drain current increases approximately linearly with drain voltage.
- The MOSFET behaves similarly to a voltage-controlled resistor.

---

### Saturation Region

As the drain voltage increases further,

- The channel becomes pinched off near the drain.
- Drain current becomes relatively insensitive to drain voltage.
- The MOSFET operates as an amplifier.

---

## Transfer Characteristics

The transfer characteristic describes the relationship between the drain current and the gate voltage.

Important parameters include:

- Threshold voltage (VTH)
- Transconductance (gm)
- Subthreshold region
- On-state current

<img width="806" height="527" alt="image" src="https://github.com/user-attachments/assets/b3dca5d8-55ab-4216-8b04-97d2cf4f6342" />


---

## Output Characteristics

The output characteristic shows how the drain current changes with drain voltage under different gate voltages.

Typical regions include:

- Linear region
- Saturation region

Output characteristics are widely used in device characterization and compact model extraction.

<img width="800" height="527" alt="image" src="https://github.com/user-attachments/assets/88fd379c-6d92-4a2f-b49e-5aaef1ece325" />


---

## Applications

MOSFETs are widely used in modern electronic systems, including:

- CMOS integrated circuits
- Digital logic
- Analog integrated circuits
- Power electronics
- Memory devices
- Semiconductor sensors

In this portfolio, the operating principles introduced here are further explored through:

- Device Characterization
- MOSFET Parameter Extraction Toolkit
- Research Publications

---

## References

1. S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed. Wiley, 2007.

2. Y. Tsividis and C. McAndrew, *Operation and Modeling of the MOS Transistor*, 3rd ed. Oxford University Press, 2011.

3. Columbia University, *MOS Transistors* Course Materials.
