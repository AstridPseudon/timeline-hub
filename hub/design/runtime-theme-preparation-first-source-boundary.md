# Runtime M3 Theme preparation: first source boundary

Status: source-review handoff; the concrete-carrier note is not present in
the shared design directory. The previously described step that requires an
already Runtime-authorized `theme.json` before the private preparation is
circular and is not a solution. This note records the existing source/read
surfaces and the exact unresolved private boundary for peer agreement.

## Existing normal source/read path

The current Agent integration tree is `57d6635616f2982b814cfcc059b670ea1a7c9f2c`.
The Runtime worker tree is `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`.

The real normal Agent pack is `rendering.render` in
`astrid/packs/rendering/pack.yaml:1021-1063`. Its optional file port is the
existing `theme` input at `:905-907`; the command maps that port to `--theme`
at `:1062-1064`. This is the pack/host identity to preserve. It is not a
second Theme source or a new mode.

The host's actual managed read is:

1. `astrid/core/execution/generic_host.py:6511-6518` starts from the admitted
   `input_spec` and its host-prepared values.
2. `:6888-6904` requires the Runtime client, verifies the digest against the
   task's authorized input IDs, fetches the bytes, writes an attempt-local
   `managed-objects/theme.json`, and exposes the same path as
   `materialized_objects["theme"]`.
3. `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:64-170`
   receives the attempt-local `timeline_path` and that `theme_path`; at
   `:167-169` it calls the existing
   `rendering_backend._resolved_theme_for_render(timeline_path, theme_path)`.
   That is the one semantic resolver. It reads the complete runtime file and
   merges the frozen timeline's `theme_overrides`; the timeline `theme` slug
   is metadata, not a lookup authority.
4. The resulting complete value is placed in `merged_props["theme"]` and the
   private props file is written at `root_preparation.py:248-257`, then
   deleted at `:259-263`. This proves the normal read and resolver, but not a
   durable Theme output before render.

The normal requester-side managed preparation does not contain the missing
source. `astrid/sdk/invocation.py:_prepare_managed_render_inputs()` ends at
`:1527-1545` with only the frozen `timeline_snapshot` (`config`, `registry`)
and `timeline_authority`. It has no selected Theme bytes or Theme object
identity. Runtime's `_freeze_managed_render_inputs()` currently derives the
ordered IDs from canonical media and refuses a supplied sequence that differs
from it (`runtime_protocol/store.py:2105-2117`). Therefore a new or guessed
Theme ID cannot be inserted into the ordinary managed request.

## Existing INTERNAL invocation and output carriers

The exact internal process carrier is already present in Agent:

- `astrid/core/execution/generic_host.py:8882-8885` recognizes the existing
  private context from `child_delegation`, `delegated_parent`, or
  `delegated_recoverable_outputs` in the admitted spec.
- The same host dispatches the existing capability with the existing request
  fields `out`, `inputs`, `project`, `project_was_auto_resolved`,
  `python_exec`, `run_root`, `invocation="runtime"`, and (for private
  context) `run_id=None` at `:9544-9577`.
- `invoke_capability()` serializes that request together with the admitted
  definition/admission and the attempt-local `result_path` in
  `.astrid-capability-request.json` (`generic_host.py:8261-8276`). The child
  receives `ASTRID_INTERNAL_INVOCATION=1`; this marker is an internal host
  boundary, not Theme authority.
- The child returns the existing `outputs`, `payload`, and `error` shape to
  `.astrid-capability-result.json` (`generic_host_worker.py:157-170`).

Runtime already has the corresponding output custody. `settle_attempt()`
accepts the existing top-level `outputs` list and stages/publishes it
atomically (`runtime_protocol/service.py:7372-7504`); the existing
`_associate_managed_outputs()` records each durable object with Runtime-owned
task/attempt/project/fence provenance and lifecycle (`store.py:5312-5422`).
The delegated-child settlement checks are also existing custody
(`service.py:7430-7441`). None of these APIs currently says that an output is
the selected Theme; transport membership alone cannot supply that meaning.

## Exact unresolved boundary (noncircular)

There is no existing normal callsite that both (a) has the selected explicit
Theme source before semantic preparation and (b) can settle a canonical Theme
output before final render. The current normal source is only available after
an already-admitted named `theme` object has been materialized. The current
INTERNAL carrier is only process/attempt custody; it does not manufacture
that source. The current render output declaration contains `video` and
`provenance`, not a pre-render Theme output (`pack.yaml:1023-1039`).

The missing peer-agreement boundary is therefore precise:

> Within the existing managed render attempt, after Runtime has frozen the
> saved selector or candidate-plus-retained-base and the host has materialized
> the normal trusted pack inputs, an existing INTERNAL continuation must make
> one already-selected Theme source available to the Agent preparation call
> and route the preparation result through the existing child/attempt output
> settlement before final render dispatch. The continuation must use the
> existing `inputs`/`out`/`run_root`/`result_path` carrier and existing Runtime
> output custody; it must not introduce a public DTO, endpoint, provider,
> store, resolver, wire alias, caller hash, slug authority, browser value, or
> renderer `projects:write` credential.

This is a missing private continuation/source-binding agreement, not a claim
that an already-authorized `theme.json` exists. The concrete source itself is
still unresolved: no current App payload, Runtime frozen snapshot, Agent
requester helper, or normal producer emits a retained selected Theme object
before this step. A slug/browser hash and the existing post-admission
`materialized_objects["theme"]` path cannot be promoted into that source.

## Owner split once that boundary is supplied

- **Runtime/host:** retain the existing managed authority tuple (project,
  timeline, saved head or candidate/base, frozen config/registry/facts/profile,
  idempotency, and ordered CAS inputs); keep source binding and output
  association under existing Runtime custody. It must refuse a source whose
  project/authority identity or bytes do not match the attempt.
- **Agent:** consume only the host-provided attempt-local source and frozen
  `timeline_path`; call `_resolved_theme_for_render()` exactly once; emit the
  canonical complete `{id, visual}` bytes as the private preparation output.
  It does not select a source or mint authority. The existing final render
  then continues to use the already-admitted named `theme` materialization.
- **App:** remains a requester/forwarder of the existing managed invocation;
  `theme_id`, browser-resolved values, and caller hashes remain
  non-authoritative.
- **Viewing:** remains a consumer of the existing
  `materialized_objects["theme"]` path and does not add a resolver or source
  lookup.

Until the first bullet's private source-binding continuation is explicitly
identified and peer-agreed, explicit-theme completion is **UNCERTIFIED**. The
default fallback and its existing behavior remain unchanged; source review is
not explicit-theme completion.

## Evidence boundary

This is a read-only source/design review. No product, test, schema, renderer,
generation, or activation change was made. The exact source path above proves
the existing normal read, one resolver, internal request/result carrier, and
Runtime output custody. It does not prove a live private preparation,
pre-render settlement, explicit-theme parity, browser render, or full suite.
