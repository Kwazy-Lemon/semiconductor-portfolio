# Project 2 — ECSE 472

Nonlinear DC operating-point analysis, extended from the existing `../project_1/mna_dc.py` implementation. **Project 1 is preserved as an independent deliverable.** Project 2 contains its own complete solver and does not import or modify Project 1.

## What carries over and what changes

All nine Project 1 element types remain supported: `R`, `V`, `I`, `C`, `L`, `VCVS`, `CCVS`, `VCCS`, and `CCCS`. Their MNA stamps and current-reference conventions are retained. Capacitors are open circuits and inductors are zero-voltage branches at DC.

Project 2 adds:

- A diode entry: `Dname anode cathode`.
- The Shockley model with `Is = 1e-15 A`, `Vt = 0.025 V`, and ideality factor 1.
- A diode companion stamp, updated at every Newton iteration.
- Damped Newton-Raphson iteration, with forward-voltage step limiting and backtracking against the original nonlinear residual.
- Explicit convergence and singular-matrix errors, residual reporting, and diode-current output.
- Row scaling in the inherited linear solver, finite-number validation, and correct handling of the assignment's `* diode circuit` title line.
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

## Diode stamp and solution

For `Vd = Va - Vc`, the model and its derivative are:

```text
Id  = Is * (exp(Vd / Vt) - 1)
gd  = (Is / Vt) * exp(Vd / Vt)
Ieq = Id - gd * Vd
```

The companion model is a conductance `gd` in parallel with a current source `Ieq` directed from anode to cathode. In `A*x_new = z`:

```text
A[a,a] += gd       A[a,c] -= gd
A[c,a] -= gd       A[c,c] += gd
z[a]   -= Ieq      z[c]   += Ieq
```

Ground rows and columns are omitted. `build_mna(elements, operating_point)` applies these stamps on top of the inherited linear stamps. Calling it without an operating point returns the fixed linear portion, including all node and branch indices.

`solve_dc()` evaluates the true residual `F(x)` from the fixed linear equations and original diode currents. It solves the equivalent Newton correction equation `A*delta = -F(x)` using the existing linear-solver structure, then selects a step `x_new = x + alpha*delta`. Forward diode-voltage increases are limited to `0.1 V` per update. Backtracking requires the scaled equation residual to decrease. The printed matrix is the companion-model matrix **at the final operating point**.

Convergence requires every node KCL residual to be at most `1e-11 A` and every voltage-defined branch constraint error to be at most `1e-9 V`. The defaults allow at most 200 updates. A matrix check also rejects underdetermined circuits that happen to have zero residual at the initial guess. No hidden ground conductance is added, and the physical diode curve is not clipped.

Reference for the diode companion model: [Qucs technical documentation — Non-linear DC Analysis](https://qucs.sourceforge.net/tech/node16.html).

## Validation

The automated suite has 22 tests, covering all nine Project 1 types, the repository's original circuit, the Deliverable 1 divider, the Deliverable 2 diode example, an independent scalar bisection reference, multiple diodes, reverse bias, a controlled source driving a diode, grounded diode stamps, invalid input, floating circuits, and convergence failure.

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

See [中文说明](README_中文.md) for a short guide to the relationship between the two deliverables.
