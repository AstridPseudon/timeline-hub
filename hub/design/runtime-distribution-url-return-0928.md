## Report

- Verdict: **source/provenance PASS; isolated child FAIL/HOLD**.
- No Runtime files changed; worktree clean. `git diff --check`: PASS.
- Commit message recorded; `DONE` marker created.

### Corrected source/provenance

Both Agent heads declare the exact raw URL:

`git+https://github.com/banodoco/astrid-agent.git@242f9c4306bf3b501222cb041a9eb246ef47bc85#subdirectory=packages/timeline-schema/python`

- Selected `9cd3dbe8`: `pyproject.toml` blob `82244ebbdd26ee0cae75b81169ace65425f0a79f`, declaration at line 57.
- Current `ba55ac1e`: `pyproject.toml` blob `59517ccf460b7383788c613c16c73ecc12b2cd66`, declaration at line 59.

The retained installed schema metadata instead records:

`https://github.com/banodoco/ArtAgents.git`

with the same commit and subdirectory. These URL spellings are different; repository equivalence is **not asserted**.

Commit `242f9c4306bf3b501222cb041a9eb246ef47bc85` and `packages/timeline-schema/python` are absent from both available Agent checkouts. The lead-owned fetch/source custody remains the genuine missing input.

The existing local App vendor route `/home/user/work/app/vendor/timeline-schema/python` is a possible local producer route, but is not authenticated here to the required Agent commit and cannot substitute for it.

### Farm distribution facts

The retained 09:25 physical listing confirms:

- `astrid_runtime` and its dist-info are present.
- Runtime child `direct_url.json` points to the retained source snapshot:
  `file:///home/user/work/bench-store/entries/child-a952c90d18f34bb935d3f509e612fa35af745c574a4d1edaff3586e193fc0f60/.child-venv-source-venv-agent-child-farm-v3-9cd/runtime`
- `banodoco_timeline_schema`, `pytest-xdist`, and `execnet` are absent.

### Full-farm test distributions

Source and retained Agent metadata establish:

- `pytest==9.0.2`
- `pytest-cov==7.1.0`
- `pytest-split==0.11.0`
- `pytest-timeout==2.4.0`
- `pytest-xdist==3.8.0`
- `execnet==2.1.2`

`pytest-xdist` metadata requires `execnet>=2.1`. The full command is retained as `/home/user/work/venv-agent/bin/python -m pytest -q -n 3`.

`requirements/proof.in` and `requirements/proof.lock` contain pytest and timeout, but no xdist or execnet entries. No retained wheel/hash lock input for those two distributions was found. Ambient installed metadata is insufficient for authenticated child readiness.

Retained prior targeted evidence remains: **84 passed**, one warning. It was not rerun per the no-duplicate-suite instruction.

Recommended next step: lead supplies authenticated schema custody plus locked wheel/hash inputs for `pytest-xdist` and `execnet`, then reruns the normal maker and farm preflight.