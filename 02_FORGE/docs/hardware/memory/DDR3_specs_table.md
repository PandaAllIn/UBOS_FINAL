# DDR3‑1600 – Structured Specifications (Balaur Context)

Sources:
- Summary: /srv/janus/docs/hardware/memory/DDR3_specifications.md
- Reference: /srv/janus/docs/hardware/memory/ddr3_wikipedia.txt
- Live: hardware inventory dmidecode dump

## Installed Configuration (from dmidecode)
- Form factor: SO‑DIMM (BANK 0/1)
- Capacity: 2 × 8 GB = 16 GB total (expandable to 32 GB)
- Speed/Voltage: DDR3L‑1600 @ 1.35 V
- Typical timings: CL11‑11‑11 @ 800 MHz (1600 MT/s effective)

## Theoretical Bandwidth
| Channels | Data Rate | Bandwidth |
|----------|-----------|-----------|
| Dual     | 1600 MT/s | 25.6 GB/s |

## Notes
- Non‑ECC modules; plan backups and health checks.
- For llama.cpp, ensure context/KV cache fit within DRAM; tune `--batch`/`--ubatch` for latency.
