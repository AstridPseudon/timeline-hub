# Runtime M3 Main explicit Theme custody review

## Verdict

**REQUEST CHANGES — do not approve the current source.** The independent
custody review found no corruption in the existing ordinary named-CAS carrier,
but the committed product seam is absent. The paired regression proof is
decisive: a real project-owned imported `theme.json` is refused by the managed
`timeline_ref` admission as an extra ordered input.

This is a source review only. No Runtime product, test, schema, client,
resolver, task, delegation, private-mode, or artifact file was changed here.

## Pinned source and ownership

- Runtime review base: commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
  tree `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Current Agent integration producer: commit
  `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`, tree
  `5997f0162374dcfb56597b636caaad597c951b68`.
- Current App integration caller: commit
  `692765846fef511047445fecef3e55ec8bb6a5bf`, tree
  `e615c0a3aafca34504ba3544560de3887e4de38d`.
- The regression worker’s test was uncommitted during review; its report
  correctly records base `95bd3c5`, but its Agent/App labels are older than
  the current integration trees above.

Ownership is clear. Agent owns the existing explicit source producer and SDK
file-input manifest (`media.import_file` -> descriptor -> `inputs.theme`);
Runtime owns project/CAS admission, ordered binding, claim and retry custody;
Viewing owns consuming the already materialized named `theme.json` and passing
it to the existing resolver. App’s current `renderRouter.ts` is not an
authority: it sends `theme_id` as a slug and `input_object_ids: []`, so it must
not turn browser state or a slug into Theme authority.

## Source findings

The preserved Main path is present in Agent:

1. `astrid/sdk/remote.py:1543-1552` imports authored bytes into project CAS
   and returns the Runtime descriptor.
2. `astrid/sdk/invocation.py:2639-2657` carries declared file-port digests in
   the existing admission manifest; `theme` is a declared render file port.
3. `astrid/core/execution/generic_host.py:6888-6904` requires the admitted
   object, verifies its bytes through the existing authorized fetch, and
   materializes it as `theme.json` / `materialized_objects["theme"]`.
4. `astrid/packs/rendering/shared/rendering_backend/__init__.py:89-123` is
   the one resolver. It reads that file, merges only `theme_overrides`, and
   does not resolve a slug. Remotion receives the resulting `props.theme`.

Runtime’s ordinary no-`timeline_ref` task path already retains named inputs.
However, the normal regression uses the current managed `timeline_ref` path,
where `runtime_protocol/store.py:2105-2117` compares supplied IDs only with
canonical registry media IDs. The genuine Theme descriptor is therefore
rejected before claim/materialization. The paired admission worker’s “no
Runtime patch” proof exercised the ordinary carrier but did not cover this
managed caller; it cannot approve the failing managed path.

## Required product change

Make the smallest change at the existing Runtime managed-freeze seam. When
the existing named `inputs.theme` descriptor is present, accept exactly that
one additional project-owned CAS object in the task’s ordered input list, with
the descriptor’s `object_id` and `digest` equal and the existing safe
`theme.json` filename. Preserve the request’s established order (the focused
regression expects Theme first, then canonical media, then the Runtime-owned
snapshot). Reject every other extra object.

The seam must recheck, without a new contract:

- selected project membership and managed relation;
- exact CAS digest and bytes, size, and `application/json` MIME metadata;
- the existing named descriptor / `input_digests` / ordered
  `execution_request.inputs` identity;
- claim materialization and attempt-local hash/size checks;
- exact idempotent retry and restart identity.

Keep canonical timeline authority and media closure unchanged: the Theme is a
normal named task input, not inline certificate data, a timeline snapshot
member, a slug lookup, or a new Theme selection contract. Missing, foreign,
tampered, corrupt, or MIME/size-inconsistent explicit descriptors must refuse
without writes and must never invoke the builtin fallback. An absent Theme
descriptor must retain current default behavior.

No new ThemeDocument, `app.astrid.themeSource`, DTO, endpoint, store,
resolver, preparation task, delegation, private mode, worker scope, namespace,
schema/client pin, or artifact is authorized. Private preparation remains
DEFERRED.

## Evidence

The paired focused regression worker reported:

- `python -m pytest -q tests/test_timeline_explicit_theme_main_preservation.py`:
  0 nodes because the integration-marked tests were deselected.
- `python -m pytest -q -m integration tests/test_timeline_explicit_theme_main_preservation.py`:
  **1 passed, 1 failed**. The foreign/tampered no-write negative passed; the
  positive failed at `render input_object_ids do not match the canonical
  timeline registry` before claim/materialization.
- `python -m py_compile tests/test_timeline_explicit_theme_main_preservation.py`:
  passed; collection found 2 nodes; `git diff --check` passed.

Independent custody negative run (this worker; the only test run here):

`PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_runtime_control2.py::test_hc04_admission_rejects_unready_duplicate_and_foreign_inputs`

Result: **1 passed in 0.46s**. This verifies the existing project-custody
refusal boundary, not explicit-theme positive parity.

The original strict suites were source-reviewed but not duplicated: canonical
closure/scene-object integrity in `tests/test_canonical_render_admission.py`,
candidate and closure forgery negatives in `tests/test_capture_candidate_actual.py`
and `tests/test_snapshot_authority_refusal.py`, and restart/exact-retry
identity in `tests/test_render_admission_exact_retry.py`. No full, default-five,
old28, browser, live-socket, renderer, MP4, or duplicate green suite was run.

Approval requires the narrow managed-freeze source change, a committed
regression test, and one rerun of only the previously failed positive node.
