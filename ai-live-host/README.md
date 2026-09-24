# AI Live Host MVP

AI Live Host is a credential-free control-plane MVP for an autonomous live host.

## Implemented
- AI conversation controller
- short session memory
- chat and support event handling
- optional OpenAI Responses API integration
- YouTube Live chat adapter
- safe dry-run mode
- mobile-friendly dashboard
- no credentials committed to Git

## Run
```bash
python ai-live-host/server.py
```

Open the dashboard at `http://HOST:8790/`.

Health: `/health`
Status: `/api/status`
Demo: `POST /api/demo`
Chat: `POST /api/chat`
Support simulation: `POST /api/support`
YouTube chat: `POST /api/youtube/chat`

## Environment
Optional AI:
- `OPENAI_API_KEY`
- `OPENAI_MODEL`

YouTube chat:
- `YOUTUBE_ACCESS_TOKEN`
- `YOUTUBE_LIVE_CHAT_ID`

Use `LIVE_DRY_RUN=1` (default) while testing. Set it to `0` only after the YouTube configuration and authorization have been independently verified.

## Boundary
The MVP does not store OAuth tokens, automate OAuth consent, create a public stream automatically, or claim monetization is active. Platform eligibility remains controlled by the platform.
