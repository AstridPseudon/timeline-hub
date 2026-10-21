# Runtime raw OLD swap existing-carrier review

Date: 2026-10-21 UTC  
Scope: source-only reciprocal review of Runtime `f53bf58` and projection
candidate `449d13d`; no product edit, schema generation, pin, freeze, or
native qualification.

## Decision

**Runtime ACK: the existing private `raw_media_info` commit-port read is safe
to reuse for the bounded raw OLD operand without a Runtime change.** The
closed OLD alternative is exactly the existing `MediaManifestEntry` shape:

```json
{"media_id": "sha256:<64 lowercase hex>", "content_digest": "sha256:<same>"}
```

It belongs inside the existing `old_media` argument. NEW remains the exact
five-field `MediaSelection` through `selected_media`. This is a source ACK
only. It does not choose the Agent's eventual compatible widening/version,
and it does not authorize generation, pin, adoption, public endpoint/DTO,
or activation.

The current Agent implementation is not already compatible: its swap path
calls `_verified` for both `old_media` and `media`. That is the concrete
remaining Agent source work. It must be a bounded closed alternative, not a
conversion of the old positive into refusal. The existing raw OLD positive and
its parent/occurrence wire assertions remain OPEN and must stay strict.

## Existing Runtime carrier trace

The review checked `f53bf588bf70b0908e0bed5ccb7d91157771b6` (tree
`d82f37052847949e77c12e1704c3f27c6dd56a46`) at these source points:

| Requirement | Existing source and result |
| --- | --- |
| Request-declared capture | `RequestCommitPort.__declared` is the object walk of the request commands. `raw_media_info` requires the exact two-key pin and refuses unless that exact pin is declared. No caller duration, metadata, latest lookup, or managed-generation authority is accepted. |
| Project custody and one-FD verification | `MediaReads.raw_media_info` validates the request project/realm, joins the exact digest to `project_objects` with `relation='managed'`, opens one CAS descriptor, and `_verify_open_file`s its fd against the digest and catalogued size. Foreign, missing, referenced-only, or changed bytes refuse. |
| Transaction recheck | `RequestCommitPort.validate` requires the captured raw pin in the candidate manifest, checks captured object identity, and calls the same exact raw read again before acceptance. `_validate_closure` then independently validates the retained manifest media and bytes in the acceptance transaction. |
| Candidate-manifest retention | The raw read contributes to `authorized_media`; a candidate media pin not captured through the port is refused. The normal closure persistence stores the pin and dependency row. The raw pin therefore cannot be used as an unretained side input. |
| Exact NEW selection | `MediaReads.selected` requires exactly `asset`, `generation_id`, `variant_id`, `object_id`, and `catalog_digest`, resolves the project-owned completed generation/variant, verifies managed CAS bytes and intrinsic metadata, and rechecks the catalog digest. The port rechecks the selected result before acceptance. |
| Retry/restart | `TimelineCommitStore.accept` performs ledger lookup before provider/port execution. The existing raw-capture test proves exact retry after restart does not reread raw media. Projection candidate `449d13d` has the same transaction/ledger placement. |

This is enough Runtime custody for OLD. Runtime deliberately does not return
generation ID, variant ID, catalog digest, or intrinsic duration from the raw
read. Those would turn the raw object into a fabricated managed selection or
caller-supplied authority.

## Agent-side guards required by the ACK

Runtime's ACK is conditional on the eventual Agent branch preserving these
existing semantic guards:

1. Guard the original accepted-base clip row, its old asset alias, and its
   exact OLD manifest pin. A stale original base, changed clip binding, or
   changed old registry binding refuses before mutation. The request's
   `base_revision_id`/`base_publication_id` remains the outer head pair; no
   new base DTO is needed.
2. Call `raw_media_info(old_media)` only for the exact declared OLD pin. Do
   not pass a `MediaSelection`, derive a latest generation, or use caller
   metadata/duration.
3. Call `selected_media(media)` for NEW and keep its exact five-field shape.
   The NEW alias is created from that verified result if absent, or is
   accepted only when its existing binding is exactly equal. A conflicting
   occupied NEW alias refuses atomically.
4. Keep the OLD alias, sibling/other clips, and the authored source window
   unchanged; change only the target clip's asset binding plus the scoped NEW
   alias creation when required. The old source window is already part of the
   accepted original-base clip guard. Since the settled operation preserves
   that window, Runtime's intentionally metadata-free raw read is not a gap.
   If a future implementation instead demands a fresh OLD intrinsic-duration
   check, this carrier cannot provide it; that would be a separately reviewed
   widening, not permission to use caller duration.
5. Preserve recorder reads/selections/bindings/created IDs and the existing
   guarded inverse behavior: disjoint rebase may proceed, an intervening
   write including A→B→A must block inverse, and reload/exact retry must not
   regenerate or create a second alias.

The current Agent `_swap` calling `_verified` for OLD is therefore a precise
source mismatch, not evidence that Runtime needs a new endpoint, DTO, table,
or raw carrier. The proposed boundary fake is useful design evidence only;
it is not a Runtime positive.

## Candidate 449 projection review

`runtime_protocol/timeline_commit_reference_projection.py` is orthogonal to
clip/alias swap semantics. It projects only the accepted parent carrier's
`config.app.astrid.timeline_references` into the existing reference rows and
snapshot. It does not supply the OLD clip, old alias, source window, or
original-base guards, and must not be treated as doing so.

Its source is compatible with this ACK:

- `_desired` requires a closed source reference and exactly one matching
  media pin in the accepted manifest;
- `prepare_reference_projection` compares the candidate with the immediately
  previous accepted carrier and requires an exact live-row ownership match for
  occupied IDs and removals, while retaining unrelated rows;
- `accept` computes the projection after normal closure validation and under
  the existing serialized transaction; `_publish` advances the timeline
  version, then `apply_reference_projection` checks the expected next version
  and writes the projection in that same transaction;
- a projection refusal rolls back the closure/publication as one transaction,
  and ledger-first retry returns the original result without rerunning the
  provider.

Thus candidate 449 neither weakens nor replaces the raw swap guards. It is
safe as an existing projection consumer, but it is not evidence of a native
raw OLD swap success.

## Evidence and limits

Direct no-socket targeted run on this Runtime worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  --timeout=60 tests/test_timeline_raw_capture.py \
  tests/test_timeline_unplaced_reference_projection.py
10 passed in 1.84s
```

The source tests exercise the actual Runtime port and projection, but their
provider is the approved ephemeral acceptance setup; they do not qualify the
normal Agent provider's future raw-OLD source generation path. No full,
socket, browser, schema-matrix, or repeat raw-carrier qualification was run.
No Runtime files were changed by this review.

## Handoff

Agent may proceed with the exact `MediaManifestEntry` OLD union branch and
choose the non-reused compatible operation spelling/version after its own
paired source review. Do not freeze or generate from this ACK. App should
retain its current writer/draft until the actual native Agent+Runtime proof;
this review supplies only the bounded source/carrier disposition.
