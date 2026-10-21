# Agent Gate7 current repository checks

Date: 2026-10-21 UTC

## Source and environment

- Main497: `497714c73531f164082555ec81b61ca5bc8b6554`, tree
  `daaeb1149898dd327947e21c554b484094f960b2`.
- Published014: `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree
  `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`.
- Current checked source: `cc37291af12ac6504eb48dd71ea39b9dfdb56d71`, tree
  `0698a30b3eb42d47db84ed5ed2e21221158795d`.
- Structure/doc checks used the read-only pinned Runtime source
  `/home/user/work/wt/rt-pin-95bd3c5f` (`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`).

## Commands and results

All commands used `/home/user/work/venv-agent/bin/python`; no package install,
pytest, full suite, build/install, Remotion, renderer, browser, or test-service
request was made.

```text
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-agent/bin/python -B -m scripts.reshape.compare_structure_baseline
Structure violations: current=13 new=0 fixed=0     PASS

PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-agent/bin/python -B scripts/reshape/check_doc_references.py
doc-refs: 0 error(s), 0 warning(s); checked 194 docs, 547 capability refs, 238 CLI refs in 22.5s     PASS

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/reshape/import_cycles.py \
  --baseline scripts/reshape/baselines/import_cycles.json
FAIL: 1 NEW cross-package cycle(s) introduced: rendering <-> timeline

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
Ruff findings: current=2160 baseline=2203
ERROR: Ruff improved by 43; lock it in with ... --write-baseline     FAIL (stale shrink-only baseline)

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_mypy_baseline
ERROR: mypy failed to execute (exit 2) ...     FAIL (environment/type contract)

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/reshape/ci_doctor.py
CI doctor contract check failed (exit 1)
python: No module named astrid     FAIL (environment/package installation)
```

The unqualified structure/doc invocation initially failed at
`astrid/core/execution/persistent_supervisor.py:17` because the shared venv has
no `runtime_protocol`; rerunning with the pinned Runtime path above passed.
The doctor subprocess is intentionally hermetic at
`scripts/reshape/ci_doctor.py:39-50`, then runs `python -m astrid` from a temp
cwd at `scripts/reshape/ci_doctor.py:80-82`; the venv has no installed Agent
package. This is inherited environment setup, not a current Timeline source
failure. No install was attempted because the task forbids package changes.

## Classification

### Timeline/current source

- The current published014 Timeline source had one directly owned Ruff defect:
  `astrid/sdk/_remote_timeline.py:103` used a blanket `except Exception`.
  It now catches `(AuthoringBundleError, KeyError, TypeError)` and imports
  `AuthoringBundleError` at `astrid/sdk/_remote_timeline.py:29-32`. Targeted
  `ruff check astrid/sdk/_remote_timeline.py --output-format concise` passes;
  `git diff --check` passes. This reduced the repository count from 2161 to
  2160 without changing the baseline.
- The import-cycle failure is real relative to Main497 but not new on the
  current tip: Main497 reports six baseline pairs with no new cycle, while
  Published014 and current both report seven, adding `rendering <-> timeline`.
  The concrete edges are `astrid/core/rendering/profile.py:13`,
  `astrid/core/rendering/storage.py:18`, and
  `astrid/core/rendering/window_inputs.py:55-56` into Timeline, with the
  reverse scene-query imports at `astrid/core/timeline/scene_answers.py:18,
  25, 32, 58, 156-157`. This is the known cross-area Scene/M3 seam and is not
  a minimal Agent-only lint fix; Viewing/Timeline owners should remove the
  cycle at that seam before changing the baseline.

### Inherited Main / toolchain

- Ruff is a shrink-only baseline mismatch, not a current regression: the same
  command measured Main497 `2204` findings (one above its `2203` baseline),
  Published014 `2162`, and current `2160`. Do not write the baseline as part
  of this triage.
- Mypy is not executable under the supplied environment. Current and
  Published014 both fail on missing YAML stubs at
  `astrid/core/element/project_packs.py:23`,
  `astrid/core/model_catalog/registry.py:169`,
  `astrid/core/pack/agent_index.py:28`, `canonical.py:21`, `cli_basic.py:18`,
  `loader.py:11`, `manifest.py:9`, `validate.py:25`,
  `validate_first_party.py:14`, `astrid/core/timeline/clip_fields.py:19`,
  `astrid/core/timeline/scene_roles.py:62`, and `astrid/core/scaffold.py:121`;
  NumPy also emits `.../numpy/__init__.pyi:737: Type statement is only
  supported in Python 3.12 and greater`. The project declares
  `python_version = "3.11"` at `pyproject.toml:230-234`, while the shared
  interpreter is Python 3.13 and the lock selects NumPy 2.5.2 for Python >=
  3.12 at `requirements/runtime.lock:669`. `types-PyYAML` is not declared
  beside `PyYAML` at `pyproject.toml:16`; dependency/type-contract ownership
  is required before any pin or environment change.
- The doctor failure is the same inherited installation issue described above.

## Next bounded action

Viewing/Timeline owners should make the `scene_answers`/rendering seam acyclic,
then rerun only `scripts/reshape/import_cycles.py --baseline
scripts/reshape/baselines/import_cycles.json`. Separately, the environment
owner should provide the pinned Runtime import path plus an installed Agent
package and a Python-3.11-compatible mypy/NumPy environment; no dependency
pin, baseline, or ignore was changed here.
