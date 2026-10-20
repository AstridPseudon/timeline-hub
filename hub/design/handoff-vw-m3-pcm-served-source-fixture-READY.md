Prepared, execution HELD: no manager final source + test scope grant received.

Test source (UNAPPLIED main-suite file):
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-source-fixture-test_normal_audio_served_sources.py

Central controller:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-source-fixture-controller.py

After the producer harness commits, manager reviews its FINAL SHA, freezes this test/controller, grants scope, and registers ONE named suites.conf line (substitute the final SHA and approved existing project path; do not run this template literally):

agent integration-viewing-pcm-served-sources /home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-served-source-fixture-controller.py --source-sha FINAL_PRODUCER_SHA --project APPROVED_INSTALLED_PROJECT --node /tmp/vw-m3-agent-gate-node20.19.4/bin/node --scope whole

Then ONE central request (not submitted by this worker):

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-normal-pcm-producer-current integration-viewing-pcm-served-sources) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"

Scope whole = 7 expected passing module integration cases: two native stereo source/clock positives (30 and 30000/1001 fps); wrong original URL/asset + forged render_source/double apply; altered selected staged bytes; partial batch failure; wrong managed digest; interrupted consumption. Same-clock/envelope swapped WAVs are detected by an independent PCM oracle inside each positive, not by a nonexistent public content-authentication API. All PCM-producing positives GET actual 127.0.0.1 URLs while the actual materializer/server are alive. Original files, selected key/digest, opaque props, gains and source clock remain pinned; cleanup checks success/error and unrelated siblings.

Scope with-phase = same 7 plus 2 ordinary positive requirements for actual window/layer slicer original fade phase. They intentionally DO NOT supply invented authority or a manually assembled original_clips mapping. Missing real owner transport stays RED (no xfail/skip). This scope is not ready to pass until source owner joins; manager must grant it explicitly. A whole-only pass does NOT close window/layer requirements.

Project precondition: existing installed public12 project with exact source helper bytes, 77 archive members equal the immutable release12 SHA256 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3, React/react-dom18.3.1, Remotion/media/layout-utils4.0.509, Node20.19.4. Producer's current candidate scratch is ORCH/workers/vw-m3-normal-pcm-producer-current/checks/remotion; it has NOT been granted as a stable final project. Controller does no install, extraction, copying of helpers, browser or rendering. It compares snapshot tree to exact approved final producer tree; no worktree/branch mutation. --check runs offline preflight only, and actual pytest requires the central .test-* snapshot.

This is inactive asset-stage module integration, not host source admission, _execute_remotion_locked activation, Player/export parity, or full render. No fake source factory, source grant, custom auth protocol, new DTO or mocked HTTP bytes.
