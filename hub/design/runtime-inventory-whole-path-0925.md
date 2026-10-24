## Result

Independent read-only whole-path review completed. No runtime source changes; worktree remains clean.

Verdict: **current verifier security FAIL**. The proposed inventory is **conditionally sound but not supported by current authenticated inputs**.

## Source facts

- Creation runs bootstrap `pip==26.2.1`, `setuptools==80.9.0`, `wheel==0.46.3` without hash-locked wheel input (`make-child-venv:374-378`).
- Seeded dependencies use retained original wheels and locked hashes (`make-child-venv:385-396`).
- Store verification runs on creation and reuse; seeded reuse rechecks retained wheels (`make-child-venv:301-336`, `bench_store.py:688`).
- `installed_integrity()` enumerates distributions but only authenticates active wheel artifacts. It does not close the distribution set or scan arbitrary `bin/` files (`verify_dependency_seed.py:255-418`).
- Independent 09:03 probes reproduced acceptance of:
  - foreign distribution/package files;
  - an unowned `/bin/foreign-launcher`.
- Existing 84-control result remains retained: **84 passed**, one expected duplicate-ZIP warning, with static checks passing.

## Required closed inventory

The corrected design must:

- Require exactly the active locked wheel distributions plus only the three exact bootstrap distributions.
- Build one global physical ownership map across all distributions and all installed files.
- Reject foreign distributions, unowned package files, arbitrary executables, fabricated RECORD ownership, duplicate/overlapping rows, symlinks, traversal, `.data` relocation, and writable/foreign files.
- Permit `.pyc` only when derived from an authenticated wheel source with matching compilation bytes.
- Permit console scripts only when declared by authenticated wheel `entry_points.txt`, with canonical pip wrapper bytes, relocation-safe shebangs, and matching RECORD hash/size.
- Preserve interpreter bytes, Agent/Runtime source snapshots, client tuple, lock/wheel hashes, installed sizes, Store identity, and creation/final/reuse verification.

## Genuine missing input

The current maker authenticates only bootstrap names/versions and the child interpreter identity. It does not retain authenticated bootstrap wheel bytes/hashes or a trusted pre-bootstrap venv file inventory. Therefore a closed inventory cannot safely distinguish legitimate bootstrap files from fabricated RECORD ownership.

Sol0923 needs either:

1. immutable, hash-authenticated bootstrap wheels plus retained pre-bootstrap venv inventory; or  
2. an equivalent trusted manifest covering every bootstrap and interpreter-owned path, hash, size, and provenance.

The failed `0c2c/becfe` child’s installed RECORD rows and staging tree are absent; exact NumPy attribution remains **UNKNOWN**. The retained NumPy wheel is clean, but no cause is inferred.

The Farm child `a952c90d` was genuinely created normally and passed isolated `runtime_protocol` import, but it was an unseeded route; its later preflight lacked schema/xdist inputs. It does not qualify the seeded inventory or final Farm readiness.

## Checks

- Static source probe: PASS; confirmed bootstrap command, creation/final/reuse call sites, and missing explicit bootstrap inventory.
- `bash -n` maker/requester: PASS.
- Python compile probe without bytecode writes: PASS.
- Manifest hashes: **7/7 PASS**.
- `git diff --check`: PASS.
- Worktree: clean.
- No install, child inspection, retry, network, Store mutation, full suite, lint/typecheck rerun, or product edit.

Commit message and `DONE` marker were created.