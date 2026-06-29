# MOSFET Parameter Extraction Toolkit

A MATLAB-based toolkit for compact MOSFET parameter extraction, verification, visualization, and model evaluation.

---

## Overview
This project strives to create a MATLAB-based toolkit for the extraction, verification, visualization, and evaluation of compact MOSFET parameters.

The toolkit presently only considers analytical compact MOSFET models and seeks to enhance their consistency, automation, repeatability, and engineering friendliness.

Future iterations of the toolkit will eventually be able to handle more advanced compact MOSFET models.

---

## Objectives

The project is designed to:

- Extract Level-1 MOSFET compact model parameters automatically
- Reduce manual parameter tuning and improve repeatability
- Verify extracted parameters under multiple bias conditions
- Compare different optimization strategies
- Visualize extraction quality and fitting accuracy
- Provide reusable MATLAB implementations for semiconductor research

---

## Features

### Parameter Extraction

- Threshold voltage extraction
- Mobility parameter extraction
- Channel-length modulation extraction
- Output resistance estimation
- Multi-bias parameter extraction

### Parameter Verification

- Multi-bias consistency verification
- Analytical model validation
- Error analysis
- Parameter stability evaluation

### Visualization

- I–V curve comparison
- Fitting error plots
- Parameter comparison charts
- Statistical analysis

### Simulation Support

- LTspice data processing
- MATLAB automation
- Compact model validation
- Device characterization

---

## Workflow

```        LTspice
            │
            ▼
     Data Acquisition
            │
            ▼
 Parameter Extraction
            │
     ┌──────┴──────┐
     ▼             ▼
Verification   Visualization
     │             │
     └──────┬──────┘
            ▼
     Compact Model
        Evaluation
```

---

## Repository Structure

```
03_MOSFET_Parameter_Extraction
│
├── README.md
├── docs/
├── matlab/
├── ltspice/
├── datasets/
├── figures/
└── results/
```

---

## Current Progress

### Completed

✔ IEEE Conference Publication

✔ MATLAB Extraction Algorithms

✔ Level-1 Extraction Framework

✔ LTspice Automation

### In Development

- Parameter verification module
- Visualization toolkit
- Automated extraction workflow

### Planned

- Graphical user interface (GUI)
- Support for higher-order compact models
- Additional optimization algorithms
- SPICE model generation

---

## Related Publications

### Conference Paper

- **A Systematic and Bias-Consistent Parameter Extraction Framework for Level-1 MOSFET Models**
  - IEEE EICCT 2026
  - Published

### Journal Manuscripts

- Robust Parameter Extraction for MOSFET Compact Models Using Multi-Bias Regression and Simulation
  - Under Review

- Comparative Analysis of Optimization Strategies for MOSFET Compact Model Parameter Extraction Under Noisy Conditions
  - Under Review

---

## Skills Demonstrated

Modeling

• MOSFET Modeling
• Compact Modeling

Programming

• MATLAB
• LTspice

Research

• Parameter Extraction
• Numerical Optimization
• Device Characterization

---

## Future Development

Future versions of this toolkit will include:

- Higher-order compact model extraction
- BSIM model support
- Automatic report generation
- Python implementation
- Cross-platform support
- Open-source benchmarking datasets
The long-term goal is to develop an open-source compact modeling toolkit for semiconductor education and research.
---

**Author:** Jianhao Wu

**Research Interests**

- Semiconductor Devices
- MOSFET Modeling
- Compact Modeling
- Parameter Extraction
- Electronic Design Automation (EDA)
