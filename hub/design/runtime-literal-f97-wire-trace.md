# Runtime literal-media f97 wire trace

Date: 2026-10-20 UTC

## Scope

This trace covers only the unchanged `literal-media` parameter of
`tests/test_timeline_public_s2_mixed_cli_journey.py`, with Runtime source at
`7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e` and the exact Agent f97 checkout
`f97b2b87688abb20280572a5fc23e4f69ec9e3f8` (`agt-pin-f97b2b87`). The
historical-audio parameter, control journey, comprehensive pair, and full
suite were not run.

## Evidence

Central test-service run:

```text
runtime targeted --files tests/test_timeline_public_s2_mixed_cli_journey.py
pytest effective selection: -m integration --runxfail -k literal-media
```

Result: `1 failed, 1 deselected`. The deselected case is the forbidden
historical-audio parameter. The central log is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-literal-f97-wire-trace-targeted-1020180059-5521/log.txt`

The test starts the normal Runtime daemon and door, performs the normal
credential/handshake/import/publication setup, and reaches the real HTTP
commit route. No fake acknowledgement, provider, schema, fixture, or auth
override was used. A passive external wrapper around the original
`RuntimeHandler._route`/`_send` retained the raw request and response; it did
not alter the test or product code.

## First remaining literal failure

The first assertion failure in the unchanged test is its observer lookup at
`tests/test_timeline_public_s2_mixed_cli_journey.py:328`:

```text
trim_wire = next(row for row in observed if row["key"] == key)
StopIteration
```

This is not a pre-POST refusal. The original route received:

```text
POST /v1/projects/7b6f2bae8ffe42bf925216c38249ed79/timelines/literal-film/commit
Idempotency-Key: public-s2-cli-trim
base_publication_id: txn-581c6cb2faf049179b384b8cf7d8059f
command: clip.trim parent/clip:literal-media args {in_s: null, out_s: 4.0}
source: {via: cli}
```

The response was an actual Runtime refusal:

```text
HTTP 409
code: conflict
message: original authored guard changed
details.status: conflict
details.reason: dependency_changed
details.conflicts[0].ref: parent/track:music
details.conflicts[0].kind: dependency_changed
details.conflicts[0].base: {id: music, kind: audio}
details.conflicts[0].theirs: {id: music, kind: audio, label: Independent Python label}
details.conflicts[0].ours: absent
```

The HTTP/auth/provider path therefore worked far enough to evaluate the
command and return a structured conflict. The failure is not health, door
reachability, schema mismatch, missing provider, or credential refusal.

## Why the unchanged observer is empty

The test's `_send` observer records only when
`getattr(handler, "_defer_response", False)` is true. Runtime's normal
`RuntimeHandler._dispatch` sets that flag while `_route` runs and stores the
pending response. It then sets the flag false and flushes the pending response
through `_send`. The test observer is installed before the request, not too
late; its condition simply excludes the actual response-flush call. The
passive wrapper saw the same body/key at `_route` and the 409 payload at
`_send`.

## Source of the semantic refusal

Agent f97's `astrid/packs/timeline/cli_native.py:commit_trim` delegates the
no-pending native path to `TimelineSession.trim`. The f97 trim capture then
executes `clip.trim` in `_trim_commands.py`; for an audio clip it reads
`parent/track:music` as a whole entity to validate the active audio track.
That whole-entity read is recorded in the command's `reads` and `expect` data.

The peer edit changes the track's `label`, so Runtime's dependency comparison
correctly sees the recorded track value as changed and refuses the stale trim.
The unchanged journey expected the label edit to be disjoint and the trim to
rebase with HTTP 200. That expectation is not met by this command's current
read granularity.

## Handoff

Agent should decide how the raw-audio active-track guard can record only the
fields it actually needs, while preserving the guard and Runtime's genuine
conflict semantics. Do not make the Runtime accept this 409, weaken auth, or
rewrite the unchanged journey. The observer's `_defer_response` condition is
a separate diagnostic/test-harness issue; it must not be used to claim that
the POST was never sent.
