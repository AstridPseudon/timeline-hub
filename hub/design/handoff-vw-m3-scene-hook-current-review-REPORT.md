# APPROVE — CURRENT capture scene-props hook

## Verdict

APPROVE for landing the recorded current-base prerequisite at `18ec2b573c5dd035bae9800363a18bc4cbcee176`, relative to base `7261b4ad5827466b2e17f1a30bf35d2fd05e0700`.

There is no blocking issue in the complete two-file diff. The minimal landing scope is the existing change to `astrid/packs/rendering/rendering/renderers/remotion/run.py` plus its direct test file `tests/packs/rendering/test_remotion_capture_scene_props.py`. Preserve current private paths and do not activate callers, source checks/labels/mouth consumers, or delete private evaluation in this landing.

## Verified behavior

- `capture_remotion_frames` canonicalizes the requested frames once as a sorted, deduplicated tuple. The same tuple reaches the callback, persistent frame-session request, and CLI `--frames` argument.
- The callback runs synchronously after final `merged_props` construction, alpha-theme neutralization, effect-asset staging, and the exact `json.dumps(merged_props)` write, but before capture submission. It therefore observes the final Root props mapping and the actual selected frame batch while the materializer, staged effect files, and invocation asset server remain live.
- Opaque nested values, explicit `None`/`False`/empty values, resolved assets, staged parameters, resolved theme, review, and alpha handling are covered by the direct preparation test. The callback does not alter the serialized props consumed by Node.
- Omitted and explicit `on_scene_props=None` preserve the old locked-executor keyword shape. Video renders do not invoke the observer.
- Callback exceptions propagate with identity unchanged and prevent capture submission. Capture failures and omitted-frame failures retain their existing errors. All exercised outcomes clean up props, temporary staging, public effect roots, asset-server state, and the placeholder output.
- No asynchronous save, renderer result, or later acknowledgement is needed for callback execution. A successful callback is only preparation evidence; callers must discard retained observations if capture later fails or requested frames are missing.
- The hook exposes no source certification. Props shape, resolved assets, and frame preparation do not prove historical/source/occurrence facts, evaluator parity, or any SDK check. The recorded canonical-profile seam remains the required basis for any later caller join; thumbnail resizing is not the composition basis.

## Evidence

Commands run from this review worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= tests/packs/rendering/test_remotion_capture_scene_props.py tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_remotion_frame_bench.py tests/packs/rendering/test_remotion_scratch_guards.py
41 passed in 3.52s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE tests/packs/rendering/test_remotion_capture_scene_props.py
All checks passed

git diff --check 7261b4ad5827466b2e17f1a30bf35d2fd05e0700 HEAD
passed

Renderer lint diagnostic comparison against base 7261b4ad5
identical: 7 pre-existing diagnostics; no new diagnostic
```

Not run by this review: full suite, browser, real rendering/SSR, live sockets, installation, network, or central test service. The focused tests use existing host seams and synthetic PNG outputs, so they are not pixel/render qualification.

## Decisions and next step

No judgment call or plan deviation was required. The next landing step is the recorded source-owner join: derive composition basis from the same frozen materialized inputs via `_canonical_profile`, then join frozen post-resolve, historical, and occurrence facts. That later work must retain this hook's lifetime and failure semantics and must not treat this prerequisite as source certification or as a D09/M3/Gate 6 result.

