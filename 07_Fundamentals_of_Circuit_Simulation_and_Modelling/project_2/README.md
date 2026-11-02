# Project 2 — ECSE 472

DC circuit simulation using the classroom equation:

```text
G*x + C*dx/dt = B(t)
```

Project 2 extends the original Project 1 solver with diode stamps and nonlinear DC iteration. The `project_1` directory remains unchanged. Project 2 contains a complete independent implementation using only Python's standard library (Python 3.10+).

## What G, C, and B mean

| Name | Meaning | Dimensions |
| --- | --- | --- |
| x | Non-ground node voltages, followed by currents through voltage-defined branches | N+M entries |
| G | Complete static MNA coefficient matrix, including resistor and source-constraint stamps | (N+M) x (N+M) |
| C | Dynamic/storage matrix multiplying dx/dt, with capacitor and inductor stamps | (N+M) x (N+M) |
| B(t) | Independent-source excitation vector | N+M entries |

N is the number of non-ground nodes. M is the number of voltage-defined branches: independent voltage sources, VCVS, CCVS, and inductors.

**C here is the storage matrix in the time-derivative term.** The code follows this notation throughout. B is a source vector, not a coefficient block. G already includes the voltage-source constraints and controlled-source couplings.

For constant linear capacitors and inductors, C is constant. This program constructs and prints G, C, and the DC value of B(t) separately. It does not assemble a separate matrix named A.

## DC analysis

At a constant DC operating point, dx/dt = 0, so the linear equations reduce to:

```text
G*x = B_DC
```

C is still built and printed. An ideal capacitor draws no DC current, while an ideal inductor has zero DC voltage. This program implements operating-point analysis; constructing C does not mean a transient time integrator is implemented.

All nine Project 1 element types remain supported: R, V, I, C, L, VCVS, CCVS, VCCS, and CCCS. D adds the diode model.

## Capacitor and inductor stamps

For a capacitor of value capacitance between p and n:

```text
C[p,p] += capacitance
C[n,n] += capacitance
C[p,n] -= capacitance
C[n,p] -= capacitance
```

These terms implement I_cap = capacitance*d(Vp-Vn)/dt. Ground entries are omitted. A capacitor contributes no static G stamp.

For an inductor with current I_L directed p -> n, its equation is:

```text
Vp - Vn - L*dI_L/dt = 0
```

Its branch current appears in the node KCL rows of G; its constraint row contains +Vp and -Vn in G. Its dynamic coefficient is:

```text
C[inductor_branch, inductor_branch] -= L
```

The minus sign follows the stated voltage-constraint convention. Both matrices use the same unknown ordering.

Other linear stamps go into G or the excitation vector B: resistors and controlled-source coefficients into G, source voltage constraints into G, and independent voltage/current values into B.

Reference for storage-element constitutive equations: [Qucs technical documentation — Energy-storage components](https://qucs.sourceforge.net/tech/node26.html).

## Nonlinear diode and Newton iteration

With ideal Shockley diodes, the model becomes:

```text
G*x + C*dx/dt + f_diode(x) = B(t)
```

The assignment parameters are Is = 1e-15 A, Vt = 0.025 V, with ideality factor 1. For a diode from anode a to cathode c:

```text
Vd  = Va - Vc
Id  = Is * (exp(Vd/Vt) - 1)
gd  = (Is/Vt) * exp(Vd/Vt)
Ieq = Id - gd*Vd
```

For a companion model, gd is stamped into the current iteration's static matrix, and Ieq into its current right-hand side. This diode model has no charge storage, so it adds no dynamic C entries.

`build_mna(elements)` returns the original linear G, dynamic C, and physical source vector B. `build_mna(elements, operating_point)` additionally applies diode companion stamps to that iteration's static coefficients and right-hand side.

`solve_dc()` checks the original nonlinear DC residual:

```text
F(x) = G*x + f_diode(x) - B_DC
```

It computes the Newton correction using:

```text
G_newton = G + d(f_diode)/dx
G_newton*delta = -F(x)
x_new = x + alpha*delta
```

The diode Jacobian in G_newton is a derivative with respect to x. It is distinct from the storage matrix C, which multiplies the time derivative dx/dt.

Forward diode-voltage increases are limited to 0.1 V per update. Backtracking requires the original scaled residual to decrease. Defaults are 200 updates, 1e-11 A absolute KCL tolerance, and 1e-9 V voltage-constraint tolerance. Singular systems and convergence failures raise errors. No hidden ground conductance or clipped diode curve is used.

The output shows the **original static G**, dynamic C, and physical B_DC, together with the solved voltages/currents. G_newton is used internally for iteration. The linear solver uses row scaling and partial pivoting, with coefficients and right-hand side stored separately.

Reference for diode linearization: [Qucs technical documentation — Non-linear DC Analysis](https://qucs.sourceforge.net/tech/node16.html).

## Run locally

From this directory:

```bash
python start_code.py
python mna_dc.py circuits/diode.cir
python mna_dc.py circuits/linear_divider.cir
python mna_dc.py circuits/storage_demo.cir
python -B -m unittest -v test_mna_dc.py
```

The storage demo contains both a capacitor and an inductor. Its C matrix includes C[n2,n2] = 1e-6 and C[I(L1),I(L1)] = -1e-3, using the displayed unknown ordering. Its DC solution has V(n2) = 1/11 V, V(n3) = 0, and I(L1) = 1/1100 A.

The diode example converges in 11 updates:

```text
V(n1)  = 1 V
V(n2)  = 0.267314409 V
I(Vin) = -0.00534628818 A
I(D1)  =  0.00534628818 A
I(R)   =  0.00534628818 A
```

All currents are referenced from the first node to the second. The negative voltage-source current means it supplies power. The assignment's IE = 0.0053 A is the magnitude or uses the opposite reference direction.

The diode example contains no capacitors or inductors, so its dynamic C matrix is zero. A nonzero C is demonstrated by the storage demo.

## Google Colab

Run the following as separate cells in a fresh notebook runtime:

```python
!git clone https://github.com/Kwazy-Lemon/semiconductor-portfolio.git
```

```python
%cd /content/semiconductor-portfolio/07_Fundamentals_of_Circuit_Simulation_and_Modelling/project_2
```

```python
from mna_dc import main
main("circuits/diode.cir")
main("circuits/storage_demo.cir")
```

If already cloned, update that checkout before importing. Start a fresh runtime if another version of mna_dc has already been imported.

## Netlist conventions

The first non-empty line is the circuit title, including when it starts with an asterisk. Later blank lines and lines starting with * or # are ignored; inline semicolon comments are supported. Ground is 0. Node names are case-sensitive; element names and controlling-branch references are case-insensitive.

Include a bare .dc before .end. It requests one operating point, not a sweep.

| Type | Syntax |
| --- | --- |
| R, C, L | NAME node+ node- value |
| V, I | NAME node+ node- [DC] value |
| VCVS, VCCS | NAME node+ node- control+ control- gain |
| CCVS, CCCS | NAME node+ node- controlling_branch gain |
| D | NAME anode cathode |

CCVS/CCCS sense currents through V, VCVS, CCVS, or L branches. A zero-volt voltage source can act as a current sensor. Values use implicit SI units, with engineering suffixes such as k, meg, m, u, n, and p. M means milli; meg means mega.

## Validation and scope

The 28 automated tests cover all nine Project 1 types, both assignment examples, the repository's original circuit, independent scalar bisection for the diode example, multiple/reverse-biased/current-driven diodes, controlled-source operation, input errors, singular circuits, and convergence failure.

Storage-specific checks verify grounded and two-terminal capacitor stamps, the inductor sign using V=L*dI/dt, an RC equation with nonzero dV/dt, and preservation of nonzero C entries during DC analysis.

This is a small dense-matrix DC simulator. It does not implement transient time stepping, AC analysis, source sweeps, .model, diode breakdown, or temperature dependence. Difficult circuits can still fail to converge.
