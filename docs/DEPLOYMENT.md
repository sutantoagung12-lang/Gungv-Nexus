# Gungv Federation Deployment

## Runtime topology

Gungv-Nexus is the control plane. Gungv-CMRA provides memory/reasoning, Gungv-Workers provides disposable execution capacity, and Gungv-Automation provides durable scheduling/workflows.

## Required runtime environment

- NEXUS_API_TOKEN: bearer token for protected control-plane deployment endpoints.
- CMRA_URL: URL of the deployed CMRA API.
- CMRA_TOKEN: optional token for CMRA API access.
- GUNGV_RUNTIME_URL: URL of the main Gungv runtime.
- WORKER_SHARED_TOKEN: token used by workers to authenticate with their execution service.

Never commit values for these variables. Store them only in the deployment provider's secret/environment configuration.

## Deployment order

1. Deploy Gungv-CMRA and verify `/health`.
2. Deploy Gungv-Nexus and set `CMRA_URL`.
3. Register Gungv and Gungv-Workers in Nexus.
4. Deploy worker instances and register/heartbeat them.
5. Deploy Gungv-Automation and point approved jobs to Nexus.
6. Verify end-to-end health before enabling production automation.

## Safety

Direct main-branch writes remain disabled by policy. Repository changes should use branch/PR workflows. External repositories remain read-only adapters. Production credentials are never stored in Git.
