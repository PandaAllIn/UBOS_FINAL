# deploy_groq_to_balaur.sh

Automates the Groq dual-speed integration rollout to Balaur.

## Steps Performed
1. Verify SSH access to `panda@100.94.145.78` (override via `GROQ_DEPLOY_USER`/`GROQ_DEPLOY_HOST`).
2. Install/upgrade `groq` and `python-dotenv` on the vessel.
3. Upload `groq_client.py`, `dual_speed_brain.py`, `.env.groq`, and the test suite.
4. Copy the environment template into `/srv/janus/config/.env`.
5. Run `pytest` to exercise offline mocks (live tests gated by env).
6. Restart `janus-agent` and `janus-controls`.
7. Execute a live `fast_think` smoke check.

## Usage
```
chmod +x 02_FORGE/scripts/deploy_groq_to_balaur.sh
02_FORGE/scripts/deploy_groq_to_balaur.sh
```

Set `TOOLS_DIR` to deploy from a custom staging directory if required.
