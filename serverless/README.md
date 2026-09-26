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

Local validation:
npm install
npm run check
npx wrangler deploy
