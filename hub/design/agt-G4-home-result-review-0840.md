## G4 home result review

- Verdict: integrated G4 evidence **PASS**; held duck row remains **HOLD**, not executable.
- Worktree unchanged and clean at Agent `0ff3d103fb892977b0853829f42b748a5d567851`, tree `1d613fbec8b30a5a55c22e16a2eb88f0fa64a4d5`; reviewed `f9df90aa…` is an ancestor.
- Runtime verified clean at `becfe6db88b2cc034dba3fafa6c050117cdf2b06`, tree `7edc08e3…`; imports resolved from the explicit Agent/Runtime worktrees. Runtime auth blob: `979225ab…`; file SHA-256 `e172f8c5…`.
- Production caller is wired: `Checkout.publish → _commit_document → TimelineSession.submit`, appending `media.admit` and preserving canonical retry/receipt handling.
- Durable JUnit: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/evidence/g4-integrated.xml`, SHA-256 `52ec8bb86abb261b444150054bc271c34756e2122d7bee27f9e5bd4a13030f0c`. XML contains exactly 20 cases, 0 failures/errors/skips, across the three specified modules.
- Author evidence also reports compile, Ruff, 15/15 vendor mappings, artifact manifest, diff check, and mypy `1902 baseline / 1902 current` passing. These were not rerun.
- Duck fixture comparison: current file matches the reviewed `abdd70e395` version; all 17 assertion ASTs are identical.

### Held duck findings

- Existing installed child is Agent `ba8f0bc8…` / Runtime `f3208b26…`, so it cannot qualify Agent `0ff3d103…` / Runtime `becfe6db…`.
- Candidate Agent `0c2c28da…` / Runtime `becfe…` provisioning independently refused on `unsafe or overlapping dependency RECORD: numpy`; no body ran.
- Service `26998` is a separate setup failure: `runtime_protocol` was unavailable to pytest because `env -i` applied only to preflight, not the pytest process. It is not a product verdict.
- The staged row is also not snapshot-compatible: it requires literal `git rev-parse HEAD = 0ff3…`, while the managed runner creates snapshots with synthetic `git commit-tree` commits. The exact tree guard is valid; the literal HEAD guard must be corrected by the row owner without weakening source identity.

### Future single-child tuple

Use one newly provisioned, installed child with:

- Agent `0ff3d103…`, tree `1d613fb…`
- Runtime `becfe6db…`, tree `7edc08e3…`
- Duck test source blob `cfcf373a…`
- D32 persistence fixture blob `4eab80b3…`
- D32 selectors:
  - `test_restart_a_fresh_process_sees_every_edit_and_the_undo_history`
  - `test_two_writers_in_separate_processes_merge_different_clips_and_refuse_the_same_param`
- Preserve the existing D32 JUnit/result identity; do not create multiple old `0c` children.

No row installation, original ABA execution, preflight/realm/download/probe, product edits, or prohibited suites were performed. Commit message and `DONE` marker were created.