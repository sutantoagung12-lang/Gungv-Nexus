# Nexus Mobile Health Dashboard

Generate the standalone dashboard locally with:

`python scripts/nexus_dashboard.py`

The default output is:

`health/nexus-health.html`

Open that HTML file in Android Chrome. It is self-contained and has no JavaScript dependency, network dependency, or server requirement.

Google Cloud Build also generates the dashboard during validation. The dashboard is a build output; its existence does not prove that the build succeeded.
