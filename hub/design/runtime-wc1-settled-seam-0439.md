# Runtime WC1 settled-proposal seam qualification

Date: 2026-10-21 UTC  
Result: **SOURCE/SEAM ACK** for the existing Runtime half.  No Runtime
product source or test change was needed.

## Source and scope

- Runtime worktree: `/home/user/work/wt/rt-m2-wc1-runtime-seam-0439-r1`
- Branch: `tl/rt-m2-wc1-runtime-seam-0439-r1`
- Source commit: `b92d3e7a05eec65c142294ef4873edd059e9b31d`
- Source tree: `6abc2f117391de8e7e35c0283f575a002199894d` (manager corrected the report transcription against Git)
- Agent context only: `5a625dd4c01149a085a9df85952b34cad70801f9`

The active handoff permits only the existing producer/commit source seam and
its five Runtime test files. The five source/test paths were present and the
worktree was clean before qualification. No Agent, App, Composition,
launcher, schema, generated-client, pin, media-selection, raw-media,
transcript/order, or activation path was changed or run.

## Decision

The proposed single `publish_bundle` consumer can use the existing Runtime
seam without command guessing or snapshot diffing, provided Agent emits the
existing settled six-key artifact and forwards its contents unchanged:

1. `ProducerReads.capture` binds the request to the artifact's immutable
   `admitted_target` pair (`project_id`, `timeline_id`, `base_revision_id`,
   `base_publication_id`) and the host-owned task/attempt/executor/fence/epoch
   identity.
2. It requires a completed, current, settled attempt, the declared
   `authoring_proposal` file, one managed durable JSON output, exact project
   custody/provenance, and CAS size/hash equality. The raw settled bytes are
   authoritative.
3. It strictly parses the exact proposal shape, recomputes the canonical
   `proposal_digest`, and checks the full forwarded command suffix and
   rationale with Runtime's value equality (numeric values compare by value;
   booleans remain distinct). It never derives commands from a snapshot.
4. The existing `producer.guard` must be the first and only guard, with no
   restore/inverse authority sibling. The captured pin is then carried through
   the existing private `producer_attempt` dependency and rechecked at
   acceptance.
5. The existing acceptance/checkpoint path records the acceptance atomically,
   preserves the accepted receipt and original target, and resolves an exact
   retry/replay from the ledger after restart. The qualified cancellation,
   stale/superseded-attempt, and inverse/ABA controls remain intact.

This is a Runtime seam ACK, not an Agent migration or an end-to-end
`publish_bundle` caller qualification. Agent still owns producing the settled
artifact, retaining the original base pair, invoking `TimelineSession`'s
existing queue/flush path, and proving its production caller. Legacy
`publish_authoring_candidate` deletion remains gated by all other callers and
the paired acceptance/restart/retry/inverse run.

## Evidence

Import preflight:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -B -c \
  'import runtime_protocol.timeline_commit_producer, runtime_protocol.timeline_commit_port, runtime_protocol.timeline_commit_producer_checkpoint; print("imports: ok")'
imports: ok
```

Collection preflight used `-p no:cacheprovider` on the exact five-file set and
collected **253 tests**.

The one allowed targeted qualification command was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/test_timeline_producer_guards.py \
  tests/test_timeline_commit_producer.py \
  tests/test_timeline_producer_checkpoint.py \
  tests/test_timeline_producer_record_boundary.py \
  tests/test_timeline_current_union_contract.py
```

Result: **253 passed in 22.94s**.

No full suite, socket/browser/renderer/launcher run, or previously qualified
Agent socket/render case was rerun. No assertion was removed, weakened,
converted, or marked xfail.
