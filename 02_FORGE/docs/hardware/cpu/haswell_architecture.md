# Haswell Microarchitecture Overview

**Primary Sources**
- Intel® 4th Generation Core™ Processor Family Datasheet Volumes 1 & 2
- Intel® 64 and IA-32 Architectures Optimization Manual (Order 248966)
- Intel® Software Developer Manual (Volumes 1–3)

## High-Level Design
- **Pipeline:** 14-stage, out-of-order superscalar pipeline derived from Sandy Bridge with improved branch prediction and fetch bandwidth.
- **Execution Ports:** 8 execution ports with added integer multiplication unit and enhanced scheduler queues.
- **Micro-ops Cache:** 1.5k-entry micro-op cache for decoded instructions, reducing front-end power usage.
- **Branch Prediction:** Enhanced global predictor and loop stream detector; micro-fusion maintained for simple operations.

## Key Architectural Enhancements vs. Ivy Bridge
- **AVX2:** Full 256-bit integer vector support, gather instructions, vector FMA (FMA3) enabling significant throughput improvements for HPC workloads.
- **Transactional Synchronization Extensions (TSX):** Hardware lock elision (HLE) and restricted transactional memory (RTM) for parallel scalability (disabled in some microcode revisions due to erratum HSW136; The Balaur BIOS exposes TSX with latest microcode).
- **Improved Power Delivery:** Integrated voltage regulator (FIVR) providing per-domain power control; Devil's Canyon uses upgraded VR to handle higher base clocks.
- **Adaptive Thermal Monitor:** Real-time frequency adjustment tied to on-die thermal sensor, enabling aggressive turbo bins.

## Cache & Memory Subsystem
- Inclusive L3 cache shared via on-die ring; each core adds 2 MB LLC slice (i7-4790K totals 8 MB).
- Dual-ring architecture for SKUs with >4 cores (not applicable here) but same ring agent design.
- Memory controller supports 1N/2N command rate and low-power DDR3L modes; integrates with system agent for PCIe and DMI.

## Power Management Architecture
- **FIVR Domains:** IA (cores), GT (graphics), LLC, SA (system agent), and IO; each domain can be power gated independently.
- **Core Power Gating:** Individual cores enter C6/C7 with state flush to LLC; package C-states place uncore into deeper sleep.
- **Integrated Clocking:** Digital PLL per domain reduces jitter and improves wake latency.

## Graphics & Media Engine
- GT2 configuration (HD 4600) includes:
  - 20 Execution Units arranged in 4 slices with shared caches.
  - Fixed-function Quick Sync encode/decode pipeline.
  - Gen7.5 Media Sampler and video quality engine.
- Shared LLC allows graphics to consume unused CPU cache quota.

## Security & Virtualization
- **Intel VT-x & VT-d:** Support for nested virtualization, Extended Page Tables, and DMA remapping.
- **Intel AES-NI & Secure Key:** Hardware AES acceleration and RDRAND instruction for entropy.
- **Intel TXT:** Trusted Execution environment supported via TPM and measured launch.

## Performance Optimization Notes
- Align data structures to 32 bytes to exploit AVX2; avoid crossing cache-line boundaries for gather-heavy workloads.
- Utilize FMA for dense linear algebra; pair multiply-add operations to keep both vector pipelines busy.
- Monitor L1/L2 hit rates via hardware counters (IA32_PMCx) to tune cache blocking strategies.
- Balance power limits (PL1/PL2) for sustained workloads; Devil's Canyon thermal headroom allows brief excursions above 88 W TDP.

