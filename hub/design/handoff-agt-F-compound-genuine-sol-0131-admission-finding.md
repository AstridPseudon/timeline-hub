F-D86: blocked on an unavailable genuinely admitted source

No source edits. Assigned baseline and current candidate are both
`f6d0ae5997f634ef9743e9edce77a7f995cf715d`. The authoring file SHA256 is
`5d995d5a7399b8c0585a1ad4ffdac7b8b86a561097e8307eea8a80d9a376944e`.
Runtime source was read only at integration HEAD
`6634a17f3ffd885567ba3c91b6c7a560df7375a4`; exact observed file hashes
are in source-hashes.json, with no changes during this inspection.

The missing input is an accepted Runtime closure whose media manifest already
contains a genuine managed object that is unused by its payload graph. No such
source/pair is supplied by the compound fixture or the reviewed genuine
occurrence-media setup. This is not a claim that Runtime cannot ever retain
unused media, or that bytes cannot be ingested. It is the missing source for
this correction under the explicit ban on adding a consumer and manufacturing
accepted history.

Source chain and limits

1. `test_authoring_media.py:437-445` calls detached `inputs()`, trims its two
   occurrences to one, and appends `retained` directly to the manifest.
   `test_authoring_bundle.py:47` defines AUDIO as exactly `"sha256:" + "3" * 64`.
   Thus f6d0ae changes only the name of the old placeholder, not its value.
   There is no media ingestion, catalog selection or Runtime-admitted source
   behind this identity in that path.
2. `test_recipe_occurrence_media.py:40-66` derives inputs from
   `document_fixture()` and supplies synthetic old/new selections and metadata.
   `MediaRealm` (same file:275 onwards) derives from `DetachedRealm` and only
   overrides selected-media reads. `DetachedRealm` manufactures its initial
   history edge; this is not a genuine persisted bootstrap. Copying that
   document into Reader's canonical result does not add source authority.
3. The reviewed production setup `_create_fixture` in
   `test_commit_runtime_occurrence_media.py:21-112` uses actual empty bootstrap,
   `media.admit`, occurrence creation, payload patches, and commitTimeline.
   Its admitted old media is consumed in the payload; it does not supply an
   unused pin. It also rewrites fps, internal scope and inline text bindings
   elsewhere in the fixture, so wholesale reuse would not preserve this
   compound fixture's original full graph.
4. `timeline_commit_baseline.empty_bootstrap_document` starts with no media.
   Runtime's raw-media read can validate a genuinely ingested object, but that
   read alone does not install an accepted source manifest.
5. `native_media_admission.capture_media_admissions` captures managed raw media
   and optional exact catalog selection through the real request-private port.
   `validate_admissions` then checks each pin against the manifest produced by
   `compile_authoring_candidate`; that compiler collects payload media, not
   unused retained source pins. A manifest-only newly admitted object therefore
   encounters `admitted media is not referenced by the candidate` before
   acceptance. `commands.execute` always invokes this validation. This finding
   is source-derived, not an executed refusal.
6. `doc.patch` addresses verified payload roots, not the canonical manifest.
   `document_from_bundle` preserves pins from the authenticated source and adds
   compiled payload pins. It does not turn a caller-supplied manifest into a new
   authenticated source.
7. `native_timeline_duplicate.resolve_source` reads a Runtime-authenticated
   closure and its raw pins. Copy preserves unused pins if that closure already
   has them; it cannot originate the missing accepted source. Foreign shared
   placement likewise requires the exact source closure and child images.
8. The retained-source example at
   `test_commit_runtime_source_copy.py:414-459` really ingests bytes, then
   monkeypatches `trusted_seed._closure` to append the unused pin and directly
   accepts synthetic seed records. That is a trusted setup example, not the
   production-admission pattern required here. `trusted_seed._closure` normally
   derives its media only from payloads. Reproducing its adapter here would
   violate this task's explicit ban on fabricated accepted history.

Strategies deliberately left unapplied: adding a dummy payload/registry/item
consumer; transiently using the retained object only to bootstrap its pin;
patching trusted_seed or acceptance; supplying fake raw-media port responses;
writing SQL/custody/history; or treating a canonical-looking hash as admission.
No product guard was weakened and no expected behavior was turned into refusal.

Original-to-genuine source mapping

| Original input | Assigned baseline | Genuine replacement available here |
| --- | --- | --- |
| OLD / MEDIA, 64 ones | detached old generation/variant selection | Production managed import/selection pattern exists, but not wired into an admissible full compound baseline |
| NEW, 64 twos | detached new generation/variant selection | Production managed import/selection pattern exists, but not wired into an admissible full compound baseline |
| Unused retained pin, 64 threes | AUDIO, exactly the same digest | None supplied; ingestion alone cannot establish an accepted unused source manifest |
| Original parent revision/publication pair | parent-1 / original-publication in Reader | Synthetic, no genuine accepted pair substituted |

No old-placeholder-to-genuine mapping is claimed. The missing last two rows
prevent a faithful migration; no partial setup delta is proposed for merging.

Whole physical topology and predicate conservation

All source and helpers are unchanged. The AST audit compares both the original
0ae146e1b0 and assigned f6d0ae source with the untouched candidate. Whole-file
byte equality against f6d0ae also preserves every input, branch, decorator,
exception predicate, mutation guard and assertion beyond those listed below.

* Input graph: project-1/film; parent-1; one retained occurrence occ-a after the
  original truncation; physical chapter-shot/shot-1 -> internal-1/chapter-1.
  There is one parent, one physical shot and one physical internal revision;
  no flattening, lost mirror or simplified comparison baseline.
* Parent retains config, direct clips and registry, two clip identities,
  picture visual track, rational 30000/1001 fps, timestamp and opaque values,
  name, unknown parent literal, and the entire occurrence timing, placement,
  source_offset/speed and unknown literal fields.
* Shot retains name, internal revision edge, item-1 media and opaque metadata,
  inline narration binding, chapter metadata, and unknown.keep=None.
* Internal retains both clips with app.org.example literal/clear fields,
  track/output/registry, opaque timestamp and [None,False,0], and unknown [1,2].
  The preexisting inputs() removal of source_window and image type remain
  unchanged; no new normalization of the original rational fps occurs.
* Media retain the original same-alias old/new selection assignment and the
  manifest-only third pin. No consumer is added, even during setup.
* Both recorded=True/False Reader paths, pagination, original pair and detached
  source checks, session staging equality, native swap followed by residual
  doc.patch, reverse/move/clear/opaque/null mutations, exact plan comparisons,
  atomic merge, full readback roundtrip, three-media set membership, corrupted
  canonical-source rejection, changed-pair rejection, and recorded foreign
  source rejection all remain original. Helper assertion count stays 18.
* Exact inverse -> redo -> inverse document and roundtrip predicates remain
  original (five assertions). No history, inverse or no-write behavior changed.
* Separate ABA script test stays byte/AST exact (59 assertions); the known
  Runtime sequential-binding finding remains outside this correction. No
  Runtime repair, new refusal expectation or functional outcome is claimed.

Exact five-family selector accounting

| Selector | Status here |
| --- | --- |
| tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py::test_complete_json_script_commit_authenticates_materialized_atomic_scopes | Readonly/source exact; no new proof |
| tests/timeline/test_authoring_media.py::test_public_document_swap_and_residual_patch_use_original_sequential_closure[True] | Admission blocked; unchanged |
| tests/timeline/test_authoring_media.py::test_public_document_swap_and_residual_patch_use_original_sequential_closure[False] | Admission blocked; unchanged |
| tests/timeline/test_authoring_media.py::test_public_document_compound_inverse_restores_exact_original | Admission blocked; unchanged |
| tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba | Readonly separate Runtime finding; unchanged |

Corrected paths: zero. Tests, fixture bodies and services executed: zero.
Static commands/results are in static-checks.md. No functional, integration,
whole-family or gate PASS is claimed.

Next step: orchestrator supplies a genuinely admitted source/pair carrying a
manifest-only unused managed object, or settles an authorized source-admission
setup boundary. Then perform the faithful fixture correction, fresh protected
review, normal fixture merge, and MAIN functional proof in that order. This
report does not authorize changes to product guards or the task's constraints.
