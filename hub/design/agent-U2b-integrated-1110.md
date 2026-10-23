# U2b integrated merge-forward proof

## Verdict

PASS for the requested U2b integrated proof on the exact current Agent home.
No Agent source, test, environment, service, contract, pin, dependency, or
shared-install change was made by this worker. The worktree remains clean.

## Merge identity and preservation

- HEAD: `abfa78a657b4ce1cc625104e8472fb29938e3d64`
- HEAD tree: `ffd2a6883c8703b2052daa16e6c9ee0b0c0efdae`
- first parent (D17 current integration): `ce1d1cca87379029924b0be6f98564f556597107`
- second parent (reviewed U2b tip): `c64b900a21062789c01673c0a033b236bcda0eeb`
- reviewed c64 tree: `3020d0a43a6174b627bef13a5337d06ed1e40881`

`git diff --name-only HEAD^2 HEAD` is exactly the expected 12-path union:
the 11 reviewed D17 source/test paths plus
`tests/integrations/test_d09_managed_scene_only.py`. Therefore every other
policy, registry/guard, and conflict-resolution blob from reviewed c64 is
byte-identical in the merge result. The merge-forward delta is clean under
both `git diff --check HEAD^2 HEAD` and `git diff --check HEAD^1 HEAD`.

The 11 current D17 blobs were checked against the reviewed current-port
inventory, all 11/11 PASS:

| Path | Blob |
| --- | --- |
| `astrid/sdk/timeline/_commit_patch.py` | `081423635e9c132382c395d15af4a3ba8d34a74d` |
| `astrid/sdk/timeline/_recording.py` | `10b17db43964ed0016e3d0527910bc9e56ccaf4f` |
| `astrid/sdk/timeline/_root_inverse.py` | `5d2a1165c96e140482b427da0f3e26f06071f080` |
| `astrid/sdk/timeline/commands.py` | `e06810281e6aafced856b3d0efce1753a733833c` |
| `astrid/sdk/timeline/commit.py` | `65f55e30d7eb03f38e21fe02a26b56092859e498` |
| `astrid/sdk/timeline/inverse.py` | `6385c8c3caa9761059d766b6487c967463736fb9` |
| `astrid/sdk/timeline/native_timeline_duplicate.py` | `6f3ff25caf8d2f165c83929c0ae4b386185d2376` |
| `astrid/sdk/timeline_duplicate.py` | `1bc61a027ad8bf33e11affb472c30fe81ec31797` |
| `tests/editing_conformance/test_commit_runtime_source_copy.py` | `1cf5b42e477b28126b5ae12bfe217d6d224bae14` |
| `tests/editing_conformance/test_recipe_timeline_source_copy.py` | `89841e0475f5001a9275078254a8cbbba26b523f` |
| `tests/sdk/test_timeline_restructure.py` | `03fe581af64e9e7bcd47b50a5a51acf36761ae49` |

The D09 fixture is also unchanged from the reviewed `7abfb8d69` source:
`dfe8ed9a4d0fc8870b76079889b1cb9c9b3bd9d4` in both trees.

The live upstream probe had already established `origin/main == 74f3f7ed`;
the local check `git merge-base --is-ancestor 74f3f7ed HEAD` passes. Vendor,
artifact, hygiene, and protected-custody checks pass:

- `python scripts/vendor_lock.py check runtime.lock.json` — `ok`;
- `python scripts/artifact_manifest.py --check` — current;
- `python scripts/reshape/check_repo_hygiene.py` — exit 0;
- no tracked `.pyc` or `__pycache__` paths;
- `runtime.lock.json` source commit: `34eac0041b0891e9011966b39bcbd26053fde5bc`;
- edit-command schema SHA-256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`;
- pinned Composition artifact SHA-256: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

For transparency, `git diff --check 74f3f7ed HEAD` exits 2 with 131 inherited
EOF-whitespace diagnostics. The exact same diagnostics and exit code occur
for `git diff --check 74f3f7ed HEAD^2`; this is pre-existing in reviewed c64,
not introduced by this conflict-free merge-forward. The relevant merge delta
checks above pass.

## Central acceptance

Exactly one central request was made, as required:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-U2b-integrated-1110 u2b-policy-runpod-1053
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-U2b-integrated-1110-u2b-policy-runpod-1053-1023111150-28945 20
```

Actual result:

- request ID: `agt-U2b-integrated-1110-u2b-policy-runpod-1053-1023111150-28945`;
- service result: PASS, exit 0, wall time 24s;
- central snapshot tree: `ffd2a6883c8703b2052daa16e6c9ee0b0c0efdae`;
- exact command: the approved Python 3.13 lane/registry/skip-policy/guard and
  RunPod worker selection with `timeout 180`;
- pytest result: **99 passed in 22.39s**;
- skips: **0**; deselections: **0**; pass count: **99 (>0)**;
- no `-m` selector, `--deselect`, skip weakening, registry/default-selector
  edit, or async pytest execution was used.

This acceptance covers the upstream no-invisible-skips registry/guard policy,
reason and lane custody, zero-pass protection, and the RunPod worker neighbors.
The full v2 request/reply fields and existing production caller were not
changed by this merge: base pair, commands, label, steps/patches, reads and
ordinals, merge/read/key/dry-run/source/rationale/group_id, data/receipt,
accepted/merged/historical-rebased replies, canonical records/dependencies/
effects/history/undo steps, preview/would-status, conflict reason/head, and
invalid code/path/hint/suggested-command coverage remain the reviewed c64/D17
surface.

The reviewed quality evidence is reused exactly because product content is
unchanged outside the already-reviewed D17 11 blobs:

- `make PY=/home/user/work/venv-agent/bin/python ruff` — **2149/2149**;
- `make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy` — **1912/1912**.

No new independent review was run for this conflict-free merge-forward.

## Limits and next steps

No full, HTTP, browser, native14/58, daemon, or original58 suite was run. The
known separate current-Runtime D17 inverse-stage qualification issue remains
outside this U2b proof and is not relabeled by the 99-pass acceptance. The
next step is normal orchestrator acceptance/queue handling of this PASS.
