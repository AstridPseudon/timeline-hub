# Agent review: Runtime RT08 private carrier final pair

Date: 2026-10-20

## Result

**REQUESTCHANGES.** Native qualification, public release, pin/freeze, and artifact authority remain HELD.

The reviewed Runtime source is commit `5f22672153253ea11cf35f92590c408ea7bba556`,
tree `e40f0108feea6c681b10d607ae4b1ed198c4e908`, parent
`ade60f3225aa3b6b6db1aee683bc33e09084a4fa`. The requested current safety base is
`388eff42a644aeafa5d4605d0bb235e1ca849741`, tree
`708df14c75ef739a2c6130ca39f9e67b2758a571`; the reviewed secondary-ID source is
`ade60f3225aa3b6b6db1aee683bc33e09084a4fa`, tree
`06a68e47968f1c64774e05608e004d8edbf7ca65`. The final branch's merge base with
`388eff4` is only `2cb9bb62c88d91fdab03df230ef0b2a3bd81f513`, so this is not a
composition based on the stated `388eff4` head.

The Agent counterpart reviewed here is the exact approved source commit
`3730d0bd51686a1692450359482205df64dcc839`, tree
`3892a10bcffa9bf520b4c79591637cf3259d6724`, with private command-schema SHA-256
`f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`.

## Blocking findings

### 1. The final tree drops the `b748`/`388` safety tests

Compared with the required `388eff4` safety base, the final tree deletes:

- `tests/qualify_absent_head_repair.py`
- `tests/test_timeline_absent_head_repair_integration.py`
- `tests/test_timeline_fresh_bootstrap_scope.py`

The `runtime_protocol/service.py` bytes are equal to `388eff4`, and the
headless-authored-content guard is present, but deleting the regression and
integration controls is not acceptable under the no-test-weakening rule and
does not establish preservation of orphan/hidden-shell safety in the final
tree. Restore those tests (or an exactly equivalent, non-weakened set) and
produce a successor actually based on `388eff4`/current integration. Keep the
strict empty-shell controls from `b748ae7` as well.

### 2. The unapproved staging-ownership xfail is still present and hides a write

`tests/test_timeline_projection_ownership.py:315-327` marks
`test_frozen_artifact_does_not_yet_carry_typed_item_creation_claims` as a
strict xfail. Running that exact test with `--runxfail` on the reviewed tree
fails because the candidate reaches `_persist_closure`; the test's tripwire
reports `projection preflight wrote a revision`. It does not produce the
required public-schema refusal.

Replace this xfail with the corrected public-schema refusal control, retaining
the original assertion that the public artifact refuses the typed item claim
atomically and without writes. Add the equivalent typed positive against the
private matched schema/resource, with its original success assertion intact.
Do not use an xfail, skip, weakened expectation, or a private-schema test in
place of the public negative.

## What was verified

The exact branch's offline join lane passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/rt08-counterpart-review.cEIGge \
  /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/rt08-counterpart-review-pytest-join \
  tests/test_timeline_materialization_join.py
115 passed in 66.34s
```

The xfail control showed the problem above:

```text
... pytest ... tests/test_timeline_projection_ownership.py::test_frozen_artifact_does_not_yet_carry_typed_item_creation_claims -rxX
1 xfailed
... same node with --runxfail ...
1 failed: projection preflight wrote a revision
```

The worker's recorded bounded evidence was also read: 210 passed, 3 deselected,
1 strict xfailed in its four-file lane; the central occupancy request reported
18 passed and 17 deselected; artifact-manifest, private-bundle equality, and
compatibility checks passed. These do not override the two blockers above, and
no full/native/browser suite was run for this review.

The composed private artifacts have these exact hashes:

| Path | SHA-256 |
| --- | --- |
| `runtime_protocol/timeline_commit_port.py` | `28968f683c064af54da4b767618880781a6ec66e80586d462b8b7e2b1f96ee86` |
| `runtime_protocol/timeline_commit_store.py` | `11252cf2cb3dc5c8fc83cb447d238cd3f7b64a4051ecd1b6086444555fa278a2` |
| `runtime_protocol/timeline_materialization.py` | `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb` |
| `runtime_protocol/service.py` | `e006d1d2096bda9eac6a32ad099113dfe3e9e0ca75b76d69e9407ebdb7c6c1f3` |
| `runtime_protocol/schemas/timeline-commit-bundle.json` | `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425` |
| `contract/schemas/edit-command.json` | `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f` |
| `contract/artifacts.json` | `9e5915b912b4fb49ff7cca2bc4d43c25473a55a9a5198b562f5276058032dc62` |

Static inspection confirms the intended private path keeps version out of
authority, retains the source/owner join and authenticated own-slot checks, and
does not add a DTO or caller-authority escape. Those findings are not an
approval while the final tree is stale relative to `388` and the public-schema
negative is hidden by xfail.

## Required next step

Recompose the counterpart from current Runtime integration including the
`b748`/`388` safety tests, correct the public-schema negative plus private typed
positive, remove the new xfail, rerun the bounded Runtime tests, and request a
fresh Agent review. Native lifecycle proof/public release stays held even after
source review until the normal matched private pair proves ledger-first accepted
v1 retry/undo/redo, restart, own-slot/global-item occupancy, and draft
preservation.
