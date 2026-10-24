Oracle repaired in [test_authoring_media.py](/home/user/work/wt/agt-F-ABA-oracle-sol-0208/tests/timeline/test_authoring_media.py:950). **The required original target remains unexecuted, blocked on central suite registration.**

Only the second test changed. It resolves the raw clip through the baseline parent occurrence → pinned shot revision → internal revision, verifies `source_mapping` and the exact revision/publication pair, and compares the complete raw clip with the trusted seed and public baseline. The expected hold guard derives from that verified clip.

Validation completed:

| Exact command | Result |
|---|---|
| Qualified supplied environment, `/home/user/work/venv-agent/bin/python /tmp/w-42e473b82a/offline_oracle.py` | Passed seven baseline assertions; raw before `(at, hold) = (0, 0.9)`; unavailable publication refused |
| `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-42e473b82a/preservation_check.py` | Complete behavior preservation check passed |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python /tmp/w-42e473b82a/static_checks.py` | Scoped Ruff and private mypy: exact parent identities, **0/0 diagnostics** each |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` | Passed |
| `git diff --check` | Passed |

Original predicate map, numbered in source order:

- **1–8:** unchanged, same lines.
- **9–52:** original line +41.
- **11:** exact two-change record expectation retained; only stale hold-before `1.8` becomes the authenticated baseline value.
- **All 52 predicates remain; 59 final assertions.** AST comparison also preserves every original command, exception expectation, context manager, and other module body.

This retains after-values, source-window/null handling, opaque data, registry order, second consumer, untouched second shot, reload, whole undo, lost-ack restart/retry, disjoint rebase, refusal/no-write, redo, and ABA guards. Production, fixtures, first publication test, and C0 guards are unchanged.

Runtime imports verified as `8ea0766f5e9fb23cea26c7398770a8aaac06b258`; Agent imports resolve to this worktree. The archived fixture constructor remains from `a0dca169…`.

**Blocker:** no registered central nodes suite supplies the required startup environment and `--timeout=45`; generic `targeted` excludes integration tests and rejects option arguments. Registration was requested. No target was submitted, so there is **no new authored publication packet or downstream runtime qualification**.

Commit message and `BLOCKED` marker written; no `DONE`. Next: register the exact bounded command, run the original second node once, then perform independent no-weakening review. Vendor checker and full suites were not executed.