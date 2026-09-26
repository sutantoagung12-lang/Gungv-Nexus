# Google Cloud Build validation

This repository includes `cloudbuild.yaml` as an alternative CI validation path when GitHub Actions runs are unavailable or cannot be verified.

The build only installs the core pytest runtime and runs the repository test suite. It does not connect to Android Chrome, execute browser actions, install external integrations, or access credentials.

Recommended trigger:
- Connect the repository to Google Cloud Build.
- Trigger on pushes to `main`.
- Keep the trigger scoped to this repository.
- Review the build log and final status before treating validation as successful.

Security note: Cloud Build triggers execute repository-controlled build configuration. Review trigger permissions and webhook settings before enabling automatic execution.
