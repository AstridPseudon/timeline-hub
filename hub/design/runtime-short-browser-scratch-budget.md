# Runtime finding: short normal-browser scratch and the admitted budget

Date: 2026-10-20 UTC  
Worker: `rt-m3-short-browser-scratch-budget`  
Runtime base: `601d533d91e3726c4f7ae74723e8eff4adbe2f90`

## Decision

Runtime has no existing path-registration, scratch-root, or browser-temp
carrier that can make an Agent-owned directory outside the attempt tree
accounted, sandboxed, and cleaned. `TMPDIR`/`TMP`/`TEMP` is an existing
environment carrier only; its propagation is not quota or sandbox authority.

Therefore the proposed Viewing/Agent short-parent patch remains on hold. A
shortening inside the admitted attempt root is compatible with existing
accounting and cleanup. Selecting a pre-existing short parent outside that
root is not approved by the current Runtime contract. The minimal source-owner
change, if the normal Chrome socket fix proceeds, is Agent-owned accounting
and cleanup for that exact invocation directory, or a redesign that allocates
the short parent under the attempt root. Do not add a Runtime DTO, public
config, table/store field, wrapper, symlink, authority field, flag, or renderer
test for this finding.

## Exact normal-MP4 path

Viewing's supplied trace and current Agent source agree:

`GenericPackHost` command dispatch -> `RenderService` workspace beside
`attempt/outputs` -> Remotion `staging_parent=workspace` -> Root preparation
creates `.remotion-runtime-*` -> child `TMPDIR`/`TMP`/`TEMP` -> Chrome.

Evidence:

- `/home/user/work/agent/astrid/core/rendering/service.py:408-413` creates
  `.{output.name}.render-service-*` under `_render_workspace_parent(output)`.
- `/home/user/work/agent/astrid/packs/rendering/rendering/renderers/remotion/run.py:1651-1664`
  passes that workspace as `staging_parent`.
- `/home/user/work/agent/astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:81-86`
  chooses `(staging_parent or provenance_out_path.parent)` and creates
  `.remotion-runtime-*` there.
- `/home/user/work/agent/astrid/packs/rendering/rendering/renderers/remotion/run.py:1092-1117`
  gives the child all three temp variables pointing at that nested root.

The supplied failure is a 228-byte Darwin path ending in
`com.google.Chrome.<id>/SingletonSocket`; the equivalent short owned-parent
construction is 96 bytes. This is a path-length problem, not evidence that
the browser needs a larger Runtime quota or a different sandbox authority.

Reviewed handoff artifacts (both remain unapplied):
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-normal-chrome-socket-owner-fix.patch`
and
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-normal-chrome-socket-REPORT.md`.

## Runtime admission-to-launch trace

1. `runtime_protocol/service.py:5457-5531` receives the task admission. The
   first-class `execution_request` is normalized and persisted; optional
   `storage_estimate` is validated as exactly `{scratch_bytes, output_bytes}`.
2. `runtime_protocol/store.py:417-468` normalizes the request. Its target
   may carry placement `storage` and `mounts`, but there is no attempt path,
   temp path, or browser scratch field. `contract/schemas/task.json:94-105`
   likewise defines only target/inputs/workflow/execution/retry/lifecycle/
   limits/checks.
3. `runtime_protocol/store.py:3766-3785` performs the admission/claim free-
   space preflight against `shutil.disk_usage(self.root)`, charging the
   admitted byte estimate plus the configured free-space floor. It does not
   register or walk an Agent host temp directory.
4. `runtime_protocol/service.py:6971-7145` selects the queued task, calls
   `_claim_task`, creates the durable `attempts` row at `:7107`, updates the
   task's `attempt_id` at `:7108`, binds the verified placement at `:7109-7113`,
   and returns the immutable admitted spec, `execution_request`, binding, and
   `storage_estimate` at `:7132-7144`.
5. `runtime_protocol/local_worker_composition.py:365-390` launches the
   installed GenericHost with a fixed `cwd=profile.support_root` and a reviewed
   environment allowlist. `TMPDIR`, `TMP`, and `TEMP` may cross this boundary;
   no attempt root or scratch registration crosses it. The local launcher
   itself owns only the Worker process custody/control graph.
6. On the Agent side, the claim response is retained as the execution snapshot
   (`/home/user/work/agent/astrid/core/execution/generic_host.py:10141-10286`),
   then `run_task` allocates the attempt root at
   `/home/user/work/agent/astrid/core/execution/generic_host.py:8877-8885` via
   `_allocate_attempt_root` (`:5277-5290`). The normal render receives that
   root, but its Remotion staging workspace later overrides the child temp
   directory as shown above.

## Existing accounting and cleanup ownership

The admitted Runtime storage envelope is carried as `storage_estimate`, not
as a path authority:

- Agent `_assert_live_storage_envelope` at
  `/home/user/work/agent/astrid/core/execution/generic_host.py:3960-3999`
  computes `_attempt_tree_bytes(attempt) - _storage_tree_bytes(attempt/outputs)`.
- Final `_task_storage_envelope` at `:4002-4060` uses the same attempt-root
  walk before upload/settlement.
- `ExecutionGuardPolicy.evidence_bytes` and `EvidenceBudget` at
  `/home/user/work/agent/astrid/core/execution/guards.py:91-189,248-264`
  measure/account one root key. `GenericPackHost._renderer_scratch_account`
  at `generic_host.py:5495-5515` is only wired to the separate
  `HostRemotionSession` visualization lease, not normal MP4.
- GenericHost's live polling calls the attempt-root guard at
  `generic_host.py:8085-8098`; final evidence uses the same root at
  `:9609-9621`. Cleanup at `:9855-10002` deletes or retains only `root`, with
  the existing cleanup uncertainty latch.

Runtime's `store.attempt_staging_dir()` at `runtime_protocol/store.py:1128-1137`
is a settlement staging path under `realm/staging/settlements/<attempt_id>`;
it is not the Agent attempt root or a browser-temp registration API.

## One offline control probe

Using the Agent guard helpers, a 4,096-byte file in an external
`owned-parent` measured as `external_tree_bytes=4096` only when that external
path was explicitly passed to the helper, while the empty attempt root
reported `attempt_tree_bytes=0` and `attempt_evidence_bytes=0`. The existing
attempt-root calls therefore do not see external browser bytes.

## Recommendation to Viewing and Agent

Keep the flat owner patch unapplied and do not run the normal browser retry
until the owner proves one of these bounded designs:

1. create the short browser parent beneath the admitted attempt root, so the
   existing storage/evidence walks and GenericHost cleanup own it; or
2. if it must be outside the attempt root, extend the existing Agent-side
   accounting and cleanup calls to charge, sample, and retire that exact
   invocation-scoped path under the same attempt identity, with fail-closed
   cleanup uncertainty.

Runtime can endorse neither external quota nor sandbox escape merely because
the allowlisted temp variables propagate. Viewing's independent browser
qualification gate remains the owner of actual browser/socket qualification.

## Evidence limits

Read-only source trace and the one offline path/accounting probe were run.
No Runtime source changed; no product source, browser, renderer, pixels,
codec/profile, full suite, or live socket/capture qualification was run.
