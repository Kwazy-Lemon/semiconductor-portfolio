# A Parameter-Space Framework for Investigating Coupling and Identifiability in MOSFET Compact Models

## Publication Information

| Item | Information |
|------|-------------|
| Type | Journal Manuscript |
| Journal | Microelectronics Journal |
| Author | Jianhao Wu (Sole Author) |
| Status | Submitted |
| Submission Date | 2026 |

---

## Research Area

- MOSFET Compact Modeling
- Parameter Extraction
- Parameter Coupling
- Parameter Identifiability
- Parameter-Space Analysis

---

## Overview

This manuscript investigates parameter coupling and practical identifiability in compact MOSFET models from a parameter-space perspective.

Rather than evaluating parameter extraction only by the minimum fitting error, the study analyzes the structure of the parameter-error surface to identify coupled parameter combinations and quantify regions in which multiple parameter sets can reproduce similar electrical characteristics.

A Level-1 MOSFET model is used as a controlled framework for studying the interaction between model parameters. Single-bias and multi-bias conditions are compared to examine how additional drain-voltage information affects parameter non-uniqueness and identifiability.

The study also extends the analysis to BSIM4 to investigate parameter coupling and low-error regions in a more complex compact-model setting.

---

## Methodology

The study follows a parameter-space analysis workflow:

1. Define a reference MOSFET compact model.
2. Systematically sweep selected model parameters.
3. Simulate the corresponding electrical characteristics using LTspice.
4. Calculate normalized root mean square error (NRMSE) relative to the reference characteristics.
5. Construct parameter-error surfaces.
6. Extract the minimum-error coupling trajectory.
7. Define an equivalent parameter space using an NRMSE threshold.
8. Compare single-bias and multi-bias conditions.
9. Validate the effect of parameter-grid resolution.
10. Investigate the mathematical and physical origin of parameter coupling.

---

## Key Findings

### Parameter Coupling

The parameter-space analysis reveals an elongated low-error region rather than a unique minimum. This indicates that different combinations of model parameters can produce similar electrical characteristics.

The extracted optimal coupling trajectory shows a strong approximately linear relationship between the investigated parameters.

### Equivalent Parameter Space

Using a 5% NRMSE criterion, the fine single-bias parameter grid identified:

- 4,141 parameter combinations investigated
- 920 combinations satisfying the 5% NRMSE criterion
- 22.22% of the investigated parameter space within the equivalent region

The finite width of the low-error region provides numerical evidence of parameter non-uniqueness. 

### Multi-Bias Analysis

Three drain-voltage conditions were evaluated simultaneously to investigate whether additional bias information could constrain the parameter space.

The equivalent region decreased from:

- Single bias: **22.22%**
- Multi-bias: **21.28%**

This corresponds to approximately a **4.24% reduction** in the investigated equivalent parameter space.

The results indicate that multi-bias information provides additional constraints, but does not completely eliminate parameter coupling in the studied Level-1 model.

### Grid-Resolution Validation

Coarse and fine parameter grids were compared to verify that the observed coupling relationship was not primarily caused by the selected grid resolution.

The extracted coupling trajectories showed close agreement between the two resolutions.

---

## Tools and Technologies

- **LTspice** — MOSFET circuit simulation
- **Python** — parameter-space analysis and numerical evaluation
- **NumPy / scientific computing tools** — numerical processing
- **Linear Regression** — coupling-trajectory analysis
- **NRMSE** — model-response similarity metric
- **Level-1 MOSFET Model** — controlled compact-model framework
- **BSIM4** — extension to a more complex compact-model setting

---

## My Contributions

- Formulated the parameter-space analysis framework.
- Designed the parameter sweep and simulation methodology.
- Investigated parameter coupling under single-bias conditions.
- Developed the equivalent parameter-space analysis based on NRMSE.
- Compared single-bias and multi-bias parameter identifiability.
- Performed grid-resolution validation.
- Analyzed the mathematical origin of parameter coupling.
- Implemented numerical analysis and visualization workflows.
- Extended the investigation toward BSIM4 parameter behavior.

---

## Research Significance

This work highlights that compact-model parameter extraction should not be evaluated solely by fitting accuracy.

A model may achieve a low fitting error while still allowing multiple parameter combinations to reproduce similar electrical behavior. Analyzing the geometry of the parameter-error surface therefore provides additional information about parameter coupling and practical identifiability.

The framework provides a basis for studying parameter non-uniqueness in more complex compact models and for developing more reliable parameter-extraction methodologies.

---

## Figures

Representative results include:

- Parameter-error surface
- Extracted parameter-coupling trajectory
- Equivalent parameter-space region
- Coarse versus fine grid comparison
- Single-bias versus multi-bias comparison
- Multi-bias parameter-error surface

---

## Related Research

This work extends my previous research on MOSFET parameter extraction toward parameter coupling and identifiability.

It complements my work on:

- Bias-consistent parameter extraction
- Sensitivity-guided sequential extraction
- Multi-bias regression
- Noise-robust parameter extraction
- Compact-model parameter analysis

---

## Manuscript

The manuscript is currently under journal consideration.
