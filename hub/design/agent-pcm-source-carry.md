# Agent: PCM source carry (design + spike)

Worker: agt-m2-pcm-source-carry-design. Design only; no product code changed. Base read at Agent HEAD `aa02a691` (tl/integration snapshot). Line numbers are at that base unless marked otherwise.

## 0. Base state (verified, not assumed)

- `f29a9475` (Agent consumes Composition 0.0.12, `tl/vw-m3-agent-consume12`) is **not** an ancestor of the base. It only changes the pin (`astrid/core/rendering/remotion_runtime.py`), lock/package and fixtures. No slicer, run.py or service path is touched, so the line references below stand after it lands.
- Viewing's inactive unit `ab935f77` (patch `design/handoff-vw-m3-pcm-current-landing-batch-complete.patch`) is **not** in the base. It adds `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py::prepare_normal_audio_sources`, three JS helpers under `remotion/`, and replaces the four strict xfail bodies. The landing review (`handoff-vw-m3-pcm-final-landing-review-REPORT.md`) approves it as **inactive**: `_execute_remotion_locked` does not call it.
- Targeted baseline on the base tree (`request-test ... targeted`, run `agt-m2-pcm-source-carry-design-targeted-1020080014-2253`, tree `2dee8ae7`): `tests/packs/rendering/test_normal_audio_source_phase.py tests/core/rendering/test_service.py` → **54 passed, 4 xfailed**. The 4 xfails are the PCM regressions; they fail on `ImportError` of `normal_audio`.

## 1. The core finding: the service slices the wrong domain

The four PCM requirements need the originals in the **same domain the renderer consumes**, i.e. the compiled output of `Timeline.load(...).for_render().to_json_data()` (`astrid/packs/rendering/shared/rendering_backend/__init__.py:53-58`, `_serialize_timeline`). Today the host slices the **raw** JSON, and only later does the renderer compile the already-sliced file (`run.py:1104-1107`). So no compiled unsliced pair exists in the host at all.

Probe (throwaway test in the worktree, run via `request-test ... targeted`, tree `d0fa071d`/`59796dd5`; fixture: one audio clip `at 0.1234, from 0.125, to 2.125, fadeIn 0.5`, window 15..45 @30 fps):

| Stage | at | from | to | notes |
|---|---|---|---|---|
| compiled original | 0.123 | 0.125 | 2.125 | `_round_at_for_dump` rounds `at` to 3 dp (`banodoco_composer.py:48-51`) |
| `_window_timeline(raw)` | 0.0 | **0.5016** | 1.5016 | stamp `astrid_slice_origin.at = 0.1234` (raw) |
| `_window_timeline(compiled)` | 0.0 | **0.502** | 1.502 | stamp `at = 0.123` (compiled) |
| compile(slice(raw)) | 0.0 | 0.5016 | 1.5016 | recompiling the raw slice is stable |
| compile(compiled) == compiled | | | | True on this fixture |

The raw and compiled slices differ by 1.6 ms of source (`from` 0.5016 vs 0.502). A 1e-7 sample-exact PCM comparison at source .5 s cannot pass from the raw domain. This is the concrete reason the originals and the transformed pair must both come from the compiled domain. (One fixture only; idempotence of compile-after-compile needs a fade-bearing and track-bearing corpus before activation.)

Also noted by the probe: the raw slice keeps the authored track-id semantics, but `for_render` runs `_exclude_source_tracks` (`banodoco_composer.py:174`) and the `theme` default. Both change the layered slice's track list and must be covered by the layered tests before activation.

## 2. Call sites where originals are available (file:line, base)

| # | Site | Domain | What is there | Use |
|---|---|---|---|---|
| A | `service.py:1386-1400` (planner loop) | raw | `native_request` carries `window=segment.window` and the **unsliced** path | Unlayered windows: `_segment_request` returns the request unchanged (`service.py:1072-1073`). Remotion declares `supports_windows: true` (`renderer.yaml`), so **the Remotion normal route never slices unlayered windows**; the audio originals are the full props and need no map. |
| B | `service.py:1052` `_segment_request`, read at `:1076` | raw | the complete unsliced timeline JSON | **The only host slicing point for layered segments and `supports_windows: false` backends.** Slice at `:1093`, write at `:1106-1109`. Originals here are in the wrong domain (§1). |
| C | `rendering_backend/__init__.py:53-58` `_serialize_timeline` | compiled | the canonical compiled unsliced timeline | Must be used in B to make the originals and the transform compiled-domain. |
| D | `run.py:1067` ExitStack (materializer `:1077`, `InvocationAssetServer` `:1087-1098`), props `:1104-1107`, props write `:1167` | compiled (of the sliced file) | host-materialized, already sliced for layered segments | **Helper call site**: after `merged_props` (`:1104-1107`) and before `props_path.write_text` (`:1167`), inside the ExitStack so server and materializer outlive the render. |
| E | `run.py:1625` `_protocol_render` → `:1707-1719` `_execute_remotion` | - | where the request fields are threaded | new optional request field is threaded here (see §3). |
| F | `service.py:1206` `result["id"]` in `_window_clip` | - | the windowed id is `{id}_{start}_{end}` | the disposable id mapping the originals are keyed on. |

Helper call form to use in production: **the trusted original map** (`original_clips=`), not the helper's own `window=`/`tracks=` branch. The `window=` branch retains originals inside the renderer only when the renderer slices, which it never does for Remotion's routes (layered slicing stays host-owned: `service.py:1066-1070`, LayerRef isolation and alpha stamps). The `window=` branch remains valid for unit tests of unsliced input.

## 3. Data structure carried

Host-side value, created in `_segment_request` (B), keyed by the **compiled windowed clip id**, values are the **compiled unsliced original clips**:

```
SliceOrigins (frozen)
  window:        FrameWindow            # the window the transform used
  tracks:        tuple[str, ...] | None # the layer allowlist, None for windows
  source_sha256: str                    # sha256 of the unsliced compiled JSON
  clips:         { windowed_clip_id: compiled_original_clip }   # deep copies
```

- Keys: `f"{original_id}_{start}_{end}"` (the `_window_clip` rule, `service.py:1206`). The key is never parsed or stripped; it is an index only. Duplicate original IDs are refused (§5); `validate_timeline` already rejects them on compile.
- Serialized as `segment-inputs/NNNN-slice-origins.json` beside `NNNN-timeline.json` (`write_json_atomic`, same as `service.py:1109`). Its sha256 joins `materialized_hashes` (`service.py:1110-1115`), so it lands in `input_hashes` and in replay bundles.
- Transport: additive optional field on `RenderRequest` (`contracts.py:735`), e.g. `slice_origins: {path, sha256} | None`. `to_dict` (`:794`) omits it when None, so existing wire payloads stay byte-identical. `for_backend` (`:866-884`) must pass it through: it is the one backend input that is not a host-only field.
- Thread: `_protocol_render` (`run.py:1625`) → `_execute_remotion` (`:914`) → `_execute_remotion_locked` (`:1013`).

**Trust statement (be precise).** The renderer is a separate process (`_run_command`, `service.py:1932-1976`). The sidecar is host-written and digest-pinned, the same trust the renderer already gives the materialized timeline it reads. The check (§4) proves that the originals and the transformed clips are consistent. It does not defend against a renderer that forges both files and its output; nothing in the render protocol does.

**Alternative rejected: renderer re-slices from the unsliced path.** Passing unsliced `timeline_path` + `window` + `tracks` would avoid the sidecar, but moves layer isolation and alpha stamping into the renderer, which the service explicitly keeps host-owned. Not recommended.

## 4. Lifetime and ownership

- **Creation/owner:** the service, in `_segment_request`, from the compiled unsliced JSON it has just compiled. It is in memory only for that call and on disk in the segment workspace, deleted with the workspace.
- **Consumption/owner:** the renderer, in `_execute_remotion_locked`, inside the existing ExitStack (`run.py:1067`). The materializer and `InvocationAssetServer` are entered first; the render (`~:1293`) completes before the stack exits, so the `local_url`s stay valid.
- **Attempt directory (must fix before merge):** the helper requires `attempt.relative_to(materializer.serving_root)`. `serving_root` is the **shared** `materialized_root` when reusing materializations (`assets.py:304-316`), not the invocation's staging dir. Successful WAVs in that case persist in the shared cache, and the helper removes its directory only on failure. Fix: the caller creates the attempt directory under `serving_root` and registers `asset_lifecycle.callback(shutil.rmtree, attempt, ignore_errors=True)` before calling the helper. Successful WAVs then die with the attempt.
- **Authored files and the original registry** are untouched. The Root registry check (§5) binds the served bytes to the materializer.

## 5. What is validated and how a mismatch refuses

Validation runs in the **renderer's helper call** (the source owner's input check; the helper itself must not trust the map). Every failure raises before any Node subprocess and stays a normal render failure. It never falls back to the frame-step callback and never skips PCM (audio contract decision 4).

| Check | Mismatch → refusal |
|---|---|
| sidecar sha256 equals the request's recorded digest | `ValueError("slice origins digest mismatch")` |
| every transformed audio clip has an original key (today: `original_clips[clip["id"]]`, a bare `KeyError`) | `ValueError` naming the clip id; explicit, not KeyError |
| **re-derivation:** `RenderService._window_clip(original, start, end, window)` equals the transformed clip, including `app.astrid_slice_origin` | `ValueError` naming the clip; this is the check that rejects altered `at/from/to/params`, forged stamps and wrong windows. No reconstruction from the authored stamp: the stamp is compared, never trusted. |
| original `track` in the allowlist when `tracks` is set; transformed track equal to original | `ValueError` |
| original `asset` equals transformed `asset`, and `materializer.assets[asset]` is the one the original refers to | `ValueError` |
| `window.fps_rational` equals `props["compiledTransitions"]["fps"]` | `ValueError` before subprocess |
| duplicate original IDs (compiled input) | refuse; the helper's dict comprehension silently overwrites them today, so this check must be explicit in the helper, not left to `validate_timeline` alone |
| managed bytes: `metadata` digest present; sha256 matches the selected file | refuse; a `None` digest is an `AttributeError` today and must be a clean refusal |
| clip already carries `audio.render_source` | refuse (already present in the unit) |
| unexpected original keys (not transformed) | ignored, never used as authority |

## 6. Test plan

### Now (no helper needed)
- Base targeted (§0): 54 passed, 4 xfailed. Keep these; no test is weakened.
- **Not written in this spike.** The domain test (§1) and the carry test (§7) need `_segment_request` to produce the sidecar, so they need the seam. Writing them against the base would only assert the present (wrong) behaviour or require an invented API name. The one candidate I could write now is a probe of the raw-vs-compiled slice mismatch, which is evidence, not a regression. I ran it as a throwaway and removed it (see §9).

### With the Viewing unit (`ab935f77`) landed
- The **four** `test_normal_audio_source_phase.py` strict xfails (parametrized `asset ∈ {sound, other}` × `tracks ∈ {None, ("A1","A2")}`) become real positives for the **helper's** unsliced + `window=` branch, because the unit replaces their bodies with sample-exact PCM comparisons (1e-7, source .5 s). Map: `tracks=None` is the `supports_windows: false` materialization; `("A1","A2")` is the layered route.
- They do **not** prove the service route. Keep them as helper unit tests and add the service-route positives below. Do not remove the strict markers from the four before the helper is in base.
- The two compiler vectors 10–11 (`audio_compile_contract.json`) stay strict xfail until an active `audio.render_source` producer exists on the normal route.

### With the source-carry merge (new, failing first)
1. `_segment_request` writes `NNNN-slice-origins.json` whose clips are compiled unsliced originals, and whose windowed keys equal the transformed clip IDs. Fixture: the §1 clip (`at 0.1234`). Expect `from == 0.5016` for both the transformed clip and `_window_clip(compiled original)`, **not** `0.502`.
2. `_segment_request` refuses (raises) when the sidecar is tampered with (digest mismatch) and when an altered transformed clip differs from the re-derivation.
3. Layered route end to end (`_execute_remotion_locked`, central lane): helper receives originals; sample 15000 of the slice equals the original; the `sound` and `other` assets both pass; `tracks=("A1","A2")` allowlist kept.
4. Attempt lifetime: after a successful render, no `normal-audio-*` directory remains under the shared `materialized_root`; after a failed batch none remains either.
5. Unlayered Remotion route: no sidecar written (`supports_windows` true, no slice); helper called with `original_clips=None` on full props; the `ENVELOPE_UNRENDERED` refusal for any fade the helper does not prepare remains.
6. Compile idempotence across the fade-bearing and track-bearing corpus (`compile(compile(x)) == compile(x)`), so re-compiling the sliced compiled file in run.py is safe.
7. Existing `test_slice_*` tests in `test_normal_audio_source_phase.py` (positive now) stay unchanged.

Served HTTP (separate lane, central authorization): the two ordinary window/layer positives in the served fixture (`handoff-vw-m3-pcm-served-whole-ready-*`) still need the originals joined. Do not claim them from this lane.

## 7. Merge order (each its own gated branch)

1. **Agent `f29a9475` (consume 0.0.12)** into `tl/integration`. Pin and fixtures only. Verify `tests/packs/rendering/test_composition_package.py` and `test_scene_host.py` stay green.
2. **Viewing `ab935f77`** (inactive helper + four positives), **with** the §5 fixes folded in: explicit missing-key refusal, re-derivation check, duplicate-ID refusal, `None` digest refusal, fps check. The Viewing review approved the unit as inactive, not these checks. Recommend the Agent source owner review these before it lands.
3. **Agent source-carry** (this design): `_segment_request` compiled-domain originals + sidecar digest in `materialized_hashes` + additive `RenderRequest` field + thread through run.py + the call site at `run.py:1107-1167` + attempt-lifetime callback. Adds the §6 "with the source-carry merge" tests. Requires one contract check: no Runtime schema pins `RenderRequest.to_dict` keys (unverified here).
4. **Viewing activation of the Remotion normal route** (Viewing's ask after Agent join review), then the central served-HTTP lane.

Each step has a rollback: step 2 is inactive; step 3 is additive (no sidecar means no change; `slice_origins` absent means the helper is skipped only where it is not required, and fades still refuse).

## 8. Decisions to confirm (not decided here)

- **Activation changes audio.** Once the helper is called on the normal route, non-Player fades stop refusing `ENVELOPE_UNRENDERED` and export audio changes (intended per contract decision 4, ~0.7 dB mid-fade). The contract says the refusal stays until the join is live. This is the activation point; the owner's film-viewing list must include it.
- **Compile-before-slice changes layered renders** (track exclusion and `at` rounding, §1). This is a behaviour change for every layered render with a fractional `at`, not only fades. It is needed for exact PCM. The owner list should note it.
- Helper `window=` branch: keep for unit tests only, or delete when the trusted-map path is live. Recommend keep until the source-carry merge, then remove the unused branch.

## 9. What I did and did not verify

- Verified by reading code at base `aa02a691`: the call sites and line numbers in §2; `serving_root` and cleanup in `assets.py:296-325`; `RenderRequest.for_backend` and `to_dict`; `_run_command` as subprocess transport.
- Verified by targeted runs: base baseline 54 passed / 4 xfailed (`agt-m2-pcm-source-carry-design-targeted-1020080014-2253`); the §1 slice-domain probe (`...-1020080456-21505`, fixture fixed to pass the track `label` schema).
- **Not run:** any PCM render, Node decode, Remotion, served HTTP, full suite. The §1 compile-idempotence result is one fixture, not a corpus. The Runtime schema check in §7 was not made.
- **Cleanup problem (must be fixed before commit):** the probe file `tests/packs/rendering/test_zz_probe_source_carry_domain.py` is still in the worktree. I created it for the probe and tried to remove it, but the deletion was denied (both as a compound command and as a plain `rm`). It is an untracked, deliberately failing probe. The harness commits all worktree changes on exit, so the file must be removed before this worktree is committed. I did not work around the denial.

## 10. Commit

No product or test change was kept, so no `commit-msg` is written. The worktree is not clean until the probe file is removed (§9).
