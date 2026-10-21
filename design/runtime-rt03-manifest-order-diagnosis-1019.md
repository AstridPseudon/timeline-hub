# RT03 manifest-order diagnosis

Status: diagnosis complete; no Runtime production change and no new native
qualification run. The first corrected RT03 attempt reached the native
reference body and stopped at the unchanged assertion on
`tests/test_timeline_owned_reference_integration.py:160`. The failure is an
invalid fixture-order premise, not a custody or film-loss witness.

## Finding

The expected order in the prepared test was `[unrelated_pin, exact_pin]`
because setup creates the unrelated raw object first (`tests/test_timeline_owned_reference_integration.py:137-145`). That is not the order contract for
the canonical `dependency_manifest.media` collection.

The exact fixture inputs are:

```text
unrelated_pin = {
  "media_id": "sha256:9b6dd332e72cde4e15dd61662c430434cc97bf61d231724f4066d02c9cffdbee",
  "content_digest": "sha256:9b6dd332e72cde4e15dd61662c430434cc97bf61d231724f4066d02c9cffdbee"
}
exact_pin = {
  "media_id": "sha256:6e2ea6a28550bd8e44021d028e97191f3ef94e06e7b1b0b185d95c7643018b10",
  "content_digest": "sha256:6e2ea6a28550bd8e44021d028e97191f3ef94e06e7b1b0b185d95c7643018b10"
}
```

Lexicographic `media_id` order is therefore `[exact_pin, unrelated_pin]`.
The failed run observed exactly that result in the assertion diff. Both full
pin objects are present; only their collection order differs.

## Causal trace

1. Setup ingests both same-project raw objects and builds one command per
   reference. `_media` returns the exact two-field pin at lines 92-99, and
   `_reference_command` passes that pin as the command's `media` argument with
   the Runtime-verified raw-media memo at lines 101-113. The first commit is
   the unrelated reference (`137-140`); the second is the exact reference
   (`142-146`). This establishes authored/fixture chronology, not a manifest
   ordering promise.

2. Agent's native command accepts exactly one pin and records it as the
   `reference.media` dependency (`/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/native_parent_reference_commands.py:103-119`; the handler records the dependency at `:66-99`). It does not sort or retain a cross-reference insertion sequence in the command itself.

3. Agent's canonical compiler collects retained and newly captured media into
   a keyed map, with the prior media first and the publication media updating
   it (`/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/commit.py:349-376`). The canonical manifest helper then explicitly returns
   `"media": sorted(media, key=lambda row: row["media_id"])`
   (`/home/user/work/wt/agt-pin-6c1989ad/astrid/sdk/timeline/commit.py:60-72`).
   `document_from_bundle` verifies that exact canonical result at
   `:127-146`. This is deterministic canonical manifest enumeration, not
   arbitrary dict order and not user-visible reference order.

4. Upstream Main's authoring compiler applies the same rule before the
   Runtime-facing publication is formed: it gathers media identities into a
   set and calls `sorted(...)` (`/home/user/work/wt/agt-pin-6c1989ad/astrid/core/timeline/authoring_bundle.py:1065-1085`), then emits the media manifest in that order at `:1145-1149`. Thus the
   Agent rule is inherited from the normal source/compiler contract.

5. Runtime acceptance does not re-sort or reorder the candidate. The commit
   store requires `manifest["media"]` already to equal
   `sorted(..., key=lambda item: item["media_id"])` at
   `runtime_protocol/timeline_commit_store.py:549-559`, then verifies each
   exact managed CAS object at `:554-567`. Acceptance validates the candidate
   before persistence at `:888-930`; `_persist_closure` stores the canonical
   manifest bytes and creates dependency rows in manifest-list order at
   `runtime_protocol/timeline_commit_store.py:1057-1076`.

6. Runtime readback retains that same list order. `revision_closure` loads the
   stored `commit_manifest_json` and appends its pinned closure rows in manifest
   order (`runtime_protocol/timeline_commit_store.py:324-355`). The normal
   closure verifier also requires sorted media order
   (`runtime_protocol/timeline_commit_baseline.py:192-204`). The separate
   legacy `timeline_revisions.references_json` projection is sorted by
   reference identity at `runtime_protocol/timeline_commit_reference_projection.py:130-175`; that is a read-model order and is not the order asserted at
   line 160 for `dependency_manifest.media`.

## Test disposition

The only test edit is the oracle originally at
`tests/test_timeline_owned_reference_integration.py:160` (now line 162): it now expects the
explicit one-to-one mapping `[exact_pin, unrelated_pin]`, with both complete
pin objects preserved. The assertion does not sort either side, compare sets,
drop fields, or weaken equality. All later RT03 guarantees remain unchanged:
raw ownership, no placement, role/id, receipt, retry, restart, duplicate and
occupied refusal, foreign zero-write refusal, and inverse preservation.

No production source, immutable tuple, schema, generated client, pin, or lock
was changed. No target-body, sibling ordered run, HTTP/socket, browser,
renderer, install, or full suite was run after diagnosis. The corrected target
must receive the manager's independent assertion-conversion review before any
later execution.

## Pure probe

The source-level result was also checked without Runtime setup or target-body
execution:

```text
sha256(b"unrelated-owned-raw") = 9b6dd332e72cde4e15dd61662c430434cc97bf61d231724f4066d02c9cffdbee
sha256(b"exact-owned-raw")     = 6e2ea6a28550bd8e44021d028e97191f3ef94e06e7b1b0b185d95c7643018b10
_manifest([], [], [unrelated_pin, exact_pin], [])
    -> media == [exact_pin, unrelated_pin]
```

This probe exercises the pure Agent `_manifest` rule; Runtime acceptance and
readback conclusions above are from the cited normal-source checks and the
single observed failure, not from a second body execution.
