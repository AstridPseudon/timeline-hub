## Result: REJECT

Reviewed Agent commit `b4341044b` (`fix(rendering): omit redundant project env for native frame sessions`) read-only. The one-line controller change is appropriately narrow: `ASTRID_REMOTION_PROJECT_DIR` remains on the ephemeral CLI path and is omitted only for `frame_mode` with a `PersistentRemotionFrameSession`. Native `projectDir`, node, CLI, props/output paths, query/render/cleanup order, and host-session lifetimes are unchanged. No Composition changes were needed.

The gate is not approvable yet because the foreign-project regression is still receiver-only. `tests/core/execution/test_remotion_host_session.py::test_task_cannot_modify_host_scope_inputs_or_escape_attempt[project]` changes the request's `environment` and proves unchanged `_validate_request` rejects the extra key; it does not exercise a caller passing a foreign `project_dir` through `PersistentRemotionFrameSession.render` into the admitted host lease. The new `test_scene_source_carry.py` assertion only checks that the caller's environment mapping omits the redundant key, using a stub `Session`; it does not bind that call to an admitted project. Therefore the tests do not prove that dropping the receiver-side duplicate cannot mask a foreign caller project.

The source path is plausibly safe, but the required proof is unnamed: the host admits `ASTRID_REMOTION_PROJECT_DIR` in `HostRemotionSession.lease`, while `filmstrip_execution.py` and the frame provider independently construct `project_dir` from child state and pass it to `_execute_remotion_locked`; `_validate_project_dir` then derives `runtime_tools` from that caller value. Add a small actual-binding test (or an explicit caller assertion) that admits project A, invokes the real `PersistentRemotionFrameSession` path with project B, and observes the host rejection before approval. Do not add an allowlist, privilege, source factory, policy, DTO, or cache workaround.

## Evidence

- Exact target extraction, focused native caller/host/env-negative tests: `10 passed in 3.83s`.
- Exact target ephemeral CLI environment test: blocked before its assertion by `PermissionError: [Errno 1] Operation not permitted` while probing a local socket in `_available_remotion_port`; not a product assertion failure.
- Ruff on the three touched target files: 16 diagnostics, matching the reported baseline; no new diagnostic was introduced by the commit.
- `git diff bc888522c b4341044b` confirms only one controller condition plus the receiver-negative and stub-caller assertions; no render/query/cleanup or lifetime reorder.
- No full suite, browser, local server, network, install, socket-enabled test, or physical render was run. Browser selector handling remains dropped by native core, so Chrome/profile and actual PNG qualification are unverified and must not be claimed.

## Recommendation

Reject this approval gate until the caller/actual-binding regression and source proof are added. Then port only that owned-caller unit and rerun the narrow native caller, ephemeral CLI, and environment-negative tests. Keep ActualFreshExport28 product lines as parent work and wait for a real PNG certificate before any physical-render qualification.
