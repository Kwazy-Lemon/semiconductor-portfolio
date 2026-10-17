# Project 1 — ECSE 472

This folder contains the Python implementation for ECSE 472 Deliverable 1: linear DC circuit analysis using Modified Nodal Analysis (MNA).

## Scope

- Read a circuit netlist based on the supplied circuit format.
- Identify non-ground nodes and supported circuit elements.
- Construct the MNA matrix equation \(A x = z\).
- Solve linear DC operating points using Gaussian elimination with partial pivoting.
- Print the MNA matrix, right-hand-side vector, node voltages, and available branch currents.
- Report common input errors and singular MNA systems.

The implementation uses only the Python standard library and does not invoke SPICE.

## Files

- `mna_dc.py` — MNA matrix construction and linear DC solver.
- `circuits/simple_voltage_divider.cir` — sample netlist.

## Supported elements

- `R` — resistor
- `V` — independent DC voltage source
- `I` — independent DC current source
- `C` — capacitor, treated as an open circuit in DC steady state
- `L` — inductor, treated as a short circuit in DC steady state
- `VCVS` — voltage-controlled voltage source
- `VCCS` — voltage-controlled current source
- `CCVS` — current-controlled voltage source
- `CCCS` — current-controlled current source

Diodes, nonlinear devices, and transient or AC analyses are not implemented.

## Netlist format

The first non-empty line is the circuit title. Each element is written on its own line. The file must include `.dc` and end with `.end`.

Example:

```text
Simple voltage divider
V1 n1 0 DC 10
R1 n1 n2 1k
R2 n2 0 2k
.dc
.end
```

Ground is represented by node `0`. Common engineering suffixes such as `k`, `meg`, `m`, `u`, `n`, and `p` are supported.

Controlled-source names use the full prefixes `VCVS`, `VCCS`, `CCVS`, and `CCCS` in this project's netlist format.

## Run

From this directory, run:

```bash
python mna_dc.py circuits/simple_voltage_divider.cir
```

The program prints the MNA matrix, right-hand-side vector, DC node voltages, and branch currents for voltage-defined elements. CCCS output current is calculated from its controlling branch current and is printed separately.

## Validation performed

Manual test netlists have been used to check:

- A resistive voltage divider
- An independent current source
- Capacitor and inductor DC steady-state behavior
- VCVS, VCCS, CCVS, and CCCS controlled sources
- Unsupported element types
- Missing element parameters
- A floating circuit that produces a singular MNA matrix

These are manual checks; a committed automated test suite is not yet included.
