# P2 Main-Profile Report

Status: blocked at an existing dependency-profile seam. Zero original bodies and zero gestures reached.

- Created a private D66 profile adaptation, then removed it after testing.
- Predecessor: `2a395f...655e1`, 43,678 bytes.
- Candidate: `2898db...cfba`, 43,953 bytes (+275 bytes).
- Main Node: v20.19.4.
- Remotion: `/home/user/work/runtimes/agent-remotion-current`
- Browsers: `/opt/pw-browsers`
- All six protected test hashes and fixed four-repo tuple remained unchanged.

Service results:

- Old recipe preflight `...-27231`: exit 127, retained.
- Corrected v1 preflight `...-18912`: pass; body `...-12965`: setup failure, no gesture.
- Corrected v2 preflight `...-25455`: pass; body `...-7951`: setup failure, no gesture.
- Authoritative v3 preflight `...-11751`: pass.
- Authoritative body `...-6678`: exit 1 at hosted build after collecting one test; 1,224 modules transformed. Failure: shared composition package `0.0.2` lacks `./animations.generated`.

The pinned Composition artifact has the export, but supplying it would require forbidden shared-dependency mutation or a new overlay. Therefore the remaining three diagnostics were not submitted.

Checks:

- `node --check scripts/testing/d66-plain-stack-profile.mjs`: passed.
- `git diff --check`: passed.
- Worktree clean; no product source changes.
- No full suite requested.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-main-profile-return-2238/evidence/`

Commit message and empty `DONE` marker are present.