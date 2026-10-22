# Timeline commit contract v2 (C0)

Normative contract for PLAN v2.1 §2, 22 October 2026. Runtime is the only writer;
the Python Agent provider computes semantics, validation, rebase and inverses.
App, CLI, Python, scripts and sheets submit the same commit operation. There is
no TypeScript executor, document overwrite route or force-conflict option.
Changes to this contract require the orchestrator. C0 supplies the contract for
approval; this document does not claim implementation or approval has occurred.

This extends the existing `commitTimeline` engine, not a second store or journal.
The document version is v2; request `api_version: 1`, command `schema_version: 1`
and canonical-document `schema_version: 1` remain the existing ABI versions.
The generated request/reply schemas must explicitly adopt the fields and enums
below before consumers send them. In particular, v2 uses success `merged` where
the existing implementation says `rebased`; retain `rebased_onto` as the existing
head-pin field. An old provider must reject unsupported input rather than
silently ignoring merge policy, reads or steps. This is a coordinated schema
and client change, not a promise that the frozen R4 provider accepts v2 input.
Runtime's coordinator/port outcome validation must adopt `invalid` failures and
`merged` successes along with the generated DTOs; its present failure check only
admits `conflict`/`refused`. This document does not change those checks by itself.

Read against Runtime `cc7410a1f` (`timeline_commit_store.py`,
`timeline_commit_execution.py`) and Agent hub integration
`a086cc6db7928dc4a3516d304dd9a472b050f1cf` (`commands.py`, `commit.py`, including
its preview/accept branch at line 1061). Frozen R4 `commands.py`/`commit.py` were
also inspected; the line-1061 reference belongs to integration, not frozen R4.
Runtime's existing acceptance transaction, publisher-bound request hashing,
per-scope idempotency, verified closure, CAS and history chain remain authoritative.

Examples are finite JSON: complete HTTP bodies/envelopes where stated, otherwise
named fixture fragments or input/expected-output scenarios. A fragment is not an
HTTP body. Revision/publication/principal IDs are fixture identities. Receipt
request hashes are illustrative 64-digit values; a live Runtime calculates them
from the authenticated invocation. Content and document digests in the complete
reply examples are calculated from their actual JSON values using Runtime's
canonical JSON spelling (sorted keys, compact separators, UTF-8). The examples
are executable test inputs for implementation tasks; parsing them does not prove
that those tasks have implemented the specified behavior.

## 1. Request: base, commands, label, steps, merge, reads and idempotency

Use the existing `commitTimeline` route, scoped by `project_id`/`timeline_id`.
Its HTTP `Idempotency-Key` is required for a mutation. The base is the exact pair
`base_revision_id`/`base_publication_id` in that scope, not a content digest or
local revision counter. Equal document bytes at a later publication are a new
base. Runtime verifies membership, authorization, the base pair and ancestry.

Required body fields remain `api_version`, both scope IDs, both base IDs and a
nonempty `commands` array. New App/Agent producers supply a nonempty `label` and
nonempty `steps` array. For compatibility with existing ABI-1 callers, omission
of `label` normalizes to `Timeline edit`; omission of `steps` synthesizes one
step (`id: "edit"`, the commit label, empty intent/tags, all command ordinals)
whose complete patch the provider derives. Explicit empty/null label or steps
is invalid. Thus every accepted commit has a label and step patches, including
requests from existing semantic callers. `source`, `rationale` and `group_id`
retain their existing meanings as caller-supplied annotations. `dry_run` defaults
to false. `merge` accepts only `fields` or `atomic` and defaults to `fields`,
preserving existing native semantic rebase with captured dependencies. The
conservative patch-read rule below can make its effective mode `atomic`.
Unknown control fields/enums are invalid; open document fields stay preserved.

Commands execute in array order as one transaction. They may mix native semantic
commands (including move, trim, set, split, ripple and per-occurrence fork when
registered by the provider) and the single generic operation type `doc.patch`.
Multiple instances of `doc.patch` are allowed, for example one for each of ten
notes. This contract does not invent semantic op names for unregistered recipes.
Native commands retain their existing `op`/`version`/`select`/`args` envelope.
The provider records all authored and derived effects and checks the final
candidate's timing, structure, parameter schemas, references and media inputs.
Temporary intermediate states may violate final document constraints; guards
and path resolution must still hold at each change. Any failure rejects the
whole batch, including its steps; `fields` never means partial acceptance.

Each step contains a stable unique `id` within the commit, `label`, `intent`
(string), `tags` (unique strings), `command_ordinals` (zero-based command indices)
and `patch` (an array of changes using §2). Steps partition the command array
into nonempty contiguous runs in execution order. Each command belongs to
exactly one step. A helper that needs independent undo of ten notes emits ten
commands/steps in one request. All changes of a command share its step.

For `doc.patch`, the submitted step patch must equal its commands' ordered
changes. For semantic commands, it contains any caller-asserted expected effects
and may be empty; assertions must match authoritative execution. The provider
fills the accepted step patch with the complete actual changes, including
compiler consequences. Step patches are checked claims, never instructions to
apply a second edit. Semantic commands need not predict compiler output in
order to be submitted. Replies, previews and history always contain complete
provider-derived step patches with actual before values at the landing head.

`reads` is an optional array of the field/collection/scope dependencies defined
in §3, additional to all reads the provider captures for semantic commands.
Explicit `reads: []` declares that a free transform consulted no other state
besides its guarded patch operands. Omitting `reads` is different: Runtime
cannot infer what a script consulted. A request containing `doc.patch` with
omitted `reads` has effective mode `atomic`, even if it asked for `fields`, and
guards the complete touched document scopes. The result reports `merge_mode`.
A script consulting another scope must declare it; use a closure-scope read
when the consulted set cannot be bounded. The SDK must choose this conservative
form when it cannot capture reads, not invent `reads: []` after diffing bytes.

Complete request body (`Idempotency-Key: edit-7`):

```json
{
  "api_version": 1,
  "project_id": "project-1",
  "timeline_id": "film-1",
  "base_revision_id": "rev-0",
  "base_publication_id": "pub-0",
  "commands": [
    {
      "schema_version": 1,
      "op": "doc.patch",
      "version": "1",
      "select": null,
      "args": {
        "changes": [
          {
            "op": "set",
            "ref": "parent",
            "path": [
              "clips",
              "id:clip-1",
              "meta",
              "org.example.notes",
              "note"
            ],
            "before": {
              "state": "present",
              "value": "A"
            },
            "value": "B"
          }
        ]
      }
    }
  ],
  "label": "Clarify opening note",
  "steps": [
    {
      "id": "note-1",
      "label": "Revise the first note",
      "intent": "Clarify the opening",
      "tags": [
        "notes"
      ],
      "command_ordinals": [
        0
      ],
      "patch": [
        {
          "op": "set",
          "ref": "parent",
          "path": [
            "clips",
            "id:clip-1",
            "meta",
            "org.example.notes",
            "note"
          ],
          "before": {
            "state": "present",
            "value": "A"
          },
          "value": "B"
        }
      ]
    }
  ],
  "merge": "fields",
  "reads": [],
  "dry_run": false,
  "source": {
    "via": "python",
    "detail": "notes.py"
  }
}
```

Runtime authorizes before returning a replay. The idempotency scope remains
(project, timeline); the canonical request identity includes the operation,
route, authenticated publisher and the entire body, including base, label,
steps, reads, merge and dry-run. The first durable accepted result for a key is
the winner. An exact retry, including after lost acknowledgement or restart,
returns that same `{data, receipt}` without rerunning effects or adding history.
The same key with a changed body or principal is `idempotency_mismatch` (409),
never a second edit. Concurrent identical requests serialize through the
existing execution coordinator and acceptance lookup. Authorization is still
required on retries. A transport failure or 503 `not_ready` is an unknown
outcome: retry the exact request/key before deciding to roll back or resubmit.

Rebase retries keep the original request/key and are bounded (the existing
provider tries at most three head-CAS attempts). A `tl.commit(fn)` conflict
re-run reads the returned head and reruns the function, at most three total
function evaluations by default; each changed request gets a fresh key. Do not
rerun a function merely because its previous request's outcome is unknown.
Outbox dependents retain stable created IDs and chain from the predecessor's
canonical landed document/pair; a refused predecessor requires revalidation
against the actual head or rollback with a message. A preview cannot be an
outbox predecessor's accepted base.

## 2. `doc.patch`: closure addressing and previous-value semantics

`doc.patch` has `select: null`, `version: "1"` and `args: {"changes": [...]}`.
A change has `op`, `ref`, `path`, and tagged `before`. `set` additionally has
`value`; `remove` does not. Paths are arrays of string tokens, never dotted
expressions, JSON Pointer escapes or numeric array indices. Object tokens are
literal keys, so dots and colons in an object key have no special meaning.
An empty path identifies the addressed payload root, subject to the ownership
restrictions below. Missing ancestors are not implicitly made: first set the
missing object, then set its child, or set the complete new object in one change.

Addressable closure roots are:

| `ref` | Authored value addressed | Atomic touched scope |
| --- | --- | --- |
| `parent` | Parent composition payload, including config, clips, occurrences and registry | Parent payload |
| `shot:<shot_id>` | One reachable shot payload | That shot payload |
| `internal:<timeline_id>` | One reachable child timeline payload | That child payload |

These roots address payloads of the verified base closure; commands never write
`CanonicalDocument` image wrappers, project/timeline identity, revision IDs,
content digests, dependency manifests, receipts, history or authorization.
Root `set` is a guarded replacement of an existing payload, validated with all
other changes, not a publication overwrite. Root `remove` is invalid. A missing
shot/internal root cannot be invented by choosing a ref. Closure creation,
attachment, detachment and per-occurrence fork use provider semantic commands;
subsequent patches in the same batch can address roots those commands created.
Patching entity membership inside an existing root is supported generically.
New media/documents must already be Runtime-verified inputs, not caller-forged
manifest pins or CAS identities. Ordinary asset registration metadata can be
patched only when its references verify against those inputs.

Occurrence rows are addressed under `parent` at
`["occurrences", "occurrence_id:<id>", ...]`. Their shot identity/revision links
and shot-to-internal revision links are provider-managed closure edges, not
ordinary patchable properties; use semantic creation/fork/attachment operations.
Existing edges are preserved verbatim until the provider regenerates their
revision pins for a changed child. A changed shared shot affects every occurrence
of it; clients wanting occurrence-local ownership must fork first. No implicit
fork is performed by a field patch.

Existing native entity addresses (`parent/clip:<id>`,
`parent/track:<id>`, `occurrence:<id>/clip:<id>`,
`occurrence:<id>/track:<id>`, `occurrence:<id>/shot`, and occurrence source
addresses) normalize to the same physical roots/paths for guards, conflicts,
history and undo. Parent `clips`/`config.clips` and registry mirrors likewise
have one logical identity. The provider updates required mirrors; a client may
not write contradictory copies. Alias normalization must happen before overlap
checks: editing the same shared child through two occurrences is not disjoint.
A ref outside the authenticated closure is `outside_closure`.

For an array whose schema gives items a unique string `id`, an element token is
`id:<literal-id>`. For the occurrence array it is
`occurrence_id:<literal-occurrence-id>`. Split a token at its first colon only.
The identity key comes from the schema, never from a caller-chosen heuristic.
Duplicate/missing identity keys in an identity collection are invalid. A token
which looks like an index remains an ordinary key in an object, but is invalid
as array traversal. IDs themselves cannot be changed by setting an `id` field:
remove and create a different item with appropriate guards instead.
`set` at an existing item token may replace that complete item only with the same
ID. Inserting an absent item with `set`, or removing an item with plain `remove`,
is invalid: use the corresponding `list.*` operation and its order guard.
Whole-array/ancestor replacement is allowed with a complete tagged `before`;
its authoritative diff still records membership/order effects and checks all
introduced IDs and references. It cannot bypass allocation or closure rules.

Tagged values have exactly one of these forms (fixture fragment):

```json
{
  "missing": {"state": "absent"},
  "explicit_null": {"state": "present", "value": null},
  "empty_object": {"state": "present", "value": {}},
  "empty_list": {"state": "present", "value": []}
}
```

`set` with `value: null` writes explicit JSON null, permitted only where the
schema allows it. `remove` is the explicit clear: it removes an optional key,
not sets it to null. Clearing required keys is invalid. A missing `value` in
`set` is invalid. `remove` requires present `before`; clearing an already absent
key is invalid (`previous_value_mismatch`), so redundant clears are not silently
accepted. No unspecified key is cleared or default-filled. Unknown keys are
preserved when another key changes.

Every `before` must exactly match the authored input at that position in the
sequential base execution (including earlier commands/changes). Object key order
is irrelevant; arrays are ordered; numbers compare numerically but booleans do
not equal numbers. All JSON must be finite. Object replacement guards all its
descendants, not only keys that differ; an item/ancestor replacement overlaps a
descendant edit. A wrong `before` on the original base is invalid; a correct base
guard that fails on a later head is a conflict. Schema/timing validation runs
against the completed candidate; acceptance must not silently drop an effect.

Absent → null → absent, with an existing namespace object (patch fragment):

```json
{
  "changes": [
    {
      "op": "set", "ref": "parent",
      "path": ["meta", "org.example.notes", "reviewed"],
      "before": {"state": "absent"}, "value": null
    },
    {
      "op": "remove", "ref": "parent",
      "path": ["meta", "org.example.notes", "reviewed"],
      "before": {"state": "present", "value": null}
    }
  ]
}
```

All intermediate effects are recorded even if the final value equals its input;
that equality does not erase read/write history or create undo authority.

Ordered identity arrays have three structural operations in addition to field
edits: `list.insert`, `list.remove`, `list.move`. Their `ref`/`path` identify the
array; `id` identifies the item. `before` is absent for insertion, or the complete
present item for removal/move. All three include `order_before`, the exact array
of IDs immediately before the operation. `list.insert` includes the new complete
`value` (whose identity equals `id`). Insert/move include `after_id`: null means
start, otherwise immediately after an existing item (never after itself).
For a move, locate the anchor after removing the moved item. `order_before`
implies an ordered collection read (§3). No last-writer-wins insertion tie rule
exists: concurrent membership/order edits conflict. Removing one item guards its
whole value, so a concurrent edit inside that item also conflicts. Other items'
fields remain mergeable when no field/value read covers them.

Structural patch fragments and expected final order:

```json
{
  "initial": [{"id": "a", "kind": "video"}, {"id": "b", "kind": "video"}],
  "changes": [
    {
      "op": "list.insert", "ref": "parent", "path": ["config", "tracks"],
      "id": "c", "before": {"state": "absent"},
      "order_before": ["a", "b"], "after_id": "a",
      "value": {"id": "c", "kind": "video"}
    },
    {
      "op": "list.move", "ref": "parent", "path": ["config", "tracks"],
      "id": "b", "before": {"state": "present", "value": {"id": "b", "kind": "video"}},
      "order_before": ["a", "c", "b"], "after_id": null
    },
    {
      "op": "list.remove", "ref": "parent", "path": ["config", "tracks"],
      "id": "c", "before": {"state": "present", "value": {"id": "c", "kind": "video"}},
      "order_before": ["b", "a", "c"]
    }
  ],
  "expected_ids": ["b", "a"]
}
```

An id-less array (scalars, tuples, mixed rows, or rows without a schema-defined
stable key) is a single atomic field. Replace/remove that whole field with a
complete `before`; element traversal and `list.*` are refused
(`idless_list_address`). Never infer IDs from names or values. Whole-array
replacement remains available, including for unknown extension arrays.

Id-less-list scenario (the valid changes and invalid change are separate cases):

```json
{
  "initial": {"meta": {"org.example.notes": {"tags": ["rough", "review"]}}},
  "valid": {
    "op": "set", "ref": "parent", "path": ["meta", "org.example.notes", "tags"],
    "before": {"state": "present", "value": ["rough", "review"]},
    "value": ["approved"]
  },
  "invalid": {
    "op": "set", "ref": "parent", "path": ["meta", "org.example.notes", "tags", "0"],
    "before": {"state": "present", "value": "rough"}, "value": "approved"
  },
  "expected_invalid_code": "idless_list_address"
}
```

Creation uses caller-generated stable IDs (also across outbox retries). Native
`created` claims list the canonical entity refs; a `doc.patch` introducing a known
entity must declare its created refs in the same command envelope. The provider
verifies claims and records allocation ownership. The existing reservation
checks apply across the timeline's full allocation history, not merely live
membership: deleting an entity does not free its ID for another creation.
A collision at the original base is invalid; a concurrent allocation is conflict.
Only a verified inverse of that entity's deletion may restore its reserved ID.
No implicit renaming/remapping occurs; `id_map` contains only identity pairs (or
is empty). Arbitrary strings/keys inside `meta` are not reserved entity IDs.

Created-ID command fragment:

```json
{
  "schema_version": 1, "op": "doc.patch", "version": "1", "select": null,
  "created": ["parent/track:track-2"],
  "args": {"changes": [{
    "op": "list.insert", "ref": "parent", "path": ["config", "tracks"],
    "id": "track-2", "before": {"state": "absent"},
    "order_before": ["track-1"], "after_id": "track-1",
    "value": {"id": "track-2", "kind": "video"}
  }]}
}
```

## 3. Conflicts: fields, collection reads and atomic scopes

The provider first verifies/executes the request at its base, then obtains the
verified contiguous ancestry from that publication through the current head.
Missing ancestry or unrecorded/legacy effects cannot be assumed empty:
`history_unavailable` (409) requires a fresh read/decision. Every retry repeats
head-sensitive guards. Runtime accepts only against the exact evaluated head
pair with CAS; it never updates an obsolete candidate unconditionally.

For effective `fields`, conflict if a later publication wrote a guarded field
or item, or an ancestor/descendant of it. This includes deletes/replacements,
identity rebinding and equal-value A→B→A changes; comparisons of final bytes alone
are insufficient. Reapplying the request against the head must also pass all
previous-value checks. Disjoint fields in the same object/item can merge.
An item field write guards existence and identity of that item, but does not
implicitly read all sibling fields or sibling ordering. Ordered `list.*` does
read collection shape, as specified above. Provider semantic reads and derived
writes participate in exactly the same conflict checks as patch effects.

Declared read variants (fixture fragments; reads in a request are evaluated at
its original base, before any commands):

```json
{
  "field": {
    "kind": "field", "ref": "parent", "path": ["config", "fps"],
    "state": {"state": "present", "value": 30}
  },
  "ordered_collection": {
    "kind": "collection", "ref": "parent", "path": ["clips"],
    "members": ["clip-1", "clip-2"], "order": ["clip-1", "clip-2"]
  },
  "membership_only": {
    "kind": "collection", "ref": "parent", "path": ["clips"],
    "members": ["clip-1", "clip-2"], "order": null
  },
  "whole_child": {"kind": "scope", "ref": "internal:child-1", "path": []},
  "whole_closure": {"kind": "scope", "ref": "timeline", "path": []}
}
```

A field read is a tagged exact-value guard. Collection `members` is the complete
set of IDs in that collection, represented as a unique sorted string array;
non-null `order` is their complete ordered sequence. Membership changes always
conflict for a collection read; order changes also conflict if `order` is
non-null. It guards the full collection, not just selected items; declare field
reads too if a filter consulted item properties. A collection read does not
by itself guard item contents. For an id-less array use a field read of the
entire array. Scope reads guard the complete addressed payload; `timeline`
means the whole closure and is read-only. Base closure image pins supply scope
state; clients do not manufacture digests for scope reads. Any overlapping
intervening change conflicts even if the current state/order equals the base.
Incorrect declared reads at the original base are invalid.

For effective `atomic`, derive touched scopes from every read, write and created
entity (including semantic consequences), normalized to parent, shot and child
payloads. Any intervening change anywhere in those complete scopes conflicts;
the batch can merge only across untouched scopes. Parent changes to a child
revision pin solely caused by materializing an otherwise untouched child are
not authored parent changes; the actual child scope carries that write. A scope
read of `timeline`, explicit parent root replacement or unknown legacy scope
requires conservative guarding of the whole affected closure. No caller can
shrink a touched scope by claiming narrower reads than the generated effects.

Conflict scenarios (each starts independently at its specified base):

```json
[
  {
    "case": "disjoint_fields", "merge": "fields", "reads": [],
    "ours": "parent clip-1 note A -> B",
    "theirs": "parent track-1 label Picture -> Opening",
    "expected": "merged", "preserve_theirs": true
  },
  {
    "case": "same_field", "merge": "fields", "reads": [],
    "ours": "parent clip-1 note A -> B",
    "theirs": "parent clip-1 note A -> C",
    "expected": "conflict", "reason": "value_conflict"
  },
  {
    "case": "collection_membership", "merge": "fields",
    "read": {"kind": "collection", "ref": "parent", "path": ["clips"], "members": ["clip-1"], "order": ["clip-1"]},
    "theirs": "insert clip-2", "expected": "conflict", "reason": "selection_changed"
  },
  {
    "case": "collection_order", "merge": "fields",
    "read": {"kind": "collection", "ref": "parent", "path": ["clips"], "members": ["clip-1", "clip-2"], "order": ["clip-1", "clip-2"]},
    "theirs_order": ["clip-2", "clip-1"],
    "expected": "conflict", "reason": "selection_changed"
  },
  {
    "case": "undeclared_transform", "requested_merge": "fields", "reads_omitted": true,
    "ours": "parent clip-1 note A -> B", "theirs": "parent track-1 label Picture -> Opening",
    "effective_merge": "atomic", "expected": "conflict", "reason": "atomic_scope_changed"
  },
  {
    "case": "explicit_atomic", "merge": "atomic", "reads": [],
    "ours": "parent clip-1 note A -> B", "theirs": "parent track-1 label Picture -> Opening",
    "expected": "conflict", "reason": "atomic_scope_changed"
  }
]
```

## 4. Replies: accepted, merged, conflict, invalid and dry-run

Success keeps the existing `{data, receipt}` envelope. A non-null durable receipt
is the acceptance authority. `data.status` is `accepted` when the landed previous
head equals the requested base, or `merged` when a disjoint later head was used.
Both include the complete canonical closure, digest, normalized commands,
identity map, provider/compiler versions, complete steps, effective `merge_mode`,
base IDs, previous head IDs, accepted revision and authoritative `publisher`.
The resulting publication ID is `receipt.receipt_id`; receipt `result` is the same
accepted data. `rebased_onto` is null for accepted, the landing head for merged.
Source/label/rationale/group annotations are echoed when supplied. Merged replies
contain the other party's changes in `canonical_document`; clients adopt that
whole result before replaying still-pending local edits.

Complete accepted envelope for §1's request at pub-0:

```json
{
  "data": {
    "status": "accepted",
    "base_revision_id": "rev-0",
    "base_publication_id": "pub-0",
    "previous_revision_id": "rev-0",
    "previous_publication_id": "pub-0",
    "accepted_revision_id": "rev-1",
    "rebased_onto": null,
    "canonical_document": {
      "schema_version": 1,
      "project_id": "project-1",
      "timeline_id": "film-1",
      "parent_revision": {
        "revision_id": "rev-1",
        "content_digest": "sha256:04967dfe604339e5d7b10f29a9ae64caa2efd93b12271a400d803896c484908f",
        "payload": {
          "config": {
            "fps": 30,
            "tracks": [
              {
                "id": "track-1",
                "kind": "video",
                "label": "Picture"
              }
            ]
          },
          "registry": {},
          "clips": [
            {
              "id": "clip-1",
              "clipType": "video",
              "track": "track-1",
              "at": 0,
              "hold": 2,
              "meta": {
                "org.example.notes": {
                  "note": "B"
                }
              }
            }
          ],
          "occurrences": []
        }
      },
      "shot_revisions": [],
      "internal_timeline_revisions": [],
      "dependency_manifest": {
        "shots": [],
        "internal_timelines": [],
        "media": [],
        "documents": []
      }
    },
    "document_digest": "sha256:3bf2315c305dfba115efc48ca54207a0ec13765ccdf7029d77e6633f60280a0e",
    "commands": [
      {
        "schema_version": 1,
        "op": "doc.patch",
        "version": "1",
        "select": null,
        "args": {
          "changes": [
            {
              "op": "set",
              "ref": "parent",
              "path": [
                "clips",
                "id:clip-1",
                "meta",
                "org.example.notes",
                "note"
              ],
              "before": {
                "state": "present",
                "value": "A"
              },
              "value": "B"
            }
          ]
        }
      }
    ],
    "id_map": {},
    "provider_version": "provider-v2",
    "compiler_version": "compiler-v2",
    "merge_mode": "fields",
    "steps": [
      {
        "id": "note-1",
        "label": "Revise the first note",
        "intent": "Clarify the opening",
        "tags": [
          "notes"
        ],
        "command_ordinals": [
          0
        ],
        "patch": [
          {
            "op": "set",
            "ref": "parent",
            "path": [
              "clips",
              "id:clip-1",
              "meta",
              "org.example.notes",
              "note"
            ],
            "before": {
              "state": "present",
              "value": "A"
            },
            "value": "B"
          }
        ]
      }
    ],
    "publisher": "principal-7",
    "label": "Clarify opening note",
    "source": {
      "via": "python",
      "detail": "notes.py"
    }
  },
  "receipt": {
    "receipt_id": "pub-1",
    "command_kind": "timeline.commit",
    "idempotency_key": "edit-7",
    "request_hash": "0000000000000000000000000000000000000000000000000000000000000000",
    "project_id": "project-1",
    "project_seq": [
      2,
      2
    ],
    "event_ids": [
      "event-pub-1"
    ],
    "result": {
      "status": "accepted",
      "base_revision_id": "rev-0",
      "base_publication_id": "pub-0",
      "previous_revision_id": "rev-0",
      "previous_publication_id": "pub-0",
      "accepted_revision_id": "rev-1",
      "rebased_onto": null,
      "canonical_document": {
        "schema_version": 1,
        "project_id": "project-1",
        "timeline_id": "film-1",
        "parent_revision": {
          "revision_id": "rev-1",
          "content_digest": "sha256:04967dfe604339e5d7b10f29a9ae64caa2efd93b12271a400d803896c484908f",
          "payload": {
            "config": {
              "fps": 30,
              "tracks": [
                {
                  "id": "track-1",
                  "kind": "video",
                  "label": "Picture"
                }
              ]
            },
            "registry": {},
            "clips": [
              {
                "id": "clip-1",
                "clipType": "video",
                "track": "track-1",
                "at": 0,
                "hold": 2,
                "meta": {
                  "org.example.notes": {
                    "note": "B"
                  }
                }
              }
            ],
            "occurrences": []
          }
        },
        "shot_revisions": [],
        "internal_timeline_revisions": [],
        "dependency_manifest": {
          "shots": [],
          "internal_timelines": [],
          "media": [],
          "documents": []
        }
      },
      "document_digest": "sha256:3bf2315c305dfba115efc48ca54207a0ec13765ccdf7029d77e6633f60280a0e",
      "commands": [
        {
          "schema_version": 1,
          "op": "doc.patch",
          "version": "1",
          "select": null,
          "args": {
            "changes": [
              {
                "op": "set",
                "ref": "parent",
                "path": [
                  "clips",
                  "id:clip-1",
                  "meta",
                  "org.example.notes",
                  "note"
                ],
                "before": {
                  "state": "present",
                  "value": "A"
                },
                "value": "B"
              }
            ]
          }
        }
      ],
      "id_map": {},
      "provider_version": "provider-v2",
      "compiler_version": "compiler-v2",
      "merge_mode": "fields",
      "steps": [
        {
          "id": "note-1",
          "label": "Revise the first note",
          "intent": "Clarify the opening",
          "tags": [
            "notes"
          ],
          "command_ordinals": [
            0
          ],
          "patch": [
            {
              "op": "set",
              "ref": "parent",
              "path": [
                "clips",
                "id:clip-1",
                "meta",
                "org.example.notes",
                "note"
              ],
              "before": {
                "state": "present",
                "value": "A"
              },
              "value": "B"
            }
          ]
        }
      ],
      "publisher": "principal-7",
      "label": "Clarify opening note",
      "source": {
        "via": "python",
        "detail": "notes.py"
      }
    },
    "created_at": "2026-10-22T10:00:00Z"
  }
}
```

Complete merged envelope for that same request if pub-1 independently changed
track-1's label to `Opening`. The note becomes B and the other party's label
survives; the original base stays pub-0 and the actual predecessor is pub-1:

```json
{
  "data": {
    "status": "merged",
    "base_revision_id": "rev-0",
    "base_publication_id": "pub-0",
    "previous_revision_id": "rev-1",
    "previous_publication_id": "pub-1",
    "accepted_revision_id": "rev-2",
    "rebased_onto": {
      "revision_id": "rev-1",
      "publication_id": "pub-1"
    },
    "canonical_document": {
      "schema_version": 1,
      "project_id": "project-1",
      "timeline_id": "film-1",
      "parent_revision": {
        "revision_id": "rev-2",
        "content_digest": "sha256:c1fe2a5c5575702edad51f37da7f21805b6d8199d184adbcbb232ba8b1efd944",
        "payload": {
          "config": {
            "fps": 30,
            "tracks": [
              {
                "id": "track-1",
                "kind": "video",
                "label": "Opening"
              }
            ]
          },
          "registry": {},
          "clips": [
            {
              "id": "clip-1",
              "clipType": "video",
              "track": "track-1",
              "at": 0,
              "hold": 2,
              "meta": {
                "org.example.notes": {
                  "note": "B"
                }
              }
            }
          ],
          "occurrences": []
        }
      },
      "shot_revisions": [],
      "internal_timeline_revisions": [],
      "dependency_manifest": {
        "shots": [],
        "internal_timelines": [],
        "media": [],
        "documents": []
      }
    },
    "document_digest": "sha256:966674c611d1b1139cd6eacab70a0e45400f8d70ea2ff9b7ab24ac622e85d4af",
    "commands": [
      {
        "schema_version": 1,
        "op": "doc.patch",
        "version": "1",
        "select": null,
        "args": {
          "changes": [
            {
              "op": "set",
              "ref": "parent",
              "path": [
                "clips",
                "id:clip-1",
                "meta",
                "org.example.notes",
                "note"
              ],
              "before": {
                "state": "present",
                "value": "A"
              },
              "value": "B"
            }
          ]
        }
      }
    ],
    "id_map": {},
    "provider_version": "provider-v2",
    "compiler_version": "compiler-v2",
    "merge_mode": "fields",
    "steps": [
      {
        "id": "note-1",
        "label": "Revise the first note",
        "intent": "Clarify the opening",
        "tags": [
          "notes"
        ],
        "command_ordinals": [
          0
        ],
        "patch": [
          {
            "op": "set",
            "ref": "parent",
            "path": [
              "clips",
              "id:clip-1",
              "meta",
              "org.example.notes",
              "note"
            ],
            "before": {
              "state": "present",
              "value": "A"
            },
            "value": "B"
          }
        ]
      }
    ],
    "publisher": "principal-7",
    "label": "Clarify opening note",
    "source": {
      "via": "python",
      "detail": "notes.py"
    }
  },
  "receipt": {
    "receipt_id": "pub-2",
    "command_kind": "timeline.commit",
    "idempotency_key": "edit-7",
    "request_hash": "0000000000000000000000000000000000000000000000000000000000000000",
    "project_id": "project-1",
    "project_seq": [
      3,
      3
    ],
    "event_ids": [
      "event-pub-2"
    ],
    "result": {
      "status": "merged",
      "base_revision_id": "rev-0",
      "base_publication_id": "pub-0",
      "previous_revision_id": "rev-1",
      "previous_publication_id": "pub-1",
      "accepted_revision_id": "rev-2",
      "rebased_onto": {
        "revision_id": "rev-1",
        "publication_id": "pub-1"
      },
      "canonical_document": {
        "schema_version": 1,
        "project_id": "project-1",
        "timeline_id": "film-1",
        "parent_revision": {
          "revision_id": "rev-2",
          "content_digest": "sha256:c1fe2a5c5575702edad51f37da7f21805b6d8199d184adbcbb232ba8b1efd944",
          "payload": {
            "config": {
              "fps": 30,
              "tracks": [
                {
                  "id": "track-1",
                  "kind": "video",
                  "label": "Opening"
                }
              ]
            },
            "registry": {},
            "clips": [
              {
                "id": "clip-1",
                "clipType": "video",
                "track": "track-1",
                "at": 0,
                "hold": 2,
                "meta": {
                  "org.example.notes": {
                    "note": "B"
                  }
                }
              }
            ],
            "occurrences": []
          }
        },
        "shot_revisions": [],
        "internal_timeline_revisions": [],
        "dependency_manifest": {
          "shots": [],
          "internal_timelines": [],
          "media": [],
          "documents": []
        }
      },
      "document_digest": "sha256:966674c611d1b1139cd6eacab70a0e45400f8d70ea2ff9b7ab24ac622e85d4af",
      "commands": [
        {
          "schema_version": 1,
          "op": "doc.patch",
          "version": "1",
          "select": null,
          "args": {
            "changes": [
              {
                "op": "set",
                "ref": "parent",
                "path": [
                  "clips",
                  "id:clip-1",
                  "meta",
                  "org.example.notes",
                  "note"
                ],
                "before": {
                  "state": "present",
                  "value": "A"
                },
                "value": "B"
              }
            ]
          }
        }
      ],
      "id_map": {},
      "provider_version": "provider-v2",
      "compiler_version": "compiler-v2",
      "merge_mode": "fields",
      "steps": [
        {
          "id": "note-1",
          "label": "Revise the first note",
          "intent": "Clarify the opening",
          "tags": [
            "notes"
          ],
          "command_ordinals": [
            0
          ],
          "patch": [
            {
              "op": "set",
              "ref": "parent",
              "path": [
                "clips",
                "id:clip-1",
                "meta",
                "org.example.notes",
                "note"
              ],
              "before": {
                "state": "present",
                "value": "A"
              },
              "value": "B"
            }
          ]
        }
      ],
      "publisher": "principal-7",
      "label": "Clarify opening note",
      "source": {
        "via": "python",
        "detail": "notes.py"
      }
    },
    "created_at": "2026-10-22T10:00:00Z"
  }
}
```

Failures keep the existing `http_status`/`code`/`message`/`details` error shape
and have no acceptance receipt. The structured semantic `code`, `path` (JSON
tokens), `hint` and `suggested_command` live in `details`, with `status`, `reason`,
`base`, `current` and `conflicts`. The outer `code` stays the transport category
(`conflict` or `validation_error`). A conflict entry has normalized `ref`/`path`,
`kind`, tagged `base`/`theirs`/`ours`, and `choices` (empty when reauthoring is
required). For array-operation/collection conflicts those states describe the
full collection shape. A conflict always includes the actual head pair in
`details.current`; clients load that canonical closure using the existing read
operation before revalidation. No force/overwrite choice is offered.

Complete conflict envelope (409; no writes):

```json
{
  "http_status": 409, "code": "conflict", "message": "The note changed after your base",
  "details": {
    "status": "conflict", "reason": "value_conflict", "code": "value_conflict",
    "path": ["clips", "id:clip-1", "meta", "org.example.notes", "note"],
    "hint": "Read the current note and reapply the intended change",
    "suggested_command": "timeline show",
    "base": {"revision_id": "rev-0", "publication_id": "pub-0"},
    "current": {"revision_id": "rev-1", "publication_id": "pub-1"},
    "conflicts": [{
      "kind": "value_conflict", "ref": "parent",
      "path": ["clips", "id:clip-1", "meta", "org.example.notes", "note"],
      "base": {"state": "present", "value": "A"},
      "theirs": {"state": "present", "value": "C"},
      "ours": {"state": "present", "value": "B"}, "choices": []
    }]
  }
}
```

Invalid means the request cannot be valid at its claimed base, including malformed
patches, incorrect previous values, unsupported operations or final validation
failure. It is 422 with `details.status: "invalid"`. Include the failing document
path when known; for envelope errors use the request field path. `current` is
null only if validation happened before the authorized head could be loaded.
Do not turn a later-head guard failure into an invalid-base diagnosis.

Complete invalid envelope for the id-less-list case:

```json
{
  "http_status": 422, "code": "validation_error", "message": "Array items have no stable identity",
  "details": {
    "status": "invalid", "reason": "idless_list_address", "code": "idless_list_address",
    "path": ["meta", "org.example.notes", "tags", "0"],
    "hint": "Replace the whole tags array with its complete previous value",
    "suggested_command": "timeline edit",
    "base": {"revision_id": "rev-0", "publication_id": "pub-0"},
    "current": {"revision_id": "rev-0", "publication_id": "pub-0"},
    "conflicts": []
  }
}
```

Other stable reasons include `previous_value_mismatch`, `invalid_path`,
`invalid_document`, `invalid_steps`, `identity_collision`, `outside_closure`,
`managed_field`, `unsupported_operation`, `selection_changed`,
`atomic_scope_changed`, `inverse_conflict`, `intervening_write`,
`surviving_dependents`, `history_unavailable`, `head_busy` and
`idempotency_mismatch`. Classification follows origin: a malformed base request
is invalid, an intervening change is conflict. Legacy refusal reasons such as
`history_unavailable`, `head_busy` and `idempotency_mismatch` retain 409 with
`details.status: "refused"`, plus the structured code/path/hint/command. Auth and
availability errors retain existing HTTP semantics and cannot claim acceptance.

Dry-run extends the existing `port.preview(prepared)` path in Agent
`commit.py:1061`, not a client-only simulation. Send the same body with
`dry_run: true` and a separate key. Run the same authorization, base/ancestry,
read/previous-value, identity, schema and head checks; return the same conflict
or invalid forms if they fail. On success return `data.status: "preview"`,
`would_status: "accepted" | "merged"`, `evaluated_head`, candidate document/digest,
normalized commands, `id_map`, complete steps and `merge_mode`, with
`receipt: null`. Candidate revision IDs are provisional and cannot be used as
published base IDs. A preview persists no closure revisions, allocations,
events, history, receipt or durable idempotency winner, and moves no head.
An exact repeated preview may evaluate a newer head. Committing after preview
uses a new key and `dry_run: false`; it repeats validation and may conflict.

Complete successful merged-preview envelope:

```json
{
  "data": {
    "status": "preview",
    "would_status": "merged",
    "base_revision_id": "rev-0",
    "base_publication_id": "pub-0",
    "evaluated_head": {
      "revision_id": "rev-1",
      "publication_id": "pub-1"
    },
    "canonical_document": {
      "schema_version": 1,
      "project_id": "project-1",
      "timeline_id": "film-1",
      "parent_revision": {
        "revision_id": "preview-rev-2",
        "content_digest": "sha256:c1fe2a5c5575702edad51f37da7f21805b6d8199d184adbcbb232ba8b1efd944",
        "payload": {
          "config": {
            "fps": 30,
            "tracks": [
              {
                "id": "track-1",
                "kind": "video",
                "label": "Opening"
              }
            ]
          },
          "registry": {},
          "clips": [
            {
              "id": "clip-1",
              "clipType": "video",
              "track": "track-1",
              "at": 0,
              "hold": 2,
              "meta": {
                "org.example.notes": {
                  "note": "B"
                }
              }
            }
          ],
          "occurrences": []
        }
      },
      "shot_revisions": [],
      "internal_timeline_revisions": [],
      "dependency_manifest": {
        "shots": [],
        "internal_timelines": [],
        "media": [],
        "documents": []
      }
    },
    "document_digest": "sha256:d3708156fc92838904d3c07561361a69a866b7eaa5e3afb2408ff543e9d24c9c",
    "commands": [
      {
        "schema_version": 1,
        "op": "doc.patch",
        "version": "1",
        "select": null,
        "args": {
          "changes": [
            {
              "op": "set",
              "ref": "parent",
              "path": [
                "clips",
                "id:clip-1",
                "meta",
                "org.example.notes",
                "note"
              ],
              "before": {
                "state": "present",
                "value": "A"
              },
              "value": "B"
            }
          ]
        }
      }
    ],
    "id_map": {},
    "provider_version": "provider-v2",
    "compiler_version": "compiler-v2",
    "merge_mode": "fields",
    "steps": [
      {
        "id": "note-1",
        "label": "Revise the first note",
        "intent": "Clarify the opening",
        "tags": [
          "notes"
        ],
        "command_ordinals": [
          0
        ],
        "patch": [
          {
            "op": "set",
            "ref": "parent",
            "path": [
              "clips",
              "id:clip-1",
              "meta",
              "org.example.notes",
              "note"
            ],
            "before": {
              "state": "present",
              "value": "A"
            },
            "value": "B"
          }
        ]
      }
    ]
  },
  "receipt": null
}
```

## 5. Undo: whole commit, per-step guards and later-history scan

Undo is a new ordinary commit through the same engine, never a mutable history
entry or raw snapshot overwrite. Keep `timeline.inverse`, `select: null`, and
`args.publications` (unique target publication IDs in acceptance order). Extend
args with optional `steps`, a map from each target publication ID to a nonempty
array of unique step IDs. If `steps` is absent, undo every step of every target.
If present, it must specify every target; unknown step/publication IDs are
invalid. Selected steps are inverted in reverse execution order, newest selected
publication first. Nonselected steps in those publications remain intervening
work for dependency checks. The request still has its own label and steps; the
inverse step's submitted patch can be empty and is completed by the provider.
Store `records.undo_of` and `records.undo_steps` (the latter null for whole-commit
undo); retain original history entries unchanged.

Command fragments for a whole undo and a per-step undo (separate requests):

```json
{
  "whole": {
    "schema_version": 1, "op": "timeline.inverse", "version": "1", "select": null,
    "args": {"publications": ["pub-notes"]}
  },
  "one_step": {
    "schema_version": 1, "op": "timeline.inverse", "version": "1", "select": null,
    "args": {"publications": ["pub-notes"], "steps": {"pub-notes": ["note-3"]}}
  }
}
```

Runtime/provider load the target's authenticated complete step patches and the
actual previous landing head, never inverse writes supplied by the caller.
Reverse `set`/`remove` using their tagged before/after states; insertion becomes
removal, removal becomes insertion at its recorded position, and move restores
its previous position. A step's inverse uses its own sequential boundary states,
not the whole commit's final coalesced field values. Preserve all effects,
including derived writes and collection-shape changes. Validate the completed
inverse candidate before acceptance.

Two guards are required: (1) current values/identities/collection shape match the
selected effects' recorded after states, adjusted only for other selected
inverses; (2) scan every later accepted publication and every later nonselected
step through the current evaluated head for overlapping writes, reads and
reference dependencies. A later write to a target field or guarded read refuses
undo even if it restored equal bytes; later consumers of a created entity or a
value the inverse would invalidate also refuse undo. Selected steps with shared
fields/dependencies must be undone together when a remaining step would be
invalidated. Unknown/legacy history is `history_unavailable`, never permission
to undo. A surviving reference blocks deletion of a created entity. Independent
later steps/commits remain intact. There is no automatic cascading undo.

A merged commit's inverse is computed against the head it actually landed on:
its `previous_*`/`rebased_onto`, not the stale requested base. Thus undoing §4's
merged note B→A preserves the other party's track label `Opening`. Later work is
still subject to both guards. Redo is guarded undo of the accepted undo commit,
with a fresh key; it is subject to the same history/dependency checks.

Undo scenarios, including a value-equal A→B→A tail:

```json
[
  {
    "case": "whole_notes",
    "target_steps": ["note-1", "note-2", "note-3"],
    "later": [], "undo_steps": null,
    "expected": "accepted", "reverted_steps": ["note-3", "note-2", "note-1"]
  },
  {
    "case": "independent_note_step",
    "target_steps": ["note-1", "note-2", "note-3"],
    "distinct_paths": true, "later": [], "undo_steps": ["note-2"],
    "expected": "accepted", "preserved_steps": ["note-1", "note-3"]
  },
  {
    "case": "later_dependent_step_in_same_commit",
    "target_step": {"id": "first", "change": "note X -> A"},
    "later_step": {"id": "second", "read": "note A", "writes": "derived_summary"},
    "undo_steps": ["first"], "expected": "conflict", "reason": "inverse_conflict"
  },
  {
    "case": "A_to_B_to_A",
    "target": {"publication_id": "p1", "before": "X", "after": "A"},
    "later": [
      {"publication_id": "p2", "before": "A", "after": "B"},
      {"publication_id": "p3", "before": "B", "after": "A"}
    ],
    "current": "A", "value_guard_matches": true,
    "undo": "p1", "expected": "conflict", "reason": "intervening_write"
  },
  {
    "case": "undo_first_leg_of_A_to_B_to_A",
    "target": {"publication_id": "p1", "before": "A", "after": "B"},
    "later": [{"publication_id": "p2", "before": "B", "after": "A"}],
    "undo": "p1", "expected": "conflict", "current": "A"
  },
  {
    "case": "merged_inverse",
    "requested_base": {"note": "A", "track_label": "Picture"},
    "landing_head": {"note": "A", "track_label": "Opening"},
    "accepted_result": {"note": "B", "track_label": "Opening"},
    "later": [], "expected_after_undo": {"note": "A", "track_label": "Opening"}
  }
]
```

## 6. `meta` namespaces: placement, limits and preservation

`meta` is an optional JSON object on authored parent composition payloads,
TimelineConfig payloads (parent and internal), shot payloads, occurrence rows,
clip rows, track rows, and registry asset records. It does not belong on immutable
revision-image wrappers, manifests, commands or receipts. A parent payload's
`meta` and its config's `meta` are distinct locations; no mirroring or merging
between them is implied.

Each `meta` key is a namespace matching
`^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$`, 1–128 ASCII characters. Use reverse-domain
names for application/extension data (`org.example.notes`). Namespace values
are JSON objects; their descendants may be any finite JSON value including null
and arrays. No executable values, nonfinite numbers or implicit references.
`meta: null` and a namespace value of null are invalid; remove the namespace or
`meta` key explicitly to clear it. Empty objects are valid and stay empty.

Limits, measured independently at each `meta` occurrence in the final candidate:
at most 64 namespaces, at most 65,536 canonical UTF-8 bytes per namespace value,
at most 262,144 canonical UTF-8 bytes for the whole `meta` object, and at most
32 nested container levels below a namespace value (its root object is level
one). Canonical size uses the same compact sorted-key UTF-8 encoding as Runtime
digests. Exceeding a limit is invalid (`meta_limit_exceeded`) with the offending
path and a hint. These are schema/validation limits for V1/V2 to implement;
existing HTTP body limits may reject a larger request earlier.

Unknown namespaces and contents are preserved verbatim as JSON values through
load, patch, semantic edit, compile, acceptance, history read and undo. Do not
insert defaults, normalize strings, strip unknown keys or reorder arrays.
Verbatim means value preservation, not original whitespace/object key order.
Composition and renderers ignore unknown `meta`; it cannot alter timing or
structural validation. Namespace keys grant no write privilege. Normal field
and ancestor overlap rules apply: two leaf edits in different namespaces can
merge under `fields`; replacing the entire `meta` object guards all namespaces.
Strings in `meta` that look like IDs receive no reference integrity, remapping,
automatic deletion or dependency tracking; a script depending on them declares
reads. Core reference/asset discovery must not interpret opaque `meta` descendants
as schema-owned media references or append phantom manifest entries.

Preservation scenario (the set carries the entire previous namespace value):

```json
{
  "before": {
    "meta": {
      "org.example.notes": {"note": "A", "tags": ["rough"]},
      "com.other.tool": {"foreign_id": "missing-is-allowed", "nullable": null, "items": [2, 1]}
    }
  },
  "change": {
    "op": "set", "ref": "parent", "path": ["meta", "org.example.notes"],
    "before": {"state": "present", "value": {"note": "A", "tags": ["rough"]}},
    "value": {"note": "B", "tags": ["rough"]}
  },
  "expected": {
    "meta": {
      "org.example.notes": {"note": "B", "tags": ["rough"]},
      "com.other.tool": {"foreign_id": "missing-is-allowed", "nullable": null, "items": [2, 1]}
    }
  },
  "invalid_namespace_value": {"meta": {"org.example.notes": null}},
  "expected_invalid_code": "invalid_meta"
}
```

## 7. History: labels, steps and authoritative attribution

Store accepted label, steps (including their complete patches), requested/effective
merge modes and declared reads with the existing immutable acceptance/history
entry. `records.commands` remains the provider's authoritative command recorder;
add `records.steps` for authoritative step boundaries/patches, and `undo_steps`
as in §5. No parallel evidence ledger is introduced. Keep source, rationale,
group ID, previous head pair, publication/revision IDs, receipt,
provider/compiler versions and `records.undo_of`.

The authenticated Runtime `publisher` is the authoritative actor, also stored
on the durable receipt-bound history entry and accepted event. `source.via`,
`source.detail`, labels, tags and prose intent describe the client request and
cannot override actor identity. Do not accept client `publisher`/`actor` fields
as attribution. History/read replay must agree with the accepted result, not
reconstruct authorship from an App user name or a script string.

The existing history operation lists entries in acceptance order with
`items`, `next_cursor`, and a pinned `head` pair. Read at a chosen `through` pair;
all pages share that pair and scope. Use the existing cursor/limit behavior
(1–200, default 100), contiguous ancestry verification and authenticated reads.
Do not mix a newly moved head into an existing pagination walk. List and
single-entry reads return labels, steps and authoritative publisher without
requiring a second metadata store. Legacy entries retain
`intent: "legacy_unknown"`, missing attribution as null and missing step records as
null/absent; never invent steps or guarded undo evidence for them. Preview,
invalid, conflict, refused and unknown outcomes add no accepted history entries.

History-entry projection for the accepted example (projection omits the already
shown receipt and full command recorder; actual entries include both):

```json
{
  "publication_id": "pub-1",
  "revision_id": "rev-1",
  "previous": {
    "revision_id": "rev-0",
    "publication_id": "pub-0"
  },
  "intent": "recorded",
  "publisher": "principal-7",
  "label": "Clarify opening note",
  "source": {
    "via": "python",
    "detail": "notes.py"
  },
  "merge": "fields",
  "merge_mode": "fields",
  "reads": [],
  "steps": [
    {
      "id": "note-1",
      "label": "Revise the first note",
      "intent": "Clarify the opening",
      "tags": [
        "notes"
      ],
      "command_ordinals": [
        0
      ],
      "patch": [
        {
          "op": "set",
          "ref": "parent",
          "path": [
            "clips",
            "id:clip-1",
            "meta",
            "org.example.notes",
            "note"
          ],
          "before": {
            "state": "present",
            "value": "A"
          },
          "value": "B"
        }
      ]
    }
  ],
  "records": {
    "steps": [
      {
        "id": "note-1",
        "label": "Revise the first note",
        "intent": "Clarify the opening",
        "tags": [
          "notes"
        ],
        "command_ordinals": [
          0
        ],
        "patch": [
          {
            "op": "set",
            "ref": "parent",
            "path": [
              "clips",
              "id:clip-1",
              "meta",
              "org.example.notes",
              "note"
            ],
            "before": {
              "state": "present",
              "value": "A"
            },
            "value": "B"
          }
        ]
      }
    ],
    "undo_of": [],
    "undo_steps": null,
    "restored_from": null
  },
  "provider_version": "provider-v2",
  "compiler_version": "compiler-v2"
}
```

Implementation responsibilities follow PLAN §3: R1 implements patch/guard/read
semantics and Runtime store integration; R2 implements guarded whole/per-step
undo; R2r persists/lists labels, steps and authoritative attribution; R3 extends
preview and structured errors; V1/V2 adopt metadata and validation; A2 consumes
canonical replies through the persisted outbox; G2 provides the bounded Python
function re-run. Existing passing behavior tests stay in place. C0 changes only
this contract and its identical orchestrator design copy.

Example parsing and copy equality were checked from the runtime worktree with:

```bash
python - <<'PY'
import json
import re
from pathlib import Path

repo = Path('contract/commit-v2.md')
shared = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/commit-v2.md')
assert repo.read_bytes() == shared.read_bytes()
for path in (repo, shared):
    source = path.read_text()
    blocks = re.findall(r'^```json\n(.*?)^```$', source, re.M | re.S)
    assert blocks
    for index, block in enumerate(blocks, 1):
        json.loads(block, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    assert len(re.findall(r'^## [1-7]\. ', source, re.M)) == 7
    print(f'{path}: {len(blocks)} JSON blocks parsed; 7 required headings')
PY
```

The following fixture-consistency check also passed. It uses the existing
Runtime digest function; it does not run an unimplemented v2 provider:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python - <<'PY'
import copy
import json
import re
from pathlib import Path
from runtime_protocol.timeline_commit_validation import digest

source = Path('contract/commit-v2.md').read_text()
examples = [json.loads(block) for block in re.findall(r'^```json\n(.*?)^```$', source, re.M | re.S)]
request, shapes, clears, structural, idless, created, reads, conflicts, accepted, merged, conflict, invalid, preview, undo, undo_cases, meta, history = examples
for outcome in (accepted, merged, preview):
    data = outcome['data']
    document = data['canonical_document']
    assert digest(document) == data['document_digest']
    assert digest(document['parent_revision']['payload']) == document['parent_revision']['content_digest']
    assert data['commands'] == request['commands']
    assert data['steps'] == request['steps']
for outcome in (accepted, merged):
    assert outcome['receipt']['result'] == outcome['data']
    assert outcome['receipt']['receipt_id'] == outcome['data']['accepted_revision_id'].replace('rev-', 'pub-')
assert preview['receipt'] is None and preview['data']['would_status'] == 'merged'
assert merged['data']['previous_revision_id'] == merged['data']['rebased_onto']['revision_id']
assert merged['data']['previous_publication_id'] == merged['data']['rebased_onto']['publication_id']
assert merged['data']['canonical_document']['parent_revision']['payload']['config']['tracks'][0]['label'] == 'Opening'
assert accepted['data']['canonical_document']['parent_revision']['payload']['config']['tracks'][0]['label'] == 'Picture'
assert history['steps'] == history['records']['steps'] == request['steps']
assert [i for step in request['steps'] for i in step['command_ordinals']] == list(range(len(request['commands'])))
assert [change for step in request['steps'] for change in step['patch']] == [change for command in request['commands'] for change in command['args']['changes']]
rows = copy.deepcopy(structural['initial'])
for change in structural['changes']:
    assert [row['id'] for row in rows] == change['order_before']
    before = next((row for row in rows if row['id'] == change['id']), None)
    assert change['before'] == ({'state': 'present', 'value': before} if before else {'state': 'absent'})
    if change['op'] == 'list.insert':
        row = change['value']
    else:
        row = rows.pop(next(i for i, row in enumerate(rows) if row['id'] == change['id']))
    if change['op'] != 'list.remove':
        anchor = change['after_id']
        index = 0 if anchor is None else next(i for i, row in enumerate(rows) if row['id'] == anchor) + 1
        rows.insert(index, row)
assert [row['id'] for row in rows] == structural['expected_ids']
assert shapes['missing'] != shapes['explicit_null']
assert conflict['details']['current'] and invalid['details']['code'] == idless['expected_invalid_code']
assert all(key in failure['details'] for failure in (conflict, invalid) for key in ('code', 'path', 'hint', 'suggested_command'))
aba = next(case for case in undo_cases if case['case'] == 'A_to_B_to_A')
assert aba['target']['after'] == aba['current'] == aba['later'][-1]['after']
assert aba['expected'] == 'conflict' and aba['reason'] == 'intervening_write'
assert meta['before']['meta']['com.other.tool'] == meta['expected']['meta']['com.other.tool']
assert not any(line.rstrip() != line for line in source.splitlines())
print('PASS: Runtime digests, receipt/result equality, step partition, ordered-list transitions, merged preservation, preview, structured errors, ABA, meta preservation and whitespace')
PY
```
