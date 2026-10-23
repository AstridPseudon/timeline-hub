# Runtime handoff: R0 public-trim profile

**Disposition: qualified facts only; no product change.**

The supported normal frozen34e profile is:

```text
producer=astrid-runtime
producer_version=sha256:d5f98db3213e91d96d4a7f5b184e17bf5268357b37dc06eaa5b568c4b788a572
source_commit=34eac0041b0891e9011966b39bcbd26053fde5bc
source_tree=9853574865f25e08284e82ffb26c0bdecaa16a30
manifest=contract/artifacts.json
manifest_sha256=7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d
artifact_count=78
timeline_schema_sha256=sha256:4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd
contract_version=0.2.14
protocol=workspace.v1
component_manifest_sha256=sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5
runtime_schema_digest=sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c
```

The current App lock at `4c4c9c77c96fab70c4efef09db9a3bc456b0d803` names exactly this `34eac` source and maps 13 consumer files to manifest entries. A read-only Python finite-JSON/hash audit matched all 78 official Runtime artifact entries to `git show` content and all 13 App lock mappings to those manifest digests.

`ad823e0a0f5be4a7acf1d3006df6f794709da63d` is a child text-materialization repair, but the official artifacts, manifests, schema/provenance, and generated clients are byte-identical to `34eac`. The App lock's source identity remains `34eac`; this handoff does not authorize adopting `ad823` or creating a new tuple.

The current App `public-trim-preflight.ts` / `.test.ts` is historical95bd-specific in its exact tuple: it expects Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290…`, producer version `sha256:54205…`, schema artifact `sha256:f52b…`, Runtime schema digest `sha256:7d4afa…`, and 76 artifacts. The historical App lock at `4301732b6a3cfddd80d8878524bddf337b2d951d` supports those values. Current normal lock and helper are therefore mismatched; the narrow pure preflight fails before source comparison on the producer-version mismatch.

App owns the minimal correction: point the normal preflight at the frozen34e profile, or isolate the old exact tuple as a named historical fixture. Preserve valid, wrong-producer/version, forged-digest (manifest/vendor-lock authority), and mismatched source/path/extra-entry negatives. The helper's structural assertion alone only checks digest syntax, so it must not be treated as forged-content verification.

The generated 34eac client statically contains the C0 v2 request fields and accepted/merged, conflict, invalid, and preview reply shapes; no Runtime wire or schema change is indicated. Live socket/production-caller execution and the App fixture repair were not run or claimed.
