# Canonical EditCommand — M0 schema handoff

2026-10-19. Agent-owned design artifact, not an implemented provider or product
gate result. PLAN wins. Runtime `commit-contract.md` §4.1 owns every request,
closure, context, port, candidate, prepared, record, response and history
envelope. This document supplies the referenced command/semantic leaves and the
inverse/restore signatures; it does not replace any Runtime DTO.

## Authority, versions and artifact projection

The authoritative M0 source is
`ORCH/design/edit-command.schema.json`, where `ORCH` is the directory containing
PLAN.md. It is an actual self-contained JSON Schema Draft 2020-12 document.
Its stable `$id` is
`https://astrid.local/schemas/timeline/edit-command.schema.json`; it is an
identifier, not a network fetch requirement. The root validates one command.
`#/$defs/CommandBatch` validates the nonempty ordered command array and the
sole-command restore constraint. Public semantic references are
`#/$defs/AgentState`, `AgentWrite`, `AgentRead`, `AgentSelection`, `AgentBinding`,
`AgentCreatedID`, `AgentDependency`, and `AgentDerivedWrite`. Operation argument
references are `#/$defs/InverseArgs`, `RestoreArgs`, and `ClipMoveArgs`.

At the implementation port, move authority into Agent's packaged
`astrid/core/timeline/schema/edit-command.schema.json`. Main's
`pyproject.toml` already packages `core/**/*.json`; no packaging framework is
needed. Runtime pins a **byte-identical** copy at
`contract/schemas/edit-command.json`, registered in its existing schema manifest.
Runtime's commit schema references `edit-command.json#/$defs/CommandBatch` for
`CommitRequest.commands` and `edit-command.json#/$defs/EditCommand` for a single
command. `CommandRecord.command` and `Candidate.commands` use the command type;
the latter is not a new request. All semantic leaf refs point to that same file.
The filename change must not rewrite `$id`, contents, definitions or versions.
No independently maintained Runtime command schema survives.

Concrete copy/check sequence for the implementing managers (not executed here):

```bash
cp "$ORCH/design/edit-command.schema.json" "$AGENT/astrid/core/timeline/schema/edit-command.schema.json"
cp "$AGENT/astrid/core/timeline/schema/edit-command.schema.json" "$RUNTIME/contract/schemas/edit-command.json"
cmp "$ORCH/design/edit-command.schema.json" "$AGENT/astrid/core/timeline/schema/edit-command.schema.json"
cmp "$AGENT/astrid/core/timeline/schema/edit-command.schema.json" "$RUNTIME/contract/schemas/edit-command.json"
```

Here `ORCH`, `AGENT`, and `RUNTIME` name explicit checked-out design/implementation
roots. Use the existing Runtime generator and manifest checks from
`commit-contract.md` §6 after registering this file; both generated Python and
TypeScript must export `EditCommand` with the same required/optional/null fields,
`CommandBatch`, and the named semantic leaves. Generated validators must consume
the pinned JSON schema, including per-operation conditionals. Do not substitute
the old `OPCALL_SCHEMA`. Load Agent's source with
`importlib.resources.files("astrid.core.timeline").joinpath("schema/edit-command.schema.json")`;
compare its bytes to Runtime's pinned file in the cross-repo contract check.
Also compare the generated clients' existing Runtime `SCHEMA_DIGEST` to the
Runtime release, as its generator checks require. File equality and the Runtime
digest serve different purposes; the command file is not the whole contract.
After packaging authority moves to Agent, the design copy is an archived M0
snapshot: subsequent edits start in Agent and refresh Runtime through the same
copy + `cmp` check. Never edit three sources independently.

| Layer | Exact version / identity |
| --- | --- |
| Runtime commit body | `api_version: 1`, unchanged Runtime-owned envelope |
| Command schema | required integer `schema_version: 1` |
| Operation implementation | required nonempty **string** `version`; these three operations use `"1"` |
| Semantic recorder | Runtime `Recorder.schema_version: 1`, unchanged |
| Provider ABI | initial slim integer `interface_version = 1`; main has no prior provider ABI |
| Provider load | fixed zero-argument `astrid.sdk.timeline.commit.create_runtime_commit_service()` |
| Provider compatibility | `provider_id = "astrid-v1"`, exact generated Runtime `SCHEMA_DIGEST`, synchronous `commit(context, port)` |

R4's nullable tool-release `version` is deliberately tightened: builders must
supply the pinned operation version **before** persisting the outbox/in-flight
request. Neither server defaults nor current installed tool version may alter a
retry. There is no new operation-version framework. Unsupported operation
versions refuse before execution. Unknown operations/arguments are validated by
the installed registry and refuse if unsupported; passing this extensible
envelope alone does not mean an operation can execute.

## Fields, presence, paths and recorder authority

Required fields are `schema_version`, `op`, `version`, `select`, `args`.
`select` is string or null, not omitted. Optional fields are exactly `resolved`,
`expect`, `bindings`, `created`, `authorship`, `reads`, `selections`, `intent`,
`rationale`, `group_id`. Optional recorder arrays/maps are omitted when not
claimed; null is invalid for them. Empty arrays/maps express an explicit empty
claim and are verified accordingly. `rationale` is the sole metadata spelling;
`reason` is not an alias. Batch label/source/rationale/group remain Runtime's
`BatchMetadata`; a command does not carry authentication or a receipt.

The pre-existing command field types come from frozen Agent R4 at
`11caf1d9de291d76f491cf69f7942606b7471d7a`, read via `git show`:

* `commands.py:EditCommand` / `schemas/change-contract/opcall.schema.json`:
  `resolved` and `created` are ordered scoped-ID arrays; `bindings` maps exact
  authored TimeRef text to an **identity string**, not an object. `expect` maps
  target keys to tagged states. `authorship` maps those keys to `direct` or
  `consequence`, not an actor. `version` is a string. No dictionary replaces a
  scoped-ID list and no typed provenance object replaces a binding string.
* `commands.py:write_key/write_target`, `inverse.py:_tokens`, and
  `_member_path/state_at`: old expectation/authorship keys use entity ID plus
  property-token string, not JSON Pointer or a mutable row index. Empty path
  means the whole entity. New recorder leaves use normalized token arrays as
  described below. Examples:
  `params.x`, `modifiers["fade"].params.opacity`, `app["org.example"].payload`,
  `params[0]`, and `["x.y"]`. Bracket strings are JSON strings; bracket numbers
  are nonnegative JSON integers. Overlap compares parsed token ancestry:
  `params` overlaps `params.x`, not `paramsExtra`; `params["x.y"]` is one key.
  Numeric tokens inside a value never select a clip/track/entity by position.
* `commands.py:capture_binding` and `core/timeline/moments.py`: R4 binding
  values include scoped IDs, `word:<line>:<index>`, `beat:<index>`, and
  `cut:<id>:start|end`. Retain those string shapes for compatibility, with their
  immutable source/time-map dependencies recorded as reads. They are not a
  guarantee of stable identity after re-transcription/re-detection. The exact
  `source-word` TimeRef has six quoted document/lineage/revision/clip/snapshot/word
  strings; it remains the binding **key**/operation argument where applicable,
  with its exact source captured in reads. Do not add a speculative marker or
  signal grammar before the approved primitives schema exists.

`ScopedId` preserves R4's grammar:
`parent|shot:<id>|occurrence:<id>` plus `/clip:<id>` or `/track:<id>`;
`occurrence:<id>`, `occurrence:<id>/shot`, and `cut:<id>` are also supported.
`EntityRef` additionally supports `parent`, `parent/shot-group:<base64url>` and
`occurrence:<id>/source|registry`, because R4
`shot_groups.py:identity/semantic_states` actually records those semantic
entities. That additive leaf support does not silently widen R4's `resolved`
or `created` grammar. The R4 schema's narrower resolved grammar for shot groups
is an observed port gap; registry widening must be deliberate in M2. Local IDs
must be nonempty and contain no slash; cut IDs also contain no colon.

A target key is `id::path`, or a bare path when exactly one resolved target
exists (including a bare empty path). One canonical parser must first recognize
a valid bare property path, otherwise recognize an entity prefix plus `::` and
parse the entire remaining path. `::` inside a quoted property key is data.
R4's unconditional `split("::", 1)` cannot handle all quoted keys. The provider
must refuse ambiguous identity delimiters (`::` inside a scoped local ID) rather
than bind a different entity; the broad legacy ID regex is not authorization to
invent an ambiguous target key. Canonical producers reserve that delimiter.
Do not reinterpret path text with string-prefix overlap or use numeric selectors
for collection membership.

Absence, null and clear rules:

1. `{ "state": "absent" }` means absent; it has no `value` member.
   `{ "state": "present", "value": null }` means present-null. A present
   arbitrary JSON object/array is equally ordinary data. Unchanged writes retain
   identical before/after tagged states; they are not dropped.
2. Omitted operation parameters use only that operation version's declared
   defaults, recorded as effective normalized arguments. Null is accepted only
   by a nullable parameter schema. This schema does not insert defaults.
3. There is no universal top-level `clear` field or magic object value.
   Graph/track setters retain R4's disjoint `args.values` and `args.clear` path
   lists; `clip.clear` retains `args.keys`; migration `clip.set` controls may
   emit its operation-specific `{op:"clear"}` value. Each registered operation
   checks clearability, duplicates and assignment/clear token overlap before
   executing. None of the three schemas below has a clearable argument.
   An opaque extension object `{op:"clear"}` or `{$absent:true}` stays a value.
4. Unknown extension objects/arrays preserve arbitrary JSON recursively and
   remain atomic unless their admitted schema declares structure. Unknown
   command argument **keys** are not extension data: a registered operation's
   schema closes them. Transport rejects duplicate keys and non-finite numbers
   before schema validation/hashing; JSON Schema cannot make a non-JSON Python
   NaN into valid JSON. Whitespace/property order preservation is not promised.

All client recorder fields are claims. Provider reconstructs/verifies their
reads, selection/order, expectations, bindings, created-ID reservations and
write classifications against exact scoped inputs. Supplied IDs are reused
only after collision/authority checks. A spoofed `authorship` value cannot grant
actor authority; Runtime's authenticated publisher remains in `CommitContext`.
Accepted history is server recorder output, never a client history assertion.

Runtime `records.commands` is authoritative. At construction derive
`Candidate.commands = [record.command for record in records.commands]`;
Runtime's updated §4.1 removes independent `PreparedCommit.commands`. Any local
accessor with that name is only this checked projection, not a mutable field or
command/write store. Framework primitives generate all metadata from the
author's schema, handler, intent and fixtures, including unchanged direct writes
and structural reconstruction facts. Foundation `id_map` is empty or identity
pairs only; nonidentity results refuse until a concrete supported command
justifies extending the contract. No general fork/remapper is required.

The final recipe's **new** recorder leaves are adopted without changing the R4
command fields. `AgentRead = {ref,path,state}` and
`AgentWrite = {ref,path,before,after}` use `path:string[]`, as does Runtime's
frozen `Conflict.path`. An empty array addresses the whole entity. Parse R4
property syntax once: `params.x` and `params["x"]` both become `["params","x"]`;
`params["x.y"]` becomes `["params","x.y"]`, not three tokens. Array index tokens
are canonical decimal strings (`params[0]` becomes `["params","0"]`). Traverse
only a verified container type: object key `"0"` and array index 0 are resolved
using the pinned parent-container type, which is itself a read dependency.
A change of container type conflicts; never use numeric tokens as entity
collection positions. Unknown extension objects/arrays stay atomic. This
normalization happens once at ingress for both `expect` and `authorship`;
all downstream addresses use `(ref, tokens)`, retaining old spelling only at the
wire boundary. It must happen before overlap checks, including the old R4 case
where `params.x` vs `params["x"]` escaped raw string-prefix comparison.

`AgentSelection` retains `key,query_version,owner,members,order,boundaries,policy`.
The provider checks query registration, `order` is exactly a permutation of
unique members, and boundary identity/scope; JSON Schema cannot compare those
lists. Policy is `guard-membership` or explicitly declared `include-concurrent`;
the versioned effective policy is recorded, not discovered during replay.
Generic `intent` follows the final recipe artifact:
`ripple = none|selected|include-concurrent`, `anchor = fixed|follow`,
`ownership = shared|occurrence`, `position = absolute|relative`. Here `shared`
means shared-shot intent. Only applicable keys occur, and an operation's schema
further narrows them; there is no arbitrary serialized merge callback.

The Runtime record leaves are **enriched provider output**, not replacement
wire types for `bindings`/`created` on an EditCommand:

* `AgentBinding = {key,ref,policy,dependencies}` records an exact binding plus
  follow/fixed policy and keys of dependency captures. The command's original
  `bindings` remains a string map. Complete source/word/occurrence/time-map pins
  are in those dependency captures and tagged reads, not guessed from text.
* `AgentCreatedID = {ref,kind,owner}` records identity kind and ownership; owner
  is null only for a root. The command's `created` remains a scoped-ID list.
* `AgentDependency = {key,kind,pin,policy}`, with kinds
  `entity|media|transcript|source|time-map|authority` and policies
  `exact|follow-identity`. `pin` is an object; the registered kind schema must
  validate the full exact scoped identity (for example Runtime's five-field
  media selection or DocumentPin). Transcript/config pins resolve to Runtime's
  retained exact content snapshots for replay, inverse and compile after mutable
  Document replacement/retranscription; pins alone are insufficient. Never use
  latest reads or producer execution. Use `transcript_source` / `config_source`
  and `CanonicalDocument.dependency_manifest.documents` per Runtime §4.1;
  config dependencies use existing `kind:source`, with no new command field.
  Runtime owns mechanism and DTOs;
  this is narrow content-addressed retention, not general Documents history.
  This common envelope does not invent a
  replacement Runtime pin or authorize arbitrary data just because it is an
  object. Unsupported kinds, incomplete pins or unconsumed reads refuse.
* `AgentDerivedWrite = {ref,path,before,after,cause}` references an executed
  ordinal as cause and stays separate from direct writes. Direct unchanged
  writes remain in `writes` even when before and after are identical.

Generalized inverse translates these leaves back into R4's internal guarded
`id/path/before/after` executor. Its structural `order/source/group_containers`
are reconstructed from verified historical closures and recorded selections,
source dependencies and presence reads; they are not lost or accepted as new
client inverse arguments. Ordinal belongs to Runtime's enclosing `CommandRecord`;
flatten nested execution deterministically into contiguous zero-based records
with matching flattened `commands`. Cause ordinals and dependency keys must
resolve inside the accepted recorder. These are semantic checks, not a new
record wrapper. Registered conflict/event vocabularies outside these operations
still need the registry port; this task does not claim to finish all of Runtime
§7's per-operation payload mappings or implement event emission.

## Exact history operation signatures

`timeline.inverse`, operation version `"1"`, `select: null`:

```text
args = {publications: ID[1..]}  # ordered, unique, nonempty strings
```

List targets in **ascending Runtime acceptance order**, all from this timeline's
accepted ancestry at the submitted base publication. Schema enforces nonempty
unique strings; provider verifies chronology, same-project/timeline scope,
ancestry and that targets exist at the base. IDs are actual Runtime receipt IDs,
not revision hashes. Invert the listed records in reverse dependency/execution
order, coalescing selected writes as first-before/last-after while retaining
all intermediate observations, including unchanged writes. Non-target
intervening edges are still checked even between two selected publications.
A selected edge's own earlier/later writes are handled as part of this explicit
unit; a later unselected overlapping write, A→B→A or A→A still conflicts.

Clients can discover a display group in history, but must enumerate every target
publication in this list; `group_id` never triggers implicit history lookup,
expansion or cross-request atomicity. One request remains one atomic acceptance
and undo unit. Provider reconstructs guards/writes from verified accepted
records/closures via `history_entry`, bounded `history` and exact closure reads;
it does not trust a local journal or proposed expanded writes. Expansion lives
in authoritative `records.commands[*].writes/reads/selections/...`, not in
`args.writes`. Keep accepted command arguments in the same canonical schema.
The immutable accepted result is used for exact retries. Redo is an inverse of
the accepted inverse publication, with a new retry key and fresh guards.

Missing targets, unknown legacy intent, a missing ancestry segment, or a
baseline boundary that cannot prove the needed history fails closed as
`history_unavailable` (or the contract's explicit dependency conflict). No
snapshot diff or equal final value proves safety. Dependency checks include
surviving references to created entities, ownership, opaque-data limitations,
and selection membership/order. A multi-target failure publishes nothing.

`timeline.restore`, operation version `"1"`, `select: null`:

```text
args = {revision_id: ID, content_digest: "sha256:<64 lowercase hex>"}
```

This is the exact historical **parent** revision/digest, not the hash of
Runtime's entire `CanonicalDocument`. No source `publication_id`, caller image,
expected head, group selector or writes belong in args. Runtime's frozen restore
adapter resolves/verifies the selected revision closure and digest in scope,
constructs this command, and uses the original Invocation for retry identity.
Provider verifies the same source and records exactly
`Recorder.restored_from = {revision_id,content_digest}`; `undo_of = []`.

Restore must be the sole command in `CommitRequest.commands`, also when sent to
the ordinary commit route. Nested restore is invalid; registry macros cannot
hide it in another command. Its strict current-head pair is solely
`base_revision_id` + `base_publication_id` in that request, mapped from the
existing restore adapter's required `expected_head` + `expected_publication_id`.
Compare **both** current pins; any mismatch or head race is `stale_head`, without
automatic rebase or another acceptance attempt. Guarding only the revision misses
same-content publications. Restore replaces the whole authored scope, records a
complete-scope write including unchanged values, recompiles timing, and makes a
new accepted edge/receipt even when immutable content can be reused. It is not
ordinary property undo and cannot bypass authority or history verification.

Bootstrap and baseline remain exactly Runtime §5: new editable timelines first
have a verified empty publication receipt; existing timelines need a verified
receipt/event/closure baseline. Absent/unverifiable history is read-only to
commit/restore, not an implicit empty timeline. Agent never fabricates a base
publication or repairs provenance by accepting a replacement.

## Minimal M1 move signature

`clip.move`, operation version `"1"`, selects one exact
`parent/clip:<id>` or `occurrence:<id>/clip:<id>`:

```text
args = {on: number >= 0}  # absolute timeline seconds
```

This is a deliberately narrow **new M1 operation**, not a claim that R4 registers
`clip.move`. R4 provides `clip.on(moment)`/`clip.enter-at`; its numeric `on` can
be cut-relative, so implementation must explicitly translate absolute timeline
time to the selected authored owner's local/fixed-start representation rather
than call that method blindly. This schema uses R4's `on` argument vocabulary,
not App's existing local patch shape. Keep authored duration; clear an existing
start-follow relation through the handler's recorded presence writes; do not
ripple other clips. Quantize once at the canonical timing boundary using pinned
rational fps. Validate half-open/source constraints and compile derived timing.
Defaults are `intent = {ripple:"none",anchor:"fixed",position:"absolute"}`;
for an occurrence selection also record `ownership:"occurrence"` and use the
existing main isolated authored owner/source mapping. This does not require a
general fork or nonidentity `id_map`. A
parent selection has no occurrence ownership key. Supplied intent must agree;
shared-shot, follow, relative and ripple are outside this minimal operation.
The runner must retain writes even if `on` equals the current start. These are
implementation obligations, not behavior proven by this JSON schema.

The exact Python/generated-App capture paths, supported mapping cases, refusal
boundary and recorded follow clears are authoritative in
[edit-recipe.md, clip.move v1 capture](edit-recipe.md#clipmove-v1-shared-operation-and-gesture-time-capture).
App captures original reads/selections **at gesture time**, before preview,
never after ACK; provider validates the retained claims at HA before recording.
This minimal schema needs no new fields, `base_view` or basis DTO. M1 must prove
sequential/dependent gestures through the real App capture path, plus one small
structural command through the same framework, before claiming generality;
the M0 suffix adapter is not that evidence. Relative/follow/ripple coverage
remains a separate versioned operation obligation, not an expanded v1 signature.

## Validated examples

The comments delimit real JSON examples consumed by the isolated design tests.
"Accept" here means schema-valid, not authenticated or semantically executable.
Scope, accepted ancestry, history guards, digest equality and ID reservation
checks still belong to the provider/Runtime.

A two-publication inverse; `group_id` is explanatory metadata, never discovery:

<!-- schema: accept-command -->
```json
{"schema_version":1,"op":"timeline.inverse","version":"1","select":null,"args":{"publications":["txn-a","txn-b"]},"group_id":"drag-17","rationale":"Undo the two explicitly selected publications"}
```

Exact source pins, with strict current pins supplied by the enclosing request:

<!-- schema: accept-batch -->
```json
[{"schema_version":1,"op":"timeline.restore","version":"1","select":null,"args":{"revision_id":"parent-before-title","content_digest":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}]
```

Minimal move with an unchanged-write expectation claim:

<!-- schema: accept-command -->
```json
{"schema_version":1,"op":"clip.move","version":"1","select":"occurrence:opening/clip:title","args":{"on":2.5},"resolved":["occurrence:opening/clip:title"],"expect":{"at":{"state":"present","value":2.5}},"bindings":{},"created":[],"authorship":{"at":"direct"},"intent":{"ripple":"none","anchor":"fixed","position":"absolute","ownership":"occurrence"}}
```

Opaque extension values and tagged present-null survive envelope validation;
`vendor.decorate` still needs an installed handler/parameter schema:

<!-- schema: accept-command -->
```json
{"schema_version":1,"op":"vendor.decorate","version":"2.4","select":"parent/clip:title","args":{"payload":{"op":"clear","$absent":true,"nested":[null,{"id":"parent/clip:unrelated"}]}},"resolved":["parent/clip:title"],"expect":{"params":{"state":"present","value":null}},"authorship":{"params":"direct"},"reads":[{"ref":"parent/clip:title","path":["params"],"state":{"state":"absent"}}],"selections":[{"key":"decorate.members","query_version":1,"owner":"parent","members":["parent/clip:title"],"order":["parent/clip:title"],"boundaries":[],"policy":"guard-membership"}]}
```

Reject duplicate targets, implicit group lookup, and client expanded writes:

<!-- schema: reject-command -->
```json
{"schema_version":1,"op":"timeline.inverse","version":"1","select":null,"args":{"publications":["txn-a","txn-a"]}}
```

<!-- schema: reject-command -->
```json
{"schema_version":1,"op":"timeline.inverse","version":"1","select":null,"args":{"group_id":"drag-17"}}
```

<!-- schema: reject-command -->
```json
{"schema_version":1,"op":"timeline.inverse","version":"1","select":null,"args":{"publications":["txn-a"],"writes":[{"id":"parent/clip:title","path":"at","before":{"state":"present","value":2},"after":{"state":"present","value":1}}]}}
```

Reject mixing historical replacement with another command:

<!-- schema: reject-batch -->
```json
[{"schema_version":1,"op":"timeline.restore","version":"1","select":null,"args":{"revision_id":"old","content_digest":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}},{"schema_version":1,"op":"clip.move","version":"1","select":"parent/clip:title","args":{"on":2}}]
```

Reject current-head guards/source publication in restore args, missing versions,
and an untagged absence sentinel in expectations:

<!-- schema: reject-command -->
```json
{"schema_version":1,"op":"timeline.restore","version":"1","select":null,"args":{"revision_id":"old","content_digest":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","publication_id":"txn-old","expected_head":"current"}}
```

<!-- schema: reject-command -->
```json
{"op":"clip.move","select":"parent/clip:title","args":{"on":2}}
```

<!-- schema: reject-command -->
```json
{"schema_version":1,"op":"clip.move","version":"1","select":"parent/clip:title","args":{"on":2},"expect":{"params":{"$absent":true}}}
```

Other schema-valid proposals still refuse semantically: foreign/nonancestor or
chronologically reversed targets; changed/missing source digest; incomplete
selection/order; forged recorder claims; unknown handler versions/arguments;
ambiguous scoped IDs; undeclared source/media reads; hidden nested restore; or
stale restore pins. Schema validation alone proves none of those guards.

## Final recipe review and corrections for the Agent manager

Re-read the completed recipe after it gained its own candidate schema and spike
results. It now agrees on ABI 1, Invocation, prepared fields, inverse target
lists, exact restore pins, failure-closed history, and the richer recorder leaves
adopted above. Those earlier mismatches are resolved; do not apply stale draft
corrections. Manager applied the following reconciliation to edit-recipe.md at 18:09 UTC; this list records the choices rather than additional pending work:

1. Replace the recipe's competing
   `schemas/change-contract/edit-command.schema.json` source and
   `https://astrid.local/schemas/change-contract/edit-command.schema.json` ID
   with this task's `ORCH/design/edit-command.schema.json` source,
   `https://astrid.local/schemas/timeline/edit-command.schema.json` ID, future
   packaged `astrid/core/timeline/schema/edit-command.schema.json`, and pinned
   Runtime `contract/schemas/edit-command.json`. Retire the recipe worker's
   candidate artifact as a source rather than maintaining two schemas. Keep its
   examples/tests only after pointing them at the canonical artifact. The old
   draft `opcall.schema.json` is not the new wire authority.
2. Clarify the early universal `clear:["path"]` prose using the operation-specific
   clear builders already described later in the recipe. No top-level clear or
   global sentinel is introduced; opaque `{op:"clear"}` remains ordinary data.
3. Keep `schema_version`/operation `version` required before outbox reservation,
   not merely after normalization. Add the copy/byte-equality/generated-export
   checks above. The final recipe permits local builders to fill them before
   reservation; that local convenience must not make wire fields optional.
4. Keep old `expect`/`authorship` R4 key strings and command `bindings`/`created`
   map/list types distinct from new enriched recorder leaves. Specify the one
   property-string to `path:string[]` conversion above, including numeric
   container-type reads and quoted `::` handling. Do not copy R4's unconditional
   delimiter split or raw path-prefix overlap. Use the final recipe's intent
   values `selected/include-concurrent` and `shared`, not a third enum dialect.
5. Add `CommandBatch` sole-restore validation and the minimal numeric `clip.move`
   version `"1"` argument schema. Its absolute `on` semantics require an explicit
   adapter from R4 numeric `clip.on`, which can be cut-relative; the frozen R4
   registry does not contain `clip.move`. Keep the stated fixed/non-ripple scope
   and record same-value writes rather than promising R4 already does so.
6. Normalize structural inverse details from exact historical closure/selection
   and dependency records before invoking the R4 executor; final recipe leaf
   schemas do not retain R4's `order/source/group_containers` as write fields.
   Assert their exact restoration in M1/M2 rather than replacing them with a
   plain before/after diff. Validate derived cause ordinals and dependency keys.
7. Group IDs never expand targets; `records.undo_of` is the exact ascending
   explicit list. Retain Runtime §5 bootstrap/baseline/history refusal rules and
   strict restore current-pair comparison. These already agree in the final
   recipe; keep them when removing its competing artifact reference.

The orchestrator settled dependent suffix semantics in PLAN: wait for A acknowledgement, submit B at HA with its ORIGINAL value+identity/read/selection guards and a fresh request key; verify or conflict. Equal-state suffix ABA is allowed. There is no new proof wrapper/base_view field; accepted inverse retains its separate ABA guard. See suffix-basis.md for the required experiment.
The extensions document now uses `rationale` consistently, including its recipe counterexamples. Its marker and
opaque-remap counterexamples still apply and are not solved by widening strings.

## Verification and limits

Run from the assigned Agent worktree with shared dependencies:

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/m0_command_schema
```

The tests validate Draft 2020-12 structure/local refs, real accepted/rejected
handoff JSON, required field/version types, R4 recorder vocabulary and tagged
presence, opaque values, inverse target uniqueness, restore pins/sole-command,
and property-token syntax. These isolated M0 tests read the shared design
artifact by its explicit scratch path; before any product-suite integration,
retarget them to the packaged Agent schema. They deliberately do not import a
frozen R4 provider or claim runtime semantics from substitute implementations.
Final run: **95 passed in 0.46s**, no warnings or skips. The focused lint command
`/home/user/work/venv-agent/bin/python -m ruff check --isolated --select E4,E7,E9,F,I,BLE tests/m0_command_schema`
also passed; `git diff --check` exited 0. No `make check`, editing-conformance,
Runtime/App/Composition suites or product gates are claimed by this M0 task.
