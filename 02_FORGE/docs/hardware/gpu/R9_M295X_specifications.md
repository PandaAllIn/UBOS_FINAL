# AMD Radeon R9 M295X (Mac Edition) Specifications

**Source URLs**
- TechPowerUp GPU Database: https://www.techpowerup.com/gpu-specs/radeon-r9-m295x-mac-edition.c2587
- NotebookCheck Review: https://www.notebookcheck.net/AMD-Radeon-R9-M295X.129043.0.html
- AMD GCN Architecture Whitepaper (Tonga/GCN 3.0)

## Overview
- **Architecture:** GCN 3.0 (Tonga core)
- **Manufacturing Process:** 28 nm
- **Compute Units / Stream Processors:** 32 CUs / 2048 shaders
- **ROPs / TMUs:** 32 ROPs / 128 TMUs
- **Base Clock:** 850 MHz (The Balaur default)
- **Boost Clock:** Up to 950 MHz (OEM/thermal dependent)
- **SP Performance:** ~3.48 TFLOPs (single precision at 850 MHz)

## Memory Subsystem
- **Memory Size:** 4 GB GDDR5
- **Bus Width:** 256-bit
- **Effective Speed:** 5.0 Gbps
- **Bandwidth:** 160 GB/s
- **VRAM Voltage:** 1.5 V typical (per Tonga reference design)

## Multimedia & Compute
- **Video Codec Engine:** VCE 3.0 hardware encoder (H.264, limited H.265 decode assistance)
- **UVD:** Unified Video Decoder 4.2 for H.264/MPEG4; partial HEVC via software assist.
- **OpenCL Support:** OpenCL 1.2 (as reported by `clinfo` on The Balaur)
- **DirectX / OpenGL:** DirectX 12 (FL 11_1), OpenGL 4.6, OpenCL 1.2, Vulkan 1.1 (driver-dependent)

## Power & Thermal Characteristics
- **Typical Board Power:** ~100 W (iMac 5K design with shared cooling loop)
- **Thermal Limits:** 94 °C GPU temperature soft limit (`amdgpu_pm_info`)
- **Power States:** Dynamic frequency scaling via DPM states; accessible through `/sys/class/drm/card0/device/pp_dpm_sclk` (requires root).
- **Cooling:** Vapor chamber with dual-fan radial design inside iMac chassis; The Balaur presently uses stock cooling with thermal monitoring via `sensors` (`amdgpu-pci-0100`).

## Display & I/O
- **Display Outputs:** DP 1.2, HDMI 1.4a, dual-link DVI (availability dependent on host platform).
- **Audio:** Integrated AMD HD Audio controller over HDMI/DP.

## Performance Notes
- Tonga introduces improved tessellation and lossless delta color compression, enhancing bandwidth efficiency relative to Tahiti.
- For compute workloads on The Balaur, OpenCL acceleration is available but limited to 4 GB VRAM; CPU-based llama.cpp remains faster for inference due to memory footprint (see dual-citizen architecture document).
- VCE 3.0 provides substantial acceleration (10–30×) for H.264 encoding; recommended for Portal Oradea video workloads.

## Monitoring References on The Balaur
- `radeontop` for live GPU utilization and VRAM metrics.
- `/sys/kernel/debug/dri/0/amdgpu_pm_info` for clocks, voltages, and power draw (requires root & debugfs).
- `sensors | grep amdgpu` for temperature readouts integrated with lm-sensors.

