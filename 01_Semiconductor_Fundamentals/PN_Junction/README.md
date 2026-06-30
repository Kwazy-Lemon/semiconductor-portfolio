# PN Junction

The PN junction is one of the most fundamental semiconductor structures and serves as the building block of many electronic devices, including diodes, bipolar junction transistors (BJTs), and MOSFETs. Understanding its electrical behavior is essential for studying carrier transport, semiconductor device operation, and integrated circuit technology.

This page summarizes the physical principles, electrical characteristics, and engineering significance of the PN junction.

---

## Overview

A PN junction is formed by joining p-type and n-type semiconductor materials. Due to the concentration difference of electrons and holes, carriers diffuse across the junction immediately after contact.

This diffusion process creates a depletion region and establishes a built-in electric field, eventually reaching thermal equilibrium. The interaction between carrier diffusion and the electric field determines the electrical characteristics of the junction.

---

## Device Structure

A typical PN junction consists of two semiconductor regions:

- **p-type Region** – Rich in holes as the majority carriers.
- **n-type Region** – Rich in electrons as the majority carriers.
- **Depletion Region** – Contains fixed ionized dopants and very few mobile carriers.
- **Built-in Electric Field** – Opposes further carrier diffusion and establishes equilibrium.

<img width="777" height="508" alt="image" src="https://github.com/user-attachments/assets/6b7a17aa-dced-4508-bd54-db2f484441e3" />


---

## Carrier Diffusion

Before equilibrium is established, electrons diffuse from the n-type region into the p-type region, while holes diffuse in the opposite direction.

This diffusion occurs because carriers naturally move from regions of high concentration to regions of low concentration.

As diffusion continues, ionized donor and acceptor atoms remain near the junction, leading to the formation of the depletion region.

---

## Depletion Region

The depletion region is formed when mobile carriers leave the vicinity of the junction.

Important characteristics include:

- Very low concentration of free carriers.
- Presence of fixed ionized donor and acceptor atoms.
- Formation of an internal electric field.
- Width depends on doping concentration and applied voltage.

<img width="800" height="530" alt="image" src="https://github.com/user-attachments/assets/b775894a-16f8-4725-b70d-a6247aaab13f" />


---

## Forward and Reverse Bias

### Forward Bias

Applying a forward voltage reduces the built-in potential barrier.

As a result,

- The depletion region becomes narrower.
- Carrier injection increases.
- A large diffusion current flows through the junction.

---

### Reverse Bias

Applying a reverse voltage increases the potential barrier.

Consequently,

- The depletion region widens.
- Only a very small leakage current flows.
- The junction behaves as an insulator until breakdown occurs.

<img width="794" height="535" alt="image" src="https://github.com/user-attachments/assets/f7d25b8c-717b-4121-94d6-5f67f27ada92" />


---

## Current–Voltage (I–V) Characteristics

The electrical behavior of a PN junction is described by its current–voltage characteristics.

Typical features include:

- Exponential current increase under forward bias.
- Extremely small reverse leakage current.
- Reverse breakdown at sufficiently high reverse voltage.

<img width="804" height="528" alt="image" src="https://github.com/user-attachments/assets/4f68c215-f70c-446d-a32c-5aee137412cb" />

---

## Applications

The PN junction is the fundamental building block of many semiconductor devices, including:

- PN junction diodes
- Light-emitting diodes (LEDs)
- Photodiodes
- Bipolar junction transistors (BJTs)
- CMOS integrated circuits
- Semiconductor sensors

Understanding the PN junction also provides the foundation for studying semiconductor device characterization and MOSFET operation.

---

## References

1. S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed. Wiley, 2007.

2. R. F. Pierret, *Semiconductor Device Fundamentals*. Addison-Wesley, 1996.

3. Columbia University, *MOS Transistors* Course Materials.
