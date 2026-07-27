# Current–Voltage (I–V) Characteristics

Current–Voltage (I–V) characterization is one of the most fundamental techniques used to evaluate semiconductor devices. By measuring the relationship between applied voltage and current, important electrical parameters such as threshold voltage, carrier mobility, transconductance, and output resistance can be extracted.

For MOSFETs, I–V measurements provide the experimental basis for parameter extraction, compact modeling, and circuit simulation.

---

# Overview

I–V characterization investigates how the drain current changes under different bias conditions.

Two types of measurements are commonly performed:

- Output Characteristics (ID–VDS)
- Transfer Characteristics (ID–VGS)

These measurements reveal the operating behavior of MOSFETs under different gate and drain voltages and serve as the foundation for semiconductor device characterization.

---

# Learning Objectives

After completing this section, the reader should be able to:

- Understand the principles of I–V characterization.
- Interpret MOSFET output and transfer characteristics.
- Identify different operating regions of a MOSFET.
- Understand how electrical parameters are extracted from I–V curves.
- Relate I–V measurements to compact device modeling.

---

# Physical Principle

The electrical behavior of a MOSFET depends on the gate voltage and drain voltage.

The gate voltage controls channel formation, while the drain voltage determines carrier transport inside the channel.

By sweeping different bias voltages and measuring the corresponding drain current, the electrical characteristics of the device can be analyzed.

---

# Output Characteristics (ID–VDS)

Output characteristics describe the relationship between drain current (ID) and drain voltage (VDS) under different gate voltages (VGS).

Typical operating regions include:

## Cutoff Region

- VGS < VT
- No inversion channel
- Drain current is nearly zero.

---

## Linear Region

- VGS > VT
- Small VDS
- Drain current increases approximately linearly with VDS.

Applications:

- Channel resistance analysis
- On-state performance evaluation

---

## Saturation Region

- VGS > VT
- VDS ≥ VGS − VT
- Drain current becomes nearly independent of VDS.

Applications:

- Analog circuit design
- Parameter extraction
- Compact modeling

---

# Transfer Characteristics (ID–VGS)

Transfer characteristics describe the variation of drain current with gate voltage while keeping VDS constant.

The transfer curve provides important information for extracting:

- Threshold Voltage (VT)
- Transconductance (gm)
- Carrier Mobility (μ)
- Subthreshold Swing (SS)

---

# Typical I–V Curves

### Output Characteristics

*(Insert ID–VDS curve here)*

Suggested figure:

```
ID
│            VGS3
│          ________
│        /
│      /
│    /
│__/________________ VDS
     VGS2
     VGS1
```

---

### Transfer Characteristics

*(Insert ID–VGS curve here)*

Suggested figure:

```
ID
│
│            /
│          /
│        /
│______/____________ VGS
      VT
```

---

# Important Parameters

## Threshold Voltage (VT)

Minimum gate voltage required to form a conducting channel.

Applications:

- Device modeling
- Parameter extraction
- Circuit simulation

---

## Transconductance (gm)

Represents the sensitivity of drain current to gate voltage.

Applications:

- Analog circuit design
- Device performance evaluation

---

## Carrier Mobility (μ)

Reflects carrier transport capability inside the channel.

Applications:

- Technology comparison
- Compact modeling

---

## Output Resistance (ro)

Characterizes the dependence of drain current on drain voltage in saturation.

Applications:

- Analog circuit analysis
- Small-signal modeling

---

# Applications

I–V characterization is widely used in:

- MOSFET characterization
- Semiconductor process evaluation
- Device parameter extraction
- Compact model development
- SPICE model calibration
- Circuit performance analysis

---

# Connection to Other Modules

This section provides the experimental foundation for:

- Threshold Voltage Extraction
- Subthreshold Swing
- MOSFET Parameter Extraction
- Electronic Design Automation (EDA)

---

# Key Takeaways

- I–V measurements reveal the electrical behavior of semiconductor devices.
- Output characteristics describe the influence of drain voltage.
- Transfer characteristics describe the influence of gate voltage.
- Important parameters such as VT, gm, mobility, and output resistance can be extracted.
- I–V characterization is the starting point for compact model parameter extraction.

---

# References

1. S. M. Sze, *Physics of Semiconductor Devices*.
2. Y. Tsividis, *Operation and Modeling of the MOS Transistor*.
3. BSIM MOSFET Model Documentation.
4. Columbia University – MOS Transistor Course.
5. ASU Semiconductor Characterization Course.

