Studio Verification & Maintenance
---

Scripts
- verify_code_server.py — checks binary, services, and HTTP endpoint
- validate_gpu_acceleration.py — probes glxinfo/vainfo/nvidia-smi/vulkaninfo/clinfo
- studio_maintenance.py — orchestrates both and emits a single JSON bundle

Examples
- python3 02_FORGE/scripts/deploy/studio/verify_code_server.py --json
- python3 02_FORGE/scripts/deploy/studio/verify_code_server.py --host 127.0.0.1 --port 8080 --json
- python3 02_FORGE/scripts/deploy/studio/validate_gpu_acceleration.py --json
- python3 02_FORGE/scripts/deploy/studio/studio_maintenance.py --output /tmp/studio_health.json

Notes
- Service detection tries system and user managers: code-server@$USER, code-server (system), and code-server (user).
- HTTP probe treats 200/401/403 as “responsive”; token may be required in production.
- GPU probes are best-effort; install tools: mesa-utils, libva-utils, vulkan-tools, clinfo, nvidia-utils (if applicable).

