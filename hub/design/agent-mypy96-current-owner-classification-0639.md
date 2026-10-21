# Gate7 current-only mypy owner classification

Date: 2026-10-21 UTC  
Scope: read-only classification of the retained worker-0625 raw streams. No
checker, test, baseline, stub, target, configuration, or product edit was
made.

## Evidence and normalization

The retained current stream is Agent `18a89a0d29766bd3cec31391042836ba7c951fa1`
(tree `6802b125647c6b836749e661b6c534e1f2e9d811`). Main497 is
`497714c73531f164082555ec81b61ca5bc8b6554` (tree
`daaeb1149898dd327947e21c554b484094f960b2`). Raw files are retained under
`workers/agt-m4-mypy-current-raw-diagnostics-capture-0625/raw-{current,main497}/`.

The streams contain:

```text
current       2075
Main497       2035
normalized shared  2011
current-only     64
Main-only        24
net current/Main +40
```

The comparison is a multiset of `(path, diagnostic code, message)` with the
primary line number removed. Therefore a primary-line-only move is already in
the 2011 shared set. Message-embedded line numbers are not removed; the two
`no-redef` records below are identified as harmless relocations because their
otherwise identical messages changed only the referenced line number.

## Disposition of the 64 current-only records

### Already active; do not duplicate (9 records)

- `astrid/core/timeline/scene_roles.py`: six records (`arg-type`,
  `call-overload`, `index`, `operator`, `union-attr`) are the moved
  `onscreen.py` six-record family. The CLI/core repair worker already owns
  these.
- `astrid/packs/timeline/cli_native.py:213,214` (`attr-defined`) is in the
  active CLI repair surface.
- `astrid/sdk/timeline/checkout.py:370` (`arg-type`) is the active checkout
  repair. `timeline_sheet.py` has no current-only record in this exact
  comparison; its remaining finding is shared with Main.

### Harmless relocation; no repair request (6 records)

- `astrid/core/rendering/service.py:695` (`no-redef`) matches Main's same
  `evidence` finding, with the message's referenced line moving `686 -> 693`.
- `astrid/sdk/remote.py:956` (`no-redef`) matches Main's same
  `executor_inputs` finding, with the message's referenced line moving
  `909 -> 915`.
- The four records in
  `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py`
  at `188` (`arg-type`), `224` twice (`union-attr`), and `227` (`arg-type`)
  are the same messages as Main's `run.py:1134,1170,1170,1173`; they moved
  with the extracted helper. The remaining `root_preparation.py:180`
  (`assignment`) is a real current-only boundary and is included below.

### Three bounded remaining repair requests (49 records)

1. **Agent Timeline SDK typing (21 records).** Repair only these exact
   current-only paths/codes, preserving the command, advisory-check,
   publication, rational-time, receipt, and scene-label semantics:

   - `astrid/sdk/timeline/check.py:105,203,209,252,254`:
     `attr-defined`, `var-annotated`, `type-var`, `attr-defined`,
     `attr-defined`.
   - `astrid/sdk/timeline/publish.py:37,49,91,101,102`:
     `attr-defined` at 37/49/91, `has-type` at 101, `var-annotated` at 102.
   - `astrid/sdk/timeline/revisions.py:105,254,371`:
     `assignment`, `valid-type`, `arg-type`.
   - `astrid/sdk/timeline/units.py:121,122` (`arg-type`).
   - `astrid/sdk/timeline/model.py:442,444` (`arg-type`).
   - `astrid/sdk/timeline_elements.py:280,282,284` (`arg-type`).
   - `astrid/sdk/timeline_filmstrip.py:760` (`assignment`).

2. **SDK/generated-client and private managed-result boundaries (9 records).**
   Keep the generated `WorkspaceClient` contract and fail-closed result
   handling; do not broaden these boundaries to `Any`:

   - `astrid/sdk/_remote_timeline.py:123,143` (`attr-defined`). These are
     mixin-host `_resolve_timeline`/`_typed` shape findings.
   - `astrid/sdk/_timeline_filmstrip_scene.py:29,169,170,351`:
     `var-annotated`, `list-item`, `list-item`, `var-annotated`.
   - `astrid/sdk/invocation.py:2878,2882` (`union-attr`), introduced by the
     capture-authority/forwarded-candidate admission branch.
   - `astrid/sdk/remote.py:384` (`arg-type`), optional idempotency key passed
     to generated `WorkspaceClient.create_timeline_view`.

3. **Current element/rendering extraction boundaries (19 records).** Route
   each path to its established owner; this is not a baseline decision:

   - `astrid/core/element/project_packs.py:483,502` (`index`; one extra
     multiset record among the two observed sites).
   - `astrid/core/element/schema.py:405,419` (`return-value`) and
     `406,414` (`assignment`).
   - `astrid/packs/rendering/actions/timeline_visualize/composed_frame.py:717`
     (`operator`), `748,749` (`index`), `842` (`arg-type`).
   - `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py:423`
     (`arg-type`).
   - `astrid/packs/rendering/actions/timeline_visualize/scene_only.py:128`
     (`attr-defined`).
   - `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py:93`
     (`union-attr`).
   - `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:180`
     (`assignment`).
   - `astrid/packs/rendering/rendering/renderers/remotion/run.py:1358`
     (`arg-type`, six overload-expanded argument diagnostics).

## Baseline, Main, and environment

The committed `scripts/reshape/baselines/mypy_astrid.json` has only
`finding_count=1979`; it has no per-finding IDs or messages. Its latest
content-changing commit is 2026-10-19, while Main497 is a 2026-10-20 source
commit. The baseline command also records an older developer checkout path
(`tp-merge-20261018/wt/land`), so the baseline is demonstrably older than
Main497's source history. The baseline file does not record interpreter,
mypy, NumPy, Runtime/client, or stub versions, so an older *environment* is
not proven.

Current and Main497 were captured in the same private environment:
Python 3.11.17, mypy 1.17.0, NumPy 2.4.6, Runtime95/client, and the
test-only `types-PyYAML==6.0.12.20260906` wheel (SHA-256
`bca893ff0d51df5c9053137d5d0e6ccd36e939a196356f1d5c16372422f5137b`). This
is one untracked stub distribution. There are **0 proven isolated
environment-only differential records** because both streams use that same
stub; its standalone contribution to either total is **unknown** because no
no-stub stream was authorized or captured. No count attribution to PyYAML is
made.

The `+56` gap between Main497's 2035 and the committed 1979 baseline is
therefore source/environment mixed and cannot be split from message evidence.
The exact comparison proves the current-vs-Main `+40` and the 64/24
partitions, but does not justify a baseline, stub, target, or config change.
The 2011 shared records, including the known 123-record `has-type` cluster in
`astrid/core/execution/custody_broker.py`, are inherited by current under this
environment and are not assigned as current-only repairs.

No upstream baseline decision is currently unavoidable. If a future owner
decision is required, the reason is the baseline's missing per-finding and
environment provenance—not evidence that the 49 bounded repairs are
unrepairable.

## Verification boundary

No mypy/checker invocation, pytest, Make target, full suite, browser, or
renderer test was run for this classification. No repository product,
baseline, stub, target, configuration, or dependency file was changed.
