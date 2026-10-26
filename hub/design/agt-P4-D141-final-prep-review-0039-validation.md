# P4 D141 independent cumulative FIRSTRETURN validation

Result: `PASS_PREPARATION` with finite `BODY_NOT_READY` status.

## Exact static checks

- `git status --short --branch` — PASS: clean `tl/agt-P4-D141-final-prep-review-0039` worktree.
- `git rev-parse HEAD` — PASS: `28e56cacb42d3da85b02e5b3543895b44f3d0f70`.
- `git rev-parse HEAD^{tree}` — PASS: `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`.
- `git rev-list --parents -n 1 HEAD` — PASS: `28e56cacb42d3da85b02e5b3543895b44f3d0f70 c585cb2aa73c5298d474e614cb2144f58f27e605 b4eb5db76fda523407b90a9dbe820f4e20cc1f1d`.
- `sha256sum` on launcher, installer, protected P4 source/support files — PASS; hashes are recorded in `source-manifest.json`.
- `sha256sum` over the three primary runtime source hashes — PASS: `cf65539e79e9731c468368e72da4dba44298107c517715042aceb8d3c6d0e727`.
- Direct live CAS read of `/tmp/.../orch/tests/suites.conf` — PASS: mode `0600`, SHA-256 `38a5a5f808b14f1778ba75d90d4024fb3cb38941ed60669c7e113c0c86bc797b`; named row occurs once and has five D84 selectors.
- Direct live row/manifest read — PASS: row SHA-256 `db3ee5aac42aa0be7e98a5bd7b8a0bf2cd87c228db3806aaf53d187b92ea7f59`; D84 manifest SHA-256 `13e5c3080d0df736b70924ba785eeb55a8af4ebd7ea575da6e433d4ab93b9636`.
- `bash -n tools/p4-d73-pinned-launch.sh` — PASS.
- `python3 -m json.tool` on retained 0026/0028/0034 JSON artifacts — PASS.
- `git diff --check` — PASS.
- Static caller/CAS inspection — PASS: `authoring_commit_request`, `publish_authoring_candidate -> writer.commit_timeline`, generated `commitTimeline`, launcher SHA/tree/parent guards, installer preimage assertion, and owned-row-only replacement are present.
- Frozen R4 refs read with `git show`/`git ls-tree` only — PASS; no checkout, merge, fetch, or ref mutation. `docs/projects/timeline-r4` is absent from the four candidate trees.

## Deliberately not run

No pytest, test collection, imports, provider, browser, controller, wait, request-test submission, suite installation, row installation, profile/acquisition, service body, comparator control, full suite, or shared-dependency operation was run. No product, test, generated, pin, schema, kit, suite, registry, checkout, or source file was changed. Historical receipts were not retargeted.

