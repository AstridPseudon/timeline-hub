# Agent PRIVATE017 placement two-failure diagnosis

Date: 2026-10-21 UTC

## Disposition

The second failure is a new test oracle defect, not loss of accepted source or
owner authority. `bundle_from_document` produces a fresh authoring projection
from the current canonical document. After materialization, that document's
physical destination is `D`, so the derived `source_mapping.shots[D]` correctly
has `shot_id == D`. The accepted record remains the authority for the original
source `S` and owner `O`.

I made the bounded test-only correction in
`tests/editing_conformance/test_commit_runtime_identity.py`: reload now compares
the derived source entry one-for-one with the pure
`bundle_from_document(document_from_bundle(expected.bundle))` projection, and
asserts the projected shot identity is `D` with the verified empty item map.
The existing accepted-history assertions for `S`, `item_id_map == {}`, and
`materialization.owner:D -> occurrence:occurrence-1` remain unchanged.
No product, Runtime, schema, DTO, store, authority, pin, fixture, or public
metadata was changed.

## Exact identities

- Agent HEAD/source before this uncommitted test correction:
  `95e1ada1953d40710039d8e70525387cc64d065b`, tree
  `50cb3fcaf0a2ece1c0d320f5cca7948b32eac92f`.
- Base `tl/agt-review-private017-placement-oracle-fixed-one-proof-1036` is the
  same commit/tree.
- Runtime checkout used by the preserved native result:
  `/home/user/work/wt/rt-pin-42a7203f`, commit
  `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`.
- Agent `astrid/core/timeline/schema/edit-command.schema.json` and Runtime
  `contract/schemas/edit-command.json` are byte-identical:
  `sha256:6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`.
- Agent `runtime.lock.json` SHA-256:
  `a9046ae72a4ee1ff9cb7e8062f301d599803f826eb6f2dbb025e7cc5b1d27a6c`.
  Runtime `contract/artifacts.json` SHA-256:
  `0c0e3379302f5ded0bef96d9a5c7d7e72a29962d83bbb5b1500c0cfd7344e06f`.
  Both identify producer version
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.

## Fixture and provenance facts

The identity fixture starts with two occurrences sharing original source shot
`S = shot-1`. The new placement command materializes occurrence-1 into
`D = shot-placement-271ff5ac6e7f5c9457f24655a71debca8383cec79839f3a52381233be3abb738`.
The captured identity source has no shot items, so its source pin has
`item_id_map == {}`; this proof is shot-only and the global/item allocation gap
is explicitly retained.

At accepted admission, the record contains the source dependency
`materialization.source:shot:D` with `kind == entity`, `policy == exact`, and a
complete parent/source pin whose source shot is `S`. Its owner binding is
`materialization.owner:shot:D -> occurrence:occurrence-1`, policy `fixed`,
dependent on that source dependency. The accepted response/readback has
occurrence-1 physically at `D`, the edited clip at `0.5`, and the expected
shot-only map `{shot:D: D}`. The receipt/history therefore retains S/I
authority while the canonical film/image retains D/O physical placement.

Runtime's own-slot contract confirms this separation. Its materialization join
returns `D -> (O, original pin)`, checks the captured closure edge `O -> S`,
checks the exact source/revision/internal digests and original item membership,
checks the pre- and post-commit physical edges, and validates the flat map. It
does not require the later authoring projection to repeat the historical source
pin.

After restart, `bundle_from_document` receives only the accepted canonical
document. `open_authoring_bundle` derives each source entry from the document's
current occurrence edge and child image. Since D is now the current physical
shot for occurrence-1, the fresh derived entry is `source_mapping.shots[D]`
with `shot_id == D` and `item_id_map == {}`. It has no history argument and
cannot legitimately reconstruct S from the receipt. Comparing this field to
the accepted dependency pin was therefore the wrong assumption. The corrected
assertion compares it to the pure document-to-bundle projection while the
history assertions continue to check S.

Relevant live callers of this projection are Agent commit `_load` (the normal
Runtime closure load), `TimelineCommitProvider.capture_candidate_inputs` and
`project_capture`, source-closure recovery in `_materialization.source_bundle`,
exact source restoration in `_command_state`, and the explicit group migration
builder. None of these callers treat `source_mapping` as accepted history;
materialization recovery uses the recorded dependency and authenticated
closures.

## First and second failures

- Central result
  `.../tests/agt-m2-gate1-private017-native-materialization-small-proof-1014-private017-placement-one42a-integration-1021102411-25065`:
  failed before admission at `next(iter(item_id_map.values()))` because the
  identity fixture's item map is empty. This remains a real global/item fixture
  gap, not a product success, and was not erased.
- Preserved one authorized follow-up
  `.../tests/agt-review-private017-placement-oracle-fixed-one-proof-1036-private017-placement-one42a-integration-1021103708-3710`:
  exact source tree `50cb3fcaf0a2ece1c0d320f5cca7948b32eac92f`; accepted and
  read back successfully, then failed only at the reload assertion with
  expected `shot-1` and observed `D`.

The second result is not evidence of authority loss. Because the failure
stopped before own-slot reuse, inverse, and ledger-first retry assertions ran,
those requirements remain required and unqualified by this diagnosis. The
unrelated-occupancy refusal, canonical film/image preservation, strict source
pin/history, and existing inverse/retry requirements remain in place.

## Checks

Passed after the test-only correction:

- `git diff --check`.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_commit_runtime_identity.py`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_materialization_version_boundary.py tests/editing_conformance/test_materialization_map.py` — **66 passed in 17.56s**.

An initial run of the same pure command without the Runtime checkout on
`PYTHONPATH` failed collection with `ModuleNotFoundError: runtime_protocol`; it
was immediately corrected and did not execute tests.

Not run, by instruction: any native/integration test body, HTTP/socket/body
run, retry, repeated 66/76 controls, full or full* suite, browser/render, or
third native attempt. The preserved 25065/3710 central results are historical
evidence, not reruns in this worktree.

## Readiness and blocker

The derived-metadata oracle is now minimally corrected and the source/history
diagnosis is complete. No product fix is proposed. The placement lifecycle is
not qualified here: the only authorized native follow-up stopped at the now-
diagnosed reload oracle, and the task authorizes no third native run. An
orchestrator-authorized future run may proceed from this corrected test; it must
still prove own-slot reuse, unrelated occupancy, inverse/restore, and
ledger-first exact retry, while keeping the global/item gap explicit.
