# AG01 documented sheet history — real proof

Date: 2026-10-21 UTC

## Disposition

PASS for the narrow accepted-history frontier. No product diff was needed.
The documented `apply_sheet(..., client=...)` API remains live, and its
Runtime-history fallback remains required. This is not a claim that all of
AG01, WC7, or WC8 is complete.

## The prior skipped node

The earlier central targeted request was:

```text
tests/sdk/test_timeline_checkout_history_runtime.py
```

It collected as exactly `1 skipped in 0.19s` in
`agt-m2-ag01-detached-sheet-history-tail-targeted-1020231851-29700`. The
skip was the module-level `tests.helpers.runtime.use_runtime()` locator path:
the default targeted command had no `-m integration` environment and no
`ASTRID_RUNTIME_CHECKOUT`, so `locate_runtime()` found no Runtime sibling.
No assertion ran; this was fixture setup absence, not a product result.

## Real qualification

Central result:

```text
agt-m2-ag01-documented-sheet-history-real-proof-native014-sockets-integration-1021015751-27007
```

Exact command run by the central service:

```text
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-current \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169 \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-current/node_modules \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  -m integration tests/sdk/test_timeline_checkout_history_runtime.py
```

Result: **4 passed in 16.12s**, exit 0. The snapshot tree was
`5997f0162374dcfb56597b636caaad597c951b68`; the named lane used the normal
socket-capable environment and Runtime checkout
`/home/user/work/wt/rt-pin-a0dca169` (`a0dca16975dfe8f5e762703b99d9791a16cf7fd7`).
The test module explicitly archives and runs its catalog-visibility Runtime
candidate `3b900c377e7126e14eeb92dc2ce73114cbda5a0e`; it does not fabricate
accepted records or use SQL, a legacy writer, a new DTO, or a new store.

The four passing nodes exercise:

- accepted `TimelineSession` moves, reopened `Checkout`, retained sheet basis
  lookup, guarded accepted undo, CLI publication redo, and Runtime readback;
- raw Runtime revision rows and canonical closure round-trip;
- consumed local draft-step fencing across accepted restore and reload;
- catalog archive/recover plus actual accepted-history preservation and the
  normal Runtime restore path.

The supported fixture is the existing `film` fixture from
`tests/editing_conformance/test_commit_runtime_m1.py`: it calls Runtime's
`timeline_commit_film_fixture.build_film_fixture(tmp_path)` to build the
API-backed duplicate realm/CAS fixture. The daemon is started by the normal
`tests/conftest.py::real_runtime` fixture against that duplicate root. The
four tests pass `authoring_profile="astrid"` at the existing daemon call
sites because these scenarios exercise the Agent authoring/commit provider;
this is the scenario's provider selection, not a fixture writer or authority
substitute.

## Source and boundary proof

`astrid/sdk/timeline_sheet.py:849` preserves the public
`apply_sheet(tl, text, *, client=None)` signature. For a non-current sheet
version, `find_version(..., client=client)` first permits only same-base
working-copy snapshots, then calls the authenticated Runtime history route
with the exact project/timeline scope, `limit=100`, and cursor progression;
each returned revision is reopened through `Checkout.open(..., revision_id=,
client=client)`. It does not obtain accepted history from the local undo
stack or journal. The central first test proves this with actual accepted
Runtime revisions and exact document equality, including source pins.

The central run therefore proves the split required by AG01:

- accepted history and retained sheet bases: Runtime only;
- unsent edits/retry identity and local draft recovery: the existing outbox
  and local draft stack only;
- accepted undo/redo: Runtime commands/publication IDs, leaving detached draft
  bytes untouched.

The narrow direct boundary command was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_checkout_history.py::test_local_restore_stops_at_accepted_base_and_keeps_new_unsent_edits \
  tests/sdk/test_timeline_checkout_history.py::test_sheet_local_basis_does_not_cross_accepted_base \
  tests/sdk/test_timeline_journal.py::test_publish_records_the_message_as_reason_and_the_new_head_as_evidence \
  tests/sdk/test_timeline_journal.py::test_an_in_memory_checkout_writes_no_journal
```

Result: **5 passed in 0.96s** (the first test is parametrized twice). This
keeps local draft history fenced at an accepted base, proves a local sheet
basis cannot cross that fence, preserves the legacy publish rationale note,
and proves an in-memory checkout writes no journal.

## Accepted-journal deletion and ledger disposition

The exact duplicate accepted-journal append was already deleted in
`a7e5abeaa` (`_PublishMixin.publish()`'s accepted-history journal append).
The retained sheet consumer was moved to Runtime history/pagination in the
same bounded sequence (`77945bb62` and its successors), and the documented
client argument was restored by `fb465b336`.

No exact-zero-call accepted-journal helper remains in the current tree, so no
additional leaf was deleted here. `transaction.py` and `checkout.py` journal
writes remain local working-copy/edit/recovery records. `publish.py` also
retains one local `kind="publish"` note with `reason` and revision evidence;
`dd7c1985d` intentionally restored it because the WC7 legacy whole-document
publisher has no Runtime reason carrier. It is not used to read accepted
history and is not a dead accepted-history consumer.

Proposed ledger disposition:

| Segment | Disposition |
| --- | --- |
| duplicate accepted journal consumer | **DELETED / qualified** |
| documented `apply_sheet(..., client=...)` and Runtime history fallback | **KEEP / qualified** |
| local draft journal and pending outbox boundary | **KEEP / qualified** |
| WC7 legacy whole-document writer and rationale note | **REMAINING** |
| WC8 remaining sheet writer boundary | **REMAINING** |
| whole AG01 | **IN PROGRESS**, not claimed closed |

Not run: the prior unchanged 41-test direct lane, Gate3, any full suite,
browser, or live journey. No full* suite was requested.
