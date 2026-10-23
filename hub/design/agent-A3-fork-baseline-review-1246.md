# A3 fork source-baseline independent review

## Verdict

**PASS — retained/copied baseline authenticity and unchanged guard behavior.**

Reviewed `tl/agt-A3-fork-source-baseline-1232/bfcf78db99` against
`d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`. The candidate changes only
`authoring_bundle.py`, `native_occurrence_duplicate.py`, and the new
`test_occurrence_fork_source_baseline.py`.

The internal `_CopiedShot` subclass is preserved by recorder/deepcopy paths,
but its `source` attribute is not part of dict iteration or JSON, so it adds no
portable authored/protocol field. The compiler does not trust caller
`base_payload`, `base_internal_timeline`, mutable source mappings, or serialized
claims for copied shots. It verifies the immutable `_runtime_document`, exact
project/timeline and parent revision pair, source occurrence/shot/revision,
destination occurrence/shot placement, then reconstructs the baseline through
the existing deterministic item remap. The existing media-addition and
competing-selection checks therefore still run against the verified source
baseline, and materialization remains required for the new root.

The source caller path is the real native fork → `document_from_bundle` →
document emitter path. The retained source media/metadata, sibling placement
and order, null/opaque values, and dependency media manifest remain intact;
the selected fork can then receive a supported edit without changing the
original owner. New competing shot/internal selections, stale source pins,
foreign/outside owners, occupied identities, old-payload claims, JSON-stripped
provenance, and source-map/closure tampering remain refused without input
mutation.

No source or guard finding requires a change. The separately reported combined
fork + patch whole-commit undo failure (`inverse stage native writes do not
cover its authenticated effect image`) remains an R2/inverse limitation. This
review does not claim that inverse journey passes; the source-baseline result
is PASS only because the existing fork-only undo/refusal behavior remains
passing and this candidate does not broaden that inverse gap.

## Evidence

- Targeted new + existing fork/duplicate set: **105 passed in 12.98s**.
  This includes the 17 new tests, existing fork undo/redo, stale/refusal
  controls, duplicate controls, and the unchanged portable native golden.
- Actual current 3b RuntimeService witness, `-m integration`: **1 passed,
  16 deselected in 3.81s**. It exercised preview (`would_status=accepted`, no
  receipt/write), acceptance, canonical closure equality, selected edit,
  unchanged sibling images/order, and the real `astrid-v1` provider.
- Caller/tamper probe: **passed**. An arbitrary caller-constructed
  `_CopiedShot` with an exact-looking binding could not authorize a mismatched
  new media pair; deepcopy preserved the subclass and JSON serialization
  excluded `source`.
- Loaded origins: Agent modules came from this review worktree;
  Runtime service/provider loader came from
  `/home/user/work/wt/rt-pin-3b926efa`; `load_timeline_commit_provider('astrid')`
  returned the real `RuntimeCommitService`.
- `make ruff`: **2149/2149**, unchanged from baseline.
- `make mypy`: **1912/1912**, unchanged from baseline.
- Scoped Ruff on the three touched files: **passed**.
- Vendor lock check: **ok**, matches producer manifest.
- Artifact manifest: **current**.
- `git diff --check`: **passed**.

The first attempted pytest command used the assigned worker `tmpdir` path,
which is an existing regular file in this environment; pytest consequently
reported setup errors before running tests. Re-running with a private `/tmp`
basetemp produced the 105-pass result above. No full, browser, HTTP/socket,
P1/P4, broad native, or combined-inverse suite was run.

No product/test files were edited by this review; only this durable report was
written.
