# P4 D141c validation

## PASS checks

- `git -C <four frozen checkout> rev-parse HEAD HEAD^{tree}` and parent receipts: exact Agent `28e56`, Runtime `6a011`, App `867cb273`, Composition `635f4de0`; all four clean before and after controls.
- Python stdlib `shlex` parsing: corrected candidate contains `run -- -m pytest` before later `-m integration`; exact three original selectors; timeout 45, `addopts=` clear, cache provider disabled, and JUnit under its own body-evidence directory.
- Read-only contract check: frozen `contract/commit-v2.md` retains the full C0 request, command, step, reply/conflict/invalid/preview field families and the Runtime `commitTimeline` / Agent provider caller.
- Python stdlib JSON/hash/AST checks: prior packet JSON valid; launcher and installer source parse/claims inspected; normal manifest hash `67ef4348b4b77eb02b74abe20ad6fefdb075f980dc8ca563c0a3c79d1f0e5b9f` matches the 0047 registered manifest and copied run output.
- `bash -n /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh`: pass.
- Exact final-path positive production `run` control: `p4-d141c-normal`, preflight `0`, stub exit `17`, one counter line.
- Exact final-path agent-SHA poison production `run`: exit `1`, zero counter lines, mismatch refusal.
- Realpath/symlink/samefile/inode checks: input and materialized manifest are distinct regular files and equal by bytes, not by inode.

## FAIL checks

- Read-only active registry check: current row is exactly the old 0047 row (`d58f649a...`), not the corrected candidate (`21f40728...`).
- Active row lacks `-m pytest` and aliases manifest/evidence parent paths, so the preserved actual 1347 failure remains the production route’s outcome.

## Not run by instruction

No suite CAS install, request-test, pytest, product imports, test collection, provider, original body, full suite, alternate route, or registry/source mutation was performed.
