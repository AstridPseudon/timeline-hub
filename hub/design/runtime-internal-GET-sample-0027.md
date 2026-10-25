Completed one authenticated internal revision GET on Runtime `a3cd1a321`. No product or test changes.

| Measurement | Result |
|---|---:|
| Outcome | HTTP 200; payload matched acceptance |
| Caller wall | 5.254 ms |
| Caller main-thread CPU | 0.849 ms |
| Handler wall | 4.000 ms |
| Handler thread CPU | 3.370 ms |
| History/accepted-verification/sequential calls | 0 |
| Pending at 3s / 8s | No / No; no dumps |

Fresh supported setup produced **5 genuine accepted commits plus 1 bootstrap**, confirmed by public history and stored counts. Both internal revisions share the parent timeline’s scope. This matches P2’s source-derived pre-reload history length; the original numeric history payload was unavailable locally.

The top positive profile frame was `_route` at 2.308 ms cumulative. **Reliable whole-handler ranking is UNKNOWN:** the raw profile contains negative root timings and caller-side frames. Independent wall and thread CPU intervals remain usable.

Validation:

- `/home/user/work/venv-runtime/bin/python …/evidence/sample_get.py` — exit **0**. Exact environment and command: [sample.command.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-internal-GET-sample-sol-0027/evidence/sample.command.json).
- `/home/user/work/venv-runtime/bin/python …/evidence/validate_evidence.py` — exit **0**: script compilation, 103 pinned import identities, counts, watchdog disposition and `git diff --check` passed.
- All **4,087** inventoried source files remained byte-equal. No suites or browser journeys run.
- Initial setup exited **1** before any commit or measured GET because the diagnostic omitted required initializer fields; preserved and corrected.

[Durable evidence checksums](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-internal-GET-sample-sol-0027/evidence/evidence-hashes.json) cover logs, scripts, profile and dispositions.

Finding: this isolated GET was cheap with the counted history. The original App wait’s cause remains **UNKNOWN**; smaller payloads and no concurrent workload limit comparison. No repair is justified by this sample alone.

Commit message and `DONE` created.