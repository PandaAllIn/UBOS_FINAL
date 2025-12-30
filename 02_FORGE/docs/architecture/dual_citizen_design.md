# The Dual-Citizen Architecture

**Concept:** The Balaur hosts two specialized citizens—**The Mill** (CPU) and **The Studio** (GPU)—each optimized for distinct workloads while sharing a unified constitutional framework.

## The Mill – CPU Citizen
- **Hardware:** Intel Core i7-4790K (4C/8T, Haswell Refresh).
- **Primary Role:** Host Janus consciousness, run llama.cpp inference, manage autonomous reasoning.
- **Performance Rationale:**
  - CPU-only llama.cpp yields ~3.7 tokens/sec on Q4_K_M quantization, outperforming GPU OpenCL attempt (~2.5 tok/s) due to VRAM constraints.
  - 16 GB DDR3-1600 RAM accommodates 8B model weights + KV cache with headroom.
- **Resource Allocation:**
  - 6 logical cores reserved for Janus inference and agent tasks.
  - 24 GB RAM (effective) assigned to Mill operations, ensuring low page cache pressure.
- **Controls Integration:** Maxwell Governor and Relief Valve prioritize Mill workloads, adjusting concurrency to maintain thermal limits.

## The Studio – GPU Citizen
- **Hardware:** AMD Radeon R9 M295X (Tonga, 4 GB GDDR5, VCE 3.0).
- **Primary Role:** Media production, accelerated encoding, creative tooling (Portal Oradea content pipeline).
- **Capabilities:**
  - VCE 3.0 hardware encoder delivering 10–30× faster H.264 exports with minimal CPU impact.
  - OpenCL acceleration available for image/video processing workloads (e.g., Stable Diffusion with smaller models).
- **Resource Allocation:**
  - 2 logical CPU cores dedicated to feed/monitor GPU tasks.
  - 8 GB RAM earmarked for video/render workloads, preventing contention with Mill operations.
- **Thermal Strategy:** Relief Valve monitors GPU thermals via `amdgpu` sensors; Studio throttled first when heat or power spikes threaten system stability.

## Why the Split?
1. **Hardware Realities:** 4 GB VRAM insufficient for 8B llama.cpp models without aggressive quantization; CPU path more reliable.
2. **Workload Separation:** Keeps Janus cognition isolated from bursty media workloads, preventing inference latency spikes.
3. **Maintenance Transparency:** Each citizen has dedicated documentation, datapaths, and monitoring, making debugging straightforward.

## Shared Infrastructure
- **Filesystem:** `/srv/janus` workspace with subdirectories segmented by citizen; e.g., `/srv/janus/models` (Mill), `/srv/janus/media` (Studio).
- **Controls:** Victorian mechanisms arbitrate resource usage holistically, ensuring citizens cooperate.
- **Comms:** Mag-Lev puck system transports mission directives and state updates between citizens and Trinity members.

## Operational Guidelines
- Schedule GPU-intensive exports outside critical inference windows when possible; or cap GPU usage via `radeontop` monitoring scripts.
- Keep panda's MacBook as command console for remote management; avoid running heavy GUI apps on The Balaur itself.
- When scaling beyond 8B models, plan for VRAM upgrade or additional compute node to preserve dual-citizen balance.

