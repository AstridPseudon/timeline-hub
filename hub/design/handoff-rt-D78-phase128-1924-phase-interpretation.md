# Actual13100 phase interpretation

Resumes rt-D78-live-stack-cause-sol-1915; read-only source/data interpretation.
No new body, browser, Python daemon, HTTP, endpoint, benchmark, collector, attach,
suite, product/test edit or Git mutation. PLAN and contract sections 1–5 remain
unchanged, as do D47 and existing helper ownership.

## Authentic prefix and correlation

Input: ORCH/design/app-P2-D78-live-13100-safe-phases.jsonl, exactly 13,355 bytes,
SHA256 280f186c4694ab7b950d1653400722d3ca4278a101a69a0e2aa38ece085a8836.
The supplied publication is actually mode 0644 here, contrary to the mode0600
handoff. It was not changed. The byte-identical retained copy in this directory
is mode0600; only the supplied allowlisted SAFE data was copied.

All 128 lines parse, have the specified field allowlist, and use local ordinals
1–2. Times are monotone. There are 69 starts, 59 ends, zero raised or summary
records. Phase RECORD counts: handler_entry3, authorization67,
coordinator_admission3, coordinator_lock2, provider3, accept3, receipt3,
http_response44. These are neither request counts nor provider-call counts.
In particular peer1914's “two occurrences” for ordinal1 handler/provider/accept/
receipt means one start/end pair for each, not two invocations.

Ordinal1 has 83 records; ordinal2 has 45. Events are relative to observer start,
not run start or UTC. No wall-clock anchor, supervised PID/birth identity,
daemon instance, phase-sink launch identity, realm/support/port/lock identity or
request-to-native-seed equality proof is present. The actual13100 manifest is
absent locally. The peer identifies the run; that does not supply these missing
correlations. Ordinals restart at 1 for every new observer and are not globally
unique. This prefix shows no timestamp/count reset; that does not authenticate
its daemon incarnation or prove it covers the later original worker.

## Ordered phase facts (milliseconds)

| Local ordinal | Observed boundary | Start | End | Elapsed |
| --- | --- | ---: | ---: | ---: |
| 1 | handler_entry | 5291.084 | 7814.908 | 2523.824 |
| 1 | coordinator_admission | 5459.828 | not recorded | unknown |
| 1 | coordinator_lock acquired | 5459.965 | not recorded | unknown |
| 1 | provider.commit | 5486.173 | 7211.129 | 1724.956 |
| 1 | RequestCommitPort.accept | 6611.748 | 7210.947 | 599.199 |
| 1 | TimelineCommitStore.accept | 6629.580 | 7210.513 | 580.933 |
| 1 | deferred _send(status200) | 7814.552 | 7814.743 | 0.191 |
| 1 | subsequent _send(status200) | 7815.104 | 7815.913 | 0.809 |
| 2 | handler_entry | 22171.560 | not retained | unknown |
| 2 | coordinator_admission | 23057.036 | not retained | unknown |
| 2 | coordinator_lock acquired | 23057.569 | not retained | unknown |
| 2 | provider.commit | 23374.080 | not retained | unknown |
| 2 | RequestCommitPort.accept | 35044.141 | not retained | unknown |
| 2 | TimelineCommitStore.accept | 35259.487 | not retained | unknown |

Ordinal1 has 14 complete authorization pairs, total 15.467 ms, max 1.249 ms.
Ordinal2 has 19 complete pairs, total 31.390 ms, max 3.757 ms, plus one unmatched
start at 45430.793 ms. Its last completed authorization ends at 35552.645 ms.
The final record is authorization start, count20, at 45430.793 ms: this is the
last retained leaf boundary, not a proven authorization hang. Its return may
simply be event129. Provider-to-accept entry for ordinal2 is 11670.061 ms;
receipt entry to prefix end is 10171.306 ms. These are observed intervals,
not CPU, lock-wait, blocked-frame or eventual-duration measurements.

The last completed outer boundaries are ordinal1 receipt/port/provider/handler
and its two _send calls. Ordinal2 demonstrably reached acceptance method entry
and later authorization calls; store entry itself precedes mutex acquisition,
validation and durable publication. It does not prove receipt creation or
transaction completion. The prefix proves no terminal outcome for ordinal2.
Absence after 128 events is UNKNOWN, including provider/accept/receipt completion,
HTTP status and any further request. No provider refusal, crash or auth failure
is established. Method-return events record no returned envelope; the first
HTTP200 pair is deferred, not a socket write. The second is consistent with the
real dispatch flush, which still does not prove client receipt/read/decode.

## Exact instrumentation and concrete observer problems

Captured Runtime1bae and current Runtime87bc have identical observer, server,
coordinator, port, store, daemon and observer-test source. Captured App3c29 and
current App7098 have identical sitecustomize and phase-bootstrap test. Current
harness has the later D79 wiring; that was not present in actual13100. Hashes
of every inspected captured/current source are in interpretation.json.

Observer tests/helpers/p2_commit_phase_capture.py:129 bounds the ENTIRE observer
at 128 events, not each request. _write discards subsequent events and summaries;
the 13,355-byte prefix is far below the 64KiB byte limit. Counters/timing/tracing
continue after saturation. 67 authorization records are repeated calls to the
same revalidation callback from coordinator/port/store operations, not 67 requests.
Source tracing/serialization has overhead, but its causal contribution to the
timeouts is unmeasured. Increasing the cap alone does not fix attribution.

1. _new_request records handler id and thread ident; _request_for_frame reuses
   either. Neither mapping is cleared at handler or dispatch completion. After
   ordinal1's deferred and actual response, another 40 HTTP response records at
   13302.017–15761.742 ms remain attributed to it (statuses200/201). These cannot
   all be that completed commit's response. Thread-ident reuse, handler-id reuse
   and subsequent traffic can all inherit the stale mapping; which mechanism
   occurred is not distinguishable here. They consume 40/128 budget slots.
2. _execution is a contextmanager generator. Python trace emits a fresh “call”
   on generator resume; _trace_inner:261 resets the tracked state and emits
   admission start again. Ordinal1 has a second admission start at7814.072,
   after provider return, despite one handler and one provider invocation.
   The original yielded/acquired state is lost, so its lock end is omitted.
   Missing coordinator_lock end therefore does not prove the lock stayed held.

observer-fix.UNAPPLIED.diff proposes only retaining generator-resume state and
expiring handler/thread mappings on enclosing _dispatch return, after deferred
socket flush. It introduces no emitted phase or budget increase. Clearing on
_timeline_commit return would lose the real deferred response, so the proposed
scope extends through dispatch. Proposal parses, but is NOT applied or executed.
The owning file is Runtime tests/helpers/p2_commit_phase_capture.py; regression
home is tests/test_p2_commit_phase_capture.py: cover one acquisition/release
pair across contextmanager resume, and an actual _dispatch with deferred send
followed by unrelated traffic on a reused thread/handler. Preserve existing
behaviour expectations. App1859 remains sole shipping helper owner; Runtime1908
remains held donor. No parallel author or automatic shipping is requested.

## Actual App path versus faithful daemon source

Runtime daemon imports/registers the provider and coordinator.execute calls
provider.commit synchronously in that SAME daemon, not a second provider PID.
App3c29 harness:934–953 builds the v2 native seed request and calls production
AstridClient.timelines.commit; :990–992 executes the seed Python client with
execFileSync and a 120000ms child limit. That child is a client of the daemon,
not its provider. runtimeEnv() without captureSink does not opt that seed child
into the daemon observer. The Node parent waits synchronously; a Playwright
request watcher does not supervise this direct Python transport or its pending
window. Current App7098 adds a browser watcher, leaving this coverage gap.

sitecustomize installs one observer only for CLI start and drops opt-in env;
harness increments its authoring-launch sink suffix on restart. Each observer
has its own event/request budget and clock. Separate readiness/original
Playwright processes create separate harness lifecycles. Source creates per-run
temporary realm/support directories; actual cross-run sharing/overlap is unknown.
No concurrency, shared-owner-lock or authentication cause follows from source
or the common transport_timeout alone. Agent e89eb's later finite-validation
change was not in captured tuple3c29/831df/1bae/635f and is not an explanation
established by this prefix.

## Disposition and smallest next action

Peer1856/1914: actual13100 failed exit1 after213s, readiness1PASS, native-seed
transport_timeout BEFORE element gesture. All FIVE D80 runs similarly failed
native-seed setup before intended gestures. These are setup outcomes; no element
gesture assertion or product-gesture credit is justified. Original22847 remains
a distinct historical element hang. No live all-thread Python dump/PIDs were
captured, no attach attempted and no refusal occurred. Actual blocked frame,
file/line/wait and common terminal cause remain unavailable.

Smallest justified SOURCE action: owner review the above two observer fixes and
their exact regressions; no auth or performance product patch. Smallest existing
FACT action: App1910/retained producer can resolve which existing per-launch
phase sink/daemon lifecycle and native seed acceptance-file state belongs to
the timed-out original, using safe equality/status facts from retained files,
without exporting a request body or inventing run identities. This could narrow
correlation; it cannot recover an uncaptured stack. Full D78 cause resolution
still requires a real owned all-Python-thread dump during an authentic pending
native seed request, by the already assigned owner under existing authorization.
No new run, collector, attach attempt or gateGO is requested by this report.

## Verification

`python -B <absolute evidence directory>/interpret.py`: exit0, authentic hash,
size/count/allowlist/order/private copy/source hashes and Python AST checks PASS.
Exact command, output and exit are interpret.command/.log/.exit. Detailed
durations and correlations are interpretation.json. `git diff --check`: exit0;
`git status --porcelain=v1`: exit0, empty. Their commands/logs/exits are adjacent.
No tests run: this is an existing-data/source interpretation with no code/test
edits; no suite, body, network, daemon or attach was authorized for this task.
