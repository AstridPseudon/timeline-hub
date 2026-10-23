# Runtime G5 inverse boundary diagnosis handoff

**Disposition: precise bounded blocker; no Runtime cause captured.**

The requested one-shot invocation used Runtime `3b926efab2eed122d374540baee297d4cdcec62a` / tree `b794170504544b259781e50d7ca4d61b6729e67c` with Agent candidate checkout `/home/user/work/wt/agt-pin-5dcf78e3` at `5dcf78e31977019d7878cce7313db31c0422d2ec` / tree `6e07ede8f92ebed01e2d5e73a32405fe96038720`. The candidate checkout receipt was verified at `queue/done/checkout-agent-5dcf78e319`.

The candidate fails before Runtime is called. Its fixture defines `open_composition` as a two-argument lambda at `tests/sdk/test_timeline_restructure.py:392`, while the candidate’s `restructure_inverse_runtime` fixture restores the real `RemoteTimelines.open_bundle`; that implementation calls `open_composition(project, ref, revision_id=revision_id, limit=1)` at `astrid/sdk/_remote_timeline.py:48`. The exact target therefore raises `TypeError: restructure_runtime.<locals>.<lambda>() got an unexpected keyword argument 'revision_id'` at the first `timeline.open` (`test_timeline_restructure_guarded_runtime.py:71`) in 6.73s.

The Runtime-side observer was scratch-only and passed Ruff/Pyright. It was designed to flush bounded request, raw accepted-restructure/inverse request, prepared arguments, head/history and port boundary evidence as coordinator/provider/port-factory/verify/close seams ran, preserving predicates and re-raising exceptions. No seam ran in this invocation, so no underlying Runtime/provider/port/close traceback exists to attribute. The bounded capture is in the worker evidence file `evidence/g5-setup-blocker.md`; no Runtime source or tests were edited.

This is an Agent fixture harness blocker, not a guard refusal and not evidence of a Runtime semantic correction. Hand back to Agent firstreturn1229 for the fixture-fidelity repair and exact public-pair/no-write qualification. Once a corrected candidate checkout is independently qualified and supplied, Runtime should rerun exactly one instrumented target invocation to obtain the first underlying traceback before any owner-directed repair. G5 remains blocked; no undo/redo/refusal qualification is inferred.

