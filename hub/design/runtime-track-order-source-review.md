# Runtime track reorder source review

## Verdict

**Bounded Runtime SOURCE ACK for the media-only `track.reorder@1` source
shape.** The current Runtime generic command, request, read/write/selection,
recorder, JSON-reload, and idempotency envelopes can carry the source contract
without a new DTO field, endpoint, store column, or persisted `track_order`
leaf. This is a source-contract ACK only. It is not a public schema acceptance,
generation, pin, freeze, native qualification, activation, or writer-deletion
claim.

## Exact immutable source identity

The requested `Agent3684/treece34` resolves through the hub ref
`refs/remotes/hub/timeline/agent/tl/agt-m2-track-order-shared-doc-closure` to:

- Agent commit: `3684b8458389d70ee0713d669c44cdd67a9ddcf8`
- Agent tree: `ce34c03784dfb28ab7d25af325304a45afa8c5d2`
- Parent source-proof commit: `c1ae9e93d31c1c091b93c952ae803059a890bf61`
- Parent source-proof tree: `a54be6e2269e191c032496b3b73cfcf761d7402e`
- Source schema blob: `c0c28e55349493bf26b999b6052c97518c7e1549`
- Source schema SHA-256: `c338671597411bb50937fa4678cf1ef0e58ef90df52d0b630694f35ac3b72218`

Commit `3684b845` only removes the handoff document from the Agent repository;
the source implementation and focused proof are inherited unchanged from
`c1ae9e93`. The reviewed source files are:

- `astrid/sdk/timeline/_track_commands.py` (blob
  `dee358e499a47b595eb39cae7c64bc83e624c806`)
- `astrid/sdk/timeline/_command_state.py` (blob
  `6d3206cff3e419bd108cfff1781c31e23be5f706`)
- `tests/editing_conformance/test_recipe_track_order.py` (blob
  `4ec107df8236260d73f05ed53d02bea50c6f6850`)

## Runtime boundary reviewed

Runtime base is commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`. Its installed command schema is
SHA-256 `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
The Agent source schema's `track.reorder` clause is not in that public/current
operation inventory, and the Agent schema digest `c338...` is **not** accepted
or pinned by this review. Runtime's generic `EditCommand` envelope is
intentionally operation-extensible: it validates the common shape and finite
JSON while the installed semantic provider validates operation-specific args.
That is why this is a bounded ACK rather than a claim that `track.reorder` is
already public or activated.

The generic carrier checks pass for the exact source shape:

- `track.reorder` uses `select: "parent"`, `args.order`, and
  `args.expected_order`; Runtime does not serialize a separate order field.
- `parent::track_order` is a valid generic target key for `expect` and
  `authorship`; `AgentRead`/`AgentWrite` token paths and `AgentSelection` carry
  the collection claims; `Recorder` retains them as ordinary JSON claims.
- `timeline_commit_port.command_leaves` has no special rejection for this
  non-batch operation. `timeline_commit_store` persists the command and
  recorder as canonical JSON, compares the recorded command to the accepted
  result, and uses the existing request hash/idempotency ledger.
- There is no Runtime-owned authored `track_order` persistence leaf. The
  virtual address remains an overlap/inverse guard; the raw `config.tracks`
  rows remain the carrier.

## Source semantics and boundaries

The exact Agent handler and focused proof provide the operation-specific
meaning Runtime deliberately does not infer:

- capture selects the complete parent `config.tracks` collection and records
  the original membership/order; execution requires a complete unique
  same-owner permutation before arranging existing raw rows;
- raw track objects are reordered in place, preserving labels, null/false/zero
  values, clips, opaque fields, config siblings, and
  `timelineDataLanePlacement` without creating `track_order`;
- disjoint track-label edits rebase, while changed membership/order/identity
  refuses; inverse checks the complete intervening history and rejects a real
  `A -> B -> A` sequence; serialized bundle/record reload, replay, inverse,
  redo, and equal-final-state replay are covered by the focused proof;
- the `lanes` argument is rejected. A lane-bearing App gesture changes
  `config.app.timelineDataLanePlacement` as well as track order and must remain
  unsupported atomically for this media-only command.

App2's existing media-only producer is therefore the bounded consumer
prerequisite: it may eventually capture the exact raw parent track identity
permutation, but it must retain the current serializer until command-session,
outbox/recovery, and native-consumer proof exists. The lane-bearing branch must
not be split, and serializer/fallback deletion is not authorized by this ACK.

## Evidence

Targeted no-socket discriminator, run against Runtime base `95bd3c5`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python - <<'PY'
  # validates exact track.reorder envelope, virtual guards, Recorder, request,
  # and JSON reload
PY
```

Result: **passed**. `EditCommand`, `Recorder`, and `CommitRequest` each
accepted; JSON reload was exact; output explicitly confirmed “no new DTO
field.” No full, matrix, browser, live-socket, generated-client, pin, or
publication test was run.

The source proof was inspected at the immutable Agent identity above. The
prior App2 source-compatibility report records the inherited focused Agent
proof as **3 passed** and the App2 controls as **46 passed**; this Runtime
review does not relabel those results as Runtime acceptance.

## Non-claims / next step

There is no accepted-public-`6ba7` `track.reorder` claim here. The eventual
native qualification must pair the exact Agent provider/schema with the
Runtime contract through the normal generation/pin process, then prove App2
command-session/outbox/restart/retry behavior and deletion of the old media-only
writer. Mixed lane ordering remains a separate atomic carrier problem.
