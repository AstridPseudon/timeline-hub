# ordinary014 current-preserving private pin review

Date: 2026-10-20 22:18 UTC

## Verdict

**APPROVE on the declared base for private staging only.** The reviewed
consumer pin is `c9b9e279f3677d47a9b4a98aabc69e47118ff06f`, tree
`8b6f266e1911d006ca478cc06716ee67dfa3dcc3`, whose parent is the declared
`81873ccf270e1c099c9f76b86103ccf3c9275cf4` (tree
`5164f267bb08eafc497ae19e081861eabec9bb67`). It is not an integration pin,
release, activation, or matching-server qualification.

The later `32ebd610016195c69e6eceb5fc7530dbbf634cb5` merge is a sibling of
the reviewed staging commit: both descend from 818. Its only source delta is
the parent-trim commit `9e42dd409c9122321c2cb8e8caff837cb0c35cf4`. Therefore
the old-base difference is a mechanical carry requirement, not evidence that
the ordinary014 pin dropped an assertion. A conflict-free three-way result of
the reviewed pin plus that carry has computed tree
`0fe8fa612ac7fb53094613696ab9875d8bf11415`.

## Exact producer and lock boundary

- Immutable Runtime producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Runtime package/release: `0.2.14`.
- Runtime wire schema digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Agent raw command schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  the current schema has 55 definitions and 29 operations and is byte-identical
  to the producer's `contract/schemas/edit-command.json`.
- Producer artifact version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`;
  the producer manifest is `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- `runtime.lock.json` contains 15 consumer paths. The normal check against the
  detached immutable producer passed, confirming all 15 bytes and manifest
  hashes match the approved f021 artifact. The lock names the full a0 source
  SHA and does not change the public 0.2.13 pin.

## Preservation review

The following current-main files are byte-identical between 818 and the
staged pin: restore/session behavior (`astrid/sdk/timeline/sync.py`, including
restore), retry/error identity (`astrid/sdk/workspace_client.py` and
`astrid/core/execution/generic_host.py`), canonical image/read fixes
(`astrid/sdk/timeline_filmstrip.py` and
`astrid/core/rendering/verified_source.py`), D10/rendering boundaries, the
filmstrip cache helper, and the sheet/cut-owner plus Gate3 assertion files.
The 4095 restore/cache lineage and D10 lineage remain ancestors of the staged
commit. No production private392, materialization, group, or new-field source
was reviewed or added; the only name-level scan hit is the scoped
`test_grouped_clip_cache_inverse.py` test, which remains outside this review.

The staged source preserves the prior producer evidence: the earlier review
records 350 passed / 54 skipped for the ordinary source/facade/history lane
and 165 passed / 9 skipped for sheet, restore recovery, accepted history, and
publication retry. Those lanes were reused, not rerun here. No generator,
wheel, TypeScript, full, live, browser, or registered-render repeat was run.

## Required 32eb carry

Carry exactly the four paths from `9e42dd409` onto the staged pin:

1. `astrid/sdk/timeline/checkout.py`
2. `astrid/sdk/timeline/native_checkout.py`
3. `tests/editing_conformance/test_owned_move_publish_runtime.py`
4. `tests/sdk/test_timeline_owned_move_publish.py`

This is the later approved parent-trim support: selector validation, trim
capture/publish, stale rebase, lost-ack/restart exact retry, and guarded undo
coverage. The 32eb diff from 818 contains exactly these four paths (151 added,
5 removed); there is no other later-base carry to apply. The computed final
tree above has only these four paths changed relative to the staged tree.

## Checks run

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
  scripts/vendor_lock.py check runtime.lock.json \
  --producer /home/user/work/wt/rt-pin-a0dca169
PASS: ok runtime.lock.json (matches producer manifest)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider tests/test_vendor_lock.py \
  tests/stage1/test_vendored_workspace_client_parity_luna.py \
  tests/sdk/test_timeline_current_union_schema.py
PASS: 63 passed in 187.38s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python <client export/DTO identity probe>
PASS: 7/7 new public DTO exports identity-match their DTO module and are in __all__

git diff --check 81873ccf2 HEAD
git diff --check 81873ccf2 32ebd6100
PASS
```

The actual matching server and hold-clear failed-node handoff were not
provided, so no live-node result is claimed. Do not promote, release, or
integrate until the four mechanical carry paths are applied and the owning
manager supplies that separate server evidence.
