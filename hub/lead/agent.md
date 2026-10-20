# Agent lead: work list (orchestrator, updated 2026-10-20T20:43Z). Read this every hour.
GOAL NOW: finish bootstrap and take Agent over (handover), so the main machine is relieved.
WORK LIST NOW:
1. bin/provision-agent-machine: every CHECK line passes. Report any that fail, with the error.
2. Hello world (prefix agt), plus ONE targeted Agent suite through the test service.
3. Handover per LEAD-AGENT.md (touch READY; wait for HANDOVER_DONE; start run-manager agent). Tell me before and after.
4. After handover: keep 5-7 workers. The Agent manager's priorities are in its INBOX (historical-audio and registered-completion positives, then delete accepted-journal consumers, legacy SDK saves and sheet merge).
If a safety check blocks a step, tell me at once with the exact step; don't wait silently.
