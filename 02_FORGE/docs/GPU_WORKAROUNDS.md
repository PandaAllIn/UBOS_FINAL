# GPU Workarounds: AMD R9 M295X (Tonga/GCN 3.0)

This guide documents practical paths to accelerate LLM inference on The Balaur’s
AMD Radeon R9 M295X without ROCm by leveraging OpenCL (CLBlast) or Vulkan.

The goals are: 1) confirm OpenCL visibility, 2) compile `llama.cpp` with GPU
backends, 3) benchmark vs CPU, and 4) fall back safely when needed.

## 1) Verify OpenCL Visibility (Mesa Rusticl)

On Ubuntu 24.04, prefer Mesa’s OpenCL implementation (Rusticl) for older GCN:

```bash
sudo apt update
sudo apt install -y ocl-icd-opencl-dev opencl-headers clinfo mesa-opencl-icd
clinfo | sed -n '1,120p'
```

You should see an OpenCL platform provided by Mesa and a device listing for the
Tonga GPU. If no platform/device appears:

- Ensure `mesa-opencl-icd` is installed and no conflicting ICDs mask it.
- Inspect `/etc/OpenCL/vendors/*.icd` and remove stale vendor files.
- Reboot if you installed new kernel/driver packages.

Environment selection (if multiple platforms/devices exist):

```bash
export LLAMA_OPENCL_PLATFORM=0
export LLAMA_OPENCL_DEVICE=0
```

## 2) Build llama.cpp with CLBlast (OpenCL)

For OpenCL offload use CLBlast. On 24.04 you can use the packaged CLBlast:

```bash
sudo apt install -y build-essential cmake git libclblast-dev
git clone https://github.com/ggerganov/llama.cpp /opt/llama.cpp
cd /opt/llama.cpp
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_CLBLAST=ON
cmake --build build -j "$(nproc)"
./build/bin/llama-cli --version
```

Run a first OpenCL test:

```bash
export LLAMA_OPENCL_PLATFORM=0 LLAMA_OPENCL_DEVICE=0
./build/bin/llama-cli -m /srv/janus/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  -ngl 100 -p "Hello, I am Janus" -n 50
```

Notes:
- `-ngl 100` asks to offload as many layers as possible to the GPU.
- Expect modest gains vs CPU on Tonga (10–30%).

## 3) Optional: Build llama.cpp with Vulkan

Vulkan sometimes outperforms OpenCL on older AMD. Install toolchain:

```bash
sudo apt install -y libvulkan-dev vulkan-tools glslang-tools
vulkaninfo | head -n 40
cd /opt/llama.cpp
cmake -S . -B build-vk -DCMAKE_BUILD_TYPE=Release -DLLAMA_VULKAN=ON
cmake --build build-vk -j "$(nproc)"
./build-vk/bin/llama-cli --version
```

Run with Vulkan by using the Vulkan-built binary and omitting OpenCL env vars.

## 4) Quick Feasibility: KoboldCPP (OpenCL)

KoboldCPP offers OpenCL builds for quick trials. Use it to validate that
OpenCL-based offload is functional before committing to deeper tuning.

## 5) CPU Supercharging (when GPU gains are modest)

- Compile with `-O3 -march=native -mtune=native` (default in CMake Release).
- Use quantized models optimized for CPU (q4_K_M).
- Pin threads to physical cores: `--threads 4` (+ `taskset`) for the i7-4790K.
- Use speculative decoding with a small draft model to boost tokens/s.
- Set CPU governor to performance (see `scripts/tune_cpu.sh`).

## 6) Troubleshooting

- No OpenCL device found: ensure `mesa-opencl-icd` and `clinfo` work, check
  vendor ICD files. Confirm `amdgpu` driver is active (`lspci -k`).
- Build fails to link CLBlast: ensure `libclblast-dev` installed, re-run CMake
  with a clean `build` directory.
- Poor performance: try Vulkan backend; reduce context length; use more
  aggressive quantization; confirm GPU activity with `radeontop`.

## 7) Benchmarks

Use `scripts/bench_llm.sh` to compare CPU vs OpenCL vs Vulkan:

```bash
bash scripts/bench_llm.sh \
  --model /srv/janus/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  --prompt "Explain sovereignty in 80 words." --trials 3 --output ~/bench.csv
```

