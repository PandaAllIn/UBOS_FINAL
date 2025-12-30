# Thermal Dynamics Primer (For Balaur)

This primer covers CPU/GPU heat generation, heat flow, and practical monitoring.

## Heat Transfer Basics
- Conduction: Q = k·A·ΔT/L. Dominant inside heat spreader and heatsink interfaces.
- Convection: Q = h·A·(T_surface − T_air). Case airflow and fan curves control h.
- Radiation: Minor for typical CPU/GPU temperatures; increases with T^4 but usually negligible here.

## CPU/GPU Thermal Behavior
- CPU (i7‑4790K): Turbo Boost 2.0 raises clocks up to 4.4 GHz within PL2/Tau limits; AVX2 may trigger AVX frequency offset.
- GPU (R9 M295X): PowerTune adjusts SCLK/MCLK states; soft limits near 94 °C. VRAM and VRM thermals can bottleneck sustained performance.

## Monitoring on Balaur
- `sensors`, `turbostat` (PkgWatt), `amdgpu_pm_info` snapshots; see hardware inventory for command outputs.
- Relief Valve thresholds: warn > 85% CPU load or > 90% RAM; degrade further if temps or watts exceed safe envelope.

## Practical Guidance
- Maintain clean heatsink fins, correct fan curves, and quality TIM.
- Under sustained loads, prefer fewer concurrent llama.cpp tasks with higher token rate over many throttled tasks.

Sources: Incropera & DeWitt (heat transfer), Intel power/thermal guides, AMD PowerTune documentation.
