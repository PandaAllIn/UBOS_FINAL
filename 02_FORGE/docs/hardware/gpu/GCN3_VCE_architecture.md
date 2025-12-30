# AMD GCN 3.0 Graphics & VCE Architecture Notes

**References**
- AMD Graphics Core Next Architecture Whitepaper (2014)
- AMD Video Codec Engine (VCE) Documentation
- TechPowerUp, NotebookCheck technical breakdowns for Tonga/M295X

## Graphics Core Next (GCN) 3.0 Highlights
- **Compute Units:** Each CU contains 64 stream processors arranged in 4 SIMD units with 16 lanes, shared scalar unit (SALU), and local data share (LDS).
- **Tonga Enhancements:**
  - Delta Color Compression v2 reduces memory bandwidth usage ~40% for render targets.
  - Improved tessellation engine with larger off-chip buffers.
  - Updated geometry engine supporting larger caches and improved primitive discard.
- **Instruction Set:** 64-bit addressing, IEEE754-compliant FP32/FP64 (FP64 rate 1/16 for M295X), hardware scheduling via ACE (Asynchronous Compute Engines).
- **Memory Subsystem:** 512 KB shared L2 cache, 32 ROPs, 256-bit GDDR5 interface supporting up to 160 GB/s throughput.

## Video Codec Engine (VCE) 3.0
- Dedicated encode pipeline separate from shader core; handles motion estimation, entropy coding, and rate control.
- **Formats Supported:**
  - H.264/AVC High Profile encode up to 3840×2160 @ 30 fps (bitrate dependent).
  - MJPEG encode/decode up to 1080p.
  - HEVC/H.265 assisted via shader core (no fixed-function encoder for H.265 on Tonga).
- **Use Cases:**
  - Offload streaming/recording via FFmpeg (`-hwaccel vce`) or OBS Studio with AMD VCE backend.
  - Large reduction in CPU usage for Portal Oradea content pipeline.
- **Quality Modes:** Baseline, Main, High profiles; constant bitrate (CBR) and variable bitrate (VBR) supported through driver API.

## Power & Thermal Considerations
- Separate power domains for graphics core, memory controller, and display engine; managed by AMD PowerTune.
- Dynamic frequency control uses SCLK and MCLK states enumerated in `pp_dpm_sclk` / `pp_dpm_mclk` (requires root to read).
- Cooling demands: maintain GPU temps below 85 °C for sustained performance; The Balaur monitoring via `amdgpu-pci-0100` sensor ensures Relief Valve can react when GPU heat impacts system thermal budget.

## Debug & Monitoring Tools
- `radeontop` for live utilization (Compute vs Graphics vs VCE).
- `amdgpu_pm_info` for clock/voltage/power snapshots.
- `clinfo` to validate OpenCL runtime visibility of Tonga device.
- Vulkan `vkcube` / `vulkaninfo` to validate driver stack (Mesa RADV on Ubuntu 24.04).

## Integration with The Balaur
- GPU reserved primarily for The Studio citizen (media workflows), while The Mill (CPU) handles llama.cpp.
- Victorian Relief Valve monitors GPU thermal contribution; if VRM exceeds safe thresholds, agent throttles GPU-bound tasks first.
- Future enhancement: integrate VCE encode pipeline into janus_agent tools for automated recording/export tasks.

