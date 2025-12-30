# Electrical Basics Primer (For Balaur)

## Fundamentals
- Voltage (V), Current (I), Power (P): P = V·I. Energy draw increases with frequency and voltage roughly quadratically.
- VRM: Converts 12 V rail to low CPU/GPU core voltages; SVID/VR12.5 for Haswell.

## Memory Signaling
- DDR3L at 1.35 V uses SSTL_15 with on‑die termination (ODT); integrity depends on trace length, impedance matching.

## Practical Topics
- Ripple/Noise: Affects stability under turbo; high ripple can reduce max turbo residency.
- PSU Headroom: Reserve ~30% margin over peak combined loads.

Sources: Intel VR12.5 spec, motherboard VRM app notes, JEDEC DDR3.
