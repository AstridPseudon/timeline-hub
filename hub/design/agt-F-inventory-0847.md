# Agent F-inventory handoff

## Bounded result

Source tree: Agent worktree at base
`e837e18c5156e762eca05e6d9bb15779cf847b60`.

The exact assigned group was initially **11 failed** and now is **11 passed
in 63.57s**. Neighboring occurrence-fork conformance is **26 passed in
7.00s**. Full evidence remains the approved terminal run only; no full rerun
was requested.

## Exact source/test delta

- `tests/editing_conformance/test_pristine_initialize.py`: compare the frozen
  S2 slice after removing the approved doc.patch and inverse-step additions;
  retain the exact S2 digest and operation checks.
- `tests/sdk/test_timeline_composed_schema.py` and
  `tests/sdk/test_timeline_current_union_schema.py`: record D15's intentional
  provider-only `occurrence.fork` exception without adding a frozen schema
  tuple; retain closed args and negative unknown-field checks.
- `tests/test_schema_contract.py`: retain optional V1 `meta` namespace support
  while preserving the original full-fixture digest input and all other exact
  fixture-key checks.
- `astrid/core/timeline/__init__.py`: remove three unused metadata validator
  exports; direct production imports use `validators.meta`/`banodoco_schema`.
- `astrid/sdk/timeline/emitter.py`: remove the unused
  `DocumentEmitterError` alias; no production caller exists.
- `docs/giant-file-rationale.md`: refresh six stale physical counts and add
  `astrid/core/dev/journey.py` at 1,404 lines.
- Delete the two tracked P1 handoff documents under repository-root
  `design/`; handoff/report are outside the repo as required.

Protected edit schema SHA-256 is unchanged:
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
Runtime lock SHA-256 is unchanged:
`320d278366bc344aad35f3564845d9b62d9cc5f2e000a8a4cc6b6fea508d6cd2`.

## Commands and results

- Exact named 11-node pytest command with
  `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.:/home/user/work/runtime`,
  `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`, and existing
  `ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-composition14-255b6856`:
  **11 passed**.
- Exact neighboring fork files: **26 passed**.
- Scoped Ruff: passed.
- `make ruff PY=/home/user/work/venv-agent/bin/python`: **2149 current / 2149 baseline**.
- `scripts.reshape.compare_mypy_baseline` using
  `/home/user/work/venv-agent-typecheck-v2/bin/python`: **1912 current / 1912 baseline**.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`:
  passed.
- `scripts/artifact_manifest.py --check`: passed.
- `git diff --check`: passed.

No shared dependency, generated schema/map, pin, or full suite was changed or
rerun.

## Remaining owners

The original full terminal inventory remains 316 environment/resource/
collection, 40 confirmed integration, and 24 unconfirmed, with no targeted
upstream-431 attribution. Other confirmed Agent groups remain with their
named core/rendering, platform, provider/inverse/graph, and
publish/persistence/checkout owners. The 24 unconfirmed nodes require farm
prerequisite repair and exact bounded diagnostics. See
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-inventory-0847/detailedreport.md`
for the full command transcript and decisions.
