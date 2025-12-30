# test_groq_integration.py

Location: `/srv/janus/tests/test_groq_integration.py`

## Purpose
Automated regression coverage for the Groq dual-speed stack. Uses `unittest` with extensive mocking to validate Groq client retries/timeouts, rate limiting, and dual-speed routing. Optional real API checks run when `GROQ_RUN_LIVE_TESTS=1`.

## Running Locally
```
python3 -m pytest 02_FORGE/tools/groq_integration/tests/test_groq_integration.py -v
```

Set `GROQ_API_KEY` and `WOLFRAM_APP_ID` to enable the live web search/Wolfram tests.
