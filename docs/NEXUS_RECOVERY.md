# Nexus Recovery Planner

The recovery layer converts health diagnostics into safe, explicit recovery plans.

It is **plan-only**:
- no browser action is executed;
- no Android Chrome action is executed;
- no credentials are discovered or changed;
- no dependency is installed automatically;
- approval requirements remain intact.

Generate a report with:

`python scripts/nexus_recovery_report.py health/nexus-recovery.json`

The report uses schema `nexus-recovery/v1`.

A recovery plan is considered complete only after its recommended validation is performed and a new health report confirms the resulting state.
