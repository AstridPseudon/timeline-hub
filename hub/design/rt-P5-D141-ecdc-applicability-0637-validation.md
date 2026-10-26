# Validation record

Read-only validation completed 2026-10-26 UTC. No test or product command was
run.

## Git identity and exact successor delta

```text
git -C /home/user/work/agent show -s --format='commit=%H%n tree=%T%n parents=%P%n subject=%s' 8585ed9c0404d0187b2ce70242d25114a32747c2
commit=8585ed9c0404d0187b2ce70242d25114a32747c2
tree=92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c
parents=28e56cacb42d3da85b02e5b3543895b44f3d0f70 5d202569f3af3852476d182ff49683787bb1e881
subject=Merge tl/agt-U2-D141m-upstream-merge-sol-0408

git -C /home/user/work/agent show -s --format='commit=%H%n tree=%T%n parents=%P%n subject=%s' ecdc242ed9b673f641759ecf029f95e89a2c6f92
commit=ecdc242ed9b673f641759ecf029f95e89a2c6f92
tree=d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735
parents=432f9dcbc66fb80b539d9ef709a63ef8065dbc92 00ec0f2f841401b69dad26fb1b23d31cce11efab
subject=Merge tl/rt-U4a-D141-host-receiving-review-0549

git -C /home/user/work/agent diff --name-status 8585ed9c0404d0187b2ce70242d25114a32747c2 ecdc242ed9b673f641759ecf029f95e89a2c6f92
M  runtime.lock.json
M  tests/timeline/test_authoring_feedback.py
M  tests/timeline/test_authoring_media.py
```

`git diff --stat` returned `3 files changed, 3 insertions(+), 3 deletions(-)`.
The exact diff was read with `git diff --unified=80`; the two test changes are
only `_bundle` → `_capture_bundle`, and the lock change is only the source
pointer.

## Runtime and Composition identities

```text
git -C /home/user/work/runtime show -s --format='%H %T %P %s' 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d
6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d ac5b862744bece65b2e30565db1777bacd60da28 0ca306dfd3cf4e21976271cc4b2e779b10e025b0 24107e83b096264e59f64ed5bd65e00650567f22 Merge tl/rt-U1-D141-final-join-2345

git -C /home/user/work/runtime show -s --format='%H %T %P %s' 95d98f038320d5d46bd679ac000ab3e15825c935
95d98f038320d5d46bd679ac000ab3e15825c935 78df31d62c5b9ba4c84dee4ea346e43a767718c1 857e4c3bce8fd7fc862d7e6e5831e63f24e8cce5 012889c1b0bbfe5f290f757cb6d31dd7d995ccc7 Merge tl/rt-F-D141-REG-upgrade-fix-next

git -C /home/user/work/wt/rt-P5-D141-ecdc-applicability-0637 show -s --format='%H %T %P %s' HEAD
635f4de06fda22a85fc2e4cfc764d0153a4c9f40 5ab5191a296980a0a6bcd1178ab6902d6478a148 7a95a40b07ea0d273e17afb69dbc3456b603f2bc c05fdb171fe37c1d5817a060ecb716a329ee821a Merge tl/vw-V1-composition-meta
```

## Closure and custody checks

The following read-only checks passed:

- Runtime 6a → 95d exact diff: three paths only. All retained Runtime P5
  module blobs are equal except `runtime_protocol/upgrade.py`; its changed
  hunk is the `_validate_candidate` inspector setup, called by `upgrade_realm`,
  while P5’s crash setup calls `migrate_canonical_to_current` at line 81.
- Agent 8585 → ecdc exact retained provider/capture/commit closure: all five
  Agent module blobs and SHA-256 byte hashes are equal.
- Runtime `contract/artifacts.json` Git blob and SHA-256 are equal at 6a and
  95d. The successor lock contains 15 entries; all 15 lock hashes equal the
  manifest and exact Runtime 95d source bytes.
- Runtime `tests/conftest.py`, `tests/lanes.py`, and
  `tests/astrid_checkout.py` were read directly. P5 resolves conftest/lanes
  from Runtime; `ASTRID_CHECKOUT` supplies only the Agent package root.
- The authoritative receipt and peer source files were read. Local Git
  independently authenticated ecdc’s full commit/tree/parents and the exact
  Runtime 95d tuple.

The complete path/blob/hash and 15-entry custody table is in
`source-manifest.json`.

## Prior evidence custody

The original 6934 XML was read and parsed: 38 cases, 38 unique, 0 failures,
0 errors, 0 skipped, 0 xfail; recorded XML SHA-256 is
`04b7bcea10a693d691a4ccaff85df8c94a0e1e634ea14ae1de87f0a25ddca688`.
The original 0513 evidence hashes are unchanged:

```text
p5-applicability.json  a46bcb2d7e566b01c54da297968a2236eb81d6598f5ac85bf18c55e70d096389
source-manifest.json   9eb45d29e3c51ea639835b7aec3526fb4b5532b68e6cd618de37c967a424e5f2
handoff.md             53604c56e3d3083960de700c79160b22e186401732edad734ae1083b320e67cb
```

The 0619 immutable correction outputs are unchanged and match their hub copies:

```text
correction.json                 4f8326ae2b4d32cbe0fffd33bcf2986e300af16554a97bde8700ce165c39a83b
p5-applicability-corrected.json 688d08bc899c3c1583fb2010d0f8ff2251e2c593b24d62d2a703856d90a26ce6
handoff.md                      e41b3a2ac99b12fafd52533792e7428861f94c3fc43480fea8a54e22bac37739
validation.md                   a794f2aabedffec825d369631b2c3c7117a88ba5f0f720633b02e69e736f6af9
```

## Explicit non-runs

```text
tests/typecheck/lint/import/collection/provider/preflight/body: NOTRUN
full suite: NOTRUN
P5 rerun: NOTRUN
vendor-lock and generator commands: NOTRUN
```
