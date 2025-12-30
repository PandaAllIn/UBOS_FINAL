# AMD Radeon R9 M295X – Structured Specifications (Balaur)

Sources:
- TechPowerUp dump: /srv/janus/docs/hardware/gpu/r9m295x_techpowerup.txt
- NotebookCheck dump: /srv/janus/docs/hardware/gpu/r9m295x_notebookcheck.txt
- Summary: /srv/janus/docs/hardware/gpu/R9_M295X_specifications.md

## Key Specs
| Field              | Value                       |
|--------------------|-----------------------------|
| Architecture       | GCN 3.0 (Tonga)             |
| Compute Units      | 32 CUs (2048 shaders)       |
| TMUs / ROPs        | 128 TMUs / 32 ROPs          |
| Base / Boost Clock | ~850 MHz / up to ~950 MHz   |
| Memory Size        | 4 GB GDDR5                  |
| Bus Width          | 256‑bit                     |
| Effective Speed    | 5.0 Gbps (typical)          |
| Bandwidth          | ~160 GB/s                   |
| VCE                | Version 3.0 (H.264 encode)  |

## Monitoring (Balaur)
- `clinfo` (OpenCL devices), `vulkaninfo` (driver), `radeontop` (utilization), `/sys/kernel/debug/dri/0/amdgpu_pm_info` (clocks/voltage).
- Thermal soft‑limit ~94 °C; Relief Valve should prioritize Studio throttling under heat.
