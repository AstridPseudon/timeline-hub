# D123 current Agent source package

Source package after the exact current-normal predicate repair. Gating remains frozen; no integration, release or final-cut qualification claim.

## Exact inputs and result

- Upstream base: `b742893426a46a99a2f30583a54faeebe2bd98b7`, tree `ccb2f286eae9419b95a3f54b11208f68c57b27cf`.
- Historical sole-author candidate: `47f6c72acb62da4f62c3eb8a4e140c6ec806af41`. Its D108 patch does NOT include later current-normal changes.
- Authentic stopped checkpoint: commit `80d185d3fb72f90c1bb47cab0bb300dde3a43d4b`, tree `43bcbc8afbcdca3ca929ecaada61ab4aded84ccf`; captured normal `3ab324c891d3121c46d4aff0a339468a9339e0f2`.
- Checkpoint original full-index patch SHA256 `6c0249f4f0c4d439ac5758e7243ff2d02b66481da47b09de9f0c67779d4541c0`, 12,064,418 bytes: independently reproduced exactly by ordering tracked diff sections before added files. Historical D108 SHA256 independently reproduced: `f5d49d5e63ddc0e7a0fb85966280024af70e498eb4f75bd6595bfb59a52a204a`.
- Current Agent normal captured ONCE: `b545b616a41388e24d6f2a59b7b45c26cb057d2c`, authentic hub Agent integration object plus batch1232 finalized normal receipt. Local integration `547e104562` is the older frozen gating input, not current Agent normal.
- Product source tree excluding this review metadata: `e3c142543bf2ec35b12f3826d1f23e37464934f8` (Git tree framing computed without object/index writes).
- Complete b742 source patch: `evidence/b742-current-agent.patch` under worker `rt-F-D123-predicate-return-1314`; SHA256 `b0ff420595441fccb3d0a37b70715e5b2bff373cecd9d2e51c82be51cbe58f6b`, 12,072,718 bytes. Reverse apply check passed; excludes this worker metadata.

## Later normal changes: present and absent

The six paths from checkpoint normal3ab324 to current normalb545 are explicitly accounted for:

1. `astrid/installer/service.py`: current-normal Windows XML string fix already byte-identical via upstream b742; no replacement needed.
2. `tests/fixtures/installer/task.xml`: already byte-identical via upstream; no fixture generation.
3. `tests/test_installer_platforms.py`: preserve upstream Windows predicates; carry only normal's real local-schema/remotion staging fixture setup. The omitted line is restored exactly as captured from b545: `assert 'Hidden' not in service.render('win32', version, data, log)`.
4. `astrid/sdk/timeline/commit.py`: carry exact normal sealed predecessor manifest fix, producer82b6 now genuinely normal.
5. `tests/editing_conformance/test_commit_document_input_capture.py`: carry exact normal additive producer controls.
6. `astrid/packs/rendering/docs/scripts/timeline_document.py`: carry exact normal private `_capture_bundle` caller, atomic8a410 now genuinely normal.

Installer adcb/e2da/04b7, producer82b6 and atomic8a410 were absent from the stopped checkpoint but are already normal at this capture, so they are included solely through that normal delta. Host bae5/ef4c/21b, nativebindingf3a6 and D1003aaf remain absent. The separate active producer1247 branch and all integration branches were untouched. Later normal changes are not chased after capture.

## D123 conflict decisions

Read b742's OMP path first. Preserve its exact npm or `{repo, sha}` selection, HTTPS-to-codeload route, local committed-tree route, native archive integrity, source-tree and Bun-lock checks, package version, recipe and platform handling. No acquisition, installer stage or producer selection occurred. Recipe/tools content remains upstream-equivalent apart from retained EOF whitespace; service.mjs is byte-exact upstream.

Keep upstream behavior wherever retained changes are incidental. Current census: 75 upstream paths, 39 current overlaps; checkpoint had 38 overlaps and seven rejects, historical author1212 had 35 overlaps and six rejects. Added overlap is current-normal installer service, already identical to upstream. Source maps name every path.

Preserve the approved D77(1)/D77a local canonical JSON integrity migration: regular-file/symlink refusal, Runtime `from` pin and exact SHA256 remain enforced; no transitive external Python schema install. Correct the inherited Windows key lookup from `str(relative)` to `relative.as_posix()`: runtime.lock.json keys are POSIX on every host. D123 requires preserving Windows installer purposes; this normalization removes a platform representation mismatch without relaxing any integrity predicate. Four additive POSIX/Windows checks verify both success and tamper refusal.

Other inherited substantive upstream overlaps remain the doctor exception import and C0 one-writer rendering guidance, as reviewed in1212/1222. No new unrelated source repair.

## Protected source and C0

All 173 checkpoint-mapped predicates are conserved (173 retained, 0 missing or weakened). Thirteen mapped files are byte-exact checkpoint; the remaining platform file retains every case AST except the current-normal staging fixture setup, whose assertion ASTs remain exact, including the restored b545 renderer guard. The Windows native task registration and cleanup controls remain exact upstream and were not executed on Linux. All chat files are blob-identical to reviewer1222's approved candidate, so its successful central chat body remains applicable under D120.

Generated client/types, TimelineSession and commit_session remain byte-exact current normal. Request fields, steps/reads and Idempotency-Key are retained. Provider preview/accept and transport's full decoded response pass-through remain intact. This packaging does not newly qualify the full C0 reply/no-write matrix. Inherited `CommitAccepted` DTO does not explicitly enumerate all of head/effects/bindings/dependencies named in the brief; complete authoritative wire-shape qualification belongs to Runtime/future cut, not handwritten generated changes here.

## Commands and results

Run from this worktree; Python is `/home/user/work/venv-agent/bin/python`.

- `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/w-1dd7039c35/pytest-installer tests/test_installer_omp_source.py tests/test_installer_schema.py tests/test_installer_platforms.py tests/test_installer_shim.py tests/test_omp_agent_key.py tests/test_installer_lifecycle.py`: **212 passed in10.51s**.
- Same environment, `--basetemp=/tmp/w-1dd7039c35/pytest-capture tests/editing_conformance/test_commit_document_input_capture.py`: **11 passed,6 integration deselected in2.86s**, unchanged default lanes; no mounted/socket body run.
- `NODE_PATH=/home/user/work/app/node_modules bun run scripts/build-chat.ts --check`: PASS, configured build Bun1.4.2. Source check only, not an exact-dependency/runtime qualification claim; shared installs unchanged.
- `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --check astrid/chat/service.mjs`: PASS.
- `/home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-1dd7039c35/mypy astrid/installer/backend.py astrid/installer/tools.py`: PASS2sourcefiles.
- `/home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-1dd7039c35/mypy --follow-imports=skip astrid/installer/service.py astrid/packs/rendering/docs/scripts/timeline_document.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_commit_document_input_capture.py tests/test_installer_platforms.py tests/test_installer_schema.py`: PASS7sourcefiles.
- `/home/user/work/venv-agent/bin/python -m ruff check astrid/installer/backend.py astrid/installer/tools.py tests/test_installer_schema.py tests/test_installer_platforms.py astrid/installer/service.py astrid/sdk/timeline/commit.py astrid/packs/rendering/docs/scripts/timeline_document.py tests/editing_conformance/test_commit_document_input_capture.py`: exit1, only inherited upstream backend I001 and BLE001; exact upstream stdin comparison matches codes/messages.
- `env PYTHONPYCACHEPREFIX=/tmp/w-1dd7039c35/pycache /home/user/work/venv-agent/bin/python -m py_compile astrid/installer/backend.py astrid/installer/tools.py astrid/installer/service.py astrid/packs/rendering/docs/scripts/timeline_document.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/inverse.py tests/test_installer_schema.py tests/test_installer_platforms.py tests/editing_conformance/test_commit_document_input_capture.py`: PASS9files.
- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json`: PASS. `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`: PASS.
- `tests/test_installer_platforms.py::test_windows_task_settings_and_no_console_executable`: **1 passed** after the repair. The prior candidate's installer suite remains **212 passed**; it was not repeated for this one-line predicate restoration.
- Mypy: **PASS**, 7 source files. Compilation: **PASS**, 9 files. Ruff reports only the two inherited upstream backend findings (`I001`, `BLE001`). `git diff --check`: **PASS**.
- Full-index patch reverse check, per-path full-index blob/mode identities, all 173 mapped predicates, and current-normal six-path checks: **PASS**; refreshed evidence is under the assigned worker evidence path.

Previously approved central chat command: `request-test rt-F-D123-review-1222 rt-wc8-current14-integration --files "test_d123_chat.py"`, service result `rt-F-D123-review-1222-rt-wc8-current14-integration-1025122544-10178`: **1 wrapper passed in107.87s**, underlying `bun test ./astrid/chat` exit0. No new chat body needed because every chat blob is unchanged. Refused absolute wrapper was not retried. Prior268 installer suite was not repeated.

## Limits and handoff

Reviewer1222's wheel fixture still has the upstream-equivalent `ModuleNotFoundError: astrid.core` gap. No new wheel/body run or wheel qualification claim. No full/core/browser/render/P4, stage/downloads, D54a or matrix run; no hand-edited schema/pin/generated files, dependencies or Git mutations. Final D54a/matrix belong to the later cut onb742; independent exact-source review is next.

Evidence is under the authorized worker/evidence path (patches/maps under20MB). The prior D30 prohibition on worker writes to design/ remains observed; the harness owns report.md and committing. Full C0/wheel/core/full/browser/render/stage/P4/download/actual-host qualification remains unverified as before.
