# Development journeys

`astrid-tools dev journey render --project PROJECT [TIMELINE]` renders an
existing canonical timeline through the current Runtime. When `TIMELINE` is
omitted it uses the project's configured default. The command reads the
timeline head first, passes the observed Runtime version as a render CAS pin
when available, waits for the managed render, then reads the head again. Its
result reports the render run/task/output identifiers and whether the timeline
head stayed unchanged.

Use `--range START..END` to request a half-open interval and `--json` for a
machine-readable result. The command only connects to an already-running
selected Runtime. It does not start a service, create a project, seed a
timeline, or infer a production/GATE result.

This current-contract runner is not a recovery of the historical
`checkpoint-20261013` film journey. That source and its exact commit provenance
must be recovered independently before claiming the original checkpoint
journey has been ported.
