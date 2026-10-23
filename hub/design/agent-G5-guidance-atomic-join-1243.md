# G5 guidance atomic join — DRAFT ONLY / P1 NO-GO

## Result

The current G5 guidance branch at `71d1602dc` now contains exactly the two independently reviewed R1 atomic-scope blobs. This was a direct two-file import; no old-ancestry merge was used.

- `astrid/sdk/timeline/_commit_patch.py` = `c2993997edecda94ad6bd9853cbc40a2e3ce804d`
- `tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py` = `81734d78d1244655b18eff3bfd7027f25d4beded`
- Both hashes are byte-identical at reviewed `dcb4cee32285712f0639063f9efb96f810b357d7` and integrated `5b1b4db8253f46e0e085908e79f309d492877386`.
- Existing G5 guidance fixture work from `71d1602dc` was preserved. No other repository path was changed.

The retained source-authority qualification from `agent-G5-guidance-authority-review-1239.md` remains valid; this worker did not alter its fixture or production callers.

## Authorized workflow run

Ran exactly once after the final join:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/v10/test_domain_cli_projects_timelines.py -k editing_guidance_consumes_its_json
```

Result: **exit 1; 1 passed, 2 failed, 106 deselected in 9.13s**.

- `checkout`: passed.
- `file`: publication was accepted, but the retained assertion at line 1422 found landed `inside.params.x == 15` instead of `90`.
- `draft`: same accepted-publication/landed-value failure.

This is a new causal failure after the R1 join, distinct from the prior atomic dependency-union refusal. I stopped immediately and did not blindly repeat it, weaken/skip/xfail the original assertions, add a guard workaround, or change the fixture.

## Causal evidence

The preserved artifacts are under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-guidance-atomic-join-1243/evidence/`

For both failing variants, the raw editable input and prepared candidate show `inside.params.x == 15`, not `90`. The accepted publication response shows the emitted `doc.patch` also has `value: 15`; its canonical document and landed record retain `15`. The copied Runtime SQLite histories preserve the exact accepted history row, full `records_json`, command writes/reads, step dependencies, effects/materialization bindings, 15 input/effect/materialization/atomic bindings and associated boundary/origin/authorship fields. Outbox state records the accepted head and no pending flight.

Therefore the failure occurs before Runtime acceptance: the file/draft edit path never emitted the requested `x=90` change. The R1 join is accepting and recording the emitted `15` payload; it is not the cause of the wrong requested value. The exact cause/owner of the file/draft edit-path value loss remains unmodified and unqualified here.

## Checks

- Exact reviewed blob hashes: pass.
- `git diff --check`: pass.
- `python3 -m py_compile astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py`: pass.
- No full suite, browser/socket/HTTP, native14/58, D17, P1/P4, or shared-install operation was run.
- No plan decision was changed. G5 remains **DRAFT ONLY / P1 NO-GO** pending investigation by the guidance-path owner.

