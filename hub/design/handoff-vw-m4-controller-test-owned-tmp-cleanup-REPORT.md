# Handoff: vw-m4-controller-test-owned-tmp-cleanup

Base: App integration `157eef8cf` (`tl/integration`). The controller graph
fixture helper is absent there because it is on owner-active App port
`597c25552`.

The owner port already removed the large App checkout in favor of a minimal
fixture and already has real-`tmpdir()` containment and setup cleanup. The
worker prepared a non-overlapping test-only patch for that owner file:

- `TAB_AUDIO_TASK_TMPDIR` is honored as the per-run carrier, with the
  existing `os.tmpdir()` fallback.
- Existing real-directory/direct-child ownership checks and cleanup stay
  intact.
- A tiny fake-tree regression proves carrier selection, success cleanup, and
  exception cleanup without allocating the real fixture clones.

Patch: `handoff-vw-m4-controller-test-owned-tmp-cleanup.patch`

Do not apply it to `tl/integration` directly; apply after the owner port has
landed and run the owner controller test lane with a private carrier. No
controller source, package, browser, floor, grant, or provenance controls were
changed.

Verification:

- Assigned-base direct controller suite with pinned Node20: PASS, 1 file,
  0 failures.
- Patch applicability against a private extraction of 597c25552: PASS.
- Patched tiny cleanup regression with pinned Node20 syntax check and
  name-filtered test: PASS, 1 test, 0 failures.

No browser, render, install, live socket, full suite, or real large clone was
run.

