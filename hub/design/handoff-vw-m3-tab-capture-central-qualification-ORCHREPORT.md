# Handoff: Chrome155 tab-capture capability qualification

READY for manager final-SHA review/grant. The App probe/controller now binds
the actual pinned Node20.19.4 executable, Chrome155 `--version` plus dpkg
version and frozen 255-file tree, Playwright-core 1.60.0 and frozen 106-file
tree, and all six reviewed Remotion/Player hashes. Setup uses the absolute
Node path and `PATH` prefix, and controller preflight/claim require the real
shared flock.

The qualified result is deliberately bounded to one live video track, one
live tab-audio track, controlled tone presence, and native per-stream PTS.
Lossy VP8 decoded marker bytes are retained only as `diagnosticOnly` data with
`phaseClaim: false`; pure analysis still has one strict positive and one strict
failing marker control. No alignment, normalization, resampling, parity,
global-origin, Player/export-bound, timing, or audio-tolerance claims changed.

Targeted tests pass: pinned Node syntax checks, analysis/controller Node tests
(2 files, 0 failures), setup `bash -n`, probe/config ESLint, and `git diff
--check`. The direct controller fingerprint is sandbox-blocked by
`spawnSync git EPERM`; central preflight must perform it. No browser, socket,
central service, network, install, or full suite was run because exact
final-SHA approval/grant is not present.
