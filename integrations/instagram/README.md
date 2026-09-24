# Instagram Connector

Gungv-Nexus connector for the Instagram API with Instagram Login.

## Supported flow

1. Generate an OAuth authorization URL with a cryptographically random state.
2. User authorizes an Instagram professional (Business/Creator) account.
3. Exchange the authorization code for a short-lived token.
4. Exchange the short-lived token for a long-lived token.
5. Read the profile.
6. Create image or Reel media containers.
7. Publish a completed container.
8. Query container status.

The connector does not store access tokens or app secrets. Put secrets in the runtime secret manager/environment, never in Git.

## Environment

- `INSTAGRAM_CLIENT_ID`: Instagram App ID.
- `INSTAGRAM_CLIENT_SECRET`: Instagram App Secret.
- `INSTAGRAM_REDIRECT_URI`: exact OAuth callback registered in Meta.
- `INSTAGRAM_API_VERSION`: Graph API version selected for the deployed app.

Default scopes are `instagram_business_basic` and `instagram_business_content_publish`. Add messaging/comment permissions only when those capabilities are explicitly needed.

The current Instagram Login permission names are the `instagram_business_*` names; the older `business_*` names were deprecated in January 2025.

## Security

- Never commit `INSTAGRAM_CLIENT_SECRET` or access tokens.
- Validate OAuth `state` against a server-side session before exchanging a code.
- Keep callback URLs exact and HTTPS in production.
- Treat all API responses as external data until validated.
- Publishing is an external side effect and must remain behind an explicit execution gate.

## References

Meta's official Instagram Postman workspace documents Instagram Login, content publishing, messaging, and current permission names.
