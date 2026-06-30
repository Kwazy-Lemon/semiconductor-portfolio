# Carrier Transport

Carrier transport describes how electrons and holes move inside semiconductor materials under the influence of electric fields and concentration gradients. It is one of the fundamental concepts in semiconductor physics and directly determines the electrical behavior of devices such as PN junctions and MOSFETs.

This page summarizes the two primary carrier transport mechanisms—drift and diffusion—as well as the physical parameters that influence carrier motion.

---

## Overview

Electrical current in semiconductors is produced by the movement of charge carriers.

Two transport mechanisms dominate semiconductor devices:

- **Drift** – Carrier motion caused by an external electric field.
- **Diffusion** – Carrier motion caused by carrier concentration gradients.

Most semiconductor devices operate through a combination of both mechanisms.

---

## Drift Current

When an electric field is applied, electrons and holes move in opposite directions due to their opposite charges.

The drift current density is expressed as


`J_drift = q(nμ_n + pμ_p)E`

where

- \(q\) is the elementary charge,
- \(n\) and \(p\) are the electron and hole concentrations,
- \(\mu_n\) and \(\mu_p\) are the carrier mobilities,
- \(E\) is the electric field.

<img width="797" height="506" alt="image" src="https://github.com/user-attachments/assets/0ca5f51a-bbbc-4984-ae22-ad96699422fc" />


---

## Diffusion Current

Carrier diffusion occurs when carrier concentrations are not uniform throughout the semiconductor.

Electrons and holes naturally move from regions of high concentration to regions of low concentration.

The diffusion current density is given by

`J_n = qD_n(dn/dx)`

`J_p = -qD_p(dp/dx)`
where

- \(D_n\) and \(D_p\) are the diffusion coefficients.

<img width="779" height="524" alt="image" src="https://github.com/user-attachments/assets/eb278829-c8ce-4015-8a4a-85a452052ee3" />


---

## Carrier Mobility

Carrier mobility describes how easily charge carriers move under an electric field.

Several factors influence mobility, including:

- Temperature
- Impurity concentration
- Crystal quality
- Electric field strength

Higher mobility generally leads to higher conductivity and faster device operation.

<img width="784" height="524" alt="image" src="https://github.com/user-attachments/assets/04fea889-8e7e-4853-9a53-631b244dc57a" />

---

## Einstein Relation

Carrier mobility and diffusion are related through the Einstein relation

`D/μ = kT/q`
where

- \(D\) is the diffusion coefficient,
- \(\mu\) is the mobility,
- \(k\) is Boltzmann's constant,
- \(T\) is the absolute temperature.

This relationship links drift and diffusion transport in thermal equilibrium.
<img width="776" height="520" alt="image" src="https://github.com/user-attachments/assets/958e7136-2314-4c84-92c4-b51a031dd1d0" />

---

## Importance in Semiconductor Devices

Carrier transport plays a central role in the operation of semiconductor devices, including:

- PN junction diodes
- MOS capacitors
- MOSFETs
- Bipolar junction transistors (BJTs)

Understanding carrier transport is also essential for:

- Device characterization
- Compact model development
- MOSFET parameter extraction

---

## References

1. S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed. Wiley, 2007.

2. R. F. Pierret, *Semiconductor Device Fundamentals*. Addison-Wesley, 1996.

3. Y. Tsividis and C. McAndrew, *Operation and Modeling of the MOS Transistor*, 3rd ed. Oxford University Press, 2011.
