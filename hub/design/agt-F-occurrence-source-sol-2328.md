**READY_FOR_BATCH for the current-Runtime occurrence fixture, static only. No PASS_SOURCE claim.**

Preserved Sol2323 WIP and changed only the assigned test file: shot-patch guards now use the editable closure payload, leaving managed revision-link generation to the compiler.

AST checks confirm all 48 cases, 28 assertions, decorators, parameters, and authored inputs remain unchanged. Compile checks passed.

Static commands passed, with `PY=/home/user/work/venv-agent/bin/python` and `F=tests/editing_conformance/test_commit_runtime_occurrence_media.py`:

```bash
$PY -m ruff check --no-cache --config 'include = ["tests/editing_conformance/test_commit_runtime_occurrence_media.py"]' "$F"
$PY -m mypy --cache-dir=/tmp/w-bf322b5988/mypy "$F"
git diff --check
```

No pytest, test bodies, services, builds, or profiles ran, per D85.

**Unapplied downstream seam:** the parent-media fixture defaults to historical Runtime `b2a1d9f`, whose `RequestCommitPort` lacks `raw_media_info`, required by current `media.admit`. That caller remains read-only. [Source evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-occurrence-source-sol-2328/evidence/downstream-source.txt).

Next: independent protected review, then the single D85 Agent batch covering occurrence, parent-media, and transitive manifest consumers. Behavioral results remain unverified.

F-D85 commit message and `DONE` written.