## Verdict: FAIL

Independent review of `tl/rt-R5-occupancy-fixture-0113` found lost predicates and scenario substitution. No tracked edits were made.

### Coverage

- Unrelated destination ×4: partial. Authenticated v2, real provider, CAS/no-write checks pass, but repeated refusal and exact error-shape assertions were removed.
- HTTP F1: pass; real daemon/client path, `destination_occupied`, no writes.
- Missing shot head ×2: partial; refusal/no-write preserved, exact guard details/head not asserted.
- Exact retry: partial; same-key replay passes, but original accepted-head and conflict-head predicates are absent; `stale_head` became unverified `value_conflict`.
- Tamper cases:
  - Receipt: partial; generic refusal only.
  - Occurrence: partial; generic refusal only.
  - Digest: pass; exact `422 invalid_closure`.
  - Projection: fail; mutation is on `main`, but candidate targets fresh `target`, so refusal occurs independently of the tamper.
  - Removed member: fail for the same reason.
- Historical reuse ×2: fail. Both cases map `shot-1` to fresh IDs (`historical-shot`/`linked-shot`), so preserving the newer global `shot-1` head is vacuous. `inline=False` and `inline=True` also submit the same v2 shape.

The dedicated old-route `410 retired_route`/no-write test is present and passes.

### Evidence

Runtime source: `24b6d923d2e6b3c09deb9599f35e785eb17ccf04`, tree `7537ab7378655948afec15805f874781a43bdd39`.

Provider used by the rerun: `/home/user/work/agent`, SHA `521c88802330901281cc37ba25818baf2575f05e`, tree `fcd3135b3dc8e93009b86b7e4b75053a4e5b9476`; loaded through `astrid.sdk.timeline.commit` and `load_timeline_commit_provider("astrid")`.

Commands:

- Targeted pytest: **16 passed**
- Ruff: **passed**
- In-memory compile: **passed**
- `git diff --check`: **passed**
- Pyright comparison: candidate 0 diagnostics, parent baseline diagnostics only, **0 new normalized diagnostics**
- Worktree: clean

The retained full census was `6479 passed, 36 failed`; no full suite was rerun and no full-suite PASS claim is made.

Recommended next step: repair the historical-reuse, projection, and removed-member fixtures so the tampered/current identities are the ones actually evaluated, then restore exact refusal/retry/head assertions.