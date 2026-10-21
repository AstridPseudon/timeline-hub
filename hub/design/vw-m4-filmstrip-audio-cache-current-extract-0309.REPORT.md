# Filmstrip audio-cache extraction

Base branch SHA: `ed3ec73954dea96b758b19d4575e8117669119f1`
Base tree: `bfa34169ef6913f4f7c925e2a5466a956fe4d5d6`
Branch: `tl/vw-m4-filmstrip-audio-cache-current-extract-0309`

Applied the source-owner extraction narrowly:

- Added `timeline_visualize/_audio_cache.py` with the unchanged `_audio_cache_path`, `_cached_audio`, and `_store_audio_cache` bodies.
- Imported the two call-site helpers and removed only the old inline definitions.
- Declared the helper in the rendering pack implementation resources.
- Kept the rationale reference at 2,015 lines and updated only its description; the resulting execution file is 2,045 lines, within the fixed 50-line tolerance.
- No cache key, path, retention, source/PNG, or mint-on-hit behavior changed.

Static evidence:

- AST/body equality: PASS for all three moved helpers against `git show HEAD:.../filmstrip_execution.py`.
- Pack resource closure: PASS.
- `git diff --check`: PASS.
- Worktree file SHA-256 values: `_audio_cache.py` `dc6e45378ab108085cecc916b10e2a17dfb6748a7d13a29df2993ec4ea313bbc`; `filmstrip_execution.py` `f161eeb9d541fb8c1f4f31f50599fb7aad063f027b6f149b3f819be09c8456e8`; `pack.yaml` `c73945c0397ee61e2e6e76b32b70b7bafe3cbdcb47c12054eec2ecda54db92d0`; `giant-file-rationale.md` `6cb244a23009efa8bc8805e04ed292f6acaedb93562f953b2dcfe9732ddd18ce`.
- No generated artifact was changed.

Tests:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_audio_analysis.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py` — **69 passed**, 1 deprecation warning.
- The requested structure node was run in the combined command with those neighbors. It reported the pre-existing unrelated mismatch `astrid/sdk/timeline_filmstrip.py`: actual 1,691 lines vs rationale 1,251 (440 over tolerance). The touched files passed; this worker did not modify the unrelated inventory entry.

The harness should commit the worktree. The exact post-commit SHA/tree is therefore not available before harness commit; the base SHA/tree above and flat patch/filelist are exact. No full suite was run.
