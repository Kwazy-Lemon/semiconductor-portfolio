# Project 2 — ECSE 472

Nonlinear DC operating-point analysis, extended from the existing `../project_1/mna_dc.py` implementation. **Project 1 is preserved as an independent deliverable.** Project 2 contains its own complete solver and does not import or modify Project 1.

## What carries over and what changes

All nine Project 1 element types remain supported: `R`, `V`, `I`, `C`, `L`, `VCVS`, `CCVS`, `VCCS`, and `CCCS`. Their stamp equations and current-reference conventions are retained, with stamps now written explicitly into G, B, C, and D. Capacitors are open circuits and inductors are zero-voltage branches at DC.

Project 2 adds:

- A diode entry: `Dname anode cathode`.
- The Shockley model with `Is = 1e-15 A`, `Vt = 0.025 V`, and ideality factor 1.
- A diode companion stamp in G and i_vector, updated at every Newton iteration.
- Damped Newton-Raphson iteration, with forward-voltage step limiting and backtracking against the original nonlinear residual.
- Explicit convergence and singular-matrix errors, residual reporting, and diode-current output.
- Row scaling in the direct block solver, finite-number validation, and correct handling of the assignment's `* diode circuit` title line.
- Automated regression checks for all nine original element types and nonlinear cases.

Only Python's standard library is used. Python 3.10+ is recommended.

## Run locally

From this directory:

```bash
python start_code.py
python mna_dc.py circuits/diode.cir
python mna_dc.py circuits/linear_divider.cir
python -B -m unittest -v test_mna_dc.py
```

`start_code.py` is an ordinary Python script. It runs the diode example even when launched from another working directory.

## Google Colab

In a fresh notebook, run these as separate cells:

```python
!git clone https://github.com/Kwazy-Lemon/semiconductor-portfolio.git
```

```python
%cd /content/semiconductor-portfolio/07_Fundamentals_of_Circuit_Simulation_and_Modelling/project_2
```

```python
from mna_dc import main
main("circuits/diode.cir")
```

If the repository is already cloned in Colab, update that checkout before importing the module. Project 2 uses the same module name as Project 1; use a fresh notebook runtime if Project 1's `mna_dc` has already been imported.

## Netlist conventions

The first non-empty line is always the circuit title, including when it starts with `*`. Subsequent blank lines and lines beginning with `*` or `#` are ignored; inline `;` comments are supported. Ground is `0`. Node names retain Project 1's case-sensitive behavior. Element names and current-control references are case-insensitive.

The file must contain a bare `.dc` before `.end`. This assignment's `.dc` means a single operating point, not a sweep. For example:

```text
* diode circuit
Vin n1 0 DC 1
D1 n1 n2
R n2 0 50
.dc
.end
```

| Type | Syntax |
| --- | --- |
| R, C, L | `NAME node+ node- value` |
| V, I | `NAME node+ node- [DC] value` |
| VCVS, VCCS | `NAME node+ node- control+ control- gain` |
| CCVS, CCCS | `NAME node+ node- controlling_branch gain` |
| D | `NAME anode cathode` |

Current-controlled sources sense a voltage-defined branch: `V`, `VCVS`, `CCVS`, or `L`. Place a zero-volt voltage source in series with a branch when a current sensor is needed. Engineering suffixes follow Project 1: `k`, `meg`, `m`, `u`, `n`, `p`, etc.; `M` means milli and `meg` means mega. Values use implicit SI units without trailing unit names.

## Separate G, B, C, D equations

The code creates, stamps, solves, and prints these four matrices separately:

```text
G*v + B*j = i_vector
C*v + D*j = e_vector
```

Here v contains the N non-ground node voltages and j contains the M voltage-defined branch currents.

| Block | Size | Meaning |
| --- | --- | --- |
| G | N x N | Node-voltage coefficients in the KCL equations |
| B | N x M | Branch-current coefficients in the KCL equations |
| C | M x N | Node-voltage coefficients in the voltage constraints |
| D | M x M | Branch-current coefficients in the voltage constraints |
| i_vector | N entries | Node-current right-hand side |
| e_vector | M entries | Voltage-constraint right-hand side |

The block named D is **not a diode**. With resistors and independent voltage sources, D is zero. A CCVS adds a term such as D[output_branch][control_branch] -= gain. Likewise, the block C is distinct from an element whose name starts with C (a capacitor).

The implementation never joins the four blocks into a full coefficient matrix or an augmented matrix. The function `solve_block_system(G, B, C, D, i_vector, e_vector)` performs row operations on the separate blocks. It permits row exchanges across both equation groups, so it also handles circuits where G itself is singular.

### Where each stamp goes

| Element | Contributions |
| --- | --- |
| Resistor | G |
| Independent current source | i_vector |
| Independent voltage source | B, C, e_vector |
| Capacitor at DC | No contribution (open circuit) |
| Inductor at DC | B, C (a zero-volt branch) |
| VCVS | B and C, including control-voltage terms in C |
| VCCS | G |
| CCVS | B, C, and a control-current coefficient in D |
| CCCS | A control-current coefficient in B |
| Diode | Differential conductance in G; companion current in i_vector |

For an independent voltage source, B connects its current to node KCL and C writes its terminal-voltage difference. Controlled sources can make C different from the transpose of B.

### Diode update

For Vd = Va - Vc:

```text
Id  = Is * (exp(Vd / Vt) - 1)
gd  = (Is / Vt) * exp(Vd / Vt)
Ieq = Id - gd * Vd

G[a,a] += gd       G[a,c] -= gd
G[c,a] -= gd       G[c,c] += gd
i_vector[a] -= Ieq
i_vector[c] += Ieq
```

Ground rows and columns are omitted. `build_mna_blocks(elements, operating_point)` applies these contributions along with all linear stamps. Without an operating point, the same function returns the fixed linear blocks for checking the true nonlinear residual.

`solve_dc()` evaluates the two groups of true equation residuals and solves their Newton corrections directly in block form:

```text
G*dv + B*dj = -F_node
C*dv + D*dj = -F_branch
```

The update uses a damping factor. Forward diode-voltage increases are limited to 0.1 V per step, followed by backtracking that requires the original scaled residual to decrease. The output shows each block's dimensions, entries, node order, and branch order at the final operating point.

Convergence requires every node KCL residual to be at most 1e-11 A and every voltage-defined branch constraint error to be at most 1e-9 V, within 200 updates by default. A block-system check also rejects underdetermined circuits with zero initial residual. No hidden ground conductance is added, and the physical diode curve is not clipped.

Reference for the diode companion model: [Qucs technical documentation — Non-linear DC Analysis](https://qucs.sourceforge.net/tech/node16.html).

## Validation

The automated suite has 28 tests, covering all nine Project 1 types, the repository's original circuit, the Deliverable 1 divider, the Deliverable 2 diode example, an independent scalar bisection reference, multiple diodes, reverse bias, a controlled source driving a diode, grounded diode stamps, invalid input, floating circuits, convergence failure, explicit block values, singular-G circuits, empty blocks, and preservation of the original stamps.

The diode example converges in 11 updates:

```text
V(n1)  = 1 V
V(n2)  = 0.267314409 V
I(Vin) = -0.00534628818 A
I(D1)  =  0.00534628818 A
I(R)   =  0.00534628818 A
```

Every reported current is positive from the first node to the second. Thus the source current is negative while it supplies power; the assignment's positive `IE = 0.0053 A` is its magnitude or the opposite reference direction.

The Deliverable 1 divider still produces `V(n1)=6 V`, `V(n2)=2 V`, and `I(Vin)=-0.04 A`.

## Scope

This is an educational, dense-matrix DC solver. It does not implement AC, transient analysis, source sweeps, `.model`, temperature dependence, or diode breakdown. Difficult or extreme circuits may still fail to converge; errors are reported rather than returned as operating points.
