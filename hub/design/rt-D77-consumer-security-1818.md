# D77 Consumer Migration Security Review

## Verdict: PASS

Scoped review of `tl/rt-D77-consumer-migration-sol-1758` against D77a, PLAN G4/V3/F, and contract §§1–5 passed. No product or test files were changed.

Reviewed candidate `dfea1e17b7ed227b73bcb06aa9b334f9edc2fb5d` against baseline `2a1637a1438ec7c373ce369097bfa9a9ec03f997`. The baseline diff contains only the expected rendering/schema consumer changes.

The verified chain is intact:

`Backend.stage` → service declaration with selected source checkout → host bootstrap derives the exact canonical JSON file → strict Remotion validation → worker/render readiness validation.

Relevant checks include:

- Canonical schema origin, ownership, symlink/path identity, mode, digest, runtime.lock pin, closure, inventory, reference resolution, finite JSON, mutation detection, and schema validation.
- Canonical reader remains authoritative; no dict/model bypass or ambient fallback.
- Actual worker readiness calls `_validated_runtime` in `astrid/core/execution/generic_host.py:8101–8106`.
- Renderer passes the validated schema environment through `run.py:1138–1144`.
- Backend/service paths remain unchanged and preserve the selected source checkout.
- Canonical schema digest remains `sha256:4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`.
- Runtime contract digest remains `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.
- All 197 shared dependency file hashes are unchanged; no generated, pin, or contract drift.

External package verification showed all inspected exports are `TypedDict`s, not runtime validators. Sources explicitly state validation uses JSON Schema:

- `banodoco_timeline_schema/__init__.py:3–7`
- `generated.py:1–8`
- `validate.py:1–5,16–40`

## Tests and checks

Exact staged-host target union:

```bash
PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/runtime/packages/python" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest @"/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D77-consumer-migration-sol-1758/evidence/selected.txt" -q -oaddopts= -pno:cacheprovider --basetemp="$TMPDIR/d77-review-final" --junitxml="$TMPDIR/d77-review-final.xml"
```

Result: `228 passed, 66 warnings`.

Focused adversarial controls covering foreign origins, ownership, integrity, mutation, references, malformed/nonfinite JSON, canonical-reader enforcement, and fallback refusal:

```bash
PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/runtime/packages/python" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest tests/core/rendering/test_local_schema.py tests/test_installer_bootstrap_schema.py tests/stage1/test_cold_launch_autobootstrap.py::test_source_profile_provisions_explicit_render_runtime tests/packs/rendering/test_render_export_task_adapter.py -q -oaddopts= -pno:cacheprovider -k 'foreign_origin or bad_integrity or writable_inputs or foreign_owner or invalid_schema or foreign_ref or missing_ref or nonfinite or canonical_reader or strict_probe or rejects_changed_canonical_authority or refuses_foreign_schema_origin or rejects_changed_installed_content or schema_import_archive_absence_to_presence or rejects_mutation_during_read or refuses_a_nonisolated_interpreter' --basetemp="$TMPDIR/d77-review-adversarial" --junitxml="$TMPDIR/d77-review-adversarial.xml"
```

Result: `34 passed, 134 deselected, 10 warnings`.

Additional checks:

- Ruff: 19 existing findings, zero new findings versus baseline.
- Mypy: 24 existing findings, zero new findings versus baseline.
- Python compilation: 8 changed files plus both embedded probes passed.
- `git diff --check`: passed.
- Worktree remains clean.

## Limitations and next steps

The authentic installed renderer/final render remains unverified by design. The D13 fixture source-path hunk is still unapplied, and the D67 environment gap is unchanged. No full, browser, HTTP, child-process, install, acquisition, or live-render suites were run.

Next step is to apply the D13 fixture seam and run the central final-render gate with the authentic installed source profile and pinned runtime dependencies.