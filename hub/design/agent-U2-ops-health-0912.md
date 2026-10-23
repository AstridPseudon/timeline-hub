# U2 ops health handoff

Diagnosis: ordinary FIFO queue blockage plus a separate process-namespace false-orphan event.

The dispatcher is explicitly host/outside-sandbox (`bin/dispatcher-daemon:2`), selects oldest pending entries (`:7-8`), and executes `CHILDVENV`/`RUNTIME` synchronously (`:11-12`) before updating `dispatcher.heartbeat` (`:30`). At 09:07 the queue was blocked by `childvenv-venv-agent-child-f0905-current`; `runtime-agent-remotion-0013` followed it. The reviewed merge requests at 09:07/09:08 consequently remained pending behind provisioning. The host-lead record at 09:43:29Z identifies a hung pip in that child-venv build from 09:07–09:42; after the host lead terminated that pip, the heartbeat advanced and the existing queue drained.

`ensure-daemons` is unsafe as a worker-sandbox liveness authority: its `ps -eo args` checks (`:12`, `:14-15`, `:31`) observe only the caller's process namespace, while its `:33` finalizes any worker whose worktree is absent from that view. Four reviewed workers were marked STOPPED 09:08:13–09:08:31 even though their logs/reports completed later. This establishes false liveness, not real worker death or a host restart. The PID-file mtime at 09:08:49 is not proof of a host restart; the authoritative evidence is the stale heartbeat followed by the host-lead recovery and advancing heartbeat.

Existing continuations, do not duplicate: `agt-F-V2-resume-0911`, `agt-F-Composition-resume-0911`, `agt-F-writer-resume-0911`, and `agt-F-provider-review-resume-0911`. Owner next step is the actual host lead using the existing serialized queue/daemon route. No code or process patch was installed.
