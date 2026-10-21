# APPROVE — Theme validation-context fixture correction

Verdict: APPROVE the exact minimal fixture-only patch at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m3-theme-env-lifetime-correction-review-0912.patch`.

Patch SHA-256: `87ce86901a802368fe8949f62e458d1813181755bf41594c60a0e3cf39e23cb8`

The patch wraps only the existing SDK discovery call in
`with monkeypatch.context() as invoke_env:` and changes the deletion to
`invoke_env.delenv("ASTRID_PACKS_PATH", raising=False)`. On exit, the launch
validated environment is restored before Root validation. It does not alter
production code, source authority, DTOs, pins, validation, or a test matrix.

## Evidence checked

- Fixture launch sets `ASTRID_PACKS_PATH` to the private workspace pack root at
  `tests/integrations/test_generic_host_remotion_render.py:239-241`; the
  validation snapshot is created at `:286-300`.
- The 0907 retained evidence shows the unscoped deletion at `:572` removed
  that selector before the Root consumer reached
  `remotion_runtime._validated_runtime`. d971 source compares the exact
  normalized registry context at
  `astrid/core/rendering/remotion_runtime.py:474-539,1082-1113`; this is why
  the failure is fixture lifetime, not a product defect.
- SDK discovery still runs with the private selector absent inside the scope;
  d971 `astrid/sdk/invocation.py:4062-4087` is unchanged. The selector returns
  afterward, so the existing launch artifact remains the context used by Root.
- The canonical actor remains `PACK_HOST_ACTOR` (`astrid/sdk/host_bootstrap.py:48`),
  and the fixture still passes it to `GenericPackHost` and asserts the same
  registration actor at `:547-558`. Owner admission and worker-token use are
  unchanged.
- The SDK call's descriptor names, values, filenames, and literal order at
  `:573-596` are unchanged. Existing admission checks remain at `:597-604`:
  input manifest identity and admitted input descriptors. d971's normal
  caller preserves the claim snapshot (`generic_host.py:10284-10338`) and
  materializes the managed Theme through the existing `theme` branch
  (`generic_host.py:6460-6474,6888-6904`).
- Existing Theme assertions remain untouched: managed `theme.json`
  materialization at `:615-628`; Root props and explicit Theme identity at
  `:630-650`; omitted-theme builtin separation at `:652-655`; and forged
  local-source refusal at `:657-667`. The saved managed call and forged call
  are both byte-for-byte outside the proposed hunk.
- The patch does not disable or re-mint validation. It only restores the
  already validated launch context before the existing consumer comparison.

## Pure controls

- `/home/user/work/venv-agent/bin/python` in-process `pytest.MonkeyPatch`
  control: PASS. A present `ASTRID_PACKS_PATH` is restored after the scoped
  deletion; an originally absent variable remains absent. No central proof,
  retry, browser, helper, Runtime, socket, render, Node, install, or full
  suite was run.
- In-memory application of the exact proposed transformation followed by
  `ast.parse`: PASS.
- `git apply --check` against the current worktree: PASS.

No new test matrix is requested. A later owner/orchestrator run may exercise
the already existing single proof after applying this fixture patch; that is
not part of this review and was not claimed here.
