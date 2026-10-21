# Agent Gate 1 / Gate 3 exact proof index

Date: 2026-10-21 11:40 UTC

This is an index of retained executions, not a new qualification run. The
worker's current Agent source is `1a50cf3f30398500e9f1ccf0b94d59fe7a8bdb3f`
(tree `b286a34197313b552132b442915b8f318b7bb062`). A retained result is a
current-source proof only when its recorded tree is the source under review;
otherwise its scope below is intentional.

## Exact behavior index

| Gate 1/3 behavior | Exact existing selector(s) | Retained result and scope |
| --- | --- | --- |
| CLI/Python/NativeSheet opaque data and explicit clear | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_label_clear_is_lossless_across_native_frontends` (`[python]`, `[cli]`, `[sheet]`); `tests/editing_conformance/test_conformance.py::test_conformance[look.clear.plate-asset-opaque-{cli,sheet,python}]` | `agent-gate1-labelclear-current-b92-integration-1021090212-22884`: **3 passed**, Agent tree `d687c5a31e0bf25c65a13e2c9caebfeb76066200`; public `/v1` HTTP/service with Runtime b92/tree `6abc2f1`, normal95 producer/tree `d3a290b`. The opaque/clear conformance nodes are retained source-only evidence in `gate1-current-integration`: **83 passed**, tree `b614c4d7036ad8b93517969fc595e9f43c9f8ff4`.
| Null/presence safety and history | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_document_diff_null_presence_and_track_roundtrip_is_authenticated` | `agt-m2-document-history-reviewed-one-http-0818-document-diff-null-track-http-integration-1021081908-10363`: **1 passed**, Agent tree `7920ab3097e24b12ddb124f49bc01f41439f95be`, Runtime b92/tree `6abc2f1`. This closes the reviewed unsafe comparison only; it does not claim arbitrary-field support. The source-only null/presence/clear neighbors are included in the retained 83-pass `gate1-current-integration` lane.
| Occurrence isolation and shared-source retention | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends` (`[python]`, `[cli]`, `[sheet]`); `tests/editing_conformance/test_conformance.py::test_conformance[timing.occurrence.source-isolation-{cli,sheet,python}]` | The HTTP three-frontend cases passed within `agt-m4-gate13-schema-only-env-one-diagnosed-run-0850-gate13-current-b92-integration-1021085125-5217` (**7 passed total**; Agent tree `c6ecc87ab4b5c7500de07715ab4f4a5803f1e1de`, Runtime b92/normal95). The pure conformance occurrence nodes are retained source-only evidence in the 83-pass lane. Assertions include untouched shared sibling/source, dependency pins, reload, inverse and redo.
| Rational fps and half-open timing | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends` (`[python]`, `[cli]`, `[sheet]`); `tests/editing_conformance/test_word_binding_recipe.py::test_half_open_window_and_exact_rational_fps_are_validated_at_acceptance`; `tests/editing_conformance/test_word_binding_recipe.py::test_typed_second_offset_preserves_main_precision_at_rational_frame_boundary`; `tests/sdk/test_timing_compiler.py::test_rational_fps_anchor_and_exact_frame_offset` | The HTTP three-frontend cases passed in result `...1021085125-5217` above; the exact rational HTTP-only retained lane `agt-m2-gate1-rational-connected-timing-gate1-rational-connected-timing-1020233921-10834` passed **3**, tree `17209aea25704e23ce0dceec741db08bf3a7e56c`. Source-only timing neighbors are part of the 83-pass lane. The connected cases assert exact half-open windows (`[30,60)` and occurrence `[270,360)`).
| Transcript/source binding and exact identity | `tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py::test_fresh_word_transcript_frontends_exact_pin_roundtrip` (`[python]`, `[cli]`, `[sheet]`); `tests/editing_conformance/test_recipe_text_binding_spike.py::test_set_round_trip_records_exact_identity_and_dependency`; `tests/editing_conformance/test_word_binding_recipe.py::test_same_word_in_reused_cas_clips_retains_raw_source_through_undo` | Retained public HTTP/service result `agt-m2-gate1-fresh-transcript-b92-one-current-proof-0751-gate1-fresh-transcript-b92-current-source-integration-1021075556-26071`: **3 passed**, Agent tree `856769372ca7e850d3be5eb10cd069182ffc6f11`, Runtime b92/tree `6abc2f1`; this is not the latest `1a50cf3` source. The pure word/source tests are source-only evidence in the 83-pass lane. The separate retained SDK-read lane is private/source-boundary evidence and is not relabeled as ordinary public qualification.
| Exact undo/redo, reload, retry and ABA guards | `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo`; `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_sheet_lost_ack_restart_exact_retry_original_guards_and_aba`; the rational and occurrence selectors above | The retained `main95bd-real-fixture-qualification` result `agt-m2-gate13-published014-current-proof-main95bd-real-fixture-qualification-1021031102-23927` passed **11** on Agent tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`, with public HTTP/service Runtime95bd and C13. It is the retained exact inverse/retry control; no duplicate replay is needed. Source-only exact inverse/redo neighbors are included in the 83-pass lane.
| Renderer-stopped commit/reload/undo and honest unavailable preview | `tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable` | The selector passed in the retained 11-pass result above and in `current-sheet-gate3-integration` result `agt-m2-current-sheet-gate3-pair-recheck-current-sheet-gate3-integration-1020215346-19046` (**2 passed**, tree `5164f267bb08eafc497ae19e081861eabec9bb67`). The retained `gate3-agent-current-integration` source-only lane also passed **26**. The latest current-source public attempt is deliberately recorded separately below because it failed before this assertion.

The current-source/public boundary is the corrected `gate13-current-b92-integration`
run `agent-gate13-current-b92-integration-1021083835-1139`: all **7/7**
authorized cases executed and failed at import-origin/health negotiation
(`7d4afa` Runtime versus `8de823` child client), so it is **not** a semantic
failure and gives no current-source product PASS. Diagnosis
`agent-m4-gate13-schema-origin-first-cause-0844-report.md` identifies the
whole C13 site-packages path as the stale-client origin. The earlier 5217 PASS
uses the corrected schema-only origin and remains retained evidence; neither
result should be silently relabeled as the latest tree.

## Single next uncovered M2 milestone selector

```text
tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_placement_materializes_own_slot_reload_inverse_and_exact_retry[fresh]
```

Existing named suite: `private017-placement-one42a-integration`.
`agt-m2-private017-placement-exact-snapshot-one-proof-1119-private017-placement-one42a-integration-1021112055-20692`
passed **1** on Agent tree `5b6dc1c4eed688bdfc2c7f53b21607b0f169683d`,
Runtime42a, direct service/provider scope. It is shot-only and private: it
does not qualify public/HTTP/native adoption, item allocation, or the current
public tuple. That is the single remaining milestone selector to carry into a
future public/current qualification decision. Earlier 25065 and 3710 results
remain failures and are not credit.

## Full aggregate preflight (identified, not requested)

Use the existing coherent-current handoff
`run-on-main-agent-coherent-public-current.md` and result disposition
`run-on-main-result-coherent-public-current.md`; do not use the stale
`full-c13-5c5173dc-integration` profile or C13/0013 as final evidence. The
preflight must verify, together, the exact Agent/Runtime/client tuple, a
b3c-built immutable Composition runtime, a private symlink-free profile with
164 pins and 166 `RECORD` files, three local product wheels, eight import
origins, source/wheel/install byte parity, Node/VibeComfy/ffmpeg tools, and
the wrapper's direct `pytest -q -n 3` invocation.

The handoff is **CODE APPROVED / STORAGE HOLD**, not a full result. The new
b3c Composition runtime and private profile are absent, and the recorded
filesystem value is below the strict existing `>13 GiB` admission floor.
The separate current-final preflight also records the stale giant-file
inventory, the pending Viewing-owned Remotion helper binding, and the lack of
an installed child built from the final Agent source. Until those prerequisites
are satisfied, no full aggregate request is valid.

No tests, HTTP/service bodies, browser, renderer, full suite, new suite,
product source, test source, schema, lock, or pin were changed or run for this
index.
