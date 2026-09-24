# ChatGPT Bridge

This is the runtime side of the Gungv-Nexus bootstrap bridge.

## Endpoint
- `GET /bootstrap` returns the current Nexus bootstrap context.

## Security
This bridge is read-only. It must be deployed behind authentication before being exposed to the public internet. Do not place GitHub tokens, OpenAI keys, or other secrets in this repository.

## Important
Creating this bridge does not itself register a ChatGPT connector. A ChatGPT-compatible connector/MCP endpoint must be connected in the ChatGPT environment before new chats can retrieve this endpoint automatically.
