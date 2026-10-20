# Lint drift in generic_host: classification (read-only, 2026-10-20)

**Finding.** Agent's ruff gate counts `warm_hold`-era findings in `generic_host.py`. `warm_hold.py` itself is lint-clean.

| Finding | Location (tl/integration) | Introduced by | Main or ours | Owner |
|---|---|---|---|---|
| E402 (module import not at top), line 118 `from astrid.core.execution.warm_hold import ...` | `astrid/core/execution/generic_host.py:118` | b45f89eb "Pack host: idle release for the warm Wan2GP child and VibeComfy session" | **main** (ancestor of origin/main and of worker base 3eba65d2) | Agent (astrid) repo, pack-host area |
| BLE001 (blind `except Exception`), warm-hold idle release | `generic_host.py:5558` | b45f89eb (same commit) | **main** | same |
| E402 x26 more, lines 83-173 | same file | 71d43e003 (startup-phase marker at line 81 precedes all imports) | **main** | same |
| BLE001 x~50 in shutdown/cleanup paths | `generic_host.py:5670-13683` | 71d43e003, 6a90e9adb, 32b044360, 8214f6f2a and others | **main** | same |

**Facts checked.**
- `generic_host.py` and `warm_hold.py` are byte-identical between `origin/main` and `tl/integration` (`git diff --stat` empty). Our integration work did not change either file.
- Whole-tree ruff on `tl/integration` (ruff 0.12.0, `venv-agent`): 2212 findings. E402 824, BLE001 212.
- `scripts/reshape/baselines/ruff_astrid.json` (committed at 3eba65d2) says E402 823, BLE001 212, total 2220.
- Per-file diff of changed Agent `.py` files (3eba65d2 vs tl/integration, in ruff's include scope): zero E402 change. So the +1 E402 gap is not from a file we changed. It is a stale baseline: the same tree gives E402 824 at 3eba65d2 too. The worker's "102 vs 100" and "2219" numbers came from its own worktree, not tl/integration.

**Recommended action.**
1. Leave the generic_host findings as inherited main debt. The warm-hold commit added one E402 and one BLE001, and both are on main. Do not fix them in this stream.
2. The real gate issue is the baseline JSON, not our code: E402 is 824 vs 823 committed. Agent manager should regenerate the baseline from tl/integration once, with explicit approval (it is a count baseline, so this is a deliberate reset, not a silent widen). Do not add an allowlist.
3. If M4 touches generic_host, the cheap cleanup is `# noqa: E402` on the single block after `_emit_startup_phase` (or moving the startup marker), owned by the Agent pack-host owner.

**Runtime (our files vs origin/main).** Runtime has no ruff config or CI gate, so this is informational. Per-file deltas (ruff 0.12.0, Agent's rule set E4/E7/E9/F/I/BLE; I001 excluded because stdin mode over-counts it):
- New `runtime_protocol/timeline_commit_store.py`: BLE001 x4 (lines 340, 351, 542, 586).
- New `runtime_protocol/timeline_commit_execution.py`: BLE001 x2 (lines 90, 96).
- New tests: F811 x67 (pytest fixture names re-imported and shadowed; typical false-positive pattern), F401 x10, F841 x4, E731 x2, F541 x2, BLE001 x1 (`test_timeline_commit_crash.py`).
- Largest F811 files: `test_timeline_text_selection.py` 15, `test_render_admission_exact_retry.py` 13, `test_timeline_commit_execution.py` 12, `test_timeline_projection_occupancy.py` 10.
- Recommended: no action now. If Runtime adopts a ruff gate, move fixtures to conftest or drop the unused F401 imports first; the BLE001 in the two store/execution modules needs a per-line decision by the Runtime timeline-commit owner.
