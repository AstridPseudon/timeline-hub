# PRIVATE017 ordered/RT03 source-only preflight

Date: 2026-10-21 UTC. Worker: \`agt-m2-ordered017-proof-packet-source-preflight-0846\`.

## Disposition

This is a source/preflight handoff only. It does not authorize either Runtime body, an Agent lifecycle, a native/HTTP proof, a pin activation, or public adoption.

Exact artifact/source tuple already approved for compatibility:

- Runtime42a: commit \`42a7203f49bb89f299ec854cfbf2b1444e815a7c\`, tree \`1f220b3d3a27e8eb061b15c944bad784c8fdb82e\`, package \`0.2.17\`.
- Agent frozen feature source ed5: commit \`ed5fd33c4a7fa9956178f9b24eb127415eaca9e6\`, tree \`f4a632e4f627499e0b15d8477db9aaab78ebb3d2\`.
- Agent raw schema SHA-256 \`6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16\`; canonical SHA-256 \`9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6\`; 65 definitions / 37 \`EditCommand\` clauses.
- Runtime health/schema digest \`sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd\`; raw bundle \`sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f\`; artifact version \`sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0\`; 76 artifacts.

These approvals are artifact-only. The normal Agent consumer c964 review remains **REQUEST CHANGES/HOLD** until the current-safety repair is independently reviewed. Repair0828 reports a complete uncommitted patch, but no repaired commit/tree or independent approval exists in this handoff. The repaired pin must be the later exact harness commit, not c964 relabeled and not the prospective pre-harness tree.

## Exact Runtime preparation and ownership

Prepared Runtime node:

- commit \`aa0c26e0dafc6a749a1c8aae5ccfe971a1ce27d4\`, tree \`09699414ff8ca79f3e9146b44b5713a10b8ef132\`;
- parent is Runtime42a; its only changed path is \`tests/test_timeline_owned_reference_integration.py\`;
- the file is marked \`pytest.mark.integration\`.

The two and only two Runtime-owned nodes are:

1. \`tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo\` (aa0 lines 239–340).

   It seeds \`config.app\` with ordered siblings \`before\`, \`com.example.compiler-canary\`, and \`after\`; removes one null-valued key; requires the two recorded writes and exact \`insertion_order\`; restarts; retries the same body/key with provider execution forbidden; compares durable dump/history; then performs guarded inverse and inverse-of-inverse redo while checking exact opaque/null values and order.

2. \`tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract\` (aa0 lines 127–237; the distinct original RT03 body).

   It creates an owned raw parent reference through the normal Runtime door; checks the projected \`timeline_references\` row and revision snapshot; keeps occurrences/clips empty; restarts and exact-retries without provider execution; refuses changed same-key payload, foreign raw media, and occupied identity atomically; then inverses only the accepted reference while retaining the unrelated reference and original document payload.

Runtime owns both nodes. Agent must not add a duplicate ordered lifecycle or a second RT03 body. RT03 is not the materialization proof.

## Bounded current Agent source required by those nodes

The exact repaired Agent checkout must retain these source semantics and callers.

### Frozen ordered feature

- \`astrid/core/timeline/schema/edit-command.schema.json\`: optional \`AgentWrite.insertion_order\`, string-array items, absent-key compatible, closed object; the raw/canonical and 65/37 counts above remain exact.
- \`astrid/sdk/timeline/_project_data_commands.py:79-124\`: parent-only \`project-data.write\`, explicit target/key/finite JSON and size limits, \`replace\`/\`remove\`, absent-key guarded no-op, namespace pruning, and complete sibling order passed to \`ctx.clear\` when the empty target is removed.
- \`astrid/sdk/timeline/_recording.py:88-157\`: \`verified_media\` is retained; \`assign\`/\`clear\` emit \`insertion_order\` only when supplied and never invent it for ordinary writes.
- \`astrid/sdk/timeline/_command_state.py:391-565\`: exact present/absent state writes and order-aware restoration; missing target/order or changed historical order refuses rather than reordering an unrelated container.
- \`astrid/sdk/timeline/inverse.py:31-102,164-193,332-506\`: guarded inverse forwards the carrier, validates membership/order and dependency reads, and preserves strict history-unavailable/inverse-conflict behavior.
- Existing semantic witnesses remain \`tests/editing_conformance/test_recipe_m2_project_data.py\` (especially lines 126-263 and 367-394) plus the Runtime ordered node. The old ordinary absent-key negative remains; no passing assertion may be converted to refusal.

### Original RT03 source feature

- \`astrid/sdk/timeline/native_parent_reference_commands.py:1-119\` is the Agent carrier. It writes only the namespaced parent source reference, uses existing \`capture_version\`, requires exact Runtime \`verified_media\` for the raw pin, validates the pin, and refuses occupied identity. It is unplaced: no occurrence, clip, shot placement, or visible-media write.
- \`astrid/sdk/timeline/commit.py:926-957\` supplies Runtime raw-media verification for \`timeline.reference\`; it must not be replaced by caller metadata or a catalog/display-ID lookup.
- \`tests/editing_conformance/test_recipe_m2_parent_reference.py:1-157\` retains the source-only positive, exact verified-media requirement, occupied-ID refusal, order/reload/inverse/redo, and no-placement boundary.
- Runtime projection remains Runtime-owned: exact parent \`timeline_references\`, role \`source\`, one matching \`media_id == content_digest\` dependency entry, project/timeline scope, and inverse-only ownership for removal. No new Agent carrier or Runtime DTO is needed.

### Current Agent caller/guard surface

Preserve current source hydration, \`verified_media\` forwarding, outbox/identity scope, transcript/source guards, document and scene/current-cache controls, Windows/readiness/custody controls, and current public014/95 boundaries. Relevant source/accepted-history checks remain in c964 \`commit.py\`, \`native_checkout.py\`, \`sync.py\`, and \`tests/sdk/test_timeline_sync.py\`. Neither Runtime node accepts a fake provider, forced schema, or catalog substitute.

Repair0828's exact seven-file patch against c964 is:

~~~
astrid/sdk/timeline/sync.py
tests/editing_conformance/test_inverse_clear_batches.py
tests/editing_conformance/test_native_sheet_current_runtime.py
tests/editing_conformance/test_recipe_occurrence_media.py
tests/packs/rendering/test_render_export_task_adapter.py
tests/sdk/test_child_bridge_d18.py
tests/timeline/test_authoring_media.py
~~~

The reported repair restores detached ordinary sync capture without private \`_client\` access, the absent-ancestor inverse dependency guard, shared-occurrence NativeSheet current proof, Remotion helper-source integrity, child-bridge identity/close behavior, and authoring/media same-alias safety. It changes the obsolete same-alias positive into refusal plus the current raw-old successor positive. This is current-safety preservation, not a change to frozen 65/37 semantics. Independent review must confirm the patch against c964 before any Runtime body.

## Frozen feature versus current safety

The intended semantic delta is narrow: ordered namespace removal adds one optional write carrier and guarded inverse; Runtime42a packages that carrier normally. Review0824 confirmed the generated carrier, all 76 artifact bytes, all 15 normal lock entries, generator/manifest/vendor checks, and no hand-written types or old-client mix.

That does not prove current safety. Review0824 found missing or broken current behavior in NativeSheet shared-source coverage, inverse absent-ancestor dependency protection, Remotion source integrity, child-bridge identity/close, same-alias media refusal/success, and authoring-media/media safety; its bounded lane was \`188 passed, 3 failed\`. Repair0828 reports \`258 passed\`, \`105\` frozen-floor passes, one child identity/close pass, AST parsing for seven touched Python files, and \`git diff --check\`, but these are worker claims, not independent approval of the repaired source. No repaired exact commit/tree is available here.

The repair must also leave these constraints untouched:

- public014/95 remains immutable and separate from private017;
- no public pin, integration adoption, generated-artifact rewrite, version relabel, caller activation, or expected-assertion weakening;
- current non-feature source is preserved by semantic/file comparison, not by assuming a merge parent resolved deletions;
- no current source/custody/transcript/scene/cache/outbox/Windows/readiness or hold/null guard is dropped while retaining ed5 schema bytes.

## Artifact and import constraints

The future normal request must use a clean, harness-committed repaired Agent checkout and immutable Runtime aa0. Record the real Agent commit/tree; do not guess them. Its \`runtime.lock.json\`, generated Python and TypeScript metadata, package version, health digest, artifact version, and all 15 lock entries must match Runtime42a's 0.2.17/all76 tuple. Generated files are read-only evidence here; no regeneration or pin update is requested by this worker.

Use the existing Agent environment because the Runtime environment lacks the Agent provider's \`filelock\` and Pillow dependencies. The source-only preflight used no dependency installation, shared-vendored writes, or cache output. Future execution, if separately authorized, must import:

~~~
runtime_protocol  <- exact aa0 Runtime checkout
astrid / astrid.sdk.timeline / astrid_runtime_client <- exact repaired Agent pin
~~~

with \`ASTRID_RUNTIME_CHECKOUT\` and \`ASTRID_CHECKOUT\` explicitly set and \`PYTHONPATH\` ordered Runtime checkout then Agent checkout. Use \`PYTHONDONTWRITEBYTECODE=1\`, \`-p no:cacheprovider\`, and private \`tmp_path\` storage. No shared venv, node_modules, runtime, cache, generated artifact, or worktree may be modified.

## Materialization controls outside the ordered node

The ordered node covers project-data order, exact retry, inverse/redo, and Runtime durability. It does **not** cover current v2 media materialization. Existing reports identify these controls without authorizing a new matrix:

- Smallest existing Agent real-provider candidate: \`tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]\`. The parameter family is image-add/image-swap/video-add/video-swap; only image-add is the bounded candidate. Existing assertions cover real media selection, v2 capture, owner/asset creation, restart, exact same-key retry with provider execution forbidden, undo/redo, identity collision, changed same-key refusal, and store integrity.
- That candidate does not explicitly prove the complete accepted v2 source/map/owner boundary and is not HTTP transport. Separate existing \`tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_semantic_batch_original_pins_reload_inverse_redo[python]\` uses an in-memory \`MemorySocket\`; it is not a live-socket proof and does not cover v2 source/map/owner or lost-ack retry. These must not be conflated with the two Runtime-owned nodes.
- Existing materialization reports additionally require all seven captured fields (resolved, expect, authorship, reads, selections, bindings, created); exact original S/I to destination D/J source and owner bindings; exact \`materialization.source\` parent/source dependency; fixed \`materialization.owner\`; flat \`shot:D\` and \`shot:D/item:J\` map; raw \`item_id\`/\`id\` distinction; opaque data, allocator seeds, stale-sibling replay, and sibling-first inverse/redo.
- Runtime-side controls remain separate: authenticated own-slot/occupancy and reservations; foreign/global/retired collision refusal; ledger-first exact retry; original-source dependent-B after A/reload/disjoint edit; inverse/redo/restore provenance; and malformed or missing source/owner/scope/map refusal without writes. Existing v1/public captures and original positive/refusal assertions remain intact.

These are existing bounded controls and source reports, not a request for a new Cartesian matrix. Materialization remains unqualified and must not be silently claimed by the ordered proof.

## One exact future manager request

After the repaired Agent patch is harness-committed and independently approved, issue one Runtime-manager request with the exact repaired Agent commit/tree substituted for placeholders:

~~~
RUNTIME_ROOT=<clean checkout of aa0c26e0dafc6a749a1c8aae5ccfe971a1ce27d4>
AGENT_PIN_ROOT=<clean checkout of independently-approved repaired c964 pin>
AGENT_PIN_COMMIT=<actual repaired harness commit>
AGENT_PIN_TREE=<actual repaired tree>

test "$(git -C "$AGENT_PIN_ROOT" rev-parse HEAD)" = "$AGENT_PIN_COMMIT"
test "$(git -C "$AGENT_PIN_ROOT" rev-parse HEAD^{tree})" = "$AGENT_PIN_TREE"
test -z "$(git -C "$AGENT_PIN_ROOT" status --porcelain)"
test "$(git -C "$RUNTIME_ROOT" rev-parse HEAD)" = aa0c26e0dafc6a749a1c8aae5ccfe971a1ce27d4

env ASTRID_RUNTIME_CHECKOUT="$RUNTIME_ROOT" ASTRID_CHECKOUT="$AGENT_PIN_ROOT" \
  PYTHONPATH="$RUNTIME_ROOT:$AGENT_PIN_ROOT" PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --collect-only -m integration \
  "$RUNTIME_ROOT/tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract" \
  "$RUNTIME_ROOT/tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo"

# Continue only if exactly 2 tests collect and independent pin approval is
# recorded; then run the same two selectors once, without --collect-only.
~~~

This is the sole future Runtime request in this handoff. It is intentionally not run now. It must not add the Agent materialization candidate, duplicate RT03, use live HTTP/browser/native/render paths, modify generated artifacts, or claim private017/public014 separation has changed.

## Evidence and limits

Read-only source inspection here used \`git show\`, \`git diff\`, and \`git grep\` against local Agent/Runtime objects. No test body, daemon, HTTP/socket, native, install, render, browser, private proof, full suite, or shared dependency operation was run.

Reused source-only evidence from existing reports:

- Runtime aa0 collection: the two exact nodes collected; no body ran.
- Runtime42a artifact review: generated/manifest checks passed; 76 current-union tests and 141 focused Runtime tests passed in the approved artifact review, with broad/full/native/HTTP/browser lanes explicitly not run.
- Agent c964 staging: normal updater/checker and bounded source checks passed, but independent review0824 rejected the consumer on current-safety grounds.
- Repair0828: reported focused current/guard \`258 passed\`, frozen floors \`105 passed\`, child guard \`1 passed\`, AST parsing, and diff check; these do not replace independent review of the exact committed repair.

No implementation or generated artifact was changed in this worktree.
