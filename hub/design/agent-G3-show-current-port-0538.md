# G3/P4 fresh-current ordinary-show port

PASS: current base `bf40d6bb5923210a3f5d210414c9ad737b40403d` received only
the reviewed three-file delta from source
`1f93b8b3057a7c2a611f7bdc186c943418b62bc`, whose parent/base is
`9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`. All three current pre-port blobs
matched the donor base before editing. A direct no-renames diff comparison of
the final worktree patch and donor commit passed.

Files changed: `astrid/core/timeline/cuts.py`, `astrid/sdk/timeline_cuts.py`,
and the existing `tests/sdk/test_timeline_show_views.py` with the reviewed
parent-native regression. The ordinary production caller remains
`cli._print_cut_table` → `build_cut_table` → `occurrences_from_bundle`.

Exact target command and result:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_cuts.py tests/sdk/test_timeline_show_views.py tests/timeline/test_cuts_views.py tests/timeline/test_mixed_mode_cut.py tests/timeline/test_multitrack_cut.py
55 passed, 2 subtests passed in 7.30s
```

Checks and exact environments:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m ruff check astrid/core/timeline/cuts.py tests/sdk/test_timeline_show_views.py
All checks passed!

make PY=/home/user/work/venv-agent/bin/python ruff
Ruff findings: current=2150 baseline=2150

make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy
Mypy findings: current=1915 baseline=1915

/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1915 baseline=1915

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
ok runtime.lock.json (matches producer manifest)

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check
PASS
```

Scoped SDK mypy has the same 3 existing diagnostics (core 1, SDK 2). The old
`venv-agent` normal mypy invocation is environment-blocked by missing
`types-PyYAML` and incompatible NumPy stubs; the persistent typecheck-v2
environment passes the required 1915/1915 ratchet. SDK scoped Ruff continues
to report its 10 existing findings, while changed core/test Ruff passes.

Import provenance: Agent modules resolve from the worker worktree and
`runtime_protocol` resolves from `/home/user/work/runtime`. The moving runtime
checkout initially failed vendor validation at `85dafdf4`; the exact pinned
producer `rt-pin-34eac004` passed. No source ancestry, merge parent, old G4/P4
imports, generated files, pins, shared dependencies, or Proof-owned HTTP
bodies were changed. No full/browser/live-socket/HTTP suite was run.
