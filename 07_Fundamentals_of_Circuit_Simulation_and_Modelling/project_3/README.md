# ECSE 472 · Project 3

Linear and nonlinear transient simulation with Backward Euler. The assignment example is a half-wave rectifier driven by a 1 V, 60 Hz cosine. A Shockley diode feeds a 50 Ω resistor in parallel with a 100 µF capacitor. This project uses `Is = 1e-14 A` and `Vt = 0.025 V`.

## Run in Colab

Paste the three lines from [start_code.py](start_code.py) into a Colab cell and run it to simulate and plot the circuit. If the repository is already cloned, replace the first line with `!git -C /content/semiconductor-portfolio pull --ff-only`.

## Run locally

From this directory with Python 3.10 or later:

```bash
python mna_tran.py circuits/half_wave_rectifier.cir --csv rectifier.csv
python mna_tran.py circuits/linear_rc.cir --csv rc.csv
```

The solver uses the Python standard library. Add `--plot` to display node voltages with Matplotlib. CSV columns contain time in seconds followed by node voltages and voltage-defined branch currents in MNA order.

## Time stepping

`.tran 0.05s 0.1ms` means a stop time of 50 ms and a nominal step of 0.1 ms. Independent sources support DC values and `COS amplitude frequency` where frequency is in Hz. The source is evaluated at the **end** of each step.

```text
(G + C/h) x_k + f_diode(x_k) = B(t_k) + (C/h) x_(k-1)
```

Starting conditions are zero capacitor voltage and zero inductor current. The zero history vector supplies the storage term for the first step. Algebraic voltages and branch currents are solved at each positive time. The CSV has 500 solved rows from 0.1 ms through 50 ms. A shortened final step lands on the requested stop time when needed.

With linear elements, each step requires one linear solve. With diodes, the previous state seeds a full-step Newton iteration. The Jacobian combines the BE matrix and the diode differential conductance. Convergence requires each node KCL residual to be within 1e-11 A and each voltage-constraint residual within 1e-9 V.

## Numerical checks

| Circuit | Check |
| --- | --- |
| Half-wave rectifier | Compare all 500 output voltages against independent bisection of the scalar BE equation at n2. At 0.1 ms, V(n2) = 0.229668 V. At 33.6 ms it reaches 0.313900 V, and at 50 ms it is 0.310205 V. |
| Linear RC | Compare every sample against the discrete charging solution, V(n2) = 1 − (1 + h/RC)⁻ᵏ. With R = 1 kΩ and C = 1 µF, V(n2) = 0.991481 V at 5 ms. |
| Partial final step | Verify both the endpoint and capacitor voltage when the last step is half the nominal length. |
