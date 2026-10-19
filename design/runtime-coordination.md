## M2 readonly census: canonical reads vs legacy metadata

**Contract.** Runtime owns read scope: `list_timeline_commits` fixes the accepted
`(revision_id, publication_id)` head; `GET .../composition-revisions/{id}` reads
the immutable parent; its `dependency_manifest` pins child revision IDs/digests.
`POST .../inspect` is the bounded current/pinned projection. Do not infer a newer
head from a catalog read. (`timeline_commit_store.py:170-264`,
`timeline_inspection.py:552-756`.)

| Read | Authority and live callers | Disposition |
|---|---|---|
| `inspect` / parent revision GET | Canonical parent head/closure. App `RuntimeDataProvider` uses `inspectCanonicalTimelineHead` then `readParentCompositionAtHead`; Agent `timelines show` uses `open_composition`/`open_bundle`. | Keep; this presents the current film. |
| Shot/internal revision GETs | Exact child IDs from the accepted parent (App `loadRuntimeShotCompositionAtHead`; `loadTimelineCommandBasis` additionally checks the manifest; Agent `open_bundle`/`read_authoring_revision`). | Keep; immutable closure reads, no mutable fallback. |
| `GET project/timeline` and `list timelines` | Identity, name, head pair, plus mutable `timeline_shots`/`timeline_references`; public projection strips config/registry. Agent resolves identity/head; App discovery/default-timeline selection uses metadata. | Keep as catalog/identity metadata, never film content. |
| Project shots/references GET/list | Mutable project catalog for Agent `RemoteShots`/`RemoteReferences` management; not used to render or present the timeline film. | Keep for catalog semantics; do not make it closure authority. |
| `GET project/timeline` in App restore | `restoreHistory` reads only `head_revision_id` + `head_publication_id` before guarded restore. | Required by plan; keep (neutral head-pair read). |
| Media selection GET | Runtime immutable selection contract for add/swap; no current App call found in source scan. | Keep per plan; verify consumer during add/swap cutover. |
| Generic `/timelines/{id}/shots|references` and `/shots|references/{id}` | Runtime legacy timeline rows; no Agent/App product caller found (generated methods/tests remain). | Candidate retirement after external-contract audit; not this PR. |

**Executable contradiction check.** `tests/timeline_commit_film_fixture.py:203-279`
builds the real three-shot/music/transcript film. An in-process probe then inserted
a bogus mutable `timeline_shots` row and legacy `timeline:film` label; `GET
project/timeline` exposed that row/label while `inspect` still returned
`film-parent-v1`, `occurrence-2`, and the same snapshot digest. This is evidence
for the boundary, not a catalog-latest-vs-pinned-past bug.

**Evidence and limits.** Source checks: `tests/test_timeline_commit_read_basis.py:19-75,159-175`
(manifest closure and fixed-head reads), `tests/test_timeline_native_inspection.py:172-227`
(pinned/current selection), `tests/test_timeline_cutover.py:64-99` (legacy shell audit),
and `tests/test_timeline_commit_film_fixture.py:35-108` (fixture/reopen). Direct
run: `PYTHONPATH=$PWD:$PWD/packages/python /home/user/work/venv-runtime/bin/python
-m pytest -q tests/test_timeline_commit_film_fixture.py tests/test_timeline_native_inspection.py
tests/test_timeline_commit_read_basis.py tests/test_timeline_cutover.py -k 'not real_http
and not daemon_generated_client and not public_timeline_document_routes'` => **45 passed,
3 deselected**. No browser/socket/full suite; no provider move/restore was needed.

**Smallest next PR.** First finish App add/swap proof, then remove only the generic
timeline-shot/reference routes/helpers after the external-contract scan: roughly
0.3–0.6k Runtime lines plus focused contract tests. Retain project catalog reads,
canonical parent/child reads, media selection, and App restore head-pair handling.
