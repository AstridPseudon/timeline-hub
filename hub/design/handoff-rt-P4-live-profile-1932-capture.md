# P4 actual-handler capture handoff

Ready for Agent's next meaningful D73 P4 submission; no live body submitted here.
Runtime base: e89eb8c7dfa8cb2c451653ab200dbf77df28b173. No product/test/kit/pin changes.
The actual-host supported-tool decision and service submission belong to Agent.
Do not run another body just to exercise this helper. Publish these exact helper
bytes and this handoff via the manager's normal flat design handoff; this worker
cannot write design/ under D30. `peer-runtime-to-agent-orchestrator-20261024T1932Z-P4-one-real-profile.md`
is the outstanding venue request, not an actual-host tool receipt.

## Exact process and boundary

The three original selectors and recipe are in Agent's
`tests/suites.conf.candidate`, executed by `tools/p4-d73-pinned-launch.sh`.
The ten-note test aliases `test_native_batch_ingress.runtime`. That fixture's
`new_runtime_daemon(..., authoring_profile='astrid').start()` creates the real
RuntimeDaemon and RuntimeHTTPServer in the pytest process. RuntimeDaemon
publishes `os.getpid()` and starts an HTTP listener thread. However, this
fixture's generated-client transport calls
`RuntimeHandler(sock, ('127.0.0.1', 1), server)` synchronously on a MemorySocket.
Both current and retained Agent f4d6c72c contain this exact route. No separate
daemon PID or external Agent Worker should be guessed for this original.

The measured server seam is `runtime_protocol.server.RuntimeHandler._dispatch`.
Its commit route calls `_timeline_commit` -> `RuntimeService.commit_timeline`
-> `_execute_timeline_commit` -> coordinator/provider -> RequestCommitPort
-> TimelineCommitStore.accept. The provider factory is
`astrid.sdk.timeline.commit.create_runtime_commit_service`.
The helper installs only after fixture setup has exposed the selected Runtime;
it never pre-imports/replaces that tree. It requires the actual handler server
to equal `daemon.httpd` and its Runtime service to equal `daemon.service`.
It restores the class method after the original test call, including failure.
The finite check exercises that installation on the actual class without
executing a daemon or handler.

## Hosted-tool choice before the ONE body

Agent lead checks installed py-spy on the supported actual service host first.
This worker has neither a host tool receipt nor a host attach result. If the
supported recorder is available, prefer its normal 50 Hz recording of the
actual service process with thread labels; retain its exact command, output,
exit and raw samples. Sampling alone cannot provide exact call counts: arrange
the boundary counters in the same submission, not another body. Do not claim
that samples count history_entry/commits. The helper below is the cProfile
option when the host confirms tool absence before any attach attempt.

Any real classifier or permission refusal ends the action. Do not switch from
a denied py-spy attach to this plugin, request another host, install packages,
or inspect an alleged host PID through this worker's namespace.

## cProfile option: exact launch addition

Keep the existing D73 source-only preflight, four SHAs captured once at request,
normal checkout receipts, manifest, timeout, selectors and existing environment.
Agent may add ONLY this private opt-in bootstrap to the next existing service
body. The launcher runs its preflight separately and retains body command,
exit, XML and runmanifest as before. Use absolute hosted paths when publishing
the exact helper bytes. Directory `actual-handler-profile` must not exist yet.

Within the existing service's env -i row, pass:

```sh
P4_LIVE_PROFILE_DIR="$P4_D73_EVIDENCE/actual-handler-profile"
```

The following is the body launch under that environment (the manifest, evidence
and request ID are the same already selected by Agent's ONE request):

```sh
"$PINNED_AGENT/tools/p4-d73-pinned-launch.sh" "$P4_D73_MANIFEST" run -- \
  -c 'import importlib.util,sys,pytest; s=importlib.util.spec_from_file_location("p4_live_profile",sys.argv[1]); m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m); raise SystemExit(pytest.main(sys.argv[2:],plugins=[m]))' \
  "$ABSOLUTE_HOSTED_HELPER/p4_live_profile.py" \
  -q -o addopts= -p no:cacheprovider --timeout=45 -m integration \
  --junitxml="$P4_D73_EVIDENCE/p4-current-becfe-http-3legs.xml" \
  tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back \
  tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo \
  tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document
```

`P4_LIVE_PROFILE_DIR` must be exported/passed by env, not merely assigned as an
unexported shell variable. Do not execute this command directly in a worker:
Agent supplies it to the existing central service. Do not run this alongside an
unprofiled copy or a separate full suite. All original test files remain exact.

## Returned artifacts and interpretation

Retain the normal D73 manifest/runmanifest, body command/exit/log and XML plus
the entire small profile output directory. `events.jsonl` fsyncs handler begin
and end records, retaining the last entered boundary on interruption. Each
handler emits a raw `handler-NNNN.prof`; `handlers.prof` merges them.
`summary.json` gives top 10 cumulative frames, exact total recursive call counts
for history_entry/_verify_accepted/accept/commit_timeline, per-handler wall,
per-note undo/redo boundaries, original timeout 45 and test protocol wall.
The latter includes fixtures, matching the test scope better than server CPU.
Events identify PID/thread/daemon instance, UTC start, helper bytes, every
original test hash before/after, and the same D73 manifest/request. Module paths
and file hashes before/after identify loaded Runtime/Agent source, including
any archive chosen by tests.helpers.runtime; do not equate archive paths with
the normal checkout without checking bytes.

Initial key `p4-ten-note-commit` covers all TEN notes in ONE request. Its counts
are shared, not ten separately observed commits. Undo/redo keys identify each
note. Report shared initial counts separately; do not silently distribute
shared/read-only requests among notes. Missing note operations after timeout
are unobserved. Call counts record method entries, not accepted receipts;
use unchanged test results/replies for durable acceptance. An exception can be
handled by _dispatch, so error_type null alone does not mean HTTP success.
If a hard process exit leaves only a begin, report incomplete capture rather
than inventing the final request's counts or cumulative frames.

Overhead is confined to this one original test's actual handler calling
threads: one cProfile instance per eligible request, no Python per-event
observer, no extra service body, and source hashing outside profiled handlers.
Profile dumping and begin fsync cost is exposed as
`capture_seconds_excluding_end_event`; end-event fsync and other test hook work
are included in protocol wall but not that field. cProfile's internal overhead
is uncalibrated and can be material. There is NO justified numerical overhead
percentage bound and NO claim that instrumented >45s is uninstrumented latency.
This run can identify a dominant seam, not establish an unprofiled gate PASS.
Do not add a control rerun or raise the timeout to calibrate it.

## Existing facts, not a new result

Retained service 16328: CLI/sheet PASS 3.013s, ten-note FAIL 45.336s at first
redo in historical canonical validation, conflict/rerun PASS 12.386s, exit 1.
Its Runtime was 327da207, not e89eb. Current helper checks confirm all three
original source files equal retained f4d6c72c byte for byte. The historical
path-bound aggregate original-test hash was
11c075bb257314cba368dd469c45e7f7b50b7b5f5964db11c0c9425a9cac74e0;
the launcher recomputes it with the new pinned absolute paths as designed.
Runtime home1919's 173+12 PASS is existing qualification, not a live P4 profile.
Agent1850's 258 history/254 verification/6299 JSON calls describe a different
finite restore control only. No repetition, P4 inference, or D78 inference.

Current actual P4 wall/top10/per-note counts: NOT MEASURED. No demonstrated new
optimization seam selected. Hosted dependency: Agent manager returns supported
tool choice and combines capture with its next meaningful D73 original body,
then publishes the raw artifacts above. No further cost source change before it.
