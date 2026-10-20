# Blocked: actual normal PCM source carry on ce251

Base: `ce2510034f3edebef7430dd018c566101ea298fb`, assigned Agent worktree
`/home/user/work/wt/vw-m3-normal-pcm-source-carry`.

## Applied prerequisite, separate from new work

Applied ONLY the exact ten-file `0a8c757723f0cee8ba128e453fce613d4c5c6262..ab935f77378ba5ea1df55ba775654f8bba233ebc` delta.
Every resulting file is byte-identical to `ab935`; no old ancestry imported.
319 product lines, 1,373 additions / 15 deletions including tests. The four
import-only strict xfails are replaced by the prerequisite's actual native WAV
tests, exactly as approved. The two active compiler xfails remain unchanged.

NEW source carry/callsite: **not implemented; blocked by missing source contract**.
No changes to service.py, banodoco_composer.py, run.py, SDK, filmstrip,
composed_frame, Runtime, client, provider or compiler. Every tracked path outside
the prerequisite was compared byte-for-byte against HEAD, including Root,
package/lock and the public12 archive. No activation flag, fallback or new
authority introduced. There is no official10 qualification claim.

## Specific blocker and recommended owner action

The requested EXISTING compiled-source admission is absent from this exact base:

- `git ls-tree -r --name-only HEAD` contains no `verified_source.py` or source
  transport; `rg 'verified_source|inherited_source|source_for_timeline|mint_prepared_source'
  astrid/core/rendering astrid/core/execution astrid/core/timeline/banodoco_composer.py`
  returns no matches.
- `RenderRequest` (`astrid/core/rendering/contracts.py:735`) carries paths,
  window, metadata and materialized media paths, but no inherited compiled-pair
  authority. `for_backend` preserves that same representation. The grant forbids
  a new DTO or a new metadata/sidecar authorization protocol.
- `_segment_request` (`service.py:1052`) reads the supplied timeline, writes
  `_window_timeline` to a new path, and replaces timeline_path/window. It has
  no admitted unsliced pair to validate or existing transformed-pair binding.
  `_window_clip` also changes IDs; its authored app stamp cannot prove origins.
- `Timeline.for_render` (`banodoco_composer.py:255`) returns a view of loaded
  JSON. Its serializer filters source tracks/defaults the theme; it retains no
  admitted original compiled occurrence map or source object.
- `_execute_remotion_locked` (`run.py:1012`) serializes the supplied path and
  materializes registry bytes; `_support_report` checks registry integrity and
  effect availability. Those checks do not bind compiled timeline bytes to a
  Runtime-admitted revision/candidate. The normal props also do not yet carry
  `compiledTransitions`, required by the inactive helper. Selecting canonical
  fps alone would not supply the missing source authority.
- Read-only comparison with `435357aec` finds
  `astrid/core/rendering/verified_source.py` and its `inherited_source` call in
  run.py. These are OLD CANDIDATE facts, absent from ce251. Even that class's
  `validate` accepts only its original exact path/digest pair; it has no
  transformed-pair operation. Porting it needs host mint/transport/serializer
  changes outside this grant and would import explicitly forbidden old scope.

Recommendation: Agent/orchestrator supplies or identifies the approved existing
admission handoff on the public12 cohort, including how the same admitted
unsliced pair authorizes its deterministic host slice. Then resume this worker
with that concrete contract/base. Retain original compiled objects before the
slice, carry their exact association through serialization, validate both
pairs, compile public transition/fps props, call the unchanged helper under
the existing asset ExitStack, and retain attempt/server through consumption.
No inference from authored app stamps, clip-ID parsing or self-authenticating
metadata is an acceptable substitute. No settled decision was changed.

## Exact targeted verification

Commands below ran from the assigned worktree, except Node commands which ran
from PROJECT. Shell variables here abbreviate these exact absolute paths:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
P=$ORCH/design/handoff-vw-m3-normal-pcm-source-carry-
PROJECT=${P}project
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
PY=/home/user/work/venv-agent/bin/python

python3 -B ${P}verify.py setup
# PASS: exact prerequisite, every other tracked ce251 byte, public12 SHA256,
# all 77 archive files, exact tested helper/test copies, peer versions.

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_REMOTION_PROJECT_DIR=$PROJECT $PY -B -m pytest -p no:cacheprovider -q tests/packs/rendering/test_normal_audio_sources.py
# 18 passed in 3.81s. ${P}pytest-native.log

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_REMOTION_PROJECT_DIR=$PROJECT $PY -B -m pytest -p no:cacheprovider -q tests/editing_conformance/test_compile_contracts.py tests/packs/rendering/test_normal_audio_source_phase.py tests/core/rendering/test_service.py
# 85 passed, 2 EXISTING xfailed in 24.98s. ${P}pytest-neighbors.log

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD $PY -B -m pytest -p no:cacheprovider -q tests/editing_conformance/test_compile_contracts.py --runxfail -k 'fade-in-needs-prepared-envelope-source or fade-out-needs-prepared-envelope-source'
# EXPECTED RED: 2 failed, 27 deselected in .12s. Both audio.render_source
# absent at test_compile_contracts.py:78. ${P}compiler-red.log
# No green-after claim and no compiler marker removed.

# cwd=$PROJECT for each Node command:
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/normal-audio-sources.test.mjs
# 8 passed, 0 failed/skipped; ${P}node-normal.log
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE tests/long-audio-source.test.mjs
# 2 passed, 0 failed/skipped; ${P}node-long.log
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/gapless-mp3-source-origin.test.mjs
# 4 passed, 0 failed/skipped; ${P}node-mp3.log
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/normal-audio-native-sources.test.mjs
# 5 passed, 0 failed/skipped; ${P}node-native.log

# cwd=assigned worktree:
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py tests/packs/rendering/test_normal_audio_source_phase.py tests/packs/rendering/test_normal_audio_sources.py
# All checks passed.
python3 -B ${P}verify.py after
# PASS: exact source checks; shared graph identical, 2056 entries.
git diff --check
# PASS.
```

Initial neighbor invocation omitted `-u NODE_OPTIONS -u NODE_PATH` and PROJECT;
it returned 81 passed / 2 xfailed / 4 failed in 23.83s, all four at the real
loader-override rejection before decode. Exact initial command:
`env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q tests/editing_conformance/test_compile_contracts.py tests/packs/rendering/test_normal_audio_source_phase.py tests/core/rendering/test_service.py -k 'not unrelated'`.
The clean-environment rerun above resolves those four. No test or launch policy
was changed. Final totals: 103 Python passed / 2 existing xfailed; 19 Node passed.

These are direct meaningful materialization/native decode/full-source WAV
tests without a listener. They cover exact stereo samples, rational clock,
window/layer helper phase, immutable source/registry, distinct assets, forgery,
double application and cleanup, plus native >64MiB and source-backed gapless
MP3. They do NOT exercise an active normal caller or real served URLs.

## Shared graph and handoffs

The only peer graph accessed for these tests is
`/home/user/work/composition/node_modules`. Its before/after file bytes,
directory topology and literal symlink targets are identical in
`${P}shared-before.json` and `${P}shared-after.json`. No baseline was replaced.
Own PROJECT/node_modules and both @banodoco/@remotion scopes are real
directories. Public12 was extracted locally from this base's exact archive
SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`;
only individual existing peers are linked read-only in use. Every destination
is checked with lexists before creation. No install or shared dependency write.

All artifacts have the flat absolute ORCH design prefix
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-normal-pcm-source-carry-`.
`prerequisite.patch` is the exact approved ten-file delta. `verify.py` reproduces
byte/topology checks. `central-qualification.md` prepares the required cases
and explicit source blocker; it is NOT a central-ready normal-route fixture.

No full suite, central request, HTTP/socket listener, browser, export, install,
network, push or git mutation ran. No parity, normal lifetime or M3/Gate6
qualification claimed. Existing normal routes/cache/retry/cancellation/mute/
amplify/source errors are unmodified. No new xfail/skip/refusal/tolerance.

Commit message is provided for harness ownership of this prerequisite-only
change. Worker BLOCKED records the unfulfilled activation task; DONE is not
created because the whole task is incomplete. No reports/build output/temp
files were added to the repository.

The owned scratch PROJECT was removed after final verification; peer symlink targets were not traversed or removed. All retained handoffs are flat files. Recreate PROJECT with verify.py setup before reproducing tests.
