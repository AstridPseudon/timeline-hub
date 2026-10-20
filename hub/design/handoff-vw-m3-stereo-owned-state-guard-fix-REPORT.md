# Stereo owned-state guard fix

Status: ready for review; no grant or capture issued.

## Changes

- Rebound controller and launcher to the retained Node 20.19.4 executable:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node`, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Rebound controller/setup state, cache, discovery, and default output paths to this worker's own state root:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-stereo-owned-state-guard-fix`.
- Added an explicit `stereo` run mode to the source fingerprint and grant checks. Setup and Playwright config refuse `mono` and pass `TAB_AUDIO_RUN_MODE=stereo` through to Playwright.
- Added the native ffprobe channel diagnostic before decode. A non-stereo stream is recorded as `unsupported` and refused; no `-ac` coercion or downmix was added. The existing `.001` tone threshold is unchanged.
- Kept the existing 5,835-file source, private graph, 77-file Composition graph, Chrome155 whole-255-file tree, six render hashes, discovery, flock, resource, fresh-grant, one-shot, short-temp, source-clean, and postflight guards.

## Tests

Passed with the retained Node executable:

```text
node --test tests/e2e/timeline/tab-audio-capture.analysis.test.mjs tests/e2e/timeline/tab-audio-capture.controller.test.mjs — 2 modules passed
node --test tests/e2e/timeline/tab-audio-capture.environment.test.mjs in a disposable source copy using the readonly private graph — passed
node --check tab-audio-capture.controller.mjs — passed
node --check tab-audio-capture.analysis.mjs — passed
bash -n tests/e2e/timeline/setup-tab-audio-capture.sh — passed
strict TypeScript probe/config check — passed
ESLint --no-cache on touched capture/controller/config files — passed
git diff --check — passed
dirty setup --prepare — refused with “Selected App source must be a clean committed worktree” as required
controller --discover with actual Playwright --list in disposable source copy — passed; 5,835 tracked files, Node SHA verified, Total: 1 test in 1 file
```

No grant, browser launch, capture, render, network, install, live socket, or full suite was run. Temporary source copies, task temps, caches, output, and discovery directories were removed.

## Decisions / follow-up

The run mode is a controller fingerprint/grant field and an environment guard because the actual stereo claim must not inherit a mono/default mode. The native channel diagnostic is attached before decoding so mono remains an explicit unsupported diagnostic rather than being forced to two channels.

After harness commit, publish a fresh fingerprint and obtain a fresh manager grant. The literal manager-only post-commit command is in the companion COMMAND file; it intentionally references the committed App source and the retained Node path, with no alias to the old source or old Node.
