# Intel Core i7‑4790K – Structured Specifications (Balaur)

Sources:
- Live inventory: /srv/janus/docs/hardware/system/balaur_hardware_inventory.md (lscpu, sensors)
- Official: /srv/janus/docs/hardware/cpu/i7-4790k-datasheet.pdf, i7-4790k-power-thermal.pdf

## Key Specs
| Field                | Value                             |
|----------------------|-----------------------------------|
| Microarchitecture    | Haswell Refresh (Devil's Canyon)  |
| Cores / Threads      | 4 / 8                              |
| Base / Max Turbo     | 4.00 GHz / 4.40 GHz                |
| L3 Cache             | 8 MB shared                        |
| TDP                  | 88 W                               |
| Socket               | LGA1150                            |
| Memory Support       | Dual‑channel DDR3/DDR3L‑1600       |
| iGPU                 | Intel HD Graphics 4600             |

## Instruction Sets (from lscpu flags)
See lscpu in hardware inventory for full list (SSE, SSE2, SSE3, SSSE3, SSE4.1/4.2, AVX, AVX2, FMA, AES‑NI, BMI1/2, TSX* if enabled).

## Power / Thermal Notes
- Turbo Boost 2.0 within PL1/PL2/Tau; 88 W nominal, short‑term excursions allowed.
- TJmax 100 °C (throttle), Tcase ~74 °C (datasheet). Use `turbostat` for package watts.

## Measured Context (Balaur)
- Check hardware inventory sensors section for current temps and governor settings.
- CPU governors: see /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor.
