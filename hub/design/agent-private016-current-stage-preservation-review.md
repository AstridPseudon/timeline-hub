# Agent PRIVATE016 current-source preservation review

Date: 2026-10-21

## Verdict

**REQUEST CHANGES before private pin.** The source-only merge preserves the frozen
PRIVATE016 schema and the reviewed current-source behavior, but it does not
preserve the required current public014/Runtime95 lock, generated-client, and
artifact bytes. Composition C13's package-lock is unchanged. The stage is not
an approved private artifact tuple and this review did not generate or pin one.

## Exact identity

The reviewed commit is `13a9d375be2a56842040984a78631957e7b7100d`, resolved tree
`a6edb7b7349f5b6e77c5aeec7a235b199dbc7432`, with parents:

- frozen source `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree
  `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`;
- current public parent `a08a500077c7551fa8455b936d82adc2aae08f41`.

The raw command schema remains SHA-256
`9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`, canonical
schema `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`,
with 65 definitions and 37 closed clauses. The public parent remains the
ordinary 55-definition/29-clause floor.

## Source-preservation findings

- WC8 author-time basis is present. Of the six qualified paths, checkout,
  `timeline_sheet.py`, and all three focused tests are byte-identical to the
  current public parent. `astrid/packs/timeline/cli.py` has an intentional
  private overlay, but its `_cmd_apply` hunk carries the current retained-sheet
  dispatch and client-aware `apply_sheet` path; it is not a stale full-file
  rollback. Stage blobs: CLI `efa312d…` / SHA-256 `b1727a…`, checkout
  `85aadb1…` / `9d17b60…`, sheet `f41ae27…` / `4cd51a…`, ordinary test
  `5b90ca2…` / `7ea0a2…`, CLI test `27e6bf6…` / `b48b81…`, native test
  `9bc70af…` / `7761fe…`.
- Scene relocation is an exact `R100`: `astrid/core/timeline/scene_answers.py`
  to `astrid/core/rendering/scene_answers.py`, blob `478e7b4c…`. The rendering
  imports in `composed_frame.py` and `scene_only.py` were updated, and no old
  `astrid.core.timeline.scene_answers` import remains in `astrid` or `tests`.
- Revision-read behavior is preserved by the narrowed
  `AuthoringBundleError`/`KeyError`/`TypeError` conversion to `protocol_error`,
  with the corrupt-closure test added in
  `tests/sdk/test_authoring_revision_diff.py`.
- `astrid/sdk/timeline/inverse.py` is not changed by the stage. Existing
  accepted-history, intervening-write, and exact-boundary guards remain in the
  source; no inverse behavior was removed.
- Architecture/documentation and the Ruff baseline are current-parent
  identical (`docs/architecture/timeline.md` blob `d193a2d…`, timeline document
  helper `9228238…`, Ruff baseline `c982ca1…`). The artifact manifest check
  reports `artifacts.json is current`.
- The stage test diff adds coverage and changes no `skip`, `xfail`, `pytestmark`,
  or `it.fails` marker. The source worker's recorded targeted evidence is 79
  passed / 83 collected and scene dispatch 2 passed / 2 skipped. I did not
  repeat the prohibited broad 186/44 run.

## Concrete byte-preservation issue

The manager brief requires immutable public014/Runtime95/C13 lock/client bytes,
but the stage resolved the first (frozen) parent for the Agent/Runtime-facing
files:

| file | stage / frozen SHA-256 | current public parent SHA-256 | stage identity |
| --- | --- | --- | --- |
| `runtime.lock.json` | `07c7be…` | `920f4a…` | source `c3d26567…`, producer `2df8eb…` |
| `astrid_runtime_client/contract_metadata.py` | `40d329…` | `cdedeb…` | contract `0.2.15` vs `0.2.14` |
| `astrid_runtime_client/generated.py` | `61b55a…` | `e2e66b…` | frozen private client vs public Runtime95 client |
| `astrid_runtime_client/timeline_commit_types.py` | `f33a50…` | `4b23c4…` | frozen private vs public generated types |
| `artifacts.json` | `6aa137…` | `81ed2c…` | frozen private manifest vs public manifest |
| `remotion/package-lock.json` (C13) | `c4d703…` | `c4d703…` | preserved |

This is not a claim that a private016 generated tuple should be created here;
generation remains out of scope. The source stage needs an explicit later
reconciliation to the required public bytes, or an orchestrator-approved
exception, before pinning.

## Separate required merge-forward

The current public `document_diff` fix is not in this stage. Stage
`astrid/sdk/timeline/document_diff.py` is blob `12af6f766…`; the separate fix
commit `aba0346aec2ea15c80cd9ea2cc850c75081594b8` changes it to blob
`90a03299d…` and adds the corresponding feedback tests. The fix is not an
ancestor of this stage (`git merge-base --is-ancestor` exit 1). It must be
merged forward and reviewed **before** the private pin if it is still not an
ancestor at pin time. I do not claim that this stage contains that future hunk.

## Circular direct import

Using the exact-scope probe from `/tmp` with the stage or current integration
root and the matched Runtime source on `PYTHONPATH`:

```text
astrid.sdk.timeline.checkout  FAIL ImportError: cannot import name 'Checkout' from partially initialized module 'astrid.sdk.timeline.checkout'
astrid.sdk.timeline_sheet      PASS
```

The five relevant blobs (`checkout.py`, `timeline_sheet.py`, legacy
`timeline_checkout.py`, `timeline/__init__.py`, and `timeline/store.py`) are
identical between stage and current integration. This is therefore a known
pre-existing circular direct-import issue, not a stage-only regression; it is
reported rather than silenced. The normal sheet import remains available.

## Checks and limits

Checks run directly against this clean stage:

- `git diff --check 10226a7f08a739ba3e41f8e91de6971eed63aa9d HEAD` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/artifact_manifest.py --check` —
  PASS (`artifacts.json is current`).
- Exact direct-import probe above — circular `checkout` failure reproduced on
  both stage and current integration; `timeline_sheet` passed on both.

No code was edited. No native, renderer, generation, installation, pin,
outer/HTTP workflow, or full suite was run. The 79/83 and 2-pass/2-skip counts
are historical evidence from the stage worker, not a new qualification run.

## Required next steps

1. Reconcile or explicitly disposition the public014/Runtime95 lock, generated
   client, and `artifacts.json` byte mismatch; do not pin while this remains
   ambiguous.
2. Merge-forward `aba0346aec2ea15c80cd9ea2cc850c75081594b8` and its tests before
   the private pin if it is not already an ancestor.
3. Track the direct `timeline.checkout` circular import as a separate fix or
   accepted limitation, then complete the independent Runtime/Agent reciprocal
   artifact review and matched proof under the orchestrator's existing gates.
