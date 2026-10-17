# 07 — Fundamentals of Circuit Simulation and Modelling

This section documents a Python-based circuit simulation project focused on the numerical foundations of SPICE-like circuit analysis.

## Objectives

- Translate circuit diagrams into SPICE-like netlists.
- Parse netlists and identify nodes, elements, and analysis directives.
- Construct Modified Nodal Analysis (MNA) matrices.
- Perform linear DC analysis using Python.
- Validate node voltages and branch currents against hand calculations.

## Implementation Plan

1. Netlist parsing and node indexing.
2. MNA matrix construction for independent sources and passive elements.
3. Linear DC solver and solution output.
4. Stamps for controlled sources.
5. DC treatment of capacitors and inductors.
6. Test cases, numerical validation, and usage documentation.

## Constraints

- Programming language: Python.
- Do not use SPICE or other circuit-simulation software to perform the analysis.
- Python numerical libraries may be used for linear algebra, consistent with the course requirements.

## Status

Work in progress. Implementation details and verified test results will be documented as the implementation and tests are completed.
