# Capacitance–Voltage (C–V) Characteristics

Understanding capacitance–voltage (C–V) characteristics is essential for semiconductor device characterization. C–V measurements provide valuable information about oxide quality, interface properties, doping concentration, and threshold voltage, making them one of the most important techniques in MOS device analysis.

---

# Overview

Capacitance–Voltage (C–V) characterization measures how the capacitance of a semiconductor device changes with the applied bias voltage.

Unlike current–voltage (I–V) measurements, C–V analysis focuses on the charge distribution inside the device. It is widely used to evaluate MOS capacitors and MOSFET structures during semiconductor process development and device characterization.

The extracted information serves as an important foundation for MOSFET compact modeling, parameter extraction, and semiconductor process evaluation.


---

# Physical Principle

A MOS capacitor consists of

- Metal Gate
- Oxide Layer
- Semiconductor Substrate

As the gate voltage changes, the carrier distribution underneath the oxide changes, producing different capacitance values.

Three operating regions can be observed:

## 1. Accumulation

- Majority carriers accumulate at the oxide interface.
- Capacitance approaches the oxide capacitance.
- Device exhibits maximum capacitance.

---

## 2. Depletion

- Majority carriers are repelled.
- A depletion region forms inside the substrate.
- Total capacitance decreases.

---

## 3. Inversion

- Minority carriers form an inversion layer.
- Low-frequency measurements recover oxide capacitance.
- High-frequency measurements remain near the minimum capacitance.

---

# Typical C–V Curve

*(Insert C–V curve figure here)*

Suggested figure:

```
Gate Voltage (VG)
        │
Cox ────┐────────────
         \
          \
           \
            \________
                 Cmin
```

---

# Important Parameters

## Oxide Capacitance (Cox)

The maximum capacitance measured during accumulation.

Applications:

- Oxide thickness extraction
- Process evaluation
- Device modeling

---

## Flat-Band Voltage (VFB)

The voltage at which the semiconductor energy bands become flat.

Applications:

- Fixed oxide charge analysis
- Interface charge evaluation

---

## Threshold Voltage (VT)

Estimated from the transition into inversion.

Applications:

- MOSFET modeling
- Compact model parameter extraction

---

# Applications

C–V characterization is widely used in

- MOS capacitor characterization
- MOSFET process monitoring
- Oxide thickness extraction
- Interface trap analysis
- Semiconductor process development
- Compact model parameter extraction

---

# Connection to Other Modules

This topic provides the experimental foundation for:

- Threshold Voltage Extraction
- Subthreshold Swing Analysis
- MOSFET Parameter Extraction
- Compact Device Modeling

---

# Key Takeaways

- C–V measurements reveal charge distribution inside semiconductor devices.
- Oxide capacitance reflects gate oxide properties.
- Flat-band voltage indicates oxide/interface charges.
- Threshold voltage can be estimated from C–V analysis.
- C–V characterization is an essential step before compact model parameter extraction.

---

# References

1. S. M. Sze, *Physics of Semiconductor Devices*.
2. Y. Tsividis, *Operation and Modeling of the MOS Transistor*.
3. Nicollian & Brews, *MOS Physics and Technology*.
4. Columbia University – MOS Transistor Course.
5. ASU Semiconductor Characterization Course.

