# Mouth browser guard correction

## Result

Corrected the retained existing-harness-retarget-0223 wrapper artifact for
the two independent custody findings in mouth-ac4-custody-physical0232:

- removed the unused absolute own variable;
- asserted the exact approved Chromium1194 realpath and SHA-256 before the
  suite;
- retained BROWSER_REALPATH and BROWSER_SHA in the retained preflight
  evidence;
- reasserted the exact realpath and SHA-256 after the suite, alongside the
  existing source, package, Node, and peer postflight guards.

The corrected wrapper is
handoff-vw-m3-mouth-browser-guard-correction-0238-run.sh; its minimal diff
from the recovered wrapper is in
handoff-vw-m3-mouth-browser-guard-correction-0238.patch, with hashes in
handoff-vw-m3-mouth-browser-guard-correction-0238.sha256.

Approved browser identity:

- realpath:
  /opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
- SHA-256:
  63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4

The Agent source remains exactly
ac4e004a664b96d58a00b66c7a2fa702a191f5bd with tree
a36a38e234813638530d03a6916dc84768caa9dd; the worktree is clean. No helper,
production source, browser allocation, install, central run, or test removal
was made. The prior failed proof remains separate and untouched.

## Suite registration

Added only the owned suite line
agent e2e-viewing-mouth-browser-guard-correction-0238 to
scratchpad/orch/tests/suites.conf. The existing
e2e-viewing-mouth-public13-existing-harness-retarget-0223 line was not
edited.

## Evidence

- bash -n on the corrected wrapper: PASS.
- bash -n -c on the exact parsed command from the new suite line: PASS.
- Wrong-browser realpath negative: PASS; rejected /bin/sh without launching
  a browser.
- Wrong-browser hash negative: PASS; rejected an all-zero digest without
  launching a browser.
- Current offline rendering controls:
  tests/packs/rendering/test_presenter_scene_capability.py,
  test_presenter_crop_equivalence.py, and
  test_presenter_selected_cut_aggregate.py: 40 passed in 12.04s.
- Node --check for presenter_crop_capture.mjs,
  presenter_crop_entry.mjs, and presenter_selected_cut_query.mjs: PASS.
- Python AST parse for the recovered helper and fixture: PASS.
- pytest --collect-only for presenter_crop_capture.py: 1 test collected.
- Published wrapper and patch hash manifest: all three entries OK.
- Published patch byte comparison against the recovered wrapper diff: PASS.

The physical Chromium/renderStill one-shot suite was not run here, by the
task boundary. No browser launch, central test request, or physical retry is
claimed.
