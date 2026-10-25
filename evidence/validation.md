# U1/F D135 independent source review

## Verdict

Source/security: **PASS** for merge `0bb3bc45cef22bc317398d79e1617da3eb430df2`, tree `73d92563277d2ba5e49b788924c07426a2fdec4a`.

The merge has the exact Runtime parent `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` and upstream parent `dbcdb97c50afc72bd5e2599cb7ead0fe56bc7c4f`. The actual merge-base is `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`. The incoming union is 29 paths: 10 overlapping and 19 upstream-only. The upstream-only paths are byte-identical to upstream. The current worktree is clean and has no conflict markers.

## Source/security checks

- `git diff --stat HEAD^1 HEAD` and `git diff --name-status HEAD^1 HEAD`: 29 incoming paths; no generated clients, pins, or schema source files changed.
- Parent/tree/object checks: exact two parents and tree recorded above; protected R2/auth/store files are byte-identical to the Runtime parent.
- Startup review: `RuntimeDaemon._start()` configures process control, probes, and announces before provider loading, service construction, credential provisioning, or listener startup; provider registration cleanup remains present.
- Process-control review: strict remains the default; bare-PID fallback is limited to sandbox mode after `ENOSYS` and start-time/identity checks; member walking refuses the current process group and signals the leader last.
- Door review: exact project-selection PUT and Astrid API-key route are present; method denial reserves exact paths before parameterized matching; product scopes and non-product actors remain enforced; denied routes do not fall through.
- C0 review: accepted/merged/preview shapes, redacted public internal-error envelope, idempotency, legacy 410/refusal guards, history/no-write paths, and Runtime provider/store authority are unchanged in protected sources. The upstream traceback is emitted only to stderr; it is not returned in the public response.
- Managed-output review: settled filename is stored as `original_name`; logical output-port identity remains separate.
- `python generators/generate.py --check`: PASS.
- Contract digest recomputation: PASS, `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.
- `contract/artifacts.json` verification: PASS, 80/80 entries.
- Canonical-15 comparison to Runtime parent: PASS, 15/15 exact.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-84f32cd3aa/source-review/pycache python -m py_compile <24 changed Python files>`: PASS.
- AST parse of the same 24 changed Python files: PASS.
- Direct door classifier matrix: PASS, 16 positive/negative route cases plus 3 canonical-path rejection cases.
- `git diff --check HEAD^1 HEAD`: PASS.

Ruff was run with a private cache over the 24 changed Python files. It reported 118 existing diagnostics. Four diagnostics landed on merge-added lines, but their content is upstream-parent content (one in `runtime_protocol/platform.py`, three in upstream-only tests); no diagnostic was attributable to the local merge resolution. No autofix was used. Pyright was run ad hoc because the repository has no Pyright configuration; it reported the broad existing baseline (677 diagnostics), so it is recorded as a limitation rather than a clean typecheck result. Added-line diagnostics were all traced to upstream content or missing test-environment imports.

## Targeted test result

The manager-submitted central run was read from its terminal result and was not duplicated:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_process_control.py tests/test_platform_signaling.py tests/test_door_routes.py tests/test_managed_output_public_api.py tests/test_timeline_commit_contract.py tests/test_timeline_legacy_authority.py
```

Result: **1491 passed, 80 errors in 40.01s**. All 80 errors are setup failures because `ASTRID_CHECKOUT` was not available at `/home/user/work/wt/astrid`; no source failure was established. Local pytest was not run because free space was 4,871,896 KiB, below the required fresh 5 GiB threshold.

No full suite, live socket/browser run, production store, build, ZIP, acquisition, or integration merge was run.

## Findings and next step

No source/security finding was identified. Before treating the targeted suite as qualified, rerun the same six-file central command with a valid Astrid checkout supplied through `ASTRID_CHECKOUT`; preserve the current source tree and do not alter the tests to accommodate the missing checkout.
