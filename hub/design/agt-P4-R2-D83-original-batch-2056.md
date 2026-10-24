## P4/R2 D83 report

Result: **NO-GO, candidate-scope only**. Exactly one service run; no rerun, merge, or independent verdict.

Changed only the owned seven-selector registry row in `tests/suites.conf.candidate`. CAS install passed; outside rows remained byte-identical. Candidate delta was donor2 only, with lock byte-identical to normal Agent home.

Pinned tuple:

- Agent `21c6f514…`, Runtime `dc55b8bc…`
- App `ce1cd9c4…`, Composition `635f4de0…`

Controls passed:

- Parsed command `bash -n`: exit 0
- Positive probe: exit 17, one stub call
- Wrong-SHA poison: nonzero, zero stub calls
- Disk: 9 GB available
- Evidence: 420 KB

Service command: `request-test integration:agent p4-current-becfe-http-3legs --no-cache`

ID: `agent-p4-current-becfe-http-3legs-1024205949-1960`

| Outcome | Duration |
|---|---:|
| PASS | 2.994s |
| FAIL timeout | 45.439s |
| PASS | 9.162s |
| FAIL timeout | 45.008s |
| FAIL timeout | 45.007s |
| PASS | 42.153s |
| PASS | 42.608s |

JUnit total: 236.497s; service exit 1. Earliest failure was the ten-note selector; raw traceback ended at `json/encoder.py:263`. No cause inference performed.

Evidence: [outcomes.tsv](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-R2-D83-original-batch-2056/evidence/outcomes.tsv), [JUnit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-R2-D83-original-batch-2056/evidence/p4-r2-d83-unprofiled-seven.xml), [raw log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-p4-current-becfe-http-3legs-1024205949-1960/log.txt).

`DONE` and commit message are present.