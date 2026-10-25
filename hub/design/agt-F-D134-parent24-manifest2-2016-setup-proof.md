# D134 setup proof

The exact reviewed IDs were preserved: `parent24 managed_edge_fixture` and
`manifest2 fixture_call_missing_required_args`.

The parent fixture’s genuine required inputs are `operation`, `media_owner`,
and `source_bytes`, in addition to request, temporary path, and monkeypatch.
The manifest caller now supplies `swap`, `parent`, and the existing parent
fixture’s real source-byte factory. No media bytes, authored operation, owner,
source pin, text binding, grouping, predicate, history, or inverse assertion
was changed.

The parent cohort was first run before the file-local change and failed at the
same shared setup write. After the manifest change, both manifest cases and all
24 parent cohort cases reach that same boundary. The boundary is the generic
shot-root `doc.patch` in the readonly occurrence-media helper. Runtime rejects
it as a provider-managed-edge write before the requested semantic caller can
run.

There is no faithful file-local replacement available in either assigned file:
recreating the shot through a semantic birth would not preserve the authored
shot/item identity and topology. The finite boundary is therefore outside this
worker’s allowed files and must be handled by the owner of the occurrence-media
helper. This worker did not alter shared setup, product code, or test
expectations.
