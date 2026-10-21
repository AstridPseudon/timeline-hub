# Runtime Theme private preparation: restart source boundary

Worker: rt-m3-theme-owned-source-restart-r1. Source reviewed on 2026-10-21.
Runtime: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`.
Agent: `57d6635616f2982b814cfcc059b670ea1a7c9f2c`, tree
`0174fd49bd175a726a44542d1d6e31bca13c0f02`.
These are the reviewed sources, not a qualified implementation pair.

## Finding requiring a concrete Agent/Runtime agreement

There is no existing source-to-result flow satisfying the brief. Two joins
are missing, not just admission of an extra digest. No product change is
safe until both are agreed.

1. **First source selection:** The normal render preparation returns only
   `timeline_snapshot={config,registry}` and `timeline_authority`
   (`astrid/sdk/invocation.py:1527-1545`). The optional `active_theme` SDK
   arguments have no consuming callsite in that module. The captured source
   admission identifies executable roots (`generic_host.py:4126-4138`);
   it does not identify a selected Theme document or bind one to a timeline
   revision/candidate. No `theme.json` or `themes/` file exists under the
   current builtin `astrid/packs` tree. The normal named Theme branch only
   fetches an already-admitted object (`generic_host.py:6888-6904`), which
   cannot be the producer of that object's first authorized bytes.
2. **Private execution/result contract:** `rendering.render` is a command
   definition (`pack.yaml:1042-1085`), whose CLI currently calls `render()`
   (`actions/render/run.py:601-666`); no Theme preparation dispatch exists.
   `_include_internal` allows private definition discovery
   (`sdk/invocation.py:4025-4026,4062-4068`); it does not choose a render mode.
   The host's existing private-context switch
   (`generic_host.py:8882-8885`) controls process/credential custody, not the
   command's semantic operation.

**New decisive result-validator finding:** The declared `provenance` output
is a `metadata/provenance` file and `_typed_outputs` checks its declared name,
attempt containment, digest and size (`generic_host.py:7087-7158`). However,
`run_task` subsequently requires every declared media output
(`generic_host.py:9665-9686`). `rendering.render` declares `video` as
`clip/visual` (`pack.yaml:1023-1034`), so a provenance-only result is refused
with `produced no result files for declared media port(s): video`. This check
also runs in private context. Thus provenance is physically able to contain
JSON but is **not an existing usable preparation settlement path** under the
unchanged render definition/validator. Do not implement a fake video, remove
that check, or silently narrow the admitted definition.

The delivered 01:22 Runtime note records tracing in progress, not an Agent
ACK. The shared Agent review still says HOLD pending first source. The prior
concrete-carrier note advertised by the peer handoff is absent from shared
design and from the interrupted Runtime worktree. No old uncommitted product
changes were present to carry. Existing shared handoffs are preserved; the
carrier question now includes the mandatory-media check above.

## Runtime surfaces to preserve

- `RealmStore._freeze_managed_render_inputs`, `store.py:1741-2172`, selects
  the saved or immutable publication and freezes the exact config/registry,
  authority and media admissions. At `2105-2117`, nonempty caller object IDs
  must exactly equal the derived canonical media/Scene IDs.
- `store.py:428-480` requires `execution_request.inputs` to mirror the
  ordered object IDs. This check is transport binding, not Theme selection.
- `RealmStore.create_task`, `store.py:2420-2476` and following snapshot
  preparation, retains existing idempotency, freeze and CAS publication.
- `RuntimeService.settle_attempt`, `service.py:7372-7504`, stages and
  publishes ordinary `outputs[]` atomically under the live task/attempt.
  `_associate_managed_outputs`, `store.py:5312` onward, binds durable output
  identities to that task/attempt/project. These functions do not assert
  that arbitrary bytes are the selected explicit Theme.
- Existing delegated producer-input resolution,
  `service.py:5954-5987`, can verify an already-settled sibling association
  and its port/live parent lineage. It cannot provide a missing first source
  producer or make the ordinary render's required video optional.
- Agent's existing semantic function remains
  `rendering/shared/rendering_backend/__init__.py:89-123`,
  `_resolved_theme_for_render(timeline_path, runtime_theme_path)`. It uses
  only the explicit materialized file or builtin default and applies the
  frozen timeline overrides. It deliberately rejects slug lookup.

## Smallest proposal; no aliases chosen

Agent/host owns the immediate prerequisite: identify an actual trusted Theme
producer/source within the admitted capture and its saved/candidate-base
selection binding, and specify a private dispatch on an existing invocation
with an existing non-media result contract. If the intended invocation is
`rendering.render`, Agent must first propose how that dispatch has a valid
admitted result contract while retaining the normal video requirement; the
current unchanged definition does not express it. This is a private
execution-contract extension, not a request for a public field or port.
If there is no suitable existing non-media contract, escalate that exact
constraint to the orchestrator rather than repurposing a port by assumption.

Once agreed, Runtime's bounded work is to preserve its existing selected
saved/candidate authority, frozen config/registry/facts/profile and replay
identity; retain the genuinely settled complete `{id,visual}` output via
existing CAS/association custody; recheck its source/attempt binding and
bytes; and derive the final named descriptor/order internally. It must not
accept an arbitrary project-associated object as selected Theme authority.
Agent performs the one resolver call; App forwards the retained descriptor;
Viewing consumes the existing materialized named input. No public API,
provider, store, resolver, certificate, worker write credential or
capture_validation.py expansion is proposed.

Implementation is blocked on Agent managed invocation/source contract,
with Runtime manager/orchestrator owning cross-area agreement. The precise
question has been sent through `hub/inbox/agent-rt-theme-owned-source-restart-r1.md`.
A private mode name and a result port are deliberately not invented here.

## Verification limits

No product/test/schema/client/pin source changed. No full suite, localhost,
browser, renderer, MP4 or default replay was requested or run. Targeted Runtime
custody controls are recorded in the worker report; they do not prove a
Theme preparation positive, selected Theme authority or explicit-theme parity.
