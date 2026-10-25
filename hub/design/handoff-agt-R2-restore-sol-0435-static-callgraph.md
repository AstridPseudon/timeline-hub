# F-D86/R2 source-only correction

Base: `7d35b32343d32fa94091b9e9f1fa160c2868e0cb`. Product ancestor
`72a5e5333171bed4221865329ab48eb233b1bbda` is unchanged. Only
`tests/sdk/test_timeline_restore_effect_order_runtime.py` is modified.

Read PLAN §3; C0 request/addressing/conflict/reply/undo rules in commit-v2.md
§§1–5; BOARD-HEADER D56/D69/D72/D83/D89/D93; both independent failures:
`handoff-agt-restore-review-0425-B-R2.md` and
`agt-R2-restore-control-rereview-0431-report.md`.

## Fixture and authorization

The new file aliases the exact fixture used by P4 runtime tests:
`runtime = test_native_batch_ingress.runtime`. No new fixture/adapter or
credential provisioner is added. Existing test conftest owns the sandboxed
HOME, workspace and project roots. The regression supplies only its own outbox.

`test_native_batch_ingress.py:44–118` uses `use_runtime(vendored_runtime_commit())`
and `new_runtime_daemon(..., authoring_profile='astrid')`; its generated client
transport serializes HTTP into MemorySocket and invokes the actual RuntimeHandler.
The injection replaces the socket only. Resolver, composition reader, bundle
reader, generated operations, credentials, handler, provider and store are real.
The fixture's direct project/timeline bootstrap is unchanged; all regression
edits and inspection of accepted history use the authenticated public client.
The regression never calls the fixture's direct-service `world.history` helper.

runtime.lock pins Runtime `6634a17f3ffd885567ba3c91b6c7a560df7375a4`.
Static inspection used that revision through git show, without checkout/import.
The local runtime integration HEAD differs in timeline_commit_store.py; the
daemon/server/service/provider/coordinator files traced here are identical.

At the pinned Runtime, daemon.py:132–136 provisions the existing owner credential;
the fixture keeps `token = daemon.token` and passes that token unchanged to
`AstridClient.open(... actor_id='owner', protocol_version='workspace.v1')`.
client.py:308–327 negotiates/validates exactly the original six SDK scopes.
No token/scopes are introduced or broadened. Restart reuses the original support
root and normal daemon credential behavior. D93's original calls/auth apply.

## Full method envelope and call trace

1. Test `opened()` → public `timeline.open` lazy export →
   commit_session.open:263 → TimelineSession.open:144. This checks the actual
   handshake realm/actor, resolves via store.resolve_ids:410 and real
   open_composition/inspection, then calls history(limit=1) even with a clean
   explicit outbox. RemoteTimelines.history:253 → _typed →
   WorkspaceClient.list_timeline_commits:502 → generated.list_timeline_commits:967.
   The generated operation exists, adds Bearer auth in generated._request:648,
   and goes through the fixture HTTP/MemorySocket handler. Handler GET commits
   authenticates projects:read and provides its reauthorization callback to
   RuntimeService.list_timeline_commits:2537 and authenticated fixed-head history.
2. Public open fetches the complete exact revision/publication pair via
   store.fetch_bundle:457 → RemoteTimelines.open_bundle:26. Real immutable
   composition reads and exact-pair source hydration run; fake resolver/open
   methods and fabricated private canonical input have been removed.
3. capture_track_create → commands.execute → track_create → Recording.create
   supplies the normal local capture. Timeline.command/_append stages it;
   Timeline.commit → TimelineSession._submit/_flush:525 freezes the exact base,
   commands, metadata, key and body in the outbox. RemoteTimelines.commit:221
   resolves canonical scope and invokes WorkspaceClient.commit_timeline:485 →
   generated.commit_timeline:963 → generated._request → MemorySocket → handler.
4. RuntimeHandler._timeline_commit:296 authenticates projects:write, checks
   scope/body/key and binds publisher from the real credential. Its callback
   rechecks projects:write and the same publisher. RuntimeService.commit_timeline:
   2448 validates route/request → _execute_timeline_commit:2464 builds authenticated
   invocation/hash and RequestCommitPort → CommitExecutionCoordinator.execute:69.
   Coordinator rechecks durable retry before/after provider execution. Daemon
   startup loads fixed `astrid` profile via timeline_commit_provider.py and
   registers it using RuntimeService.register_timeline_commit_provider:2391.
   The factory is the worktree's create_runtime_commit_service, not a test provider.
5. Restore uses the method that exists: `opened().session.restore` →
   TimelineSession.restore:464 → flush → the same authenticated commit path.
   Timeline itself has no restore method. Provider commit.py:1218–1235 requires
   one restore and the exact head pair; :1301–1310 loads the retained source and
   verifies its exact content digest. commands.execute handles timeline.restore
   through native recording, and CommitPatch records the complete closure effects.
6. Undo uses the correct public signature `Timeline.undo(publications=[...])`
   (commit_session.py:77), which dispatches TimelineSession.undo:422 → _flush.
   A positional list would select Checkout's local-draft undo path. The existing
   provider authenticates selected history and before/after closures, keeps
   original captures, and scans later/nonselected history. _step_undo.inverse_stages:
   329–359 selects the bounded ordinary-restore branch. inverse.apply_inverse:
   1127–1186 performs reversal and records stage boundaries/effects. CommitPatch
   projection :536–557 compares complete effect multisets with execution and
   retains captured sequence. This production inverse is only the implementation
   under test; no production inverse/diff/execute function computes expectations.
7. At pinned Runtime store.py:1480 preview authenticates, validates context and
   exact expected head, then returns null receipt without accept. accept:1522
   authenticates and validates again inside the outer transaction. _publish:1732
   writes the durable receipt/history and compare-and-swaps BOTH head IDs at
   :1757. The test observes complete public history and current projection before/
   after preview and receipt/head/history after acceptance.
8. Both post-restore and post-undo restarts use the original fixture. Exact retry
   calls public RemoteTimelines.commit with the recorded request and original key
   after restart. DomainResult.as_dict serializes the real CommandReceipt. Raw
   reply data/receipt must equal the recorded wire response. TimelineSession's
   two extra presentation fields are checked explicitly before comparison with
   its normalized result. Retried body bytes/key and entire history must match.

## Independent scene/oracle and conservation

Schema inspection found the predecessor fixture also invalid: track rows require
label and disallow a top-level seed. The legitimate replacement has id
opaque-track, kind visual, label Opaque track, and app.seed.opaque=[null,false].
All prior opaque literal values/types are retained. The added
{literal: new-opaque-sibling} value is now app.seed.sibling, beside the opaque
list, so the retained direct-sibling assertions actually describe the effects.
The predecessor scene's nested seed.opaque and top-level opaque were not direct
siblings under the complete recursive effect contract. This is a correction of
the new regression fixture, never a change to historical ID5 setup or policy.

The complete source patch is explicitly specified as two effects, in order:
set app.seed.opaque from [null,false,changed-seed] to [null,false]; remove
app.seed.sibling with its complete present object before value. The complete
inverse is explicitly specified in reverse order: set sibling from absent to
the original object; set opaque from the short list to the changed list.
Every op/ref/path/before/value is literal and independently specified. There is
no sorting, deduplication or dropped effect. Equality assertions check the
entire authenticated source/preview/inverse arrays and exposed/stored step lists.

The complete changed canonical closure must equal the authentic target closure
with only these two leaf changes and Runtime-generated parent revision/digest
wrappers. Restore and undo then require exact complete target/changed closure
equality, including their original immutable revision/digest pins. Stored source
receipt/result, previous pair, publication identity and publisher are checked.

All 21 predecessor assertions retain their purposes; candidate has 61 assertions
(counts alone are not the conservation proof). Exact accepted restore, target
closure, restore pins/command, three sibling predicates, preview null receipt/
accepted/no-write, changed closure, reverse order, unchanged source/history length,
undo_of, accepted head pair, exact retry and no added history remain. The
production inverse oracle is replaced by complete literal expectations; head
checks use authenticated history and current public inspection; retry equality
accounts explicitly for SDK presentation fields versus raw transport envelopes.
No expected refusal, exception handler, skip, xfail, raw SQL or forged history is
introduced. Restart, source closure, full prefix history and wire replay checks
are added. No ABA/capture/order control is replaced or claimed proven here.

The entire historical word-binding test file and the file containing the three
strict capture/order/ABA controls are byte-identical to HEAD. Static AST inspection
confirms the exact required selector definitions still exist. Hashes, static
predicates, in-memory compile results and assertion counts are in
static-validation.json; exact baseline/candidate Ruff/mypy commands/results are
in checks.txt. Configured mypy skips imports and does not check untyped function
bodies by default; this is static evidence, not execution proof.

## Required next gate (not executed here)

One fresh independent protected review, then actual MAIN old-RED/new-GREEN proof
of this regression alongside the unchanged original and original strict controls:

```
tests/sdk/test_timeline_restore_effect_order_runtime.py::test_id5_public_undo_of_restore_preserves_authenticated_effect_order
tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse
tests/sdk/test_timeline_commit_provider.py::test_original_capture_claims_are_verified_before_refresh
tests/sdk/test_timeline_commit_provider.py::test_reversed_inverse_target_order_is_refused_without_partial_acceptance
tests/sdk/test_timeline_commit_provider.py::test_undo_detects_aba_and_unchanged_write_publications
```

No pytest/collection, product/test imports, helpers/fixtures/test functions,
probes/services, full suites, browsers, installs or originals were executed.
No functional credit. Product 72a remains source-PASS/HELD; this source-only test
correction does not authorize its normal merge or substitute D95 negatives.
