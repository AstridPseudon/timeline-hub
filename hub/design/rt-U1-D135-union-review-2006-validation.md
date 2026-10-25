# rt-U1-D135 union validation

## Identity and union

- Review: `rt-U1-D135-union-review-2006`; repository: Runtime.
- HEAD: `0bb3bc45cef22bc317398d79e1617da3eb430df2`; tree: `73d92563277d2ba5e49b788924c07426a2fdec4a`.
- Parents, in order: base `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9`; upstream `dbcdb97c50afc72bd5e2599cb7ead0fe56bc7c4f`.
- Merge-base: `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`.
- `git diff --name-only merge-base upstream`: exactly 29 incoming paths.
- The 29-path union has 10 overlap paths and 19 upstream-only paths. All 19 upstream-only paths have exact SHA-256 byte equality between HEAD and upstream; see `source-manifest.json`.
- Conflict-marker scan: PASS; no exact `<<<<<<<`, `=======`, or `>>>>>>>` marker lines.
- This is an actual two-parent merge. No merge, checkout, rebase, push, or product edit was performed by this review.

## Source/auth review

PASS on source inspection.

- `runtime_protocol/daemon.py` configures process policy, probes process signaling, and announces before provider loading; provider registration, startup-only timeline-provider behavior, and cleanup/error-close paths remain wired.
- `runtime_protocol/process_control.py` retains strict default policy and rejects invalid, symlink, or non-regular policy settings.
- `runtime_protocol/platform.py` retains boot-scoped identity, pidfd behavior, strict refusal, and sandbox-only identity-checked fallback behavior. The member walk checks identity and signals the leader last.
- `runtime_protocol/door.py` reserves the ACP identity and exact selection/API-key routes; unauthorized exact methods do not fall through to parameterized routes. Existing auth/scope routes remain.
- `runtime_protocol/server.py` keeps the C0 public error envelope redacted while logging traceback details only to stderr.
- `runtime_protocol/service.py` preserves the settled managed-output filename behavior: the emitted original name comes from the managed filename field, not the port label.
- Existing C0 redaction, idempotency, old-route guards, strict identity/pidfd/auth boundaries, and provider registration/cleanup were inspected in the union. No public protocol change was found. The full v2 request/reply fields remain as specified by the authoritative contract.

## Test-union/predicate inventory

- Upstream-only process-control predicates are present byte-for-byte: strict default/settings validation; sandbox-only PID fallback; boot identity; bounded member walk with leader-last signaling; probe/doctor and cleanup behavior.
- Upstream-only platform-signaling predicates are present byte-for-byte: ABI/wrapper behavior, errno handling, identity/refusal cases, and FD cleanup.
- Upstream-only dirfd/data-root/native-custody/managed-output/seccomp families are present byte-for-byte.
- Overlap `tests/test_door_routes.py` retains local timeline/auth route predicates and upstream selection/forbidden-method predicates.
- Local `tests/test_timeline_commit_contract.py` and `tests/test_timeline_legacy_authority.py` remain present and unchanged from the base parent. No tests were weakened, skipped, deleted, or converted to refusal expectations; no new xfail/skip was introduced.
- The generated/canonical output set is unchanged by the incoming path list. No regeneration was needed.

## Validation commands and results

All commands below ran against the reviewed HEAD.

- `/home/user/work/venv-runtime/bin/python generators/generate.py --check` — PASS (exit 0).
- `/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check` — PASS: `contract/artifacts.json is current`.
- Private compile over the 24 incoming Python paths:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<private tmp>/pycache /home/user/work/venv-runtime/bin/python -m py_compile <24 paths>` — PASS.
- AST parse over the same 24 Python paths — PASS (`ast_parse=PASS files=24`).
- `git diff --check` — PASS.
- Scoped Ruff over the incoming Python paths — exit 1 with 118 existing diagnostics. Comparing diagnostic identities against the union of both parent baselines found 0 new diagnostics; no autofix was run.
- Scoped Pyright `--outputjson` — exit 1, version 1.1.414, 668 errors / 0 warnings / 0 information across 24 files. This is the repository's broad, unconfigured baseline; it is not a clean typecheck and is not claimed as a new-diagnostic-free proof.

## Functional test status

NOTRUN / UNQUALIFIED for this worker. Local targeted execution was prohibited by the disk gate: `df -Pk .` reported 4,732,916 KiB free, below the required 5 GiB light-test threshold and above the 4 GiB stop line.

The sole central targeted attempt, submitted for the author tree and not duplicated here, used:

```
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_process_control.py tests/test_platform_signaling.py tests/test_door_routes.py tests/test_managed_output_public_api.py tests/test_timeline_commit_contract.py tests/test_timeline_legacy_authority.py
```

It reported `1491 passed, 80 errors in 40.01s`; all 80 setup errors were the missing Astrid checkout `/home/user/work/wt/astrid` (the harness requested `ASTRID_CHECKOUT`). This is setup-invalid evidence, not functional acceptance.

Required farm rerun recipe after supplying a valid Astrid checkout, with the author’s exact test options:

```
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D135-private-join-1952/evidence/targeted.xml tests/test_process_control.py tests/test_platform_signaling.py tests/test_door_routes.py tests/test_managed_output_public_api.py tests/test_timeline_commit_contract.py tests/test_timeline_legacy_authority.py
```

Use a valid Astrid checkout (for example `ASTRID_CHECKOUT=/home/user/work/agent` and `PYTHONPATH=$PWD:/home/user/work/agent` in the farm environment) and do not treat the 1491/80 setup result as PASS.

The central test-service submission form is:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-U1-D135-union-review-2006 targeted --files "tests/test_process_control.py tests/test_platform_signaling.py tests/test_door_routes.py tests/test_managed_output_public_api.py tests/test_timeline_commit_contract.py tests/test_timeline_legacy_authority.py")
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

## Verdict

Source/auth/union review: PASS.

Functional targeted acceptance: NOTRUN / UNQUALIFIED due disk gate and the farm’s missing-Astrid setup error. D59 remains a merge gate.

