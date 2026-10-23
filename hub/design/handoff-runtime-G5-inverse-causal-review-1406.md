# G5 inverse causal review — independent Runtime review

## Verdict: PASS (diagnosis and evidence publication)

This is a report-only review; it is NEVERMERGE. No Runtime, Agent, test,
contract, generated, client, pin, config, environment, or Git source was
changed. The product behavior remains unqualified: the captured inverse is
refused and undo/redo/overlap behavior after that refusal was not rerun.

## Confirmed causal boundary

The exact captured pair is Agent commit `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`
(tree `ac1251cdc911b99d690d303cdd777fe14643bdb1`) and Runtime commit
`8592822fd11275540f596562f43c715676f2bc0f` (tree
`ed9856f43a4e44a058bf2230badea2c4c7080050`). The original target function
body hash is `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`
(6,798 bytes, function source plus terminal newline), as recorded in the
packet manifest and independently recomputed from the Agent checkout.

The captured public request is the normal full-v2 inverse request:

```text
base_publication_id = txn-17252a1958a443a2878f1cb4ed4d9631
base_revision_id   = authoring-parent-revision-caa332ccab292835ea80593b7a68c576fd0ae6f75c1953ccec15ff6b207551b0
command            = timeline.inverse(publications=[txn-17252a1958a443a2878f1cb4ed4d9631])
label              = Undo timeline edit
merge              = fields
dry_run            = false
project/timeline   = c565d65f3d344392b8f87bf14ad5bbf5 / t
source             = {via: python}
step               = inverse, command_ordinals [0], empty patch/tags/intent
```

The prepared record has one `inverse.stage` binding for the accepted source
publication and `restructure-0` step, with:

```text
native_write_range = [0, 10]
effect_range       = [0, 9]
```

The full captured native-write order is:

```text
0 parent/config
1 parent/registry
2 parent/clips
3 parent/occurrences
4 occurrence:chapter-shot-3f756cd1547d015ebd4b-occ (root removal)
5 occurrence:occ-film (root replacement)
6 occurrence:chapter-shot-837324ae5797370162ac-occ (root removal)
7 shot:film (root replacement)
8 shot:chapter-shot-837324ae5797370162ac (root removal)
9 shot:chapter-shot-3f756cd1547d015ebd4b (root removal)
```

The nine authenticated effect ordinals cover the corresponding accepted
inverse transition: internal revision creation, shot revision creation,
parent aggregate transition, removal of the two chapter revisions and the
old film revision, and removal of the three old internal revisions. The
prepared canonical document's accepted `parent_revision` is
`authoring-parent-revision-a58d0cd6e1a5a5575703abc0ce74423136bcda4d2f52473b1ee9508f06e1582c`,
whose `config` digest is the split image
`sha256:3261318905a6bb014857b56b1705960454c99ae9b3e7266dd898cb4867f56115`.

The first native write is instead:

```text
ref/path       = parent / ["config"]
before digest  = sha256:e6d3e22782252ab1f325c0013214ad30cd9669bcae8b7502321717371fbff4a9
after digest   = sha256:3261318905a6bb014857b56b1705960454c99ae9b3e7266dd898cb4867f56115
```

Runtime’s `_inverse_stage_boundaries` begins `native_image` from the accepted
split input and checks every native write sequentially. At the first write,
the observed `parent/config` is the split `3261` image, but the Agent claim’s
`before` is the flat `e6d3` image. Runtime’s refusal at
`runtime_protocol/timeline_commit_auth.py:958` in Runtime859 is therefore
correct: `CommitRejected: inverse stage write differs from its sequential input`.
The seam packet shows this came from `RequestCommitPort.accept` during store
validation, propagated through `provider.commit` and `coordinator.execute`;
port verification was not reached, and `port.close` completed normally.

## Owner determination

The owner is Agent inverse-stage preparation, not Runtime authentication.
Agent `astrid/sdk/timeline/inverse.py` constructs each stage from the current
accepted bundle, restores authored writes through `_restore_write`, and emits
the native range. Agent `_commit_patch.py` then derives effect ranges from the
stage transitions and appends `commit.effect` bindings. Those source paths
explain the exact mismatch: the stage boundary is the accepted split image,
but the first recorded native capture claims the earlier flat config as its
sequential input. The next repair should correct Agent stage capture/orientation
for the restructure inverse; Runtime should not waive or reorder this check.

The current integration head cfa0af0d4 includes the separately reviewed R2r
leaf patch. Source inspection shows that patch adds authenticated physical
materialization/root-turnover handling and defers root checks; it does not
change the non-root `parent/config` sequential-input check (now at line 971).
It does not alter this causal diagnosis and was not replayed.

This concrete current refusal must not be generalized to the historical public
503. The packet diagnoses only this captured `422`-class refusal; it does not
establish the historical 503’s underlying cause.

## Evidence publication and checks

The original packet and manifest were copied without rewriting to:

- `design/runtime-G5-inverse-1358-01ccdec35f2a8f3e.json`
- `design/runtime-G5-inverse-1358-01ccdec35f2a8f3e.manifest.json`

Both destination files compare byte-for-byte with the worker evidence.
Packet SHA-256 is
`01ccdec35f2a8f3e72e99541092f99ec20bda2de036adc6fe77d7f773157aaeb`;
manifest SHA-256 is
`f5a2134b05546af296693d9e1a4ddf65e3f29ab8dc2d377fb87c811835597e48`.
The original manifest records 166 events, clean credential scan, equal JSON
round-trip, and the required packet SHA-256.

Read-only checks run for this review:

- AST body-hash recomputation: required `c2711a2d...` matched.
- Runtime859 and Agent91ac source identity/tree and captured module hashes:
  matched the packet origins.
- Runtime digest recomputation for the first write: `e6d3` before and `3261`
  after matched the captured values; range/order inspection passed.
- `cmp` of both published files against the original evidence: passed.
- `git diff --check`: passed; assigned Runtime worktree remained clean.
- Typecheck: N/A; this was a read-only evidence/source review.
- No product test, service rerun, body rerun, full suite, browser, socket,
  or historical-503 replay was run, so no product-test credit is claimed.

Recommended next step: hand the exact published packet and the
`parent/config` first-write capture to the Agent inverse-stage owner for a
narrow correction and then requalify the original behavior on a fresh,
reviewed Agent/Runtime pair.
