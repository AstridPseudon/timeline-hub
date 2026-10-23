# R2 independent Runtime review — PASS

Exact reviewed source: `8ea0766f5e9fb23cea26c7398770a8aaac06b258`
(tree `6047ac3033c3594b8f83db3afd8bb2c47cafa6d6`); base
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`
(tree `f79a2355cfb39d9ada7721978bd20d5702105778`).

## Result

PASS for the narrow R2 native occurrence-order projection review. This is a
targeted/source PASS only, not a product-semantic, full-suite, or integrated
journey qualification.

The diff is exactly three authorized files: `runtime_protocol/timeline_commit_auth.py`,
the focused regression file, and the 145,292-byte finite fixture. No
coordinator/store/schema/contract/generated/client/frozen-pin or unrelated
file changed.

## Causality and artifacts

The valid original 85-member archive hash is
`a8dcf1d1fe6c2ce6905749ea11fe96057b421f7497c0e233c13ca1e0182bc3d4`.
Exact member `./run/cases/060-port-prepared.json` is
`58051ef4e6e23f717c07fdce2d12e8d2b74caa106eb8422fe6e1c604c34f9d4d`.
The retained fixture is
`50d9e08be8efa3e9f4d1d789ab99fd2c76d7e92bbeacfba543f65d2a331145c0`.
Fixture request/prepared compare equal to exact 060. History is only the
prepared `records.undo_of` entry; no claims/history/records rewrite occurred.

The exact retained order write has three authored rows without
`shot_revision_id`; the authenticated physical closure has the same three
occurrence IDs with three physical shot pins. The observed discrepancy is
therefore only the three physical `shot_revision_id` values, not a missing
Agent materialization.

Old-source control in an isolated TMPDIR overlay: **1 failed, 140 deselected**
with the original refusal `inverse stage native writes do not cover its
authenticated effect image`. Candidate result: **141 passed**. This establishes
oldRED/newGREEN without mutating the real repository.

## Authenticated behavior

The new branch is reachable inside `_inverse_stage_boundaries` from the
existing `validate` function. It is scoped exactly to parent occurrence
collection writes. Existing sequential input authentication runs first. The
branch requires a present collection and same-size unique occurrence IDs with
each after row equal to its authored before row, then reorders deep copies of
the already-authenticated physical rows. Thus authored owner/shot/internal
references and all authored bytes/unknown fields are preserved while physical
pins remain source-authenticated.

The 23 negative cases refuse losslessly: duplicate, missing, foreign,
changed shot/owner, injected pin, changed payload/unknown field,
malformed/absent, nonpermutation/order, physical-pin tamper/swap,
internal-pin tamper, effect before/after/coverage, native/effect range tamper,
and missing/foreign/tampered source history. Nine assert the new permutation
guard. Existing before/native-effect/range/history/root/managed-edge guards
remain in the unchanged surrounding validator; no arbitrary stage copy,
equal-bytes alias, invented materialization, or source exemption was added.

The production caller is live in the existing Runtime store:
historical replay calls `validate` at `timeline_commit_store.py:245-269`;
normal `_validate` calls it at `timeline_commit_store.py:867-881`, before
acceptance/reference projection.

## Commands

- Required focused suite: **141 passed in 48.86s**, exit 0.
- Old-source causal control: **1 failed, 140 deselected**, expected RED.
- Ruff on both changed Python files: PASS.
- In-memory compile of both changed Python files: PASS.
- `git diff --check`: PASS.
- AST comparison: only the three intended new fixture/test definitions;
  existing test bodies/assertions/markers unchanged.

Changed-file hashes:
`runtime_protocol/timeline_commit_auth.py`:
`ecc0149ed0c9e93bac5365ca7ab97f5a85a80b2fe3acb6a962b7ecc635c08872`;
`tests/test_timeline_inverse_stage_authentication.py`:
`c5b44e6d11209385cbf85af4cfa7114802d2ab5e8e7b8712f9ec0a8d14fc155b`;
fixture:
`50d9e08be8efa3e9f4d1d789ab99fd2c76d7e92bbeacfba543f65d2a331145c0`.

## Limits and next step

No full/socket/browser/live-HTTP suite, c271/SDK FOUR body, public undo/redo,
or integrated cross-repo proof ran. The denied Luna2017 publication and copied
report were excluded. The worker tmpdir pointer initially rejected a mkdir
(`.../tmpdir: Not a directory`); its declared TMPDIR was then used, with no
product impact.

Recommended disposition: normal own-commit-only merge, then one focused
integrated proof. No extra provider approval gate is indicated.

