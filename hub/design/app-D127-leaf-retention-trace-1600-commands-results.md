# D127 commands and results

All commands were read-only; no Runtime/App source or tests were edited.

| Command | Result |
|---|---|
| `sed -n '1,240p' .../PLAN.md` | PASS; settled PLAN v2.1 read first. |
| `git status --short --branch` | PASS; `tl/app-D127-leaf-retention-trace-1600`, clean. |
| `sha256sum tests/helpers/p2_commit_phase_capture.py` | PASS; `6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`. |
| `sha256sum tests/test_p2_commit_phase_capture.py` | PASS; `1a1b475e8095a8a70cd5d7f5c884b6d68a37d19d62807d70d982f5224025aff9`. |
| Input JSON/hash inventory for D127b facts, request binding, stack index, privacy check, and durable custody | PASS; hashes recorded in `facts.json`. |
| Sanitized parse of retained Actual10721 facts | PASS; exact element join and pending request facts preserved; no raw payload/key/preimage/body/stack copied. |
| `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_p2_commit_phase_capture.py -k 'ring_retains_late_failing_request_after_successful_setup_events or final_request_byte_bound_reports_exact_incomplete_limit or pending_request_is_the_final_correlated_request_and_shutdown_is_deterministic or watchdog_finish_raised_disabled_and_late_callbacks_are_safe'` | PASS; `4 passed, 15 deselected in 1.58s`. Offline focused helper tests only. |
| `python -m pytest ...` using system Python | Not available; `/usr/bin/python` has no pytest. Re-run with the shared read-only Runtime venv above passed. |
| `/home/user/work/venv-runtime/bin/python -m json.tool evidence/facts.json` | PASS. |
| `git diff --check` | PASS; no product worktree diff. |
| `git status --short --branch` after trace | PASS; clean product worktree. |

No full suite, live browser journey, localhost probe, new profile, source acquisition, or body/stack publication was run.

