# Validation record

Candidate source was read-only. No source, registry, queue, hub, lock, cache,
lease, install, product, App, or Runtime worktree was changed.

## Commands

| Command | Result |
|---|---|
| `TMPDIR=/tmp/w-1a39664498/d141-review-tmp python3 -I ops-d141-measured-floor/controls/real-controls.py` | PASS; 61 controls in the author JSON result |
| `bash -n ops-d141-measured-floor/bin/test-run` | PASS |
| Python AST parse of all five scoped Python files | PASS |
| `ruff check --no-cache ops-d141-measured-floor/bin/d141-append-final.py ops-d141-measured-floor/bin/d141-disk-trace.py ops-d141-measured-floor/bin/d141-validate-receipt.py ops-d141-measured-floor/bin/d141-validate-trace.py ops-d141-measured-floor/controls/real-controls.py` | PASS; All checks passed |
| `git diff --check` | PASS |

The author script's actual normal path was isolated: its installed copy was
published through `ORCH/bin/* -> hub/kit/bin/* -> receiving ORCH/bin/*`, then
executed from the received bin without `controls/` or a sibling controls
module. It exercised normal `request-test` full-ID generation, pending `TEST`,
and received `test-run`. No live product tests/import/collection/preflight,
network, browser, queue, body, install, or hub operation was run.

## Independent security probes

Using temporary fixtures under `/tmp`:

1. `d141-append-final.py` was given a symlink trace path. It exited 0 and
   appended to the target (`target_bytes=81`) instead of refusing.
2. It was given a FIFO trace path. It blocked until `timeout 2` returned 124.

These are direct reproductions of D141H-SEC-001, not inferred failures.

No central full suite was requested: this brief required targeted/static
review and isolated controls only.
