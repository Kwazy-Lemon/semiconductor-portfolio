# MOSFET Parameter Extraction
# MOSFET Parameter Extraction Toolkit

A MATLAB-based toolkit for compact MOSFET parameter extraction, verification, visualization, and model evaluation.

---

## Overview

This project aims to develop a complete toolkit for MOSFET compact model parameter extraction based on analytical Level-1 MOSFET models.

The toolkit focuses on improving parameter consistency, automation, reproducibility, and engineering usability through systematic extraction algorithms, verification procedures, visualization utilities, and simulation support.

The long-term objective is to build an open-source framework that integrates parameter extraction, parameter verification, compact model validation, and circuit simulation into a unified workflow.

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

```text
LTspice Simulation
        │
        ▼
Data Import
        │
        ▼
Parameter Extraction
        │
        ▼
Parameter Verification
        │
        ▼
Visualization
        │
        ▼
Compact Model Evaluation
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

- Initial project architecture
- Level-1 MOSFET extraction methodology
- IEEE conference publication
- MATLAB extraction algorithms

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

- MOSFET Modeling
- Compact Modeling
- Semiconductor Device Physics
- Parameter Extraction
- MATLAB Programming
- Numerical Optimization
- Device Characterization
- Data Visualization
- LTspice Simulation
- Engineering Research

---

## Future Development

Future versions of this toolkit will include:

- Higher-order compact model extraction
- BSIM model support
- Automatic report generation
- Python implementation
- Cross-platform support
- Open-source benchmarking datasets

---

**Author:** Jianhao Wu

**Research Interests**

- Semiconductor Devices
- MOSFET Modeling
- Compact Modeling
- Parameter Extraction
- Electronic Design Automation (EDA)
