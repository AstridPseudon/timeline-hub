Implemented [tools/run-h3-import-0137.sh](/home/user/work/wt/agt-F-h3-env-0137/tools/run-h3-import-0137.sh).

- Seven original fault cases: `7 passed in 3.60s`
- Preflight/postflight: PASS
- Wrong-tree control: refused
- Source/body hashes matched installed Agent c36; all seven guard branches retained.
- No product, test, profile, or shared-environment changes.

Checks:

- `bash -n tools/run-h3-import-0137.sh` — PASS
- `git diff --check` — PASS
- Evidence: 15,977 bytes outside worktree
- Script SHA256: `b0855c09041884bce9feac3642edc9e114453212921cd3b1dd619b7e5c6b805e`
- Final target tree including script: `a2d826f1f487ba59656b77c7292a81cb2fed6f78`

Qualified prerequisites: child `c886`, Agent `c36ca8c`, Runtime `8ea0766f`, backend `abd47e`, profile/archive `819acf`, Node `v20.19.4`.

Full supported invocation is the script’s `run` command with `EXPECTED_SOURCE_TREE=a2d826f1f487ba59656b77c7292a81cb2fed6f78` and the pinned paths from the task brief. Commit message and `DONE` marker created.