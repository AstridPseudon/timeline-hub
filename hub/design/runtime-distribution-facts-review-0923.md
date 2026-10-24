## Report

**Verdict: FAIL/HOLD for isolated child readiness; source facts independently PASS where stated.**

- Exact Agent declaration confirmed:

  `banodoco-timeline-schema @ git+https://github.com/banodoco/ArtAgents.git@242f9c4306bf3b501222cb041a9eb246ef47bc85#subdirectory=packages/timeline-schema/python`

- Commit `242f9c…` and `packages/timeline-schema/python` are absent from all available checkouts. The checkout queue explicitly refused it as unknown; Runtime lead fetch owns that object.
- `proof.lock` hash `236d5be…` correctly omits this dev-only VCS schema dependency. It must not be treated as proof that the schema is unnecessary.
- The installed shared schema has matching `direct_url.json` metadata for the exact URL, commit, and subdirectory. Its `RECORD` authenticates installed file bytes only; it does not establish original wheel/archive hash or source custody.
- Runtime `1d9d…` genuinely packages `astrid-runtime`, including `astrid_runtime*`, its CLI, and `runtime_protocol*`. A retained prior normal-maker receipt also records `astrid_runtime` installed from the Runtime source. Therefore the farm claim that `astrid_runtime` was absent in the v3 child is **unproven and internally inconsistent** with the import line reaching the later `banodoco_timeline_schema` failure. Treat exact-v3-child Runtime provenance as UNKNOWN, not as a packaging absence.
- Both `astrid_runtime` and `banodoco_timeline_schema` imports remain required. No import deletion or row repair is justified.

The minimal genuine missing input is authenticated custody of the exact schema source (or an equivalently verifiable immutable artifact), carried through the normal maker as an explicit source component with URL/commit/subdirectory, source identity, installed distribution metadata, `RECORD`, and receipt ownership. Ambient installs, `.pth`, `PYTHONPATH`, overlays, or installed `RECORD` alone are insufficient. No maker implementation was added because Sol0923 owns that inventory.

Separate known status: current `ffb926…` source controls passed, but the retained security review still reports two accepted private attacks (foreign distribution/package and extra unowned bin executable). That remains with Sol0923.

Evidence inspected, not rerun:

- Exact retained command:  
  `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider ops-handoff/child-dependency-reuse/tests/test_dependency_reuse.py --junitxml=.../evidence/junit.xml`  
  Result: **84 passed**, 0 failures/errors/skips, 1 duplicate-ZIP warning; durable JUnit time 14.927s.
- Retained Runtime v3 targeted result: **59 passed** in approximately 11.06s.
- Retained Ruff, shell syntax, JSON/AST, manifest, helper-pin, baseline, and diff checks passed. Mypy retained the same 9 pre-existing diagnostics with no new source delta.
- No live child probe, install, network fetch, full suite, checkpoint, or retry was performed.

No Runtime files changed; worktree is clean. Commit message and `DONE` marker were written.