# Agent M3 authorized Theme preparation review

Date: 2026-10-21

Status: **HOLD for implementation; ACK the proposed boundary.**

This is a source review of `runtime-m3-theme-authorized-preparation-seam.md`
and the preceding Agent explicit-theme blocked report. No product code or
renderer was changed.

## Decision in plain English

Agent can ACK one semantic resolver boundary, but cannot ACK an explicit-theme
implementation yet. The existing post-admission named `theme` input is the
right carrier shape and the existing `_resolved_theme_for_render` function is
the right resolver. The missing piece is an authorized **pre-admission**
`theme.json` source bound to the same saved timeline or closed candidate,
frozen config/registry, render profile, and Runtime execution authority.

A caller slug, inline Theme object, browser-resolved value, or caller-derived
hash is not an acceptable substitute. Until Runtime supplies the missing
carrier, explicit-theme parity remains uncertified and Agent should leave the
current default fallback unchanged.

## What exists now

### The one resolver

The backend-neutral resolver is
`astrid/packs/rendering/shared/rendering_backend/__init__.py:_resolved_theme_for_render`
(lines 89–123). It accepts an attempt-local timeline path and either:

- an existing absolute `theme.json` path, which is loaded and reduced to the
  complete `{id, visual}` value; or
- `None`, which intentionally selects `builtin_theme()`.

It merges only the frozen timeline's `theme_overrides.visual` over that base.
Its comment and `_resolve_theme_path` (lines 62–82) explicitly reject slug or
ambient filesystem lookup. This function must remain the only Theme semantic
resolver. The Agent-side preparation seam, once unblocked, may call it with
the frozen attempt-local timeline and the Runtime-authorized materialized
Theme source, then canonicalize the complete `{id, visual}` result. No second
resolver or alternate source-selection rule is warranted.

The final renderer already consumes the same boundary: Remotion root
preparation passes its host materialized `theme_path` to the resolver (lines
167–177 of `root_preparation.py`), and the composed-frame path passes the same
kind of path (lines 734–743 of `composed_frame.py`). The existing canonical
profile helper also accepts the resolved Theme rather than inventing a second
Theme source (`rendering_backend/__init__.py:235–245`).

### The current managed Agent preparation

The normal requester-side seam is
`astrid/sdk/invocation.py:_prepare_managed_render_inputs()` (lines
1204–1546). It resolves the Runtime-selected timeline/candidate, validates the
snapshot, builds review and transcript facts, checks the requested profile,
and returns:

```text
timeline_snapshot = {config, registry}
timeline_authority = {project/timeline identity, hashes, revision/base pins, media admissions, ...}
```

`ManagedRenderSnapshot` itself has `config` and `registry` plus identity/hash
and candidate fields (`astrid/packs/rendering/actions/render/managed_timeline.py:694–761`);
it has no Theme bytes or Theme object identity. The normal Agent profile check
(`invocation.py:882–929`) calls `resolve_render_profile` with the frozen
config/registry and no runtime Theme path, so it currently reflects builtin
Theme plus timeline overrides. That is the existing normal authority and must
not silently be replaced by a caller value.

The existing object-ingestion helper (`invocation.py:2422–2460`) can ingest
bytes it already has, but it has no way to obtain authoritative Theme bytes.
It therefore cannot solve this seam by itself.

### The existing carrier is post-admission only

The rendering pack already declares an optional `theme` file port
(`astrid/packs/rendering/pack.yaml:905–907`), and GenericHost already
materializes an admitted named object as `theme.json` and exposes
`materialized_objects["theme"]` (`astrid/core/execution/generic_host.py:6888–6903`).
The Agent task adapter validates that the value is a non-symlink file beneath
the host materialization root and forwards it unchanged
(`astrid/packs/rendering/actions/render/task_adapter.py:215–247, 349–431`).
Those are the supported transport and final-render handoff surfaces.

They are not source authority. In the normal managed path, Runtime's
`_freeze_managed_render_inputs` derives `ordered_input_ids` from canonical
registry media (`/home/user/work/runtime/runtime_protocol/store.py:2006–2065`)
and refuses a supplied list that is not exactly that order
(`store.py:2073–2085`). `create_task` installs that frozen snapshot and
authority before snapshot publication (`store.py:2434–2466`). A bare
`theme` descriptor therefore cannot be added to the current managed request
without a Runtime-owned admission continuation; membership in the input list
alone would also not prove which Theme was selected.

The timeline's authored `theme` remains a string slug and
`theme_overrides` remains config data. The Agent snapshot and Runtime frozen
snapshot carry those fields as config, not a resolved `theme.json` source.
The existing post-admission carrier is consequently the exact **missing
pre-admission carrier**, not an already usable Agent input.

## Authority that must remain frozen

Any continuation must preserve the current normal managed checks as-is:

- Runtime-selected project and timeline identity;
- saved current head, or the exact candidate plus its retained base;
- frozen projected `config` and `registry` and their digests;
- requested profile and the existing config/profile compatibility check;
- Runtime storage estimate, idempotency/replay identity, and snapshot/CAS
  publication;
- Runtime `required_facts` normalization/readiness matching and final host
  recheck; and
- ordered input-manifest identity, project association, and the existing
  named-input binding.

The carrier must be refused if it belongs to another project, timeline/base,
selected Theme, or changed frozen input. No Theme source may be inferred from
the timeline slug. Candidate preparation must not drop the parent/base pin.

## Smallest Runtime-owned next step

Runtime should extend the existing managed-render preparation/admission seam,
not add a route, public DTO, store, resolver, certificate, or renderer
credential:

1. During the existing `_freeze_managed_render_inputs` path, obtain or expose
   one already project-authorized Theme object from the existing custody
   surface, tied to the same saved revision or candidate/base and frozen
   config/facts/profile. Runtime must make the producer/source lookup explicit;
   it must not derive bytes from the slug.
2. Admit that object through the existing optional `theme` file port as the
   named descriptor `{name: "theme", object_id: digest, digest: object_id,
   filename: "theme.json", required: true}`. Append the exact returned object
   ID once in the ordered manifest, preserving all current media IDs and
   replay identity.
3. Re-run the existing project association, selected revision/base, snapshot,
   profile/facts, idempotency, and ordered-binding checks before durable task
   acceptance. GenericHost and the Agent task adapter can then use their
   existing materialization/forwarding code unchanged.

After that carrier exists, the Agent change is bounded to the current
pre-admission preparation seam: write the exact frozen config to an
attempt-local `timeline.json`, call the existing resolver with the admitted
`theme.json`, canonicalize the complete resolved `{id, visual}` once, and
publish it through the existing project CAS/object manifest. No caller value
becomes Theme authority.

## ACK / HOLD

**ACK:** the existing named `theme` CAS/materialized-file carrier and the
existing `_resolved_theme_for_render(timeline_path, runtime_theme_path)`
boundary are the right interfaces. The Agent will use no slug, inline,
browser, caller-hash, new endpoint, or new resolver.

**HOLD:** no Agent implementation or explicit-theme certification is safe
until Runtime provides the pre-admission authorized source carrier and its
saved/candidate binding. The current default fallback remains the only
uncertified behavior for this seam.

## Evidence run

Focused, non-live semantic tests:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-m3-theme-preparation-source-boundary-nosocket -k 'not writes_real_mp4_and_is_callable' tests/core/rendering/test_profile.py tests/packs/rendering/test_render_export_task_adapter.py tests/sdk/test_managed_render_invocation.py
```

Result: **140 passed, 2 deselected, 57 deprecation warnings**.

The same focused files without the filter were **140 passed, 1 failed, 1
deselected**. The one failure was the existing real-MP4 adapter test; the
worktree lacks `remotion/node_modules/@banodoco/timeline-composition/package.json`.
No browser, live render, full suite, or implementation test was run.
