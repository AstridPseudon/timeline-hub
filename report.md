# R2r leaf inverse independent review — FAIL

## Verdict

**FAIL. Do not merge or claim whole undo/redo qualification.** The candidate
has a plausible narrow Runtime materialization-turnover implementation and the
targeted suite is green, but its new positive regression is not a replay of the
retained actual first-stage capture. The complete two-stage retained replay
also remains refused at the later aggregate/root sequential-input boundary.

## Candidate and preserved scope

- Candidate commit: `6e256ea3d2786581525bafbc2e4f343c60ef6a03`
- Candidate tree: `09789d08d2b70bf4134ab5ccba836a1d286ab062`
- Requested base: `8592822fd11275540f596562f43c715676f2bc0f`
- Base tree: `ed9856f43a4e44a058bf2230badea2c4c7080050`
- Changed paths: only `runtime_protocol/timeline_commit_auth.py` and
  `tests/test_timeline_inverse_stage_authentication.py`.
- Candidate production SHA-256:
  `d2f33d455cc93e290118d63942c7681e448b4edae1f7930ad7ae583fa170425a`
- Base production SHA-256:
  `d79f2da9f47cbc4aef8d51a899d47ec04458d9140e67636c7c83e0675d0072e2`
- Candidate test SHA-256:
  `8a1a95a664dc1298dd9e6a043ea750da7ea4c0f259a62731a61a3a94ca2c0875`
- Base test SHA-256:
  `81984fb6298bdf71c9606d6d08f797aecce6ba954e275335e6577d0bb55f4d01`
- The `9c694858e` source/allocation guard paths have no diff against the
  candidate. No product, generated, pin, contract, or original test body was
  changed. AST comparison found all 17 pre-existing test function bodies
  unchanged; three new functions were added.

## Blocking finding: the positive is compact/invented, not actual capture

The new helper at `tests/test_timeline_inverse_stage_authentication.py:275-366`
is explicitly compact, but it constructs new payloads and history rather than
loading the retained package. It reuses a few actual revision/publication IDs,
then invents the closure contents:

- The actual package is
  `design/agent-R2-leaf-1246-e97f81ce7c350f08.json`, SHA-256
  `1123978b7b18c59d280f73c9ad9155b5ba18d0c64b24e45b8bdd02af30a887b0`.
  Its manifest SHA-256 is
  `803c11e3e9bd1c4a8794365f7ce11574a7224bd2f735aaafc7ec2ce942cdfc74`.
- Actual `stage_before` and `stage_after` each contain five physical roots:
  parent, the authoring shot/internal roots, and the unrelated
  `document-diff` shot/internal roots. The added helper contains only three
  main roots plus a synthetic `captured-unrelated` internal root.
- Actual canonical stage images serialize to 9,059 and 9,052 bytes (sorted
  compact JSON); the helper's synthetic images serialize to 1,651 and 1,664
  bytes. The actual images include clips, opaque fields, registries, tracks,
  occurrence metadata, shot items/media pins, and the unrelated closure; the
  helper omits those facts.
- Actual source history has `fork-edit-0` at command ordinal `[0]`
  (`occurrence.fork`) and `fork-edit-1` at command ordinal `[1]`
  (`doc.patch`). The helper invents a one-command history where `fork-edit-1`
  is ordinal `[0]`. Thus it does not exercise the actual source-step lookup or
  the complete retained history shape.
- The actual source materialization bindings carry the captured successor
  image digests (`sha256:e82ecc...` for the shot and
  `sha256:0fd72e...` for the internal image), while the helper hashes its
  invented payloads. Parent pin and sibling/unrelated closure topology are
  consequently not proven by the added test.

An independent in-memory probe did establish only the synthetic claim:
old `8592822fd` rejects the helper with
`inverse stage native writes do not cover its authenticated effect image`, and
the candidate accepts it. Comparing the helper's before/after images directly
to the actual package returned `False` for both. This is not evidence that the
candidate accepts the real captured first stage.

The eight negative parametrizations at lines 375-403 execute against the same
synthetic closure. They do not independently cover changing both an effect
image and its forged binding, or swapping equal-payload keys belonging to a
foreign owner. Those are required controls under the brief because payload
equality must not substitute for physical owner/provenance identity.

## Remaining actual failure and ownership

The durable package sections were independently inspected using these exact
hashes:

- `request`: `9513a98ac9413e4395632693701c664db3557c61e5ed150ca1875a4885e50b5b`
- `prepared`: `bd78bb8ffa030ccadddeebe62bec56ab9fa7623232c6e0c4d759523048d92afa`
- `history`: `0122a97346985a270f38b2e9f49819a28399f4f7faa3e9821622d85b2447897e`

The actual first leaf source step is the `fork-edit-1` `doc.patch` at ordinal
1, with native range `[0,1]`, effect range `[0,5]`, and the exact native write
that restores `params.text` to `hello`. The retained whole-undo request is in
`service-03-before.json`; it targets publication
`txn-1c5db05293e34736a5207e6f07c3818f` from parent revision
`authoring-parent-revision-3e2e0c9af5a5f9428f83b1f9e22589b6690dd943693bda102240e90a91447752`.

The durable refusal is `service-03-error.json`:

```text
type: RuntimeErrorBase
status: refused
reason: invalid_records
message: inverse stage native writes do not cover its authenticated effect image
conflicts: []
base/current: null
```

`service-03-after.json` shows the head and canonical document unchanged. The
existing Agent diagnosis identifies the later failing stage as `fork-edit-0`,
native range `[1,3]`, effect range `[5,9]`: Runtime's
`_inverse_stage_boundaries` aggregate/root sequential-image comparison still
fails after the leaf stage. Agent's captured prepared final canonical document
was exactly equal to the original, so the remaining source owner is the
Runtime inverse-stage boundary, not an Agent authored-field omission. The
smallest correction is a new bounded Runtime proof/handling for that exact
authenticated aggregate/root turnover, retaining all current sequential,
history, range, owner, pin, digest, effect-binding, and unrelated-closure
guards. No fabricated root writes, pin normalization, or guard relaxation is
authorized.

This evidence does not establish full undo or redo PASS.

## Checks run

Exact authorized targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_source_duplicate_authority.py
```

Result: **170 passed in 56.38s; 0 skips reported.** No full suite, browser,
native14, original20, P1-P4, or known-failing live retry was run.

```text
/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
All checks passed

PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python /root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py
0 errors, 0 warnings, 0 informations

git diff --check
passed
```

Pyright on the exact base production module also returned 0 diagnostics; the
candidate/base diagnostic identity delta is therefore zero. The preservation
check found no changed frozen/generated/pin path in the two-path candidate
diff; a separate 77-path manifest was not present in this leaf evidence
packet, so I do not claim a standalone 77-item comparison.

## Recommendation

Keep the candidate unmerged. Replace the compact helper with a lossless,
read-only test input derived from the retained package, prove old rejection and
candidate acceptance on that actual first stage, add the combined effect-image
plus-binding and equal-payload foreign-owner controls, then separately repair
and requalify the retained stage-2 aggregate/root failure before any whole
undo/redo claim.
