# P4 ten-note physical-path oracle

PASS — source correction, offline controls and independent review. Live body remains unverified.

Worktree: `/home/user/work/wt/ap2-P4-ten-physical-path-sol-0819`.

Identity:

- Current/base SHA: `148235cd8478764940dc116d3a4e3a89040f137a`.
- Base tree: `b42919b24d27675b4da95339608b06147c244261`.
- Candidate tree, calculated in memory without writing Git objects: `cc9e654ee60bc3e251070a7d7ff876994228e4e1`.
- Only changed path: `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` (9 additions, 2 deletions).
- Base blob: `94069d2cff0d0d479c19128b4e149bb8206855d7`.
- Candidate blob: `afc9c112527692536a065de8cdbfc7a25c19bc26`.
- Separate rerun file untouched, blob `72d11a2a8f9f8915a22e325bc15f2edadbae96ff`.
- Final commit SHA is pending the harness; worker did not commit.

Classification: test-oracle authority/path-boundary error, not evidence of a product defect. Source8753 accepted ten commands and passed the full authoritative command projection, then failed the old logical-path expectation at `_assert_step_patch`. The exact authoritative path is `parent` / `["config", "clips", "id:clip-a", "app", "org.example", "p4_note", note["id"]]`. No suffix/contains/either-path rule was added.

Source basis: `_doc_patch.py:102` normalizes the parent clips path, `:429` retains the submitted change and records its canonical binding path; `_commit_patch.py:414` forms the exact field dependency from that binding and observed absent state; `:474` emits the authoritative parent doc.patch step using the normalized path. C0 §§1–5,7 distinguish submitted claims from authoritative effects and require normalized identity for dependencies and undo.

Changes: assert that exact path and exact singleton absent-field dependency in the helper shared by accepted reply and history; additionally compare complete reply steps to `expected_plan.steps`. All original request operands remain logical `clips/...` and are asserted exactly. The pure plan still originates only from the authenticated pre-edit canonical document, submitted request and exact base pair. Complete command/step history records, captures, effects, bindings and dependencies remain compared without dropping fields or deriving expectations from accepted output.

Downstream audit: inspected the entire ten-note body once, including seed/shared physical closure, media pins, source_mapping, opaque/null/absence preservation, exact canonical equality, digest/head/receipt, request api_version/scope/base/commands/label/step metadata/patch/reads/merge/dry_run/key, show/history, restart and all ten per-step undo/redo cycles. No other same-boundary path comparison needed correction. The separate conflict/rerun file and its merged/invalid/conflict diagnostics were unchanged. Public `timeline.open` → `command` → `commit` and the real Runtime/provider fixture remain intact. No product defect found in this source/offline audit; live downstream behavior is not claimed.

Validation commands (all exit 0; each substantive check bounded with `timeout 45`):

```sh
export TMPDIR=/tmp/w-883d43e2da
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583"
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a5d42583
timeout 45 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration -p no:cacheprovider tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo
timeout 45 /root/.local/bin/ruff check --no-cache --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py
timeout 45 /root/.local/bin/mypy --config-file pyproject.toml --platform linux --no-incremental --cache-dir /tmp/w-883d43e2da/mypy tests/editing_conformance/test_p4_ten_note_v2_runtime.py
timeout 45 /home/user/work/venv-app2-native/bin/python /tmp/w-883d43e2da/offline_controls.py
timeout 45 /home/user/work/venv-app2-native/bin/python /tmp/w-883d43e2da/preflight.py
timeout 45 /home/user/work/venv-app2-native/bin/python scripts/vendor_lock.py check runtime.lock.json
git diff --check
```

Results: 1 exact node collected (known unknown-`timeout` config warning); Ruff clean; Mypy no issues in 1 source file; syntax compile and diff clean. Offline controls independently construct all ten original submitted note changes from the shared canonical fixture, then execute the real Agent engine with the exact request/base. All ten exact physical steps pass. 110 effect/dependency mutations reject unrelated path, unnormalized path, wrong root/clip/note/value/before, and corrupt dependency path/root/state. 50 submitted core-field mutations are rejected by the exact projection comparison. 17 complete record/step field mutations fail full equality, and 5/5 core-field mutations are refused by the real command engine. Full expected records/steps are preserved in `/tmp/w-883d43e2da/expected_plan.json`; neither oracle script consumes a Runtime acceptance or prior actual result.

Preflight: Runtime clean at `a5d4258312c979024865ee704da2d632ca5b2730`, tree `f74b016ea837f8148db4a602c972073a226ed177`. Runtime/service/store/provider/astrid_runtime module origins all resolve inside that pin; generated client/metadata origins resolve inside this worker. Normal client source_commit remains `34eac0041b0891e9011966b39bcbd26053fde5bc`; vendor-lock check prints `ok runtime.lock.json`. Public hydration owner `68d54e15a8d217634045b6dcc0acb719fd93c4aa` is an ancestor. Existing `p4-v2-http-nodes` row remains exactly one, 1379 bytes, SHA-256 `fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948`.

Contract identity: C0 document SHA-256 `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`; generated version `0.2.14`, protocol `workspace.v1`; component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`; schema `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`. Frozen edit-command schema SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. runtime.lock.json SHA-256 `320d278366bc344aad35f3564845d9b62d9cc5f2e000a8a4cc6b6fea508d6cd2`.

Independent read-only reviewer `/root/path_oracle_review` returned PASS after inspecting the full diff, test body and relevant production source. It confirmed exact canonical identity/dependency construction, unchanged logical request claims, preserved complete expected records/history and no result-derived oracle. It performed no edits or live execution.

Limits: no live HTTP/body, socket, browser, service, full suite, build, test-service request, product/generated/pin/fixture/package/lock/ops/shared-install edits or deletion. Harness `tmpdir` is a pointer file containing `/tmp/w-883d43e2da`; all scratch/caches were written under that private directory. No blocked work. Next: harness commit, confirm candidate tree/blob, then central owner runs ONE changed-evidence exact named node after reviewing this correction. No live success is claimed here.
