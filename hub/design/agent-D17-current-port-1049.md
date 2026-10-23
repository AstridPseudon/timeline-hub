# D17 current port report

## Result

Ported exactly the 11 requested source/test blobs from Agent commit
`d57207fb5e4a55be70ffe953c6b8b5604e893502` onto current integration base
`7abfb8d69f625d0aada79346d5806f5f9525ed8c`.

The source commit also changed
`tests/integrations/test_d09_managed_scene_only.py`; that path was
intentionally excluded. Its worktree hash remains
`dfe8ed9a4d0fc8870b76079889b1cb9c9b3bd9d4`, equal to the base. No other
outside path changed.

## Exact blob proof

All 11 worktree blob hashes equal the corresponding `d57207fb5` blobs:

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
| `tests/sdk/test_timeline_restructure.py` | `03fe581af64bcb7bcd47b50a5a51acf36761ae49` |

## Checks

- Exact source-copy selection:
  `40 passed in 13.72s`.
- Scoped Ruff over the reviewed changed files: pass, `All checks passed!`.
- `scripts/vendor_lock.py check runtime.lock.json`: pass, `ok runtime.lock.json`.
- `scripts/artifact_manifest.py --check`: pass, `artifacts.json is current`.
- `git diff --check 7abfb8d...`: pass.
- Diff/status scope: only the requested 11 paths are modified or untracked.
- The independent 281-test and broader quality runs were not repeated; the reviewed
  d572 evidence is reused exactly as instructed.
- No full, HTTP, browser, native14, original58, daemon, Git-write, install,
  shared-dependency, or integrated-current-runtime suite was run.

The exact-40 pytest run used the unchanged Runtime pin
`/home/user/work/wt/rt-pin-1365e4b1`. The follow-up integrated 40+281 run
against current Runtime 49ce remains with the normal queue.

## Blockers and next step

No task blocker. The worker tmpdir named by the harness was unexpectedly a
regular file, so pytest used the private temporary directory
`/tmp/agt-D17-current-port-1049-final40`; this did not affect the repository
or shared dependencies.

The harness should commit the worktree using the supplied conventional commit
message, then the normal Agent queue can perform the integrated Runtime-49ce
checks.

