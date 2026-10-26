# U2 / D141 generated return

Status: `PENDING_FINAL_RUNTIME_PROVENANCE`

## Normal commands

| Command | Exit | Result |
|---|---:|---|
| `python scripts/artifact_manifest.py` | 0 | Regenerated 166-entry `artifacts.json`; only `am-footage/component.tsx` changed. |
| `python scripts/artifact_manifest.py --check` | 0 | `artifacts.json is current`. |
| `PYTHONDONTWRITEBYTECODE=1 python scripts/vendor_lock.py check runtime.lock.json` | 0 | Local vendored bytes match the unchanged lock. |
| `PYTHONDONTWRITEBYTECODE=1 python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-fa9cd546` | 1 | Pristine `fa9cd…` manifest rejects the retained v2 client: it lacks `timeline_commit_types.py` and `commit_conflict_409.json`, and four retained mappings differ. |
| `git diff --check` | 0 | No whitespace errors. |

The final integrated Runtime producer receipt required to run the normal
`vendor_lock.py update ... --producer <actual qualified clean Runtime source>`
was not available. The lock was therefore deliberately not changed, and no
pristine or shared mutable Runtime path was treated as a qualified producer.

## Scope and preservation

The worktree diff contains only `artifacts.json`. `runtime.lock.json` remains
byte-identical to the candidate (`sha256:44dd583e198d5fcf8d176817171c6152053e60032c8ba75c08a89e44e04a58b8`), preserving all 15 consumer mappings, modes, schema/config/test inputs, and the live C0 client files. No Python source changed, so no compile-only check was applicable.

The candidate remains the true merge `aa5a91a618f4d28308772169bc08e8e79274cd6a`
with parents `c585cb2aa73c5298d474e614cb2144f58f27e605` and
`8b6ed2116fd1803d24b2be5bc08bd9490407fe4a`; independent review recorded 19
upstream-only and 922 current-only paths preserved, zero automatic non-conflict
mismatches, and exact D100a blobs.
