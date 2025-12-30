# .env.groq

Location: `/srv/janus/config/.env.groq`

## Purpose
Template configuration file that provisions Groq credentials, feature flags, and rate limits for Balaur’s dual-speed cognition stack. Copy to `/srv/janus/config/.env` during deployment.

## Contents
- API credentials (`GROQ_API_KEY`, `WOLFRAM_APP_ID`)
- Performance parameters (`GROQ_TIMEOUT_SECONDS`, `GROQ_MAX_RETRIES`, model names)
- Rate limits (`GROQ_DAILY_LIMIT`, `GROQ_HOURLY_LIMIT`)
- Feature toggles and logging controls for each oracle method

## Deployment
```
cp /srv/janus/tools/.env.groq /srv/janus/config/.env
```
Adjust limits to match production quotas before enabling unattended use.
