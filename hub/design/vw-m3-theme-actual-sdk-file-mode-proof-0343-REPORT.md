# Prepared SDK caller correction; renderer-fixture clarification outstanding

Base: `37006ab9c9586739ffc0956d9a8fe1581f73be69`. Only
`tests/integrations/test_generic_host_remotion_render.py` changed, and only
the imported Theme test (starts at line 444).

## Change

- Calls `sdk.invoke("rendering.render", kind="executor", project=..., inputs=..., client=owner)`
  at line 563, following Main's `astrid/packs/rendering/actions/render/STAGE.md:86-154`.
  Timeline, registry, and theme are owner-imported file descriptors.
- Uses the existing media-free title film shape from
  `tests/packs/rendering/test_remotion_backend.py:1506`, without authored
  overrides, and a genuinely empty registry for that film. The original
  black/silence media assertions belong to the unrelated MP4 test and remain
  byte-identical. No registry media IDs are imported or appended.
- A delegating `owner.tasks.create` observer at line 557 captures the actual
  SDK-produced request and actual admission response. It calls the original
  method without modifying the request. The test compares the Runtime task's
  IDs and inputs to that request, and prints request/response/SDK result for
  the later proof log. These are prepared observations, not evidence of an
  executed admission.
- Retains the owned fixture, real host materialization, real Root preparation
  and resolver, owner/worker token split, and independent dependency copies.
  Enables the supported production worker credentials option already used by
  the neighbouring MP4 case.

## Source-backed caller trace

1. Test imports: lines 521, 527, 533; actual caller: line 563.
2. `astrid/sdk/invocation.py:4336` calls
   `_prepare_managed_render_inputs`; file mode at line 1221 validates existing
   descriptors and returns them without deriving registry read authority.
3. `astrid/sdk/invocation.py:4580` calls `_kernel_invoke`.
   Its existing producer at lines 2639-2659 visits present file ports in sorted
   name order. For these inputs that is assets_registry, theme, timeline.
   The test supplies no manifest or ordered list of IDs.
4. `astrid/sdk/invocation.py:2985` obtains `tasks.create`, and line 2994
   supplies the producer's manifest. `astrid/sdk/remote.py:1786` performs
   normal admission preparation, line 1896 maps the manifest to wire
   `input_object_ids`, and line 1936 dispatches the prepared arguments.
5. Test line 591 reads the actual admitted task; line 605 uses the existing
   `GenericPackHost._materialize_inputs` (`generic_host.py:6460`).
   Root preparation at test line 619 retains the original real path:
   `root_preparation.py:169` calls `_resolved_theme_for_render` and places
   its value in props at line 176.

## Checks

Exact commands and environment: `COMMAND`; raw tool results: `checks.json` and `source-check.log`.

- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/integrations/test_generic_host_remotion_render.py`
  — PASS, All checks passed.
- `git diff --check` — PASS.
- Provisioned environment, `python -m pytest -q -o addopts= -p no:cacheprovider --collect-only -m integration tests/integrations/test_generic_host_remotion_render.py::test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source`
  — PASS, exactly 1 test collected in 0.54s.
- `py_compile.compile(..., cfile=<worker>/compiled-test.pyc, doraise=True)`
  — PASS via `python3 <worker>/verify_source.py`; output removed.
- AST/byte comparison against base — PASS (`assertion-inventory.json`):
  **0 existing assertions changed or removed**, all 12 retained; 7 admission/
  import assertions added. Both original with-blocks (Root preparation and
  forged-source refusal) are AST-identical. Every preceding byte, including
  all unrelated MP4 assertions and dependency setup, is unchanged.

No Runtime, test service, Theme proof, export, browser, readiness rerun,
dependency copy, install, full suite, Git mutation, or physical parity test
was run. No shared graph or dependency metadata was written.

## Blocking brief mismatch and next step

The approved base has **no renderer interception/result fixture in this test**:
it admits a task, calls host materialization directly, prepares Root props in
frame mode with `unused.mp4`, and stops the daemon. It never claims, executes,
or settles that task. The current correction preserves that scope; its
`sdk.invoke` uses the documented default `wait=False`. SDK success here means
admission, not successful final rendering. No provenance-only completion has
been introduced.

Consequently this prepared delta does **not** satisfy an interpretation that
requires a newly successful final-render task with a valid settled video.
There is no existing interception/result fixture to reuse at this approved
base. This is a mismatch in the task's fixture premise, not a demonstrated
SDK inability to render a media-free film. The known ordinary-file gap is
specifically that registry JSON does not grant registry-media read authority;
the media-free input avoids inventing that authority.

The orchestrator must identify the intended existing renderer interception/
result fixture or confirm the approved base's admission-only Root proof scope.
A clarification question is pending. Then Luna should review this exact
source/input delta before the single actual proof. No DONE marker is written
while that requirement remains unresolved.
