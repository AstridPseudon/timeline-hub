# WC1 final route assertion first-cause diagnosis

Date: 2026-10-21 UTC

## Scope and retained evidence

- Plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`
- Agent source named by the retained run: commit `8cad2a95b705862e4d8c6578780cf92a5ed1cc2b`, tree `d0d0edc5e72a081ef5dc4676ad8130c470b98ccc`
- Runtime/client lane: Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`; normal95 client; central result:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-wc1-original-binding-fixed-one-http-0911-wc1-selected-media-http-b92-normal95-integration-1021091314-15223`
- Retained run: requested `2026-10-21T09:13:14Z`, result `2 failed in 7.13s`; the result retains only `paths.append(handler.path)`, not per-request timestamps or the path list values.
- Both cases (`parent`, `occurrence:occ-a`) reached and passed durable lost-ACK persistence, exact restart retry, reload, and inverse. Both failed only at `tests/editing_conformance/test_commit_runtime_parent_media_swap.py:422`:

  ```python
  assert not any('composition' in path or 'publish' in path for path in paths)
  ```

No new run was made. No source, test, assertion, fixture, or generated file was changed.

## Recorded HTTP inventory

`P` below is the case project ID; `film` is the timeline. The two parametrizations follow the same route sequence, with different `P` and owner/selection query values. `T*` is retained-run order/phase, not a wall-clock timestamp: the test did not record individual request times.

| Order/phase | Verb | Path recorded by `RuntimeHandler._send` | Count per case | Callsite and classification |
|---|---:|---|---:|---|
| T0 client open, twice (before first attempt and after Runtime restart) | GET | `/v1/health` | 2 | `astrid/sdk/client.py:301-306`, generated client `health`; canonical transport health read. |
| T0 client open, twice | POST | `/v1/handshake` | 2 | `astrid/sdk/client.py:307-328`, generated client `handshake`; canonical authentication handshake, not a timeline writer. |
| T1 initial history and later session/history reads | GET | `/v1/projects/{P}/timelines?limit=50` | 12 | `RemoteTimelines._resolve_timeline`, `astrid/sdk/remote.py:634-703`, reached by `history`, `TimelineSession.open`, `open_bundle`, and `commit` scope resolution; canonical timeline-list read. |
| T1 initial/final history and undo-session base read | GET | `/v1/projects/{P}/timelines/film/commits?limit=1` (initial and undo-session) or `?limit=10` (final history) | 3 | `_RemoteTimelineRevisionMixin.history`, `astrid/sdk/_remote_timeline.py:155-170`; canonical accepted-history read. |
| T2/T3/T5/T7 bundle opens | POST | `/v1/projects/{P}/timelines/film/inspect` | 6 | `RemoteTimelines.open_composition` → `inspect`, `astrid/sdk/remote.py:1116-1178` and `:747-797`; canonical read operation transported as POST with an inspection body, not a write. |
| T2/T5/T7 pinned bundle reads | GET | `/v1/projects/{P}/timelines/film/composition-revisions/{revision}` | 3 | `_RemoteTimelineRevisionMixin.open_bundle`, `astrid/sdk/_remote_timeline.py:46-61`; generated route `get_project_parent_composition_revision`, `astrid_runtime_client/generated.py:890-891`; permitted immutable canonical/read GET. This is the direct false-positive for `"composition"`. |
| T2/T5/T7 pinned child reads | GET | `/v1/projects/{P}/shots/{shot_id}/revisions/{shot_revision}` | 3 | `_RemoteTimelineRevisionMixin.open_bundle`, `astrid/sdk/_remote_timeline.py:67-75`; immutable pinned shot read. |
| T2/T5/T7 pinned child timeline reads | GET | `/v1/projects/{P}/timelines/film/revisions/{internal_revision}` | 3 | `_RemoteTimelineRevisionMixin.open_bundle`, `astrid/sdk/_remote_timeline.py:77-83`; immutable pinned internal-timeline read. |
| T2 initial capture | GET | `/v1/projects/{P}/media-selection/verified?...` | 2 | `astrid/sdk/timeline_media_replacement.py:231-234` → `_verified` → `WorkspaceClient.get_project_verified_media`; one old selection and one new selection, both canonical immutable media reads. Query values differ by fixture selection. |
| T2 initial product acceptance, lost acknowledgement | POST | `/v1/projects/{P}/timelines/film/commit` | 1 | `TimelineSession._flush`, `astrid/sdk/timeline/sync.py:375-390`; `RemoteTimelines.commit` resolves scope then calls generated `commit_timeline`; accepted durably, response intentionally lost. Native product write. |
| T4 exact retry after restart | POST | `/v1/projects/{P}/timelines/film/commit` | 1 | Same `TimelineSession._flush` path; persisted original key/body/base/guards are replayed. Native product write. |
| T6 guarded inverse | POST | `/v1/projects/{P}/timelines/film/commit` | 1 | `TimelineSession.undo`, `astrid/sdk/timeline/sync.py:304-316`, then `_flush`; native inverse product write. |

Therefore, for each case the retained wrapper recorded 39 requests: 2 health, 2 handshake, 12 timeline-list reads, 3 history reads, 6 inspect reads, 3 composition-revision reads, 3 shot-revision reads, 3 internal-revision reads, 2 verified-media reads, and 3 `/commit` writes. No `/composition-revisions` POST and no path containing `publish` is in the product call graph for this explicit-selection branch.

## Bootstrap separation

The fixture is not part of `paths`: `paths = []` and the `_send` monkeypatch are installed at test lines 295-316 only after `http_editing` has yielded. The isolated pre-edit fixture bootstrap is therefore not recorded in the retained HTTP result.

Its relevant setup writer is nevertheless identifiable in the frozen source:

- `tests/editing_conformance/test_commit_runtime_occurrence_media.py:129-136` calls the in-process `service.publish_parent_composition(..., idempotency_key='popup-baseline')` to seed the initial parent composition.
- The parent/occurrence fixture is then closed at `test_commit_runtime_parent_media_swap.py:317-318`; only after that does `real_runtime(...)` take over the same root and the HTTP recorder become active.
- This is category **(b), isolated pre-edit fixture bootstrap**, not a request made by the product operation and not evidence of a recorded HTTP legacy write.

## Product writer decision

No product legacy writer remains on the exercised branch. The exact branch proof is:

1. `RemoteTimelines.replace_parent_media`, `astrid/sdk/remote.py:1241-1249`, sees all of `old_media`, `media`, and `expected_publication` and dispatches to `replace_selected_media`.
2. `replace_selected_media`, `astrid/sdk/timeline_media_replacement.py:209-215,231-256`, opens the existing `TimelineSession`, fetches the pinned bundle, verifies the two selections, captures the native swap, and calls `session.commit(...)`.
3. `TimelineSession._flush` calls the scoped `RemoteTimelines.commit`, which emits `/v1/.../commit`.
4. The legacy whole-closure path is the other branch beginning at `remote.py:1250`; its `publish_authoring_candidate`/`_Writer.publish_parent_composition` call at the later `remote.py` fallback is unreachable when the explicit selection arguments are present. It is not the callstack observed by this retained test.

The matching `/composition-revisions/{revision}` requests come from `_bundle` → `fetch_bundle` (`astrid/sdk/timeline/sync.py:179-189`; `astrid/sdk/timeline/store.py:629-642`) → `open_bundle`, before capture and again in the two explicit test reloads at test lines 400-403 and 415-418. They are legitimate canonical reads, not legacy writes. The positive native `/commit` identity and inverse coverage remains strict.

## Exact assertion repair proposal (not applied)

The broad substring assertion must not be narrowed by guessing. The one-to-one stronger check should preserve the existing `paths` collection and all existing forbidden-writer identities, while filtering only product-phase mutating requests:

```python
legacy_writes = [
    (verb, path) for verb, path, phase in recorded_requests
    if phase == 'product'
    and verb == 'POST'
    and path.endswith('/composition-revisions')
]
assert not legacy_writes
```

The recorder should append `(handler.command, handler.path, phase)` only after fixture setup, with `phase = 'product'` set immediately before `AstridClient.open` and kept through the final history assertion. The exact forbidden positive for this test is `POST /v1/projects/{P}/timelines/film/composition-revisions`; the other listed retired mutation shapes retain the existing legacy-writer boundary rather than relying on a substring.

Add one planted negative beside this check: in a separate test-only control, invoke the generated `publish_parent_composition` through the same authenticated recorder during `phase == 'product'` with a minimal already-admitted publication, and assert the exact tuple `('POST', '/v1/projects/{P}/timelines/film/composition-revisions')` is detected. This proves the guard catches the writer it claims to forbid. Keep the current strict positive/negative coverage and identities unchanged, including:

- `test_commit_runtime_parent_media_swap.py`’s `Transport.publish_parent_composition` failure at lines 213-218;
- `test_commit_runtime_occurrence_create.py`’s `no_legacy` service monkeypatch;
- `test_commit_runtime_first_clip.py`’s forbidden `publish_parent_composition` monkeypatch;
- neighboring native-sheet forbidden-writer tests.

This is a test-only proposal. No assertion or source repair was made in this diagnosis.

## Evidence status and next step

- Retained lane result: **2 failed**, both only at line 422; all durability/retry/reload/inverse assertions before it passed.
- Diagnosis: **false positive from permitted canonical GET reads**, plus an unrecorded setup writer outside the product phase; no product legacy writer found.
- Not run here by instruction: daemon, HTTP, proof, native, render, browser, install, full/private/replay lanes, or any new test run.
- Recommended next step: have the orchestrator review this inventory, then make the exact product-phase/write-only assertion repair and planted-negative test in a separate change before requesting any new proof.
