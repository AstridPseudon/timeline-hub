## FAIL — independent first-return harness review

Reviewed PLAN §3, `commit-v2.md` §§1–5, BOARD-HEADER, FAIL0619, and return0626.

Blocking findings:

1. **No manager gate.** `run-original` authorizes execution solely when the caller supplies the current script digest (`tools/run-generic-reopen-original-0605.py:518-522`). There is no manager-gate receipt, verification, or test-service registration. The normal test service has no caller for this harness.

2. **Setup failures lack required durable evidence.** The top-level failure path writes only `failure.json` and `suite-row.json` (`:627-651`). It omits safe-env values, origins, result/JUnit, exit, and complete before/after invocation evidence.

3. **Authority can be fabricated through path overrides.** Child metadata, markers, and the receipt are caller-selected; receipt checks are substring checks (`:246-259`). RECORDs are internally self-consistent but not independently pinned, and installed package origins are recorded rather than compared to fixed expected identities. This does reject the observed `ba8f/f320` child, but does not satisfy the no-custody-fabrication requirement.

4. **Post-run checks do not fail closed.** Origin/profile failures after execution are recorded but ignored; only source-target mutation changes the return status (`:575-598`). Full source cleanliness is also not rechecked after the body.

5. **Profile peer/install identity is incomplete.** The fixed lock/archive checks are present, but peer resolution and the full installed Composition dependency tree are not independently verified.

The source/body hashes, exact selector, 12 assertions, timeout, Node/profile/archive locks, source/runtime markers, and old-child refusal logic otherwise match the stated requirements.

### Static acceptance

- `python3 -m py_compile tools/run-generic-reopen-original-0605.py` — PASS
- `/home/user/work/venv-agent/bin/ruff check --no-cache tools/run-generic-reopen-original-0605.py` — PASS
- `bash -n tools/run-generic-reopen-original-0605.sh` — PASS
- `git diff --check` — PASS
- Script SHA — `3ea291035284d0a057fa2a14c7ab8622b59ea0f6aab7cbe32ace5fd5a68a39c5`

No preflight, provisioning, Node, host, test body, full suite, or browser run was performed. Worktree remains clean.

### Future caller shape

```text
tools/run-generic-reopen-original-0605.sh run-original \
  --source-root <clean-bb50-source-carrier> \
  --child-root <qualified-bb50-f320-child> \
  --provision-receipt <manager-receipt> \
  --profile-root /home/user/work/runtimes/agent-remotion-v3-819acf-1110 \
  --node /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  --evidence <private-evidence> \
  --tmpdir <private-tmp> \
  --reviewed-script-sha256 3ea291035284d0a057fa2a14c7ab8622b59ea0f6aab7cbe32ace5fd5a68a39c5
```

This command must remain held until a genuine candidate child and an independently verified manager gate exist.