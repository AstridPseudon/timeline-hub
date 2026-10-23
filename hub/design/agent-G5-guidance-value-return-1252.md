# G5 guidance value return — scoped PASS / DRAFT ONLY / P1 NO-GO

## Result and exact cause

Base: `4dffe54cb2259b8911e4bf6ac811c13d30069a4e` (the reviewed atomic join).
Changed only `tests/v10/test_domain_cli_projects_timelines.py`: file/draft CLI input `x=90` → `x=540`, with two explanatory comment lines. All original assertions, including stored `x == 90`, accepted receipt, full canonical readback, exact retry and unchanged history, remain unchanged. The source-authority fixture is byte-for-byte unchanged. No production file changed.

The second apparent value-loss failure is an independently demonstrated **test boundary unit mismatch**, not a lost edit. The unchanged fixture's `inside` clip is `am-sprite`. `Clip.set` documents canvas pixels; `Clip.set_param` calls `from_canvas`, which maps that element's six-pixel grid with `round(value / 6)`. The checkout branch directly assigns stored JSON `params.x=90`; the file/draft branches passed 90 **canvas pixels**, correctly producing stored 15. Their requests, canonical results and history therefore faithfully preserved the wrong test input for the requested stored expectation.

Before editing the test, the offline trace executed the actual ordinary file CLI handler, saved the working copy, executed its generated export command, reloaded the JSON and read back the canvas coordinate:

| Input path | Editable stored x | Exported stored x | Canvas readback |
| --- | ---: | ---: | ---: |
| CLI `--set x=90` | 15 | 15 | 90 |
| CLI `--set x=540` | 90 | 90 | 540 |
| Direct JSON `params.x=90` | 90 | 90 | 540 |

Thus 540 canvas pixels makes the existing CLI call express the same stored edit as the checkout branch, while retaining expected90. No alias normalization, authority replacement, generated read, provider/auth workaround or core edit was needed. The prior report's failure observation was accurate; its interpretation as a real value-loss defect is superseded by this unit trace. No plan decision changed.

## Exact executions

All commands ran from the assigned worktree. No full suite was requested. Workflow bodies ran **once**, after the meaningful input correction. All tests are in-process, without sockets/HTTP/browser/daemon.

Offline trace (exit 0), before the correction:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python /tmp/w-775f3ddd14/value-trace/trace.py
```

Workflow command (exit 0; **3 passed, 106 deselected in 5.53s**):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa:/tmp/w-775f3ddd14/value-trace ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p proof_capture --timeout=30 --basetemp=/tmp/w-775f3ddd14/workflows tests/v10/test_domain_cli_projects_timelines.py -k editing_guidance_consumes_its_json
```

This retains the 1243 interpreter, Runtime pin and selector, adding a 30-second timeout, private basetemp and read-only evidence capture hook. The external hook observes after the test body, reads public history/document and backs up the existing service connection before fixture teardown. It changes no fixture, read response, authority, assertion or product behavior. Each mode emitted one actual commit; exact retry did not resend. All three landed stored x=90 and retained their full assertions.

Authority negatives (exit 0; **9 passed, 100 deselected in 4.06s**):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 --basetemp=/tmp/w-775f3ddd14/authority tests/v10/test_domain_cli_projects_timelines.py -k guidance_reader_rejects_wrong_authority_without_writes
```

Safe27 (exit 0; **27 passed, 98 deselected in 4.93s**):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 --basetemp=/tmp/w-775f3ddd14/safe27 tests/sdk/test_scene_save_core.py tests/v10/test_domain_cli_projects_timelines.py -k 'scene_save_core or navigation_preserves_resolved_scope_and_editing_resources or timelines_help_is_executable or render_help_includes_copyable_flat_profile or visualize_help_describes_filmstrip_navigation or show_defaults_to_readable_authored_rows or visualization_human_navigation_footer_is_compact'
```

## Quality and frozen sources

- `PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-775f3ddd14/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python`: exit 0, **2149/2149**.
- `PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-775f3ddd14/mypy-normal make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python`: exit 0, **1911/1911**. The brief's historical 1912 is not the current baseline; the inherited 1912→1911 reduction is documented in `agent-G5-guidance-sol-1158.md`, not a new reduction here.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-guidance-value-return-1252/evidence/quality.py`: exit 0. Private base/current scoped Ruff: **3→3**; scoped mypy: **15→15**, exact path/message/code identities including multiplicity, zero added/removed. Individual lint/type commands exit 1 for the inherited findings. The script stores exact subprocess commands. AST proof: every assertion in the entire file unchanged; the sole AST difference is one input string; fixture unchanged. Isolated cache paths only.
- Unchanged core proof is reused from 1243's exact base, with current normal gate rerun; `git diff -- astrid scripts/reshape` is empty. Verified both imported R1 blobs against **both** reviewed `dcb4cee32285712f0639063f9efb96f810b357d7` and integrated `5b1b4db8253f46e0e085908e79f309d492877386`: `_commit_patch.py` = `c2993997edecda94ad6bd9853cbc40a2e3ce804d`; atomic-scope test = `81734d78d1244655b18eff3bfd7027f25d4beded`.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`: exit 0, artifacts current.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`: exit 0, manifest matches frozen producer. Execution tests deliberately retain the prior 3b926efa pin; neither checkout/pin was modified.
- `git diff --check`: exit 0. Final diff: one test file, 3 insertions / 1 deletion.

Production full-v2 caller forwarding and result handling are unchanged: the exact base pair, commands/label/steps/patch/ordinals, merge/read/key/dry-run/source/rationale/group metadata, receipts/records/effects/dependencies/history/undo/preview and structured errors retain their existing code. These selected tests directly verify their original accepted/retry assertions; this report makes no new merged/conflict/invalid or full-gate qualification claim.

## Durable evidence and handoff

Evidence directory: `ORCH/workers/agt-G5-guidance-value-return-1252/evidence/`.

- `offline-trace.json`, `trace.py`, original/exported/editable JSON and CLI stdout retain the cause and exact input path **before** the correction. `unit-implementation.txt` and origin hashes pin the unchanged conversion implementation.
- `prior-{file,draft}-*.json` copy 1243's actual wrong-value inputs, requests, prepared candidates, publications, records, histories and outboxes.
- `checkout/`, `file/`, `draft/` retain current editable/exported/prepared/check/import/publication/outbox JSON, requests, canonical document, complete public history and records, SQLite backup/export, module origins and outcome. No second Runtime owner was opened.
- `workflows.log`, `authority.log`, `safe27.log`, normal and scoped quality logs, assertion mapping, source identities and `final.patch` retain commands/results and scope.

No new failure or blocker remains within this task. No Git mutation, integration merge, shared install/cache mutation, forbidden suite, waiver or approval bypass occurred. Recommend independent review of this single test-input correction and its offline unit evidence, then the orchestrator's existing integration process. **G5 stays DRAFT ONLY / P1 NO-GO**; this is scoped guidance evidence only.
