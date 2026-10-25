# F-D86 bounded author investigation: BLOCKED

No product or test edits. The assigned base is 4dcb5a5e8a, not a normal
integration merge. Its `_commit_patch.py` is byte-identical to the actual
b415a427 MAIN candidate (SHA256
93075fbc5bb075e1628b8712e7babd40e306fb88c9a4ab347cc3ae7552f80cde).
Runtime HEAD is exactly 6634a17f3ffd885567ba3c91b6c7a560df7375a4.
Captured Agent integration is 608b6a7a2b6fa3ad17689b15fec174dd8d9ce898.

## Exact obstruction

The approved file cannot make the same dependency both a complete parent
scope for Runtime authentication and a disjoint registry field for rebase,
while retaining scope semantics and the original captured read. This is
evidence against the assumption that another bounded projection-only repair
can satisfy the current six originals. It is not permission to change Runtime,
omit a capture, narrow a declared scope, or bypass dependency guards.

Runtime `runtime_protocol/timeline_commit_auth.py:124` explicitly maps the
parent asset collection to `parent, []`, because the capture includes both
authored registry mirrors. `validate_step()` at lines 380–403 derives
`{kind: scope, ref: parent, path: []}` and requires coverage. `covers()` at
line 222 accepts exact equality or an enclosing scope only. A field dependency,
even at the parent root, does not cover that scope. A scope covering `[]` is
the parent root or timeline scope. Both overlap the disjoint parent edit in
the unchanged Agent `rebase_patch()` guard loop (lines 935–963).

## Source-only old/current trace

1. The registered `astrid` provider factory in Runtime's
   `timeline_commit_provider.py` is
   `astrid.sdk.timeline.commit.create_runtime_commit_service`.
   The original invokes the real service's `commit_timeline`, using the
   normal route and authorization, not a detached provider substitute.
2. Agent `commands.execute()` constructs `CommitPatch`, calls `before()`,
   runs native handlers through `Recording`, restores inherited declared
   reads after exact command-claim checks, and calls `metadata.finish()`.
3. Native `_registry()` unconditionally calls
   `ctx.read('parent/collection:asset')` before parent container creation.
   `State.get()` delegates to `_collections.shape()`, which preserves tagged
   registry/assets storage shape for both raw parent/config mirrors.
   `Recording.read()` retains the raw alias, empty path, and actual observed
   tagged state. No exact failed instance of this state is available locally.
4. Old 7e23790248: `canonical_site()` falls through to parent root; `finish()`
   cannot turn the object shape into an identity collection and emits parent
   scope. The original disjoint edit then overlaps that scope.
5. Held 4dcb5a5e8a / actual b415: `canonical_site()` projects to logical
   `parent/config/registry/assets`; `finish()` captures the exact field at
   the command's input closure, backing up to a safe ancestor when needed.
   Native records and declared reads are retained. This narrow field does
   not satisfy Runtime's required parent scope. This is a static caller/
   producer/consumer contradiction, independently of unseen record values.
6. Agent `commit.py:1370` calls `rebase_patch()` before replay on a moved
   head for these explicit v2 inputs. That function takes every step
   dependency as a conflict guard. Adding the Runtime-required scope to
   the field fixes coverage but restores the original disjoint refusal.
   Filtering that scope from guards would weaken the protected semantics.
7. `prepared_records()` deep-copies plan records/steps, after which
   `commit.py:1444` calls the normal port's `preview()` / `accept()`.
   Runtime `validate()` calls `validate_step()` on the authoritative steps.
   There is no existing alternative dependency-index representation in this
   path that makes a field cover a root scope without a semantic change.

## C0 union conservation

The required index includes inherited request reads, verified sequential step
reads, semantic captures/selections/bindings, and generated conservative reads.
Empty request/step reads do not erase native captures. Exact command captures
remain separately retained. The source is unchanged, so request keys, all
evaluation boundaries, original inputs/topology/opaque values, bindings,
selection/membership/order/value/ABA guards, atomic fallback, inverse and
retry behavior, and no-write checks are conserved. No narrower union or
fabricated authority was introduced.

## Exact six applicability and proof limit

Source selector:
`tests/editing_conformance/test_commit_runtime_parent_auto_completion.py::test_disjoint_head_accept_reload_exact_retry_undo_redo_and_reserved_id`

Source-derived parameter combinations (no collection executed):

| Case | Input retained | Shared path |
| --- | --- | --- |
| image-anchor | image birth, anchor-after | parent asset collection capture |
| image-fallback | image birth, fallback-at 22.25 | same |
| image-lane-end | image birth, lane-end | same |
| video-anchor | video from=0/to=2.5/speed=1, anchor-after | same |
| video-fallback | same video fields, fallback-at 22.25 | same |
| video-lane-end | same video fields, lane-end | same |

Their shared request builder sends api_version, scope IDs, exact base pair,
commands, label, steps/patch/step reads, merge=fields, declared reads=[],
dry_run, source/rationale/group_id and the normal idempotency key.
Every case preserves the concurrent
`parent/clip:anchor.params.later = [None, False, {custom: 1}]` edit, preview
no-write, accepted canonical reload, exact retry without execution, guarded
undo/redo, reservation collision no-write, and integrity assertions.
The six-source file is byte-identical to captured integration and actual b415
(SHA256 3138f2ac264cf3a5e52bdd44677eb6f8cf9f70d362a0630e5b16490307a6b22c).
The shared media module differs from newer integration only in an unrelated
occurrence-transition fixture; its `body()` / `commit()` ASTs are identical.

The retained MAIN summary reports six union failures plus two distinct word
setup errors. Exact prepared arrays, the particular rejected read in each
array, and all six behavioral outcomes after a future correction are UNKNOWN.
The local summary does not contain those records; none were invented.
The two word cases and newer f518 source remain out of scope.

## Independent coordination

After the read-only worker returned, read its complete evidence:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-parent-wholepath-0425/evidence/F-D86-parent-read-union-source-facts.md`.
It independently confirms the root-scope versus field contradiction and the
same-index rebase obstruction. It also identifies the existing public
doc.patch/clip.move comparison paths: omitted-read paths use atomic/timeline
dependencies and do not exercise this asset alias. Their reported passing
qualification is not proof for these six. This worker executed no controls.

## Focused future control proposal (not executed)

After the orchestrator resolves the allowed encoding/seam, retain exact
prepared command reads and step dependencies from the normal registered
provider for each mandatory parent selector, with the original assertions.
Compare field and atomic requests on the same normal path: fields must retain
the unrelated `later` edit; explicit atomic and explicit parent/timeline scope
reads must still refuse any intervening parent edit. Confirm native asset
shape absence/null/mirror changes and relevant timing/track/selection changes
still refuse without writes, including A→B→A; retain original retry, inverse,
reservation and undo/redo controls. A passing doc.patch/native clip.move alone
does not cover the parent asset alias. Do not construct new attacks or alter
existing expectations. Obtain ONE fresh independent protected review of the
eventual correction, then the exact MAIN six proof, before any normal merge.

No safe patch or new regression file was created. No review or proof was
requested on this unchanged blocked tree. The existing candidate remains held.

## Static validation

See `verification-commands.txt` and saved diagnostics. The initial evidence
script's full shared media fixture equality assertion detected the unrelated
newer transition setup; the final script checks the exact protected six file
and shared caller ASTs and reports that distinction. No product/test assertion
was edited. Final static checks pass; no behavioral claims are made.
