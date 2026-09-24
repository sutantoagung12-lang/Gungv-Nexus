# AI Live Host MVP

AI Live Host is a credential-free control-plane MVP for an autonomous live host.

## Scope
- AI conversation controller
- session memory
- chat event queue
- donation/fan-funding event abstraction
- YouTube Live REST adapter
- safe dry-run mode
- mobile-friendly dashboard
- no credentials committed to Git

## Runtime
The MVP uses Python standard library only. Optional AI generation uses the OpenAI Responses API through HTTPS when `OPENAI_API_KEY` is present.

Required for YouTube live operations:
- `YOUTUBE_ACCESS_TOKEN` with the required YouTube OAuth scopes
- `YOUTUBE_LIVE_CHAT_ID` for an existing live chat

The MVP deliberately does not automate OAuth consent or store tokens.

## Start

```bash
python -m ai_live_host.server
```

Open the dashboard on the configured host at `/`.

Health: `/health`
Status: `/api/status`
Demo event: `POST /api/demo`
Send chat: `POST /api/chat`
Send support event: `POST /api/support`
Generate AI response: `POST /api/respond`
Send a YouTube chat message: `POST /api/youtube/chat`

Set `LIVE_DRY_RUN=1` for safe testing (default).

## Safety boundary

The system never claims that a stream, monetization feature, or donation was activated merely because configuration exists. Runtime responses expose explicit states: `configured`, `connected`, `ready`, and `dry_run`.

Platform eligibility and monetization remain controlled by the platform account and its policies.
