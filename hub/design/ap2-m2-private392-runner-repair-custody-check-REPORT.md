# private392 runner repair custody check

## Verdict

**HOLD execution; approve the repaired source shape only.** The repair is
present in App commit `074bc23cfe50c1bf9fb2565b6ec395abe5388398` and fixes the
reviewed `exec` cleanup defect. Execution is not approved because the exact
qualified interpreters required by the launch contract are absent:

- `/home/user/work/venv-agent/bin/python` — absent
- `/home/user/work/venv-runtime/bin/python` — absent

The available `venv-app2-native` environment was not substituted.

## Source review

The committed repair is limited to:

- `scripts/testing/private392-http-runner.sh`
- `scripts/testing/private392-http-runner.test.mjs`

`runtime.lock.json` and the reviewed driver are unchanged from App source
`85ae206b815381da31c229cc9107e322cb9c612f`. The runner now keeps Vitest as a
foreground child, captures its original status, exits with that status, and
uses an `EXIT` cleanup trap plus HUP/INT/TERM status traps. The static/subprocess
failure witness passed. The source retains the ambient, public-lock,
clean-checkout, credential/project, outbox, schema, manifest, and driver-hash
guards; it does not add a pin, public lock edit, hosted-UI claim, bypass, or
unqualified interpreter substitution.

## Evidence

Passed in the writer's isolated App source worktree:

```text
sh -n scripts/testing/private392-http-runner.sh                         PASS
node --check scripts/testing/private392-http-runner.test.mjs             PASS
node --test scripts/testing/private392-http-runner.test.mjs              PASS (1 test)
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
                                                                         PASS
git diff --check                                                         PASS
```

The retained exact identities were independently checked read-only:

- Agent `1303ce6b`, parent `e010e6a3`, tree `2f2685d8…`;
- Runtime `f8da4b6d`, tree `8be43e13…`;
- all 75 Runtime artifact hashes, manifest, bundle, component manifest, and
  Agent/Runtime schema identity match the reviewed values;
- driver SHA-256 remains
  `85a6f1b2caa7929fb4f6d29855529b6ff837a4ad293b85dd187d080e74d7b981`;
- the repair commit changes only the two runner files.

No browser, hosted build, localhost/socket, live HTTP/Door, request-test,
full suite, or central live qualification was run.

## Blocker and next step

Provide the exact read-only qualified Agent/Runtime interpreter pair for
`1303ce6b` + `f8da4b6d` (or a documented child environment that preserves that
pair), then run the existing wrapper with those explicit paths and exact clean
checkouts. Do not create or modify a shared environment in this App worker.
