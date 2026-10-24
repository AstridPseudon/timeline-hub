## Result

PASS for live installation and current publication.

- Verified all four ORCH files against the reviewed manifest:
  - `bench_store.py`: `ba31adcf…903bd`
  - `verify_dependency_seed.py`: `8f95cdae…6714f`
  - `make-child-venv`: `6b3e34f9…65dbd`
  - `request-child-venv`: `08f1b00a…2fde`
- Confirmed regular, non-symlink, root-owned `0755` files.
- Confirmed exact UTC backups for all three pre-existing files.
- Protected `dispatcher-daemon`, `make-runtime`, and `request-runtime` hashes remain unchanged.
- `bash -n`: PASS for maker and requester.
- In-memory Python compile/API checks: PASS, including coherent `failure_name`.
- Runtime worktree remains clean at `33fc06bb…`.
- No maker, requester, Store, import, provisioning, network, package, process probe, or full suite was run.

Publication was old during installer observation, but later normal hub-sync propagated all four files. Publication and committed hub `HEAD` now match live exactly. The copy seam is `hub-sync` lines 109–114 (`cp -p $ORCH/bin/* hub/kit/bin/`); this was publication lag, not an allowlist defect. A 20-second read-only observation was stable.

Evidence and full manifest/hash table:

[manifest-and-live.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-kit-live-review-0739/evidence/manifest-and-live.md)

Commit message and `DONE` marker created for the harness. No blockers; real provisioning, cache/bootstrap custody, and AgentREADY remain unverified.