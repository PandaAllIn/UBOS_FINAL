# Intel Core i7-4790K Datasheet Summary

**Source URLs**
- Intel ARK: https://www.intel.com/content/www/us/en/products/sku/80807/intel-core-i74790k-processor-8m-cache-up-to-4-40-ghz/specifications.html
- Intel Datasheet Volume 1: https://cdrdv2.intel.com/v1/dl/getContent/332689
- Intel Power/Thermal Guide: https://cdrdv2.intel.com/v1/dl/getContent/332690

## Overview
- **Microarchitecture:** Haswell Refresh (4th Generation Core, Codename "Devil's Canyon")
- **Process Technology:** 22 nm Tri-Gate
- **Socket:** LGA1150
- **Cores / Threads:** 4 cores / 8 threads (Intel® Hyper-Threading Technology)
- **Base Frequency:** 4.00 GHz
- **Max Turbo Frequency:** 4.40 GHz (single-core Turbo Boost 2.0)
- **L3 Smart Cache:** 8 MB shared
- **TDP:** 88 W (configurable TDP-down not supported)
- **Integrated Graphics:** Intel® HD Graphics 4600 (Base 350 MHz, Max Dynamic 1.25 GHz)
- **Memory Support:** DDR3-1333 / DDR3-1600, dual-channel, up to 32 GB officially supported

## Core Configuration
- 2× physical cores per LLC-slice; ring bus interconnect linking cores, LLC, and system agent.
- Supports AVX2, FMA3, AES-NI, TSX-NI (Transactional Synchronization Extensions), BMI1/2, and Enhanced Intel SpeedStep® Technology.
- Intel® Secure Key (DRNG), VT-x, VT-d, and TXT available and enabled on The Balaur (see `lscpu` feature flags in hardware inventory).

## Cache Hierarchy
| Level | Size per Core | Associativity | Notes |
|-------|----------------|---------------|-------|
| L1 Data | 32 KB | 8-way | 64-byte line size |
| L1 Instruction | 32 KB | 8-way | Decoupled instruction cache |
| L2 Unified | 256 KB | 8-way | Inclusive of L1 |
| L3 Shared | 8 MB total | 16-way | Shared via ring bus, inclusive |

## Thermal & Power Envelope
- **TCASE (max):** 74.04 °C (datasheet value)
- **TJUNCTION (max):** 100 °C
- **VID Range:** 0.65 V – 1.30 V (typical)
- Integrated Digital Thermal Sensor (DTS) per core with PECI reporting.
- Supports adaptive voltage/frequency scaling via ACPI P-states (P0–P1) and C-states (C0, C1E, C3, C6, C7, C7s).
- Configurable TDP is not exposed on this SKU; however, power balancing via VR12.5 interface is supported.

## Power Management Features
- **Enhanced Intel SpeedStep® (EIST):** Dynamic frequency scaling based on OS governor (`ondemand` or `performance` on The Balaur; see hardware inventory for current governor).
- **C-States:** Deep C6/C7 with memory self-refresh; package C-states supported to C8.
- **Turbo Boost 2.0:** Up to 4.4 GHz single-core, 4.2 GHz dual-core, subject to power/thermal headroom.
- **Power Limits:** PL1 = 88 W, PL2 typically factory-set to 110 W with 1-second Tau default (adjustable via BIOS if exposed).

## Memory Controller
- Dual-channel DDR3 IMC with 128-bit aggregate width.
- Official support: DDR3-1600 at 1.5 V; DDR3L-1600 at 1.35 V (if modules installed).
- Maximum theoretical bandwidth: 25.6 GB/s (1600 MT/s × 8 bytes × 2 channels).
- Supports XMP profiles (BIOS-dependent) for higher frequencies (The Balaur currently operates at 1600 MT/s per `dmidecode`).

## Integrated Graphics (HD 4600)
- 20 Execution Units (GT2 configuration).
- Quick Sync Video, Clear Video HD, OpenCL 1.2.
- Display interfaces: DP, HDMI, DVI, VGA via motherboard outputs.
- Graphics TDP shares package power budget with CPU cores.

## Relevant Registers & Tools
- MSR 0x198 (IA32_PERF_STATUS) for frequency readback.
- MSR 0x199 (IA32_PERF_CTL) for requested P-states.
- IA32_PACKAGE_POWER_SKU (MSR 0x614) reflects power limits.
- Intel Power Gadget (Windows/macOS) or `turbostat` (Linux) recommended for live monitoring (see hardware inventory section for `turbostat` output on The Balaur).

## Datasheet Highlights
- SVID (Serial Voltage Identification) VR interface compliant with VR12.5.
- Supports per-core power gating and ring interconnect power gating for idle efficiency.
- Thermal interface material improved in Devil's Canyon SKUs for better heat transfer.
- Requires Z97/Z87 chipset with BIOS supporting Haswell Refresh microcode.

## External References
- Intel® 4th Generation Core™ Processor Family Datasheet, Volume 1 (332689).
- Intel® 4th Generation Core™ Processor Family Datasheet, Volume 2 (332690).
- Intel® 64 and IA-32 Architectures Optimization Reference Manual (248966).

