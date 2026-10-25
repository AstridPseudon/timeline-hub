# D127c preparation commands and results

| Command/check | Result |
|---|---|
| `git show -s --format='%H %T' HEAD` | PASS — `b5c9eadfa1950f46feac50d7d6a89c47f27f4881 8e10af0976b012205f27a18a432c750a27de0725` |
| `git status --short` | PASS — clean |
| Source guard SHA/blob check | PASS — `59a4d116...` / `dea8cda5...` |
| Private helper hash/mode check | PASS — `095c252b...`, `0600`; evidence dir `0700` |
| Node20 `--check` on D66 launcher and launcher test | PASS |
| Python AST parse of private helper | PASS |
| `bash -n` extracted recipe shell block | PASS |
| JSON parse of all JSON artifacts | PASS |
| D66 `p2-element --submit` | NOT RUN by instruction |
| Full/targeted/browser/live/socket suite | NOT RUN by instruction |

No skipped or filtered event was counted as a pass. No request-test service
was submitted because this task is source-only and explicitly forbids
execution.
