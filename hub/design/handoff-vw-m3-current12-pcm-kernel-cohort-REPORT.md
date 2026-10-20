Prepared the **CURRENT12 inactive PCM staging cohort** on Agent base `c456b3281497653cecf44f61acd6fa30565d83c8` (tree `4d6dd3d12d6f427842ed7ecd127f9531e7276bab`). This is branch source for the next caller worker, not ordinary-consumer adoption, a paired release, Runtime certification, activation, or parity qualification. Harness owns the eventual commit.

Exactly 14 paths change:

- Four approved public12 consumer paths from `f29a9475ee1cb5c13bc1371eee8ff36030dede3e`: `astrid/core/rendering/remotion_runtime.py`, `remotion/package.json`, `remotion/package-lock.json`, and `remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz`. Package and lock actually name `0.0.12`; no dependency override or loader alias substitutes it for a declared 10. The admission edit is solely the pinned version constant.
- The exact ten-file `ce2510034f3edebef7430dd018c566101ea298fb..2019d7e69ceb9b10f18cc311e570d635b16c15d8` prerequisite. Every final file is byte-identical to `2019d7e69` and `ab935f77378ba5ea1df55ba775654f8bba233ebc`; its file set matches `0a8c75772..ab935f773`. No old ancestry imported. These paths are `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py`; `remotion/{attempt-envelope-pcm,compiled-audio-source-clock,normal-audio-sources}.mjs`; `remotion/tests/{gapless-mp3-source-origin,long-audio-source,normal-audio-native-sources,normal-audio-sources}.test.mjs`; and `tests/packs/rendering/{test_normal_audio_source_phase,test_normal_audio_sources}.py`.

The prerequisite dry-run found one context mismatch: current main had changed a replaced test docstring link from `design/` to `docs/design/`. The entire old docstring is replaced by the approved prerequisite, so its exact final bytes were used. There were no product-code conflicts. The four old import-only xfail cases become the prerequisite's real positive PCM tests. No new xfail/skip; both existing compiler xfails remain unchanged.

Public12 archive: **58,444 bytes, 77 regular members**, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; derived SHA512 matches the lock's `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`. All 77 installed private files match exactly before/after tests, with no extra installed package files. Public DEFAULT_THEME equals the **entire** current Agent `BUILTIN_DEFAULT_THEME` object, not only selected colors.

All tracked paths outside the approved 14 paths were compared to HEAD byte-for-byte. This includes current M2/provider/client additions, service/run/Root, SDK, serializer, existing clocks, and runtime pins. `runtime.lock.json` still names source `94114269d1ce23ab3224d7eca5a85138ce2b5fed`, producer `sha256:e02a71b5b77479bdc8035a8a8d75ec57e9f1962b7f9195126739ab0d1ed063ac`; generated contract remains **0.2.9**. The historical local 0.0.10 archive remains untouched, as do its existing fixtures. Deletion was outside the four-file grant.

Private verification used real owned `node_modules`, `@banodoco`, `@remotion`, `@types`, and `@esbuild` directories. Public12 was extracted into an owned real package directory. Only dependency leaves link to `/home/user/work/composition/node_modules`, with actual React/DOM18.3.1 and Remotion/media/layout-utils4.0.509; package and host resolve the same peer identities. No App/runtime dependency graph was borrowed. All **2,056** Composition shared graph entries (file hashes, directories, literal link targets) are identical before/after. No install, cache write, shared dependency mutation, git mutation, network request, remote message, merge request, or push occurred.

Exact commands and results follow. All commands ran in the assigned worktree except Node/type commands, whose cwd was `$PROJECT`. Variables abbreviate these exact paths:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
P=$ORCH/design/handoff-vw-m3-current12-pcm-kernel-cohort-
PROJECT=$ORCH/workers/vw-m3-current12-pcm-kernel-cohort/checks/remotion
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
PY=/home/user/work/venv-agent/bin/python

python3 -B ${P}verify.py setup
# PASS: source/lock/package/77 files/peer topology. setup.log.

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-current12-pcm-kernel-cohort ASTRID_REMOTION_PROJECT_DIR=$PROJECT $PY -B -m pytest -p no:cacheprovider -q tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py tests/editing_conformance/test_compile_contracts.py
# 51 passed, 2 existing xfailed in 5.15s; exit0. pytest-native.log.

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-current12-pcm-kernel-cohort $PY -B -m pytest -p no:cacheprovider -q tests/core/rendering/test_service.py -k 'window_timeline or segment_request'
# 5 passed, 47 deselected in .27s; exit0. pytest-service.log.

# cwd=$PROJECT for each Node command:
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/normal-audio-sources.test.mjs
# 8 passed, 0 failed/skipped; node-normal.log.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE tests/long-audio-source.test.mjs
# 2 passed, 0 failed/skipped; node-long.log.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE tests/gapless-mp3-source-origin.test.mjs
# 4 passed, 0 failed/skipped; node-mp3.log.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE tests/normal-audio-native-sources.test.mjs
# 5 passed, 0 failed/skipped; node-native-direct.log.

# An earlier aggregate invocation also passed (4 file subprocesses).
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE --test tests/normal-audio-sources.test.mjs tests/long-audio-source.test.mjs tests/gapless-mp3-source-origin.test.mjs tests/normal-audio-native-sources.test.mjs
# exit0; node-native.log. Direct runs above expose individual assertions/counts.

# cwd=assigned worktree:
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-current12-pcm-kernel-cohort $PY -B ${P}package-probe.py
# exit0; package.log. Real _composition_package_problem accepts public12;
# 8 runtime exports, exact peer identity, full DEFAULT equality; exact current
# generator + unchanged composition-package.mjs custom host/SSR checks pass.
# This is package admission, not complete managed CLI runtime admission.

# cwd=$PROJECT; public-types.mts is retained at ${P}public-types.mts.
env -u NODE_OPTIONS -u NODE_PATH $NODE node_modules/typescript/bin/tsc --noEmit --strict --module NodeNext --moduleResolution NodeNext --target ES2022 --jsx react-jsx --skipLibCheck public-types.mts
# exit0, no diagnostics; types.log. Consumer type probe, not full Root typecheck.

# cwd=assigned worktree:
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-current12-pcm-kernel-cohort $PY -B -m pytest -p no:cacheprovider -q tests/packs/rendering/test_composition_package.py -k 'locked_release_is_built'
# RED: 1 failed, 5 deselected, exit1; package-current-fixture.log.
# Existing fixture expects lock.version 0.0.10; actual source lock is 0.0.12.

/home/user/work/venv-agent/bin/ruff check --no-cache astrid/core/rendering/remotion_runtime.py astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py tests/packs/rendering/test_normal_audio_source_phase.py tests/packs/rendering/test_normal_audio_sources.py
# exit1: 8 pre-existing admission-file diagnostics; ruff.log.
# Repeated HEAD admission bytes via ruff --stdin-filename <same file> -:
# exact same diagnostic output; ruff-base.log. No new lint diagnostics.
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py tests/packs/rendering/test_normal_audio_source_phase.py tests/packs/rendering/test_normal_audio_sources.py
# exit0, all checks passed; ruff-owned.log.
python3 -B ${P}verify.py after
# PASS: exact source + 77 files + shared graph unchanged; after.log.
git diff --check
# exit0.
```

The first external probe drafts had harness errors: CommonJS resolution of ESM-only `@remotion/media`, and incorrect probe assumptions about `toRuntimeTheme`'s export, playback-rate argument and WAV return type. Those private probes were corrected to use public package metadata and the actual API signatures. Initial outputs remain `package-initial.log` and `types-initial.log`; no product/package/test source was changed to address them.

Native positives cover original envelope phase across window/layer slicing, independent managed sources, rational public trim/rate, scalar gain preservation, forged/double preparations, batch cleanup, complete stereo WAV bytes beyond 64MiB, and native gapless MP3. These are local WAV/helper tests; URL strings do not prove serving or server lifetime. Existing codec origin restrictions, whole-source memory use, RIFF limits and subprocess time budgets remain. No full, browser, socket, HTTP server, video render, capture, or cross-product parity test was run.

Owner merge ordering and exact remaining adjustments:

1. Ordinary public12 adoption is already requested upstream; **no new remote request sent**. This branch supplies the four exact source paths only. Its unchanged readiness fixture is RED, so this branch must remain staging until the owning adoption supplies its fixture updates. `pending-owner-fixtures.patch` contains only the six approved f29 fixture edits, unapplied: clip-fields comment; journey manifest version; composition-package version/path/SHA/integrity; export-task adapter archive; scene-answer archive/SHA; scene-host archive/SHA/version/name. Preserve all newer test additions when applying these hunks. The old archive can be removed only when its remaining references are migrated by the owner.
2. Gate the actual public12 four-file source/adoption separately, then the unchanged ten-file inactive kernel, then the current native extent unit, then the caller relative to those frozen prerequisites. The caller worker may compose this frozen staging source before official adoption, but must report that boundary. No whole f29/ce251/2019/abd ancestry merge is needed.
3. **Root/callback conflict boundary:** this patch changes no Root or run.py bytes and requires no Root adjustment for the public12 pin/kernel alone. Any incoming older Root/runner extent patch must be ported as narrow hunks by its owner: preserve current `getMetadata` canvas/window/render-tail precedence while adding only the approved extent fact, and preserve current `capture_remotion_frames(..., on_scene_props=...)`, its conditional forwarding, and final-props callback/lifetime in `_execute_remotion_locked`. Do not replace current runner/Root from an old candidate or drop M2/provider/client changes. The parallel extent/caller tasks own the actual adjustment and tests; this report does not qualify their future composed result.
4. Activation and serving/physical parity gates remain later owner work. The two compiler xfails are untouched. No official Runtime certificate or ordinary Agent/App paired-adoption conclusion follows from this staging result.

Evidence is flat under the absolute prefix `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current12-pcm-kernel-cohort-`: `source.patch` (complete 14-path current-base binary patch), `consumer.patch`, `prerequisite.patch` (exact historical ten-file diff; note docstring context above), `source.json` (exact source/cohort identities, changed and protected file hashes), `composition77.json`, shared before/after manifests, scripts, and logs. No repository docs/build output/temp files added. Bounded staging task complete; official adoption and activation remain pending, not worker blockers.

The owned private test graph was removed after verification; symlink targets were not traversed. To reproduce, recreate it with `verify.py setup`, copy the retained `public-types.mts` into PROJECT, then run the listed probes. Original before/after evidence is retained.
