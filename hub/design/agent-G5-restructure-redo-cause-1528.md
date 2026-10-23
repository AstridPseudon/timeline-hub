# agt-G5-restructure-redo-cause-1528

## Result

G5 remains **FAIL / P1 NO-GO** at the existing public inverse boundary. No
product, test, schema, client, pin, or dependency change was made, and no new
offline reproducer was added.

The retained Runtime1456 qualification is sufficient to preserve the existing
ownership split:

- Agent `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`, tree
  `ac1251cdc911b99d690d303cdd777fe14643bdb1`; Runtime
  `9ce4242bc01f100bab9efc51032a73985cefb2b2`, tree
  `92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`.
- The unchanged public target body is 6,798 bytes,
  SHA-256 `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
- Preflight: **2 passed in 24.16s**.
- Original public body: **1 failed in 11.56s**. Forward restructure and whole
  undo were accepted; redo returned `conflict / original authored guard
  changed` before the redo assertions.
- The later overlap refusal, post-redo canonical/history/SQL no-write equality,
  and historical 503 behavior remain unverified.

## Precise source/ownership finding

The independent 1505 correction is authoritative. The completed uninstrumented
trace ends at Agent `astrid/sdk/timeline/sync.py:558`, where the returned
structured error is converted to `CommitConflict`. It does not retain the redo
request body, provider traceback, or the returned guard's `ref`, `path`, `base`,
and `theirs` values.

`astrid/sdk/timeline/_recording.py:286` is only a static candidate because it
contains the same message and is called by inverse code. It is not an observed
redo throw site. `_check_reservations` is likewise not the owner established by
the evidence: its only retained occurrence is in the excluded timed-out
forward observer (`commit.py:_check_reservations -> Runtime revision_closure`),
not the completed redo. Static source shows `_check_reservations` scans
authenticated history/reservations and does not call `recording.guard`.

Runtime `9ce4242` production sources contain no matching `original authored
guard changed` text; the only Runtime match is an existing test assertion for
an Agent provider conflict. Therefore there is no evidence for a Runtime auth
defect and no basis to attribute the redo dynamically to `_recording.py:286`,
`_check_reservations`, or the separate R2 nested `3a718...` packet.

The Runtime9ce physical occurrence-order correction remains the passing
forward/whole-undo seam. The R2 `a29df...` / nested `3a718...` evidence is a
separate Agent native-stage correspondence investigation and must not be
treated as a common cause for this G5 public redo result.

## Current-draft preservation checks

Current worker HEAD is `f57d283d2d4946bbb09d7b68da89422f2d3bfd77`, tree
`fb4385a20361ab4af88d5baa92a3517da5faa56a`. The target public test file is
byte-equal to Agent `91ac`; AST extraction of the target function again gives
6,798 bytes and SHA-256 `c2711a2d...`. Relevant protected current blobs are:

- `_recording.py` Git blob `10b17db43964ed0016e3d0527910bc9e56ccaf4f`;
- `inverse.py` Git blob `6385c8c3caa9761059d766b6487c967463736fb9`;
- `_root_inverse.py` Git blob `5d2a1165c96e140482b427da0f3e26f06071f080`;
- guarded restructure test Git blob
  `9accc758deb59fc69c614f2e433c8f8cd00cfc27`.

The worktree remained clean. No known-failed public redo was rerun.

## Exact commands and results

All commands were read-only and run from
`/home/user/work/wt/agt-G5-restructure-redo-cause-1528` unless stated:

```text
sed -n '1,240p' /tmp/.../scratchpad/orch/PLAN.md
  PASS: authoritative plan read.

sed/find/rg over the scratchpad, current Agent tree, and retained design files
  PASS: 1456 handoff, manifest, 1505 correction, original c271 body/report,
  and related R2 reports located and read.

python3 AST hash extraction of
tests/sdk/test_timeline_restructure_guarded_runtime.py
  PASS: target function 6798 bytes; SHA-256 c2711a2d...

git diff --quiet 91ac... -- tests/sdk/test_timeline_restructure_guarded_runtime.py
  PASS: target test file unchanged.

rg -n 'guard\(|_check_reservations\(|original authored guard changed|CommitConflict'
  PASS: static call graph confirms candidate guard and separate reservation scan.

git -C /home/user/banodoco/banodoco-workspace-runtime grep -n -F
'original authored guard changed' 9ce... -- ':!*.json'
  PASS: only Runtime test assertion matches; no production Runtime match.

git status --short
  PASS: clean.
```

No pytest, full suite, browser, socket, or original known-failed redo run was
made; this was intentionally limited to initial source/fixture analysis.

Retained handoff hashes:

- `handoff-runtime-G5-native-order-public-1456.md`:
  `b2bc94ba97e3973e03a69cdd9fa81ab69f5e9cf23db61f5a9f095e738792667c`;
- its manifest:
  `f520f050081c7db98a20a8cde33547fedca74495a7dcf9e0734983de07658814`;
- independent evidence correction:
  `885e7545c4a3e0a6da379bc6664d5e831498b95b929c49be03d1dfc1a0cc887c`.

## Exact missing input / next owner

The next reviewed Agent/R2 owner needs one fresh, bounded reproduction that
retains the complete redo request and returned error envelope, including exact
guard `ref`, `path`, `base`, and `theirs`, plus provider traceback/source
identity. It must also retain pre/post canonical document, accepted history,
physical bindings, and no-write state before validation. Until that exists,
the correct disposition is handback for source capture, not a Runtime patch,
guard relaxation, public-schema change, or test change.
