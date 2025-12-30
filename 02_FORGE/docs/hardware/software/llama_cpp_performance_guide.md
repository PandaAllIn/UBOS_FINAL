# llama.cpp Performance & Configuration Guide (Balaur Edition)

**Source URLs**
- llama.cpp GitHub Repository: https://github.com/ggerganov/llama.cpp
- llama.cpp performance notes (README + docs/perf.md)

## Build & Backend Configuration
- Current build on The Balaur uses CPU-only path compiled with `-DLLAMA_BLAS=ON` disabled, OpenCL backend not enabled (see `llama-cli --list-devices` output = none).
- Recommended build flags for experimentation:
  - CPU: `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release`
  - OpenCL (experimental): `-DLLAMA_OPENCL=ON -DLLAMA_CLBLAST=ON`
  - Metal (macOS) / Vulkan (experimental) not applicable to The Balaur Linux host.
- Threading: `--threads 8` matches i7-4790K logical cores; adjust `--threads-batch` for prompt processing (`--threads-batch 4` recommended when context window large).

## Quantization Formats (GGUF)
| Format | Bits | Notes |
|--------|------|-------|
| Q4_K_M | ~4-bit | Balanced quality/perf. Currently deployed (Meta-Llama-3.1-8B Q4_K_M). |
| Q3_K_M | ~3-bit | Lower memory footprint (fits better in 8 GB VRAM) but quality drop. |
| Q2_K   | ~2-bit | Minimal footprint; suitable for experimentation, not production. |
| Q5_K_M | ~5-bit | Higher quality, requires more RAM (not deployed yet). |

- GGUF format stores tensor metadata, quantization scales, and versioned structure for compatibility.
- CPU inference fits Q4_K_M easily within 16 GB RAM (model size ~4.6 GB plus KV cache).

## Recommended Runtime Flags
- `--n-gpu-layers 0` (CPU-only). Set to >0 if OpenCL backend becomes viable.
- `--batch-size` / `-b`: tune to 2048 for large prompts; reduce if latency spikes.
- `--ubatch-size`: controls micro-batch compute (default 512). Lower for reduced peak memory.
- `--rope-scaling linear` for extended context if using 8k+ prompts.
- `--temp 0.2` for deterministic proposal generation (currently used in janus-agent).
- `--top-k 40 --top-p 0.95` balanced sampling if creative output required (not used for proposals).

## Performance Benchmarks (from Balaur tests)
- CPU-only Q4_K_M inference on i7-4790K: ~3.7 tokens/sec (prompt eval ~5.9 tok/s, eval ~1.6 tok/s) — see `llama_perf_context_print` in hardware inventory run.
- OpenCL test previously yielded ~2.5 tok/s due to 4 GB VRAM limitation; CPU path adopted as primary.
- Use `llama.cpp/perf/benchmark.sh` to evaluate different quantizations.

## Memory & KV Cache Management
- For 8B model: allocate ~4.6 GB for weights + ~1.5 GB for KV cache at 4k context.
- Use `--context-size` to control KV cache size; `--context-size 4096` is current default.
- Rotary positional embedding scaling (`--rope-scale`) allows longer contexts with quality trade-offs.

## Toolchain Integration
- `llama-cli` invoked by janus-agent with JSON-only prompt to enforce structured proposal output.
- Maxwell Governor monitors token rate (via planned tokens/sec sidecar) to adjust concurrency.
- Relief Valve uses CPU temperature data to decide when to throttle inference threads (via `cpupower` and `sensors`).

## Future Enhancements
- Investigate CLBlast/OpenCL build once GPU VRAM upgrade available (≥8 GB recommended).
- Explore `ggml` BLAS integration with OpenBLAS or Intel MKL to improve CPU throughput (~20%).
- Use `llama.cpp/examples/server` with REST API for multi-client usage; secure via LAN-only firewall rules (already configured for port 11434).

