**Fixture repaired; acceptance remains blocked by a product caller gap.**

Changed only [test_duck_runtime.py:112](/home/user/work/wt/agt-U2-duck-seed-sol-0801/tests/packs/music/test_duck_runtime.py:112):

```python
parent["clips"] = parent["config"]["clips"] = [
```

Before: root clips contained `voice-1` and `music-1`; `config.clips` remained empty. After: both contain the identical original rows. Registry, raw media IDs and boundaries are unchanged. All **17 original assertion ASTs** and the entire initial-publication/scenario/adoption suffix remain unchanged.

Offline evidence goes beyond Luna’s mirror diagnosis: the repair clears emission, but production `Checkout.publish()` then refuses with `dependency_changed: patch references media outside Runtime-verified inputs`. The existing authoring adapter accepts the identical candidate using `media.admit`. New-media adoption exposes the same caller gap.

**Owner handoff:** Agent G3/G4, [publish.py:255](/home/user/work/wt/agt-U2-duck-seed-sol-0801/astrid/sdk/timeline/publish.py:255), through submission/steps at line 283. Integrate authoritative input admission while preserving retry, steps and receipt handling. Existing implementation: [authoring_commit.py:150](/home/user/work/wt/agt-U2-duck-seed-sol-0801/astrid/sdk/timeline/authoring_commit.py:150). No product or guard changes made.

Verification used `/home/user/work/venv-agent/bin/python`, `PYTHONDONTWRITEBYTECODE=1`, and this worktree plus Runtime `rt-pin-1d9ddba5` on `PYTHONPATH`:

- `-P -m pytest -q -oaddopts= -pno:cacheprovider --basetemp="$TMPDIR/targeted" tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_doc_patch_mirrors.py tests/sdk/test_timeline_normal_publish.py` — **61 passed, 72.05s**.
- `-P -m pytest -q -oaddopts= -pno:cacheprovider --basetemp="$TMPDIR/media-targeted" tests/timeline/test_authoring_commit_media.py::test_raw_media_admission_requires_real_declared_project_input tests/timeline/test_authoring_commit_media.py::test_production_authoring_writer_commit_retry_and_strict_guards` — **2 passed, 2.39s**.
- Original eight-file union with `--collect-only -q -oaddopts= -pno:cacheprovider` — **136 collected**.
- `-m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE tests/packs/music/test_duck_runtime.py` — passed.
- Python `compile()` and `git diff --check` — passed. Configured mypy sources unchanged.
- [Offline control](/tmp/w-604e00769d/duck_seed_control.py) — passed; [complete topology/results log](/tmp/w-604e00769d/duck_seed_control.log).

Agent base: `ccf87bd949fa7b702124d6eed45aa0e9021fffd4`; expected candidate tree: `3bc27e51913eb00bfa32b683af01ce75ec6e28fc`. Runtime: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree `f56c396c4495547680b46e832565278d2c375e69`.

[Exact-source service row](/tmp/w-604e00769d/u2-duck-seed-136.row) staged only. No managed body/full/browser/renderer run submitted. Commit message and `BLOCKED` written. Next: authorize the caller repair, review it, regenerate the row, then run managed duck through the normal service.