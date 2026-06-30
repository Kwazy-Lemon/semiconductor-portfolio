# MOSFET Parameter Extraction Toolkit

A MATLAB-based educational toolkit for automatic extraction of Level-1 MOSFET parameters from LTspice simulation data.

---

## Overview

The **MOSFET Parameter Extraction Toolkit** is an open-source MATLAB project developed to automate the extraction of fundamental MOSFET parameters from LTspice simulation datasets.

The toolkit focuses on the classical **Level-1 MOSFET compact model** and provides a modular workflow including data import, parameter extraction, visualization, and integrated parameter reporting.

It is designed for semiconductor education, device modeling practice, and research-oriented learning.

---

## Objectives

This project aims to:

- Automatically extract Level-1 MOSFET parameters from LTspice simulation data.
- Reduce manual calculation during parameter extraction.
- Provide reusable MATLAB implementations for semiconductor device analysis.
- Demonstrate modular software design for compact-model parameter extraction.
- Serve as an educational toolkit for semiconductor device modeling.

---

# Features

## Data Import

- LTspice Transfer Characteristics (Id–VGS) import
- LTspice Output Characteristics (Id–VDS) import
- Support for LTspice DC Sweep Step datasets

---

## Parameter Extraction

- Threshold Voltage (Vth)
- Carrier Mobility (μ)
- Channel-Length Modulation (λ)
- Output Resistance (ro)

---

## Toolkit Architecture

- Modular MATLAB implementation
- Independent extraction modules
- Unified Level-1 extraction interface
- Example scripts for each extraction routine

---

## Visualization

- Transfer characteristic plotting
- Threshold voltage visualization
- Extraction summary reporting

---

# Workflow

```text
          LTspice Simulation
                  │
                  ▼
           Data Import Module
                  │
                  ▼
        Parameter Extraction
   ┌────────┬────────┬────────┐
   ▼        ▼        ▼        ▼
  Vth       μ        λ        ro
                  │
                  ▼
        Level-1 Extract Interface
                  │
                  ▼
        Results & Visualization
```

---

# Repository Structure

```text
03_MOSFET_Parameter_Extraction
│
├── README.md
├── datasets/
├── docs/
├── figures/
├── ltspice/
├── matlab/
│   ├── examples/
│   ├── extraction/
│   ├── utilities/
│   └── visualization/
└── LICENSE
```

---

# Example

```matlab
%% Read LTspice datasets

data_transfer = read_ltspice_csv("Id_Vgs.txt");

data_output = read_ltspice_step("Id_Vds.txt");

%% Extract Level-1 parameters

parameters = level1_extract(data_transfer,data_output);
```

Example output

```text
Threshold Voltage

Carrier Mobility

Channel-Length Modulation

Output Resistance
```

---

# Current Status

## Completed

- MATLAB toolkit architecture
- LTspice data import module
- Threshold voltage extraction
- Carrier mobility extraction
- Channel-length modulation extraction
- Output resistance extraction
- Integrated Level-1 extraction interface
- Example workflows

---

## Ongoing

- Visualization improvements
- Documentation refinement
- Additional example datasets

---

# Related Publications

## Conference Publication

**A Systematic and Bias-Consistent Parameter Extraction Framework for Level-1 MOSFET Models**

IEEE EICCT 2026

Published

---

## Journal Manuscripts

**Robust Parameter Extraction for MOSFET Compact Models Using Multi-Bias Regression and Simulation**

Under Review

**Comparative Analysis of Optimization Strategies for MOSFET Compact Model Parameter Extraction Under Noisy Conditions**

Under Review

---

# Skills Demonstrated

## Semiconductor Devices

- MOSFET Device Physics
- Compact Modeling
- Parameter Extraction

---

## Programming

- MATLAB
- LTspice
- Git
- GitHub

---

## Numerical Methods

- Linear Regression
- Polynomial Fitting
- Numerical Analysis

---

## Software Engineering

- Modular Software Design
- Toolkit Development
- Data Processing

---

# Future Development

Future versions may include:

- Additional extraction methods
- Enhanced visualization
- More example datasets
- Support for higher-level compact MOSFET models

---

# Author

**Jianhao Wu**

Electrical Engineering, McGill University

---

## Research Interests

- Semiconductor Devices
- MOSFET Modeling
- Compact Modeling
- Parameter Extraction
- Electronic Design Automation (EDA)
