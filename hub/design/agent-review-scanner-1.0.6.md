# Agent review: owner film clip-look scanner 1.0.6 (sha256 1df2ee0a64709b1a275fcd8aa0a8937979f7fbe6b99e341aa309ae0cb48cefa3)

Reviewer: Agent worker agt-review-scanner-106 (2026-10-20). Review only; no repo changes, no commit-msg, nothing pushed or merged.

## Verdict

**REJECT** for the exact artifact sha256 `1df2ee0a…`.

The three 1.0.5 REJECT reasons are fixed and their tests pass. A new fail-open remains: a malformed authored element/look value makes `scan()` return `status: complete` with the look silently dropped (details below). That breaks the README's own rule that unreadable metadata is `unknown` or `incomplete`, never clean.

## Inputs checked

- Archive `artifacts/owner-film-viewing-tools-v1.0.6.tgz`: sha256 `1df2ee0a64709b1a275fcd8aa0a8937979f7fbe6b99e341aa309ae0cb48cefa3`, matches `design/handoff-viewing-scanner-final-1.0.6-metadata.json` (`archives.tgz`).
- Members read in memory with `tarfile` under `/home/user/work/venv-agent/bin/python -I -B`. Member sha256 match metadata: `owner_film_cliplook_scan.py` `e2410417…`, `tests/test_owner_film_cliplook_scan.py` `d643cac5…`, `tests/conftest.py` `ea7d8492…`, `README.md` `fb77b4f2…`.
- Flat copies `design/handoff-viewing-scanner-final-1.0.6-{scanner.py,tests.py,conftest.py}` match the same hashes.
- The archive was never extracted or executed from its directory. Code and tests were written to `$S/scanner-review-106/` (`$S` = worker session scratchpad) and run from there.

## Test run

```
/home/user/work/venv-agent/bin/python -I -B -m pytest -q -p no:cacheprovider \
  $S/scanner-review-106/tests --agent-root /home/user/work/wt/agt-review-scanner-106
→ 36 passed in 7.74s
```

- The Agent checkout was my worktree `/home/user/work/wt/agt-review-scanner-106` (branch `tl/agt-review-scanner-106`, head `481e600b`, clean). It is not the owner's extracted Agent checkout.
- `--runxfail` is not relevant: the suite has no xfail markers.

## 1.0.5 REJECT reasons

1. **Openable audio-fade source paths: fixed.** `_audio_fade_observations` emits `{source_path}.params.fadeIn|fadeOut` and `…Curve`, where `source_path` is `parent_revision.payload[.config].clips[n]` or `internal_timeline_revisions[i].payload.clips[j]` for occurrence children. `source_path` is also a top-level field on each finding. `test_audio_paths_locate_parent_and_occurrence_child` (parametrized over In/Out and payload/config layouts) asserts both the input-space paths for `audio-curved` and `occurrence-1:child-audio`, and that the `projected.` track and asset paths are kept. It passes.
   - Residual: if `source_path` is `None`, the bare fade path is dropped and the finding carries only `projected.` paths. That only happens when `_raw_clip_sources` fails, which already makes the status `incomplete`.

2. **Malformed transitions fail closed: fixed.** `_transition_inventory` adds `…clips[n].transition is unreadable` and drops the row only together with that error. `test_malformed_transition_fails_closed_without_raw_values` covers `{"id": ["…"]}`, a string `"cross-fade"`, and `{"type": {"caption": …}}`, and asserts `incomplete` with the exact error and no raw marker. `test_transition_codec_exception_fails_closed` covers a codec exception. `test_null_transition_is_an_absent_declaration` keeps `null` as absent.
   - My probes also gave `incomplete` for `transition: []`, `{"id": "", "type": ""}` and `{"id": null, "type": null}`.

3. **Duplicate internal revision ids: fixed.** `_raw_clip_sources` raises `ambiguous source index` on any repeated `revision_id`, whether or not the rows conflict, and `scan()` then reports `incomplete` with `findings: []`. The Agent projector also rejects it (`shot_composition_projection.py:531-532`, `duplicate internal timeline revision`), so the closure is incomplete from both sides. `test_duplicate_internal_revision_has_no_unambiguous_source_index` (parametrized identical/conflicting) would fail if either row were silently chosen: `pytest.raises` would fail, and the status would be `complete`.

## Re-checks

- **One Agent projector: pass.** `scan()` calls `project_runtime_parent_composition` once (`owner_film_cliplook_scan.py:549`). The other Agent calls are public helpers: `clip_fields.describe`/`read`, `audio_curves.validate`, `clip_start_frame`/`clip_end_frame`, `rate`, `load_default_registry`, `resolve_render_profile`.
- **IDs-only output: pass with the README-documented residual.** Output carries IDs, pins, property names, source paths, frame intervals and classifications. The opaque-field and marker tests pass. Asset IDs and authored transition IDs appear as documented in the README.
- **Canonical incoming transition: pass.** `test_canonical_incoming_type_mapping_is_inventoried` passes; `semantics: incoming` is set.
- **`asset=None` clears accepted: pass.** `test_projector_and_scanner_preserve_explicit_optional_asset_clear` passes; the projector and scanner both accept the clear, and the authored document is not mutated.

## New blocking finding: malformed look values fail open

`owner_film_cliplook_scan.py:600-602`:

```python
try:
    described = api["clip_fields"].describe(clip, fps=fps)
except Exception:  # noqa: BLE001 - malformed authored look remains unknown
    described = {}
```

The exception path adds no closure error and no `unknown` row. The comment's claim that the look "remains unknown" is false. Consequences:

- Probe `opacity_string` (element-a `opacity: "bad"`): `status: complete`, `closure_errors: []`. `element-a` disappears from `media_look_inventory`, and the `element-a`/`element-b` `element_clip_look_overlap` finding is lost (findings 11 → 10).
- Only element and media look categories are affected. Audio fades read raw params and still emit findings.

Required fix:

1. On a `describe` exception, add a bounded closure error such as `<source_path>.<look> is unreadable` (mirroring the transition path) so the status is `incomplete`, and emit no raw values.
2. Add a test with `opacity: "bad"` (and an entrance/exit or crop malformed case) asserting `incomplete`, the exact error, no leaked marker, and that the clip is not silently absent.
3. Correct the comment.

## Not verified

- No owner closure, and no run against the owner's qualified Agent environment or extracted owner checkout.
- No macOS claim. Linux only.
- The describe fail-open is shown by a probe run in my worktree (`PYTHONPATH` override not needed; the scanner inserts the agent root). I did not run a separate direct `describe` call, so the mechanism rests on the probe output plus the `except Exception` in the code.
