# Runtime R2r inverse-stage review handoff

Result: **FAIL** on the author commit
`a7448678786ea9d2b7e223c76760069595d1a505` (effective baseline parent
`7ca1a227815404252fec1e4768e550610f9c5705`).

The grouped image authentication is materially present: Runtime derives every
stage from the authenticated input and flat effects, validates exact native
writes, exact effect before/after bytes, physical refs, revision/content
digests, and final output equality. The real Runtime store accepted and replayed
the author's valid candidate, and the requested Runtime neighbours were 92/92
green.

Blocking finding: `runtime_protocol/timeline_commit_auth.py:719-773` treats
`inverse.stage` provenance as unchecked annotations. Because these bindings do
not carry `physical_ref`, `validate_bindings()` skips them at line 347. The
checker validates only syntactic sorted ranges and nonempty strings. It does
not bind `boundary.publication_id` to `records.undo_of`, `boundary.step_id` to
the authenticated target step, or `boundary.command_ordinals` to the actual
enclosing command/step; it also does not authenticate the stage binding's own
ref/policy/dependencies. Real-service probes changed each of those fields and
got `commit_status accepted`; history replay also returned `history_status
accepted`.

Probe outcomes:

```text
wrong_publication ACCEPTED:accepted
wrong_step_id ACCEPTED:accepted
wrong_command_ordinals ACCEPTED:accepted
wrong_stage_ref ACCEPTED:accepted
wrong_policy REFUSED invalid_prepared (schema guard only)
```

This violates C0 §2 effect-binding provenance and §5/C0c grouped inverse
boundary identity. It permits durable forged stage annotations despite correct
effect bytes. The fix must remain auth-only, use the persisted authenticated
undo target/step records and existing physical lineage, and preserve all
normal/equal/ABA/foreign/created/history/forgery protections. Do not weaken the
effect-image guard or flatten stage provenance.

Source handoff:

- Agent `_commit_patch.py:457-472` creates ordered stage/effect ranges.
- Agent `_commit_patch.py:503-522` emits per-stage effect/materialization
  bindings from provider-observed closures.
- Agent `_commit_patch.py:620-666` performs ordered historical stage replay and
  final reachability checks.
- Runtime `timeline_commit_auth.py:630-701` computes authenticated outputs;
  `:704-816` computes grouped stage images; `:343-437` checks effect bindings;
  `timeline_commit_store.py:201-295` replays persisted acceptance.

No source/test repair was made in this review. The Agent 53/58 matrix was not
available here, so no full matrix qualification is claimed.
