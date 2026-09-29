# Gungv-Nexus Serverless Runtime

This directory is the serverless execution shell for Gungv-Nexus.

It uses a persistent Durable Object as the state authority. HTTP events become queued or scheduled Nexus tasks. The runtime does not claim that a task executed until a future execution bridge is explicitly configured.

The runtime intentionally does not execute destructive browser, Android, GitHub-write, credential, or arbitrary code actions. Those remain Nexus approval-gated capabilities.

Android use: the phone only needs the deployed Worker URL to submit and inspect tasks.

Endpoints:
- GET /
- GET /health
- GET /state
- POST /task
- POST /schedule
- POST /device/capabilities (Bearer NEXUS_DEVICE_TOKEN)
- GET /device/capabilities (Bearer NEXUS_DEVICE_TOKEN)

Local validation:
npm install
npm run check
npx wrangler deploy


## Android capability registration

Configure a secret before accepting device reports:

`wrangler secret put NEXUS_DEVICE_TOKEN`

The Android Worker posts its conservative capability snapshot to `/device/capabilities`. The endpoint is authenticated and stores the latest snapshot in the persistent Durable Object state. It does not grant the phone arbitrary execution rights.
