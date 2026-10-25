<!-- farm | 2026-10-25T15:51:09Z | dispatcher heartbeat 6s | live 0 (sol 0, luna 0, other 0) | busy30 0 | status age 2m -->
# farm board, 2026-10-25T15:50Z. Active (D124.6) for ONE job: the D77 installed render. Idle until Runtime sends the stage/render command and inputs. No worker running.

Lead MAIN 16:00Z (relayed 15:43Z): the farm's agent-core-full route is DROPPED; Agent hosts it itself on a4e016 with its freed 6.1 GB. No census build, no child-venv reissue, no body.

| ID | task (short) | status | notes |
|---|---|---|---|
| F-agent-core-full | agent-core-full on Agent a4e016b6 | dropped (MAIN 16:00Z, Agent hosts it) | Left in place, untouched: checkouts agt-pin-a4e016b6, rt-pin-5e9ad1c6, app-pin-d8a1cd40, vw-pin-635f4de0 (trees verified); refused child log design/farm-childvenv-a4e016-REFUSED-unowned-retained-source-directory-20261025T1452Z.txt. The D127a diagnostic build is not run on the farm |
| F-D77-render | Genuine installed render (D124.6; Runtime handoff design/rt-D124-Farm-render-handoff-1253.md, guard PASS 1257, custody PASS 1300) | waiting for Runtime's stage/render command and inputs; stays idle until then | One heavy body at a time (D89: start needs 6.0 GB plus the job's footprint free, stop 4.0 GB); tell the lead the expected footprint before starting; normal installer only, no near-match inputs, no unverified recipe change |
| F-agent-inverse-review | Independent source/core review of Agent's inverse diagnosis | done 15:15Z: PASS (source/core); Ruff/py3.11/AST NOTRUN (approval refusal), 3-case test NOTRUN | design/farm-agt-D124-inverse-core-review-1450-report.md |
| F-host14-light | 14-node host-bootstrap proof | dropped (MAIN 14:42Z) | refusal log kept |
| F-D49 / F-final / F-zip-dry / F-P2 / F-P3 | earlier rows | stood down (D56.3) or moved | none |

Blockers: none for the farm; it is idle by order until Runtime sends the D77 render command. Disk 15 GB free.
Next ready: none.
