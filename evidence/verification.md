# Verification

All commands run from the assigned Runtime worktree, with inherited `TMPDIR` set to the harness scratch directory. Shared dependencies were read only. No full suite, original P4/R2, browser or localhost run was requested.

## Final focused security run

```sh
ASTRID_CHECKOUT=/home/user/work/agent ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/test_timeline_schema_resolution.py tests/test_timeline_validation_cost.py tests/test_timeline_commit_sequential_verifier.py tests/test_timeline_commit_authentication.py tests/test_timeline_history_authenticated_read.py tests/test_timeline_commit_validation.py::test_schema_owned_values_preserve_opaque_null_absence_and_defaults tests/test_timeline_commit_validation.py::test_bad_requests_use_the_authoritative_command_schema tests/test_timeline_commit_validation.py::test_schema_rejects_invalid_record_ordinals_and_derived_causes tests/test_timeline_commit_validation.py::test_non_json_is_rejected_even_inside_untyped_payloads tests/test_timeline_commit_validation.py::test_cyclic_json_is_rejected tests/test_timeline_commit_validation.py::test_transitive_config_schema_rejects_bool_as_number_without_inserting_defaults tests/test_timeline_commit_validation.py::test_closed_prepared_failure_and_restore_envelopes tests/test_timeline_commit_validation.py::test_every_reference_is_local_and_unknown_uris_fail_closed --basetemp=/tmp/w-12886d9c5f/final-security --junitxml=evidence/final-security.xml > evidence/final-security.log 2>&1
```

Exit 0: **258 passed in 86.02s**, zero failures/errors/skips. `final-security.xml`, `final-security.log`, and `final-security.exit` are durable. Runtime parent 44917baf5976d6a655d582fafc63fde7b6cb242d; Agent test dependency 22d00393f7d944f1d01505637ca00b1995c3e158. Source of the final candidate is exactly the measured candidate hash in `cost-comparison.json`.

Earlier runs: schema/resolution 31 passed; initial broad control 189 passed / 40 setup errors because ASTRID_CHECKOUT was absent (all errors reported the missing checkout); corrected environment 229 passed in 96.86s; FIFO-focused control 33 passed. The final run includes the new concurrent-eviction/value-release test and the additional strict schema selectors. No test expectations were weakened or skipped.

## Finite cost comparison

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python evidence/cost-comparison.py > evidence/cost-comparison.log 2>&1
```

Exit 0. Ten interleaved rounds, three complete retained-capture verifications per sample, warmed parent/candidate. Median CPU 0.387122085s → 0.329615758s (14.8548% lower); median wall 0.393285667s → 0.336657966s. Identical complete schema keyword/type and validation call maps. Per verification: 56 finite-JSON/schema calls, 54 document-image checks, four claim checks, one sequential-capture check. 21,240 → 1,942 constructors. Input fixture and installed schema hashes are identical and recorded alongside exact parent/candidate source hashes. Existing finite 1850 was read only; this is a different focused control. Original 45s acceptance remains unverified.

## Static checks

```sh
pyright --pythonpath /home/user/work/venv-runtime/bin/python --outputjson /tmp/w-12886d9c5f/baseline/runtime_protocol/timeline_commit_validation.py > evidence/pyright-parent.json
pyright --pythonpath /home/user/work/venv-runtime/bin/python --outputjson runtime_protocol/timeline_commit_validation.py tests/test_timeline_schema_resolution.py > evidence/pyright-candidate.json
ruff check runtime_protocol/timeline_commit_validation.py tests/test_timeline_schema_resolution.py evidence/cost-comparison.py > evidence/ruff.log
PYTHONPYCACHEPREFIX=/tmp/w-12886d9c5f/pycache /home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/timeline_commit_validation.py tests/test_timeline_schema_resolution.py evidence/cost-comparison.py > evidence/compile.log 2>&1
git diff --check > evidence/diff-check.log
```

Pyright parent/candidate both exit 1 with exactly one identical pre-existing `URI | None` diagnostic in `_schema_resources` (line shifted 86→87); **zero new diagnostics**, tests clean. Baseline is the exact parent file from read-only Git, with unchanged relative dependencies linked read-only in private scratch. Ruff, compilation and whitespace checks exit 0. No dependency installation or shared cache write.

## Review boundary

Only schema setup is retained. Installed schema/resolver/parent identities are held strongly until bounded FIFO eviction. Cache-hit reads do not mutate; insertion/eviction is locked. Full fresh value traversal, authority and durable-store checks remain intact. Dynamic scope, nested IDs, references/siblings, missing-reference refusals, parent registries/checkers, mutation, fresh error paths, eviction, concurrency and nonretention are covered. D47's deferred authority memo and nine open attacks remain held. D62 and all wire/legacy semantics remain unchanged.

Independent security review is still required before merge. The manager owns dispatch; Agent owns the later meaningful service proof. No claim that the original now passes 45 seconds.

The comparison script now pins the same parent commit explicitly so it remains reproducible after the harness commit; measured product bytes are unchanged. The standard-library-only ABI import probe also exited 0.
