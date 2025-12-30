GPU Validation Suite (Studio Phase 5)
---

Overview
- Location: 02_FORGE/scripts/deploy/studio/validate_gpu_acceleration.py
- Assets: /tmp/gpu_test_assets/
- Modes: default (fast), --full (adds clpeak GPU memory BW)
- Output: JSON summary (machine-readable) + human-readable stdout

What It Tests
- OpenGL: renderer info (glxinfo -B) and glxgears FPS via xvfb-run
- Video: FFmpeg VAAPI encode vs CPU baseline (speedup metric)
- Vulkan: device presence and compute queue flags (vulkaninfo --summary)
- OpenCL: platform/device presence (clinfo)
- Memory: CPU memory bandwidth (sysbench), optional GPU global mem BW (clpeak)
- Thermals: GPU temperature before/after a short load

Dependencies (Debian/Ubuntu)
- sudo apt-get update && sudo apt-get install -y \
  mesa-utils mesa-utils-extra xvfb libva-utils vulkan-tools clinfo sysbench lm-sensors \
  ffmpeg
- Optional (GPU mem BW): clpeak

AMD R9 M295X (GCN 3.0) Notes
- VAAPI should report a Mesa driver (radeonsi) via `vainfo`
- FFmpeg VAAPI device: /dev/dri/renderD128
- For headless OpenGL FPS, Xvfb is required

Run Examples
- JSON only: python3 02_FORGE/scripts/deploy/studio/validate_gpu_acceleration.py --json
- Extended:  python3 02_FORGE/scripts/deploy/studio/validate_gpu_acceleration.py --json --full

Acceptance Thresholds
- OpenGL renderer present; glxgears_fps > 30 FPS under Xvfb
- VAAPI encode completes and outputs MP4; reports speedup_vs_cpu >= 1.0 preferred
- Vulkan device listed and compute_queue_present=true (if available)
- OpenCL devices >= 1
- sysbench memory throughput > 100 MiB/s
- Thermals capture non-null readings (delta may be small for brief loads)

Outputs
- JSON: includes `summary.tests.*` detailed ToolReport objects and `pass_fail` per domain
- Human-readable: one line per test with availability, pass/fail, and key metrics

Runtime Budget
- Typical runtime: 2–4 minutes (fast mode), < 10 minutes with --full

Interpreting Results
- A domain passes only on clear success. Missing tools or permissions mark tests as unavailable/failed, not passed.
- `acceleration_ok` is true if any of OpenGL/VAAPI/Vulkan/OpenCL passes. Use per-domain statuses for deeper triage.

