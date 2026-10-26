# Validation record

## Result

`FAIL` for the finite route-membership and unsupported-floor findings recorded in `review.json`. Preparation remains `NOT_READY`; no body, GO, registration, or ship credit is claimed.

## Exact read-only/static commands

- `git status --short --branch` — `## tl/agt-P4-D141-prep-review-0028`; no tracked or untracked product changes.
- `git rev-parse HEAD` — `28e56cacb42d3da85b02e5b3543895b44f3d0f70`.
- `git rev-parse HEAD^{tree}` — `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`.
- `git rev-list --parents -n 1 HEAD` — `28e56cacb42d3da85b02e5b3543895b44f3d0f70 c585cb2aa73c5298d474e614cb2144f58f27e605 b4eb5db76fda523407b90a9dbe820f4e20cc1f1d`.
- `sha256sum` on the three primary runtime selectors and the SDK P4 support files — all matched the preparation manifest; hashes are copied into `source-manifest.json`.
- `awk 'NR>=175 && NR<=180 {print NR ":" $0}' .../scratchpad/orch/tests/suites.conf` — line 177 is the old D84 five-selector `p4-current-becfe-http-3legs` row, not the three-leg packet membership.
- `sed -n '1,120p' .../agt-P4-R2-D84a-five-2214/evidence/p4-r2-d84a-unprofiled-five.row` — same five-selector historical row and old manifest binding.
- `sed -n '1,95p' tools/p4-d73-pinned-launch.sh` — exact manifest, four checkout identity, clean tree, original-hash, profile, and evidence guards; no dynamic service API.
- `sed -n '1,110p' tools/install_p4_launcher.py` — CAS replacement of only owned D73 rows, backup, mode 0600, and outside-row byte identity.
- `sed -n '1,95p' .../scratchpad/orch/bin/request-test` — accepts worker/repo, suite name, optional files, and `--no-cache`; it has no arbitrary command/environment request fields.
- `rg -n --hidden -g '*.py' ... 'commit_timeline|api_version|base_publication_id|command_ordinals|undo_steps|would_status|suggested_command|group_id'` — generated client and DTO declarations found all settled C0 request/reply fields.
- `python3 -m json.tool evidence/review.json` — PASS.
- `python3 -m json.tool evidence/source-manifest.json` — PASS.
- `bash -n tools/p4-d73-pinned-launch.sh` — PASS.
- `python3 -m py_compile tools/install_p4_launcher.py` — PASS.
- `git diff --check` — PASS.

## Historical and control-document checks

- Read current `D141-cut-tuple.md`, `D141-morning-cut.md`, and the App 2346 recipe/handoff/manifest/validation/findings packet. The cut tuple has Agent and App pending; the App packet is explicitly prepared, not dispatchable.
- Read the source-preparation recipe, handoff, source manifest, validation, and findings. The packet correctly bounds D84a to four restart passes plus a timed-out ten-note selector, and D97 original to the sole accepted historical ten-note proof.
- Read frozen R4 candidate refs with `git show-ref`/`git ls-tree`; the specified refs exist, but `docs/projects/timeline-r4` is absent from the candidate trees and the supplied Agent checkout. No checkout or ref mutation was performed.

## Tests and execution deliberately not run

No pytest, import, collection, browser, provider, live socket, request-test submission, suite installation, service body, build, child, acquisition, Store/hub write, credential operation, or full suite was run. This is a prep-only review and the task explicitly forbids those actions.
