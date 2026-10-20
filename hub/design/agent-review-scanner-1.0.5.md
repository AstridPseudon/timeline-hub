# Agent review: owner film clip-look scanner 1.0.5

Reviewer: Agent worker agt-review-scanner-105 (2026-10-20). Review only; no product code changed, nothing pushed or merged.

## Inputs checked

- Flat copies in `design/`: `handoff-viewing-scanner-final-1.0.5-{scanner.py,tests.py,conftest.py,README.md,metadata.json,MANAGER-VERIFICATION.md}`.
- Archive `artifacts/owner-film-viewing-tools-v1.0.5.tgz`, read in memory with `tarfile` under `python -I`. Members: `README.md`, `owner_film_cliplook_scan.py`, `tests/conftest.py`, `tests/test_owner_film_cliplook_scan.py`. The three code/test members are byte-identical to the flat copies (sha256 prefixes `3dc6e8e9`, `e090d50e`, `ea7d8492`).
- The archive was never extracted or executed from its directory. Tests ran from a scratch copy: `$S/scanner-review/` (`$S` = the worker scratchpad).

## Test run

```
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -I -B -m pytest -q -p no:cacheprovider \
  <scratch>/scanner-review/tests --agent-root /home/user/work/agent
→ 24 passed in 11.06s
```

- **The brief expected 25; the suite collects 24.** The MANAGER-VERIFICATION claim of "24 ordinary + 25 with `--runxfail`" is not reproduced. The file has no xfail markers, so `--runxfail` cannot change the count. I did not run `--runxfail` separately for this reason.
- The Agent checkout was `/home/user/work/agent` (integration head, not the owner's closure-matching checkout). `git status` is clean there and in my worktree afterwards.

## Checks against the brief

1. **One projector.** Pass. `project_runtime_parent_composition` is the only projection call (`owner_film_cliplook_scan.py:157-159, 536`). The other helpers (`clip_fields`, `audio_curves`, `duration`, `rate`, `load_default_registry`) are public Agent helpers, not second validators.
2. **IDs-only output.** Mostly pass. No media bytes, absolute input paths, raw clip fields or secrets are emitted; the opaque-field test checks this. Two residual notes: asset IDs appear in `projected.registry.assets['…'].type` source paths, and `transition_id`/`transition_type` are free-form authored strings copied through unchanged. Acceptable, but say so in the README.
3. **Canonical INCOMING transition and `asset=None` clears.** Pass for the canonical shapes. `test_canonical_incoming_type_mapping_is_inventoried` and `test_projector_and_scanner_preserve_explicit_optional_asset_clear` both pass. But see item 4 below: non-canonical transition values are silently dropped.
4. **Earlier required changes (design/agent-review-viewing-20261020b.md section 3).**
   - **(1) `curve_honoured` only for a non-linear curve.** Addressed (`owner_film_cliplook_scan.py:408, 638-649`; parametrized test passes).
   - **(2) Element overlap across tracks, requiring a look property, plus single clips.** Addressed (`:650-696`; cross-track and no-look tests pass).
   - **(3) Look set: `crop_*`, `speed`, media entrance/exit as a separate listing.** Addressed (`:47-59`, `media_look_inventory`). Element `speed=1` produces no finding (probe).
   - **(4) Transition inventory plus `not_covered`.** Partly addressed. The inventory and `transition_conversion` in `not_covered` exist, but `_transition_inventory` returns `None` on any exception or non-canonical shape (`:436-444`) with no closure error and no unknown row. A malformed transition (`{"id": ["bad"]}`) or a string transition (`"cross-fade"`) gives `status: complete` and no transition row. That is fail-open, and it is exactly the "empty result reads as no difference" case the change was meant to close.
   - **(5) Source paths openable by the owner.** Not met for audio findings. The `projected.` prefix was added for track and asset paths, but `_audio_fade_observations` returns the bare `params.fadeIn` / `params.fadeOut` as the source path (`:400-417`, emitted at `:624-637`). Probe output for `audio-curved`: `['params.fadeIn', 'params.fadeInCurve', 'projected.config.tracks[1].role', …]`. Nothing says which input clip or revision the fade belongs to, so the owner cannot locate it. Both audio categories (`continuous_audio_fade`, `curve_honoured`) are affected. For occurrence children the internal revision path is also missing.
   - **(5b) `internal_indexes` dedupe.** Partly addressed. `internal_indexes` is now built by enumerating the list (`:221-225`), but it is still a dict comprehension, so a repeated `revision_id` silently keeps the last index. The test `test_duplicate_internal_positions_keep_occurrence_identity` would pass with either choice and does not check the projector's choice. A repeated internal revision id in a canonical closure is ambiguous and should make the closure `incomplete`, not be resolved silently.

## Required changes before re-review

1. Prefix each audio-fade source path with the record's `source_path` (input-space, e.g. `parent_revision.payload.clips[n].params.fadeIn`, or `internal_timeline_revisions[i].payload.clips[j].params.fadeIn` for occurrence children), keeping the `projected.` track and asset paths. Add a test that asserts the input-space path for `audio-curved` and an occurrence child.
2. Make a transition the scanner cannot read an `unknown` row or a closure error, not `None`. Add a test with `{"id": ["bad"]}` and with a string transition.
3. Treat a repeated `revision_id` in `internal_timeline_revisions` as a closure error (`incomplete`), with a test. Do not pick one row silently.
4. Correct the test count and the MANAGER-VERIFICATION claim: 24 tests, all passing, unless new tests are added.
5. Optional: note in the README that asset IDs and authored transition IDs appear in the output.

Once those land, re-run the suite against the Agent checkout and re-review. The two earlier-approved items (curve gating, look-set and element overlap) hold up.

## Not verified

- No real owner closure, and no run of the synthetic check against the owner's qualified Agent environment. The Agent checkout used was the integration head, not the owner's extracted Agent.
- No macOS claim. Linux only.
- Not checked: whether the Agent projector collapses duplicate internal revisions first-wins or last-wins (item 5b depends on that).

## Verdict

**REJECT.** The required change the owner's hard-stop list depends on most (openable source paths for audio fades) is not met, and the transition inventory fails open on malformed input. Both fixes are narrow; the earlier-approved curve gating, look set and element overlap hold up. Re-review after the changes above.
