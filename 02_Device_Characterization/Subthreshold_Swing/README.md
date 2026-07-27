# Subthreshold Swing

Subthreshold Swing (SS) is one of the most important parameters used to evaluate the switching performance of MOSFETs. It describes how efficiently the drain current changes with gate voltage in the subthreshold region and directly reflects the gate's electrostatic control over the channel.

A smaller subthreshold swing indicates better switching characteristics, lower power consumption, and higher device performance.

---

# Overview

When the gate voltage is below the threshold voltage, the MOSFET is not completely turned off.

Instead, a small diffusion current still flows through the channel.

This operating region is known as the **subthreshold region**.

Subthreshold Swing characterizes how rapidly the drain current increases as the gate voltage approaches the threshold voltage.

It is one of the most important figures of merit for low-power CMOS technology.

---

# Physical Principle

In the subthreshold region,

```
VGS < VT
```

the inversion layer has not yet been fully established.

The drain current is dominated by **carrier diffusion** rather than drift.

Consequently, the drain current increases exponentially with gate voltage.

When the transfer characteristic is plotted on a logarithmic scale, this region appears approximately linear.

---

# Definition

Subthreshold Swing is defined as the gate voltage required to increase the drain current by one decade.

\[
SS=\frac{dV_{GS}}{d(\log_{10}I_D)}
\]

Unit:

```
mV/dec
```

A smaller value represents better switching efficiency.

---

# Typical Transfer Curve

<img width="266" height="258" alt="image" src="https://github.com/user-attachments/assets/85fe279a-2420-48fc-b447-ba8d3163d812" />


Suggested figure:

```
ID (log)

│
│                     Strong Inversion
│                   /
│                 /
│               /
│             /
│___________/
│
└──────────────────────────── VGS
        Subthreshold Region

Slope → Subthreshold Swing
```

---

# Typical Values

| Technology | Typical SS |
|------------|------------|
| Ideal MOSFET | 60 mV/dec |
| Modern CMOS | 65–90 mV/dec |
| Practical Devices | 70–100 mV/dec |

The theoretical limit for conventional MOSFETs at room temperature is approximately

```
60 mV/dec
```

---

# Factors Affecting Subthreshold Swing

Subthreshold Swing is influenced by several physical factors, including

- Gate oxide thickness
- Interface trap density
- Oxide capacitance
- Depletion capacitance
- Temperature
- Device scaling

Reducing interface defects and improving gate electrostatic control can significantly improve SS.

---

# Applications

Subthreshold Swing is widely used in

- Low-power CMOS design
- Device scaling evaluation
- Technology comparison
- MOSFET parameter extraction
- Compact model calibration
- Semiconductor process optimization

---

# Connection to Other Modules

This topic is closely related to

- I–V Characteristics
- Threshold Voltage Extraction
- Mobility Extraction
- MOSFET Parameter Extraction
- Compact Device Modeling

---

# Key Takeaways

- Subthreshold Swing describes switching efficiency below threshold voltage.
- Drain current follows exponential behavior in the subthreshold region.
- Lower SS indicates better electrostatic gate control.
- The theoretical limit for conventional MOSFETs is approximately 60 mV/dec.
- SS is a critical parameter for low-power semiconductor devices.

---

# References

1. S. M. Sze, *Physics of Semiconductor Devices*.
2. Y. Tsividis, *Operation and Modeling of the MOS Transistor*.
3. BSIM MOSFET Model Documentation.
4. Columbia University – MOS Transistor Course.
5. ASU Semiconductor Characterization Course.

