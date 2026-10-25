# F-D86 historical source dependency: static disposition

Base/candidate: `595464fd1cae3204f3c5cb99f7f72a1b4d2083ba`; no repository changes.
This is a source finding, not functional qualification. No test, helper, fixture,
provider, service or module body was executed. Actual private request/source maps
and XML were not accessed. The published safe rows contain no baseline/candidate
snapshots, so exact actual snapshot deltas remain UNKNOWN.

## Decisive distinction from the previous report

The nine primary rejects are not nine independent examples of unrelated edits
blocked by revision metadata. Seven inherit the same M1 fixture that creates a
new destination; two deliberately change the transcript descriptor referenced by
the historical child. The later M1 ten and D87 six inherit that same fixture.
An aggregate basis inequality cannot identify a pin-only change, and the
available source shows stronger, independent refusal causes.

All 14 traced Agent source/test files are byte-identical to HEAD, actual9211's
`cef8a5be53f68a7cd3b5403c362171c5633a5ae9`, and actual11789's
`562ee30b6ed567a90a114f5029a96da2ece9789e`. Consequently these are findings about
the actual captured callers, not an inference from a newer integration head.
Exact checks/hashes are in `static-analysis.json`; all 25 selected published rows
are preserved in `selected-safe-outcomes.json`.

## Production call trace and source lifecycle

1. The fixtures use `RuntimeService.commit_timeline` and the registered Astrid
   provider. Runtime `RequestCommitPort.revision_closure` verifies destination
   ancestry/base pairing; its dictionary form delegates to authenticated
   `source_revision_closure`. A foreign source closure is request-private and
   does not replace destination authority (`timeline_commit_port.py:257-310`).
2. Agent `_load` checks project/timeline/revision and calls `bundle_from_document`
   (`commit.py:432`). `_verify_document` checks payload digests, physical managed
   links and complete manifest; `open_authoring_bundle` creates occurrence-local
   authoring identities and exact source rows (`authoring_bundle.py:362-535`).
   Each source row contains shot ID, shot revision/digest, internal timeline ID,
   internal revision/digest, and item-ID map. Those are not transcript-only data.
3. `_hydrate` verifies each exact document pin, scope, version and content digest,
   plus transcript kind/schema/media/source identity (`commit.py:442-524`).
   Captures go in `source_mapping.pinned_documents`. The source Runtime document
   remains private compiler/authority input. `_copy_manifest` is a dependency
   retention/materialization input, not permission to grandfather a declaration.
4. `execute` starts from the loaded destination bundle; replay starts from the
   newly loaded/hydrated head. Final validation's baseline is the destination
   bundle, landing head, or explicitly restored authenticated closure
   (`commit.py:1230-1417`). A duplicate's source is `ctx.source_copy`; it is not
   substituted for that baseline or included as a blanket historical exemption.
5. `document_from_bundle` compiles and applies physical projection, reuses exact
   unchanged original images, collects only reachable child roots, retains exact
   captures/pins, and verifies the resulting canonical closure (`commit.py:302-418`).
   If `_copy_manifest` exists or placements share authoring roots, the validation
   adapter materializes and reopens this document, then restores captured pins
   (`commit.py:1401-1409`). Otherwise validation sees the working bundle.
6. Reopening recomputes source rows from the materialized physical images. Source
   revision/digest changes can therefore accompany a legitimate compiler
   materialization. But validation also clears `baseline_internal` when physical
   shot/internal revisions, owner placement or scope differ
   (`validation.py:597-609`), before checking `_text_reference_basis`. An observed
   error can thus mean `baseline is None`, even without evaluating basis equality.
7. The legacy predicate requires a well-formed exact declaration, unchanged
   `clipType`, existing baseline clip, scope, complete selected source rows,
   matching binding-ID rows, and retained document captures
   (`validation.py:388-445`). Parent references conservatively include all child
   owners; child references include their owner. No invocation bypasses this on
   the path to `port.accept`; Runtime revalidates acceptance inputs and CAS.

## Per-ID source disposition and minimal owner

| Packet / ordinal | Original | Source finding / next owner |
| --- | --- | --- |
| 9211 / 132 | owned parent asset clear | Inherits `film = m1.film`; common M1 setup owner, before owned parent variant. |
| 9211 / 133 | owned parent transition clear | Same inherited setup; no transition-specific repair established. |
| 9211 / 134 | owned parent trim rebase | Same inherited setup; no trim-specific repair established. |
| 9211 / 135 | owned parent split rebase | Same inherited setup; no split-specific repair established. |
| 9211 / 136 | owned parent delete rebase | Same inherited setup; no delete-specific repair established. |
| 9211 / 137 | owned ambiguous owner/mixed edits | Same inherited setup; no ownership-specific repair established. |
| 9211 / 129 | scalar outbox/restart/inverse | Explicit alias to `m1.film` at scalar.py:17; common M1 setup owner. |
| 11789 / 2,3,4,5,6,7,8,9,10,11 | M1 ten | Direct `m1.film` consumers, including the auto fixture chain. |
| 11789 / 12,13,14 | D87 checkout three | `base_film = m1.film`, then checkout parent-only setup. |
| 11789 / 15,16,17 | D87 frontends three | Checkout `base_film`/`film` aliases; common M1 setup owner. |
| 9211 / 99 | rebind existing main transcript | Original transcript source is changed; word fixture/source owner. |
| 9211 / 101 | clear existing main transcript | Original transcript source is removed; word fixture/source owner. |

### Common M1 setup: a new declaration, not metadata turnover

`test_commit_runtime_m1.py:22-113` restores the captured film into an independent
realm, creates an empty `m1-journey` destination, and submits
`timeline.duplicate` followed by parent patches. It maps `shot-1` to `m1-shot-1`
and occurrences to fresh IDs. The canonical destination baseline has no child
clips. `native_timeline_duplicate.py:49-118` copies the source internal payload
and text bindings verbatim into fresh roots, preserves captures, and sets
`_copy_manifest`. It does not remap or reauthorize the historical `elementRef`.
Thus the final reopened `m1-shot-1/clip-1` cannot have an existing baseline clip
in this destination; `baseline is None` is sufficient to refuse. This proof does
not depend on aggregate dict inequality or guessing a changed transcript pin.

The six owned cases and scalar case cannot establish that their later operation
invalidated a source: their shared fixture must complete first. Later M1/D87
errors are also consistent with that earliest setup failure. The safe rows do
not expose a stack proving which later stage was reached, so none is promoted
to a functional verdict.

Minimum setup ownership is ONE `m1.film` migration, not edits to 23 bodies or
their expected replies. Required evidence for any faithful correction is an
existing genuine baseline/setup that preserves the original child declaration,
opaque values and topology while satisfying current fresh destination authority.
No such setup is established here. Reusing the old source timeline would avoid
new declaration creation but would abandon the prescribed genuine-bootstrap
migration; it is therefore not proposed as an authorized correction. Removing
the reference or comparing against the foreign source would change the required
behavior/authority. This is an explicit incompatibility in the present fixture
setup, for its owner to resolve within the existing decisions.

### Word originals: real bound-source changes

The historical fixture's original public-API constructor is available in Runtime
git history: `fa4f9cc76f^:tests/timeline_commit_film_fixture.py` (also
`4c65c3efd7`). Its first shot's transcript `_binding_descriptor` contains
`binding_id`, scope, head, media/hash, MIME/size and text; the first internal clip's
`elementRef.binding_id` uses the SAME binding argument. The current loader
restores the schema-31 captured backup; it does not reconstruct source data.
Runtime baseline `_image` retains stored payloads after digest verification;
`_text_bindings` verifies those legacy descriptors rather than normalizing them.

`test_commit_runtime_text_binding.py:245` selects that occurrence's
`{kind: transcript, slot: None}` and replaces it with `b'replacement transcript'`.
At line 342 the other original clears it. `native_text_binding.py:36-67` removes
the row on clear; on set it replaces media/hash/size/MIME and filters
`DERIVED_FIELDS`, explicitly including `binding_id`. Consequently, for the
original source shape, the matching historical basis binding row changes from
present to absent in BOTH commands; the set also changes real text/media bytes.
This is independently material to D12, regardless of unchanged pinned transcript
documents or source revision metadata. Claiming only a representation change
would be false. The exact actual archive/run row bytes are still UNKNOWN.

No faithful setup-only correction is proven for these two originals: choosing a
different binding would alter their exact target; deleting the historical child
reference would violate input preservation. The word owner needs existing safe
baseline/candidate binding and pin evidence establishing that the selected
descriptor is NOT that reference's dependency before retaining an acceptance
claim. Keep the originals' assertions; do not convert them to expected refusal.

## Why no validation patch

C0 section 4/D12 permits existing unresolved declarations only when their
referenced targets remain unchanged. D12a does not convert a new destination
declaration or changed bound transcript into an unrelated edit. C0 physical-image
identity also requires authenticated successor provenance; equal bytes or entity
IDs are insufficient. The materialization adapter can change revision metadata,
but the selected failures do not isolate a metadata-only mismatch. The validator
receives no general ordinary-execution lineage recorder, and its existing
source-bundle/restoration arguments must not become blanket source authority.

A future narrow projection repair needs existing safe evidence at the ACTUAL
validation boundary: exact baseline clip-presence and declaration/type equality;
separate project/timeline, owner/source-row, matching-binding and document-pin
comparisons; and authenticated physical predecessor/successor relation if a
revision changed. For these packets that evidence is absent. Do not rerun the
unchanged failures merely to rediscover this. Do not strip metadata, normalize
pins/revisions, whitelist copy markers or compare transcript text alone.

All original protections remain byte-identical, including
`test_commit_legacy_text_reference.py`'s create/modify/target-invalidating atomic
rejection, malformed/new reference, exact source image, retained document-pin,
clip-type and parameter checks. ABA/retry/inverse/no-write predicates and all
held candidates are untouched. A source fix, if later proven, still needs one
independent protected core review and exact meaningful MAIN originals before
merge. No product merge is proposed by this finding.

## Verification

- Static AST parse and in-memory `compile` only: PASS for 17 current source files
  and 14 HEAD counterparts; no imports or execution of those modules. HEAD byte
  and AST input/assertion conservation: 14/14 unchanged. Captured source equality:
  14/14 unchanged for each actual9211 and actual11789 tree.
- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/validation.py`:
  exit 0, `All checks passed!`.
- `/home/user/work/venv-agent/bin/python -m mypy --no-incremental --cache-dir /tmp/w-00fe139748/mypy-r1-legacy-basis astrid/sdk/timeline/validation.py`:
  exit 0, `Success: no issues found in 1 source file`.
- Parent/candidate diagnostics are the SAME invocation over byte-identical
  `validation.py`; no changed candidate exists and no separate passing result is
  claimed. Tool cache lives in private harness TMPDIR, not shared dependencies.
- `git diff --check`: exit 0. `git status --short`: empty.
- No pytest, collection, fixture/helper execution, probes, services, full suites,
  browser, render, install, originals execution, or direct git writes.
