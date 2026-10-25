D123 validation commands (pending test bodies)

Run in `/home/user/work/wt/agt-U2-D123-final-patch-sol-1221`. The exact Node20.19.4 binary exists. Do not substitute the shared Zod4.4.3 for package-lock's4.3.6. No installs were performed. CI's test Bun is1.3.14; current available Bun is1.4.2 (the build version). Do not substitute a runner version for qualification. Recover >=5GiB free before any light test body. Keep temporary fixture output in the harness TMPDIR.

The package script is `test:chat: bun test ./astrid/chat`; there is no chat Vitest config or package-supported chat typecheck/lint script. The exact targeted form of the same package runner is below; do not append paths to `bun run test:chat` because that retains the whole chat directory in the selector. service.test.ts uses a real loopback listener, so these commands require the central service, not a sandbox run. There is currently no registered Agent chat named suite in local suites.conf; manager/service owner must supply that supported route before submitting it. No test-service request was made.

```bash
PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH bun test ./astrid/chat/astrid-local-agents.test.ts ./astrid/chat/astrid-project-chat.test.ts ./astrid/chat/service.test.ts
```

Include original acp/local-agent/project/service neighbouring overlap controls in the central targeted run:

```bash
PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH bun test ./astrid/chat/acpProcessHost.test.ts ./astrid/chat/astrid-acp-models.test.ts ./astrid/chat/astrid-agent-models.test.ts ./astrid/chat/astrid-local-agents.test.ts ./astrid/chat/astrid-project-chat.test.ts ./astrid/chat/astrid-shared-acp-sessions.test.ts ./astrid/chat/service.test.ts
```

Bundle check with the package-pinned build Bun1.4.2 after exact Zod4.3.6 exists:

```bash
PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH bun run check:chat-bundle
```

Authorized primary Python test command (NOT RUN; no installer.xml generated):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U2-D123-final-patch-sol-1221 /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/test_installer_omp_source.py --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D123-final-patch-sol-1221/evidence/installer.xml
```

Exact neighbouring selectors for D77 schema carry and newly upstream post-install skill sync, using mocks rather than staging/acquisition:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U2-D123-final-patch-sol-1221 /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/test_installer_schema.py::test_staging_verifies_the_local_schema_before_declaring_services tests/test_installer_schema.py::test_local_schema_verification_rejects_a_changed_schema tests/test_installer_lifecycle.py::test_fresh_install_runs_skills_sync_after_verify tests/test_installer_lifecycle.py::test_upgrade_runs_skills_sync_after_verify tests/test_installer_lifecycle.py::test_skills_sync_failure_is_logged_as_one_line_and_install_succeeds tests/test_installer_lifecycle.py::test_backend_skill_sync_logs_output_and_failure_result --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D123-final-patch-sol-1221/evidence/installer-neighbours.xml
```

Static commands actually run are recorded verbatim in static-checks.json. Ruff exit1 contains only upstream I001 and BLE001 (see ruff-baseline-comparison.json). Mypy exit0, Node20 service.mjs syntax exit0, Python ast.parse pass. TS compiler AST parsing for predicate mapping is source inspection, not a TypeScript typecheck. TS typecheck/lint remain unverified: no such package script or configured exact chat type dependency set exists; no improvised near-match run or bypass was used.

The complete whitespace check covered tracked diff plus `git diff --no-index --check -- /dev/null <path>` for each526 imported new files. All157 diagnostics are inherited from the frozen->normal patch's162 diagnostics; no cleanup or baseline weakening. Five incidental rejected EOF additions are absent. Ordinary tracked `git diff --check` exit2 reports115; added files contribute42. `git apply --reverse --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D123-final-patch-sol-1221/evidence/b742-current-normal.patch` exit0.

No full suite, browser, P1-P5, render, stage, installer acquisition, D54 rerun, integration refresh or release was requested or performed. The final cut matrix remains the manager's later action against b742.
