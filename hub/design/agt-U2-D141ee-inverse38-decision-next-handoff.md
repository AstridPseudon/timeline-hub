# U2 D141ee inverse38 handoff

Ready for the required independent protected review and harness commit. Only product change: restore `astrid/core/timeline/inverses.py` from pristine `64197afa297f86f1e738238d5e80aff6d33e303a`, exact blob `5d2514841e6cbb3e8cd7172b59dbd315f5bf8bd1`. No test, reference, current authenticated inverse, event writer, Runtime, contract, force, hook, cache or trust change.

Authority: D141ii lead PROCEED relay SHA256 `fb6a058429c94e0a1574f8ba349fea24689be855b9667da9f3ff81dac5938d22`; owner verbatim file was not delivered at dispatch. This explicitly preserves public pure planning use. The supported direct public API is `from astrid.core.timeline.inverses import InverseRequest, plan_inverse, plan_inverses`; the 38 original tests call those functions with typed TimelineEvent objects and before/after projections. Product-wide search finds only the planner's internal `plan_inverses -> plan_inverse` call, no external production writer. No writer-caller credit is claimed.

The separate production undo route remains `commit_session.py:73 -> sync.py:422 TimelineSession.undo -> sync.py commitTimeline invocation -> commands.py:268 apply_inverse`. Its source hashes remain unchanged; it was not re-qualified by these pure tests. Runtime remains the sole persistence writer.

Validation: 38/38 approved originals PASS; mypy PASS; whitespace PASS; ruff FAIL with one pre-existing BLE001 at restored line 770. Do not report lint green. Exact byte restoration takes priority over silently fixing/suppressing that diagnostic.

Review the erased-projection limitation in validation.md: the restored planner refuses mechanical erased inversions but returns the caller's supplied projections; the preserved erased tests do not assert sanitization. A stronger redaction guarantee would require separately approved scope. All pure and erased test predicates are unchanged.

Installer2 remains HOLD and untouched; writers15 belongs to another worker. No full-suite, REG0, pin/build/ZIP, production undo requalification or delivery credit is claimed. Next: independent protected review, then the manager-owned merge queue and coordinated retained-ID qualification after other scopes settle. No manager staging wait is needed here.

Operational limitation: initial detached sampler did not persist; the terminal-session trace covers subsequent validation through finalization, with no invented backfill.
