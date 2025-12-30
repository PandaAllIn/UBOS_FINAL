# Intel Optimization Guidance Excerpts (Haswell / i7-4790K)

**References**
- Intel® 64 and IA-32 Architectures Optimization Reference Manual (Order 248966-040W)
- Intel® Software Developer Manual Volumes 1–3

## Vectorization Strategy
- Prefer AVX2 intrinsics or compiler auto-vectorization (`-O3 -march=haswell`) to leverage 256-bit integer and floating pipelines.
- Align data structures to 32 bytes (`__attribute__((aligned(32)))`) to minimize penalties from unaligned loads/stores.
- Use fused-multiply-add (FMA) instructions (`_mm256_fmadd_ps`) to cut latency and improve throughput in linear algebra.
- Balance instruction mix: pair loads, stores, and compute to keep ports 0,1,5,6 busy; avoid clustering instructions on port 0.

## Cache & Memory Optimization
- Employ cache blocking: L1 blocks around 32 KB, L2 blocks around 256 KB per core.
- Utilize streaming stores (`_mm256_stream_ps`) for large sequential writes to bypass caches when appropriate.
- For gather/scatter-heavy code, prefetch into registers or restructure data to struct-of-arrays to exploit AVX2 gather instructions efficiently.
- Monitor performance counters (via `perf stat`) for LLC misses (`MEM_LOAD_UOPS_RETIRED.L3_MISS`) and DRAM bandwidth.

## Branch & Loop Tuning
- Flatten small branches or use conditional moves to minimize branch mispredictions (14-cycle penalty on Haswell).
- Mark hot loops with `#pragma clang loop vectorize(enable)` when using Clang/LLVM or `/Qvec` in ICC.
- Employ software pipelining for latency-bound loops; Haswell scheduler handles up to 192 micro-ops in-flight per core.

## Power-Aware Performance
- Keep AVX/AVX2 utilization balanced; sustained heavy AVX loads trigger AVX offset (frequency reduction). When performance-critical, interleave scalar sections or limit vector width to maintain high clocks.
- Use `turbostat --Summary` to observe package power (PkgWatt) and frequency residency while tuning workloads on The Balaur.
- Pin latency-sensitive threads using `taskset` to specific cores to reduce context switching and maintain cache locality.

## Multithreading & Synchronization
- Favor lock-free algorithms or use Intel TSX (RTM/HLE) for short critical sections; fall back gracefully for microcode patches that disable TSX.
- Use exponential backoff in spinlocks to prevent ring contention on the LLC.
- For OpenMP workloads, set `KMP_AFFINITY=granularity=fine,compact,1,0` to maximize cache reuse on 4-core/8-thread CPU.

## Profiling Checklist
1. Compile with `-fno-omit-frame-pointer` for easier stack traces.
2. Use `perf record` + `perf report` to identify hotspots and cross-check pipeline stalls.
3. Inspect vectorization reports (`-fopt-info-vec`) to confirm loops are optimized.
4. Validate memory bandwidth using `mbw` or `stream` benchmark; compare against theoretical 25.6 GB/s limit.
5. Re-run thermal/power measurement after optimizations to ensure package power stays within 88 W TDP envelope.

