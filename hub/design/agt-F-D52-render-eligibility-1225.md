## Result

Read-only D52/G4 assessment completed. No product/test files changed; all eight callers are live, not dead scope.

| Selector | Actual route/profile | Retained evidence | Eligibility |
|---|---|---|---|
| `test_minimal_render_wire_parity` | `CommandTransport` launches fixture raw + SDK children via `sys.executable`; fixture profile 1920×1080, 24fps, MP4. | Full9758 summary only; no literal stderr, return code, result state, or traceback. | Source-only route appears eligible with existing `venv-agent`; no `819acf` relevance. Not qualified. |
| `test_request_sensitive_support_wire_parity` | Same `CommandTransport` fixture route; support request profile. | Summary-only; no causal details retained. | Same: potentially source-only eligible, but unqualified. |
| `test_passthrough_audio_wire_parity` | Same route; passthrough-audio profile. | Summary-only; no causal details retained. | Same: potentially source-only eligible, but unqualified. |
| `test_no_audio_wire_parity` | Same route; no-audio profile. | Summary-only; no causal details retained. | Same: potentially source-only eligible, but unqualified. |
| `test_attachment_wire_parity` | Same route; rendered-audio profile with attachment. | Summary-only; no causal details retained. | Same: potentially source-only eligible, but unqualified. |
| `test_intentional_failure_wire_parity` | Same route; structured-failure request. | Summary-only; no causal details retained. | Same: potentially source-only eligible, but unqualified. |
| `test_render_export_adapter_writes_real_mp4_and_is_callable` | `execute_render_export_task` → `run_executor` → canonical `rendering.render` subprocess → FFmpeg selector. Child imports `runtime_protocol`; current Agent metadata does not provide the separate `astrid-runtime` package. | Summary-only; no exact child stderr/return/result evidence. | Not eligible without installed-child/source substitution or acquisition. Existing `819acf` Remotion profile is irrelevant. |
| `test_host_derived_registry_executes_canonical_ffmpeg_executor` | `GenericPackHost` materialization → `run_executor` → canonical `rendering.render` subprocess → FFmpeg selector. Same Runtime package boundary. | Summary-only; no exact child stderr/return/result evidence. | Not eligible without installed-child/source substitution or acquisition. `819acf` is irrelevant. |

The broader retained finding that some rendering paths fail on missing `runtime_protocol` is not promoted to the six summary-only conformance rows or the two unknowns.

The existing 10:16 schema/authorization/child-admission hold remains active. No bounded follow-up is marked ready until exact per-node argv, cwd, stderr, return code, and result-file state are available.

Checks performed:

- `git status --short --branch` — clean.
- `git diff --check` — passed.
- Static caller/source/hash inspection completed against integration and frozen SDK reference.
- No tests, child launches, installs, acquisition, overlays, probes, network/cache actions, or environment changes performed.

`DONE` and the task commit message were recorded.