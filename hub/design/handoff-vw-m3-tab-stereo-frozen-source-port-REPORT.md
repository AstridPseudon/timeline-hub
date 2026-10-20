# Stereo tab source-unit handoff

Status: source unit complete; central capture remains unrun.

## Change

Based on exact App commit `2b388e769d9e153122e43b16b5d21e6e1ddf5b71`, this extends only the existing standalone tab-audio probe:

- adds independent 1760 Hz left and 1980 Hz right source tones to the existing 48 kHz stereo WAV fixture while retaining the old shared 1320 Hz tone;
- records each captured track's real `getSettings()` and `getCapabilities()`;
- checks the recorder's actual ffprobe channel count and decoded interleaved channel identity/leakage;
- preserves the existing one `MediaRecorder`, current-tab `getDisplayMedia`, native per-stream PTS, visual diagnostic, and lifecycle ordering;
- keeps the old `.001` tone-presence assertion unchanged and rejects mono output instead of downmixing or relabelling it;
- adds offline positive, swapped-channel negative, and mono negative coverage.

The recovered Composition prep is commit `147d47aea3d42e86328ad222d94109261459e412`. Its report and source-only patch were exported before use as `handoff-vw-m3-tab-stereo-mix-capability-prep.md` and `.patch`. Its original App hunk did not apply to exact `2b388e769`; the equivalent three-file change was adapted manually. No Composition branch was merged.

## Validation

The retained Node executable was verified before use: v20.19.4, SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.

Passed directly: the analysis test, strict TypeScript probe/config check, no-cache ESLint on touched source, JS syntax check, launcher shell syntax check, and `git diff --check`. The environment lifecycle tests passed 4/4 in a disposable source copy. Actual Playwright discovery passed with `Total: 1 test in 1 file` for the standalone probe. No browser was launched.

## Boundaries

No App product code, Agent, Runtime, Composition package, pin, DTO, dependency, shared node_modules, shared cache, grant, socket, network, browser capture, render, or full suite was changed or run. The source is intentionally dirty, so the controller's clean committed-source preflight and central one-shot diagnostic were not run. A fresh post-commit fingerprint and manager grant are required before capture.

## Next step

After the harness commits this worktree, independently rerun the pure controller preflight/discovery against the committed source and the frozen public12/private graph. Only then decide whether to issue one fresh manager grant and run the named central diagnostic. A mono WebM or swapped-channel detector failure must remain a failed stereo result.
