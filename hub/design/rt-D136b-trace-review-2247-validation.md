# D136b validation

## Results

All requested static checks passed. No product, test, fixture, generated file, pin, source byte, Git ref, hub file, or report file was changed.

| Check | Result |
| --- | --- |
| Trace source manifest input documents | 17/17 paths present; declared byte counts and SHA-256 values match |
| Trace source manifest entries | 68 entries; 67 Git blobs available (one intentionally absent current-home D100 file); 65 AST-parsed entries; 0 hash/blob/line/AST findings |
| Trace citations | 48 unique reference records; every Git commit/path/blob/SHA-256 and cited line range verified |
| App2211 source files | 16/16 Git source hashes, line counts, and AST parses match the saved manifest |
| App2211 controlling inventory | 45 boundaries, 30 condition maps, 31 AST blocks, 75 definitions, 307 helper calls, 9 final predicates, 6 parameter values; saved span validation has zero remaining identity errors |
| App2211 prior inputs | 37/37 declared SHA-256 values match saved copies under `orch/design`; 36 original worker paths are absent, recorded as custody limitation |
| Canonical controls | 17 input documents, 65 parsed files, 73 manifest checks, 48 citations |
| Agent current-source comparison | authoritative `hub/tl/integration` is `cd63…`; 19/21 actual2136 Agent source files are byte-identical, with only `_command_state.py` and the projection test fixture differing |
| Runtime current-source comparison | auth/port/store/coordinator/provider and selected controls/contract are byte-identical from `ab1e…` to `f103…`; `service.py` has only the unrelated filename-storage change |
| Git diff checks | PASS for review worktree, `/home/user/work/agent`, and `/home/user/work/runtime` |
| Worktree status | review worktree, Agent sampled home, and Runtime integration are clean |

## Commands run

- `sed -n '1,240p' /tmp/.../scratchpad/orch/PLAN.md` — PLAN read before review.
- Standard-library inline Python rederivation over `rt-D136b-producer-trace-sol-2233-source-manifest.json`: `git rev-parse <commit>:<path>`, `git show <commit>:<path>`, SHA-256, line counts, and `ast.parse` — PASS, 0 findings.
- Standard-library inline Python rederivation over the 48 trace references in `rt-D136b-producer-trace-sol-2233-trace.json` — PASS, 48/48 exact Git blobs/SHA-256/ranges.
- Standard-library inline Python rederivation over App2211’s 16 source files and 37 saved input hashes — PASS, 16/16 sources and 37/37 saved hashes; original worker-path absence retained as a custody limit.
- `git diff --name-status 90b59… cd63… -- <relevant Agent paths>` plus `git show` — PASS for the stated current-source correction.
- `git diff --name-status ab1e… f103… -- <selected Runtime paths>` plus `git show` — PASS for selected source equality and unrelated service delta.
- `git diff --check` in the review worktree, `/home/user/work/agent`, and `/home/user/work/runtime` — PASS.
- `git status --short --branch` for the review worktree, Agent sampled home, and Runtime integration — clean.

No pytest, imports, compile/import execution, provider/service execution, test collection, original9, full suite, browser, localhost/live socket, profile, recovery, SWAP/WAL, or private raw artifact access was performed. No temporary audit script was available or created; the checks above were independently rederived from saved manifests and Git blobs.
