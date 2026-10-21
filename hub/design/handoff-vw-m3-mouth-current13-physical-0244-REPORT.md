# vw-m3-mouth-corrected-wrapper-one-run-0244

## Disposition

**APPROVED / PASS.** The corrected wrapper-only review passed, followed by the
one authorized fresh central physical run. No source, helper, capability,
assertion, threshold, ROI, statistic, or active caller changes were made.

## Producer terminal and corrected-wrapper review

- Producer `mouth-browser-guard-correction-0238` reached terminal exit 0 at
  `2026-10-21T02:40:48Z` with `DONE`.
- Corrected wrapper:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-mouth-browser-guard-correction-0238-run.sh`
- Exact approved Chromium1194 realpath:
  `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`
- Exact browser SHA-256:
  `63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4`
- Preflight asserts both exact browser realpath and hash, retains
  `BROWSER_REALPATH`/`BROWSER_SHA`, and postflight reasserts both.
- Stale absolute `own` variable is absent.
- Wrapper diff is byte-identical to the producer's published minimal patch;
  only the requested browser pre/post proof, retained fields/status text, and
  stale-variable removal are present.
- Existing source/package77/9412/Node43d6/six peer, flock/central, source
  pre/post, and one-shot guards remain present. The fixed component-zero ROI is
  `{x:151,y:104,w:19}`; frames remain `[0,3,4,5]`; the strict `> .02`
  comparator and planted controls remain unchanged. Default, partial, and
  raw-invalid inputs remain legacy-unqualified.
- Producer negative controls were read: `/bin/sh` wrong-realpath and an
  all-zero wrong-browser hash were both rejected without browser launch.
- Corrected wrapper and patch hash manifest passed; exact registered suite
  command parsed with `bash -n -c`. The existing public13 suite line was not
  edited, and the new line is the only correction suite entry.

## Central physical run

- Test ID:
  `vw-m3-mouth-corrected-wrapper-one-run-0244-e2e-viewing-mouth-browser-guard-correction-0238-1021024258-32349`
- Suite: `e2e-viewing-mouth-browser-guard-correction-0238`
- Terminal: **pass**, exit 0; one test passed in 13.74s (central wall 26s).
- Central source tree: `a36a38e234813638530d03a6916dc84768caa9dd`, with
  `ASTRID_CHECKOUT="$PWD"`; wrapper realpath-bound the active checkout.
- The run used the shared browser lock and `VIEWING_BROWSER_FLOCK_HELD=1` /
  `VIEWING_CROP_CENTRAL=1`; no retry or second invocation occurred.
- Retained raw output and preflight:
  `/tmp/vw-m3-mouth-public13-0223-WpDP5W`
- Retained raw PNGs:
  `frame-0.png` and `frame-4.png`:
  `fa68d076a79c9c553fc79fc83128c55da7ed542aed47640f6e571598b2e3b2f6`;
  `frame-3.png`:
  `ddea7b2cb0e89d3cca6df0bd7b70e160338122d5a72d4ad12bed1ebf14e08886`;
  `frame-5.png`:
  `79ef9e2d8d7c5456f463bd32e9432c0f9a47a60ccbc7601638f63822f1b425e7`.
- `inspection.json` retained the one selected-cut aggregate row for
  `presenter` / `overlay` / `effect/am-presenter` from `astrid_motion`, at
  component frame 0, with the fixed ROI and basis 1920×1080 at 30fps.
- Natural positives were unchanged: old/compat `0.42052565707133915` and
  erase `0.8682170542635659` for all three pairs, all strictly above `.02`.
- Planted mismatch controls were unchanged: 8 points old/compat
  `0.010012515644555695` vs erase `0.020671834625323`; 15 points
  `0.01877346683354193`; 16 points `0.02002503128911139`; padding16 old/compat
  positive and erase `0`.
- Retained preflight recorded the exact source tree, Chromium1194 path/hash,
  package77 hash `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  and Node20.19.4 hash
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
  The wrapper's terminal postflight passed source, browser, package, Node,
  and read-only peer hash checks.

## Commands and results

- `git rev-parse HEAD HEAD^{tree}` — pass: `ac4e004a664b96d58a00b66c7a2fa702a191f5bd` /
  `a36a38e234813638530d03a6916dc84768caa9dd`.
- `git status --porcelain --untracked-files=all` — pass: clean.
- `bash -n` on corrected wrapper — pass.
- `bash -n -c` on the exact registered command — pass.
- `sha256sum -c handoff-vw-m3-mouth-browser-guard-correction-0238.sha256` — pass.
- Producer offline controls and negative proofs — pass, read from retained
  producer terminal evidence; unchanged ac4 audit was not rerun.
- Central named suite above — pass; one physical invocation only.
- PNG `sha256sum`, `file`, retained metadata inspection, and visual inspection
  — pass.

Not run: full suite, install, broad D09 retirement, or any retry. The source
and helper audit was intentionally not repeated; this was a corrected-wrapper
review only.

