## D69 triage report

Evidence: [authentic D69 XML](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D69-snapshot-launch-sol-1642/evidence/d69-restored47.xml). Service result: 49 cases, 39 failures, 10 passes, 0 skips/errors.

Counts for assigned six cases:

- Confirmed live regressions: 0
- Exact decision conflicts: 4
- Environment failures: 0
- PASS: 2

| XML case | Result | Evidence and classification |
|---|---|---|
| `test_d69_upstream_native_window_layer_is_materialized_once_with_pin_hold_and_alpha[0]` | Decision conflict | Current `materialize_window_input()` preserves native `FrameWindow`; XML traceback reports `adapted.window` as `FrameWindow(180,210,30/1)`, while the restored body requires `None` and sliced clocks. This is explicitly approved by `agent-review-extent-current.md`: native layers retain absolute windows; only `supports_windows:false` uses the legacy sliced/null-window path. |
| Same test `[1]` | Decision conflict | Same exact source/decision conflict, separately counted XML case. |
| `test_d69_upstream_pack_uses_rendered_frames_without_html_artifact` | PASS | XML PASS; rendered PNG/JSON/Markdown-only behavior retained. |
| `test_d69_upstream_input_only_is_a_materializable_compact_filmstrip_bundle` | PASS | XML PASS; compact filmstrip manifest and materialization behavior retained. |
| `test_d66_upstream_generic_host_hook_materializes_and_publishes_without_local_save_or_invoke` | Decision conflict | XML traceback: `AttributeError: GenericPackHost has no attribute _publish_assembled_timeline`. The exact method was retired by deletion-ledger D13 and PLAN G4/G5: publication is requester-owned through the commit/runtime path. The current supported caller is `runtime_stitch.publish_authoring_proposal()` → `client.tasks.publish_timeline_render()`. |
| `test_d66_upstream_remotion_lock_pins_the_transitive_schema_package` | Decision conflict | XML traceback: missing `node_modules/@banodoco/timeline-schema`. The body requires the superseded external v0.0.6/v0.0.1 package graph. The approved installer decision requires the immutable local Composition artifact and no separate external schema/theme lock entry; the canonical Runtime schema is the single source. |

No assigned failure had a missing supported input or environment-only signature.

PR-sized follow-ups:

1. Rendering: retain the approved native-window behavior; do not alter the restored test. Any reopening of the old sliced/null-window expectation requires an explicit owner decision covering the M2 native-layer contract and its neighboring tests.
2. Generic host: do not resurrect `_publish_assembled_timeline` or add an alias. If publication behavior is still required, implement it through the requester-owned commit/proposal path while preserving the v2 request/reply contract and Runtime-only writer.
3. Installer: separately migrate `Backend.stage`’s stale schema-path assumption to the canonical schema source/generated artifact. Do not restore the obsolete external lock entry. This is a static follow-up risk, not a confirmed live failure.

Tests: no tests were rerun, per task instruction forbidding body collection/rerun. Classification used only retained XML, frozen upstream bodies, current source/caller inspection, and settled decision documents.

No product, source, registry, or test files were changed. Commit message written and `DONE` created.