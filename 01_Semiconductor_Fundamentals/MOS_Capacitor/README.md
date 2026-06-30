# MOS Capacitor
One of the basic elements in semiconductor device physics is the MOS (metal-oxide-semiconductor) capacitor. Despite the fact that it does not perform as an active transistor, it constitutes the physical basis for understanding how a MOSFET works. Fundamental ideas such as surface potential, depletion, inversion, threshold voltage, and channel formation have their origin in the electrostatics of the MOS capacitor.

This page briefly describes the operating principles of MOS capacitors.

---

## Device Structure

A MOS capacitor consists of three layers:

- **Metal Gate** – Controls the electric field by applying a gate voltage.
- **Oxide Layer** – A thin insulating layer, typically silicon dioxide (SiO₂), that electrically isolates the gate from the semiconductor.
- **Semiconductor Substrate** – Usually p-type or n-type silicon, where charge redistribution occurs under different gate biases.

When a voltage is applied to the gate, an electric field is generated across the oxide, causing the charge distribution inside the semiconductor to change.

>*                     Gate Voltage (VG)
                           ↓
        ┌────────────────────────────┐
        │        Metal Gate          │
        └────────────────────────────┘
        │      Silicon Dioxide       │
        │          (SiO₂)            │
        ──────────────────────────────
        │                            │
        │      p-type Silicon        │
        │        Substrate           │
        │                            │
        └────────────────────────────┘

          ← Hole / Electron Distribution →*

---

## Operating Modes

The behavior of a MOS capacitor depends on the applied gate voltage.

### Accumulation

When a negative gate voltage is applied to a p-type substrate, holes are attracted toward the oxide-semiconductor interface.

As a result,

- Hole concentration near the surface increases.
- No depletion region is formed.
- The surface conductivity increases.

---

### Depletion

When a small positive gate voltage is applied, holes are repelled away from the surface.

This creates a depletion region that contains fixed ionized acceptor atoms.

Characteristics include:

- Reduced hole concentration near the surface.
- Formation of a depletion region.
- Increasing depletion width as gate voltage increases.

---

### Inversion

As the positive gate voltage continues to increase, electrons become the dominant carriers near the surface.

An inversion layer (or channel) is formed at the oxide-semiconductor interface.

This inversion layer is the physical basis of channel formation in an n-channel MOSFET.

Key features include:

- Electron concentration exceeds hole concentration.
- Conductive channel begins to form.
- Gate voltage reaches or exceeds the threshold voltage.

---

## Energy Band Diagrams

The energy band diagram illustrates how the semiconductor responds to different gate voltages.

Three typical conditions are considered:

- Flat-band condition
- Depletion
- Strong inversion

Band bending increases with gate voltage and directly reflects changes in the surface potential.

> *Flat-band        Depletion        Strong Inversion
┌────────┐      ┌────────┐      ┌────────┐
│        │      │  ╱     │      │   ╱    │
│        │      │ ╱      │      │  ╱     │
│        │      │╱       │      │ ╱      │
└────────┘      └────────┘      └────────┘*

---

## Capacitance–Voltage (C–V) Characteristics

The capacitance of a MOS capacitor varies with gate voltage.

Typical regions include:

- Accumulation
- Depletion
- Inversion

The measured capacitance depends on both the operating region and the measurement frequency.

Understanding C–V characteristics is essential for determining:

- Oxide thickness
- Flat-band voltage
- Threshold voltage
- Interface quality

> *Capacitance

↑
│        HF
│───────────────╲
│                ╲__________
│                           ╲
│                            ╲
│                             ╲────────
│
│        LF
│───────────────╲
│                ╲
│                 ╲
│                  ╲──────────────
│
└──────────────────────────────────→ VG
   Acc.      Depletion     Inversion*

---

## Importance in MOSFETs

The MOS capacitor serves as the theoretical foundation for MOSFET operation.

Many important MOSFET concepts originate directly from MOS capacitor physics, including:

- Threshold voltage
- Surface potential
- Body effect
- Channel formation
- Compact device modeling
- Parameter extraction

For this reason, understanding MOS capacitors is an essential step before studying MOSFET modeling and semiconductor device characterization.

---

## Related Projects

- Semiconductor Fundamentals
- Device Characterization
- MOSFET Parameter Extraction Toolkit

---

## References

1. S. M. Sze and Kwok K. Ng, *Physics of Semiconductor Devices*, 3rd Edition.
2. Yannis Tsividis, *Operation and Modeling of the MOS Transistor*.
3. Columbia University — *MOS Transistors* Lecture Notes.
4. McGill University ECSE course materials.
