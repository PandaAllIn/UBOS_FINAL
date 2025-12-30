# DDR3-1600 Memory Specification Notes

**Key References**
- JEDEC Standard JESD79-3F: DDR3 SDRAM Specification
- Micron DDR3L-1600 Data Sheets (MT8KTF51264HZ-1G6)
- The Balaur `dmidecode` output (see hardware inventory)

## Installed Modules on The Balaur
- **Form Factor:** SO-DIMM (per `dmidecode` locator BANK 0/1)
- **Capacity:** 2 × 8 GB = 16 GB total (expandable to 32 GB)
- **Speed:** 1600 MT/s (PC3-12800)
- **Voltage:** 1.35 V (DDR3L) detected via SPD data
- **Timings:** 11-11-11 (tCL-tRCD-tRP) at 800 MHz clock (1600 MT/s effective)

## DDR3-1600 (PC3-12800) Key Parameters
| Parameter | Value |
|-----------|-------|
| Data Rate | 1600 MT/s |
| Clock Frequency | 800 MHz |
| Peak Bandwidth (per 64-bit channel) | 12.8 GB/s |
| CAS Latency Options | CL9–CL11 (CL11 typical for 1.35 V modules) |
| tRCD / tRP | 11 cycles (13.75 ns) |
| tRAS | 28–36 cycles |
| tRC | 39–47 cycles |

## Signaling & Voltage
- **VDD/VDDQ:** 1.5 V standard, 1.35 V for DDR3L (low-voltage). The Balaur modules operate in DDR3L mode for reduced power.
- **Output Driver:** SSTL_15 (source-synchronous). ODT (on-die termination) adjustable via IMC settings.
- **ZQ Calibration:** Periodic impedance calibration via ZQ pin to maintain signal integrity.

## Reliability & ECC
- Installed modules are non-ECC (per `dmidecode`); no single-bit error correction. System relies on ECC-less operation; backups and health checks recommended.

## Bandwidth Considerations on The Balaur
- Dual-channel configuration provides up to 25.6 GB/s theoretical bandwidth.
- For llama.cpp workloads, model fits entirely in DRAM; streaming throughput limited by CPU caches and memory subsystem.
- Use NUMA-aware allocation (though single-node) to maintain locality; `numactl --hardware` reports one NUMA node.

## Power Consumption
- Typical active current (IDD7) ~ 315 mA per module at 1600 MT/s.
- Self-refresh reduces to ~6 mA (IDD6); entry triggered during deep C-states.
- Thermal design supports case temperatures up to 85 °C; The Balaur operates well below this envelope (see hardware inventory sensors).

## Timing Configuration Tips
- Maintain command rate 1T for latency-sensitive tasks; 2T provides stability for four-DIMM configurations (not applicable currently).
- Advanced features such as write leveling and read leveling are handled automatically by Haswell IMC; BIOS exposes limited tuning.
- For overclocking or tighter timings, ensure adequate cooling and adjust VDIMM incrementally (max recommended 1.5 V for DDR3L modules).

