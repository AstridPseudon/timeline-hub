Implemented on `tl/agt-m2-registered-producer-admission`: original target/closure, file declaration, exact child associations and VerifiedMedia now reach the registered assembler’s host input. Ordered associations remain separate from unique CAS IDs. Shared family mapping stays held for Runtime agreement.

Validation:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_assembly.py
```

**16 passed**; broader session/stitch/assembler tests: **90 passed**.

Central service ran:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-94114269 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_identity.py tests/packs/rendering/test_registered_assembler_admission.py tests/packs/rendering/test_registered_assembler_producer.py
```

**5 passed, 2 expected failures**. Both real admission/CAS cases pass; unchanged completion probes retain their legacy-publication failures. Six host socket cases also passed centrally. Ruff and `git diff --check` passed; the existing cycle-baseline failure remains.

Native artifact generation, settlement and requester acceptance remain the next unit. Current integration Runtime has a schema mismatch with this Agent’s pin; no pairing bypass or legacy-hook deletion was added. No full suite requested.

[Report with exact commands, source and handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-registered-producer-admission/notes/report.md). `commit-msg` and `DONE` written.