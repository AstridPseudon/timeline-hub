# current013 wrapper independent review

**Verdict: HOLD.** Follow-up fixes are required before this wrapper can qualify an exact pair. This is a completed read-only review, not a blocked worker or a browser qualification. No product, wrapper, or test code was changed.

Reviewed App commit `ba8ae7228b460b0188170276e6711725d45c352c`, tree `b1c6303ae3aa6ab3185dc89bdc772126d01e96af`, against `0ea988bdd`. The diff is exactly two added files, 271 lines: the wrapper and three tests. Read PLAN.md, app-current013-browser-gate-prep.md, and runtime-current-tuple.md. No settled project decision is disputed.

## Required follow-up

1. **P1 — App source identity can be false.** `scripts/testing/current013-integration.mjs:177-188` compares App `HEAD^{tree}` to the supplied tree but only calls `checkClean` for Agent, Runtime, and producer. A modified/staged App source file, journey assertion, package script, or build helper can therefore run under the original App tree identity. Changes outside the few fingerprinted files also escape postflight. The existing suite's `revisionSet()` checks App HEAD, not working bytes, so it does not close this hole. A review probe supplied dirty App git status and confirmed that App status was never queried; preflight instead reached the actual old App lock and refused there. Require App source cleanliness at both boundaries (account for normal ignored build/test output), retaining comparison by App TREE so a central snapshot commit with the same tree remains valid. Add focused regressions without changing original journey expectations.

2. **P1 — Python path normalization discards the supplied virtual environment.** `requiredFile` at lines 61-65 returns `realpathSync(value)`. Both shared venv executable paths resolve to `/usr/bin/python3.13`. Direct prefix probes show `/home/user/work/venv-agent` and `/home/user/work/venv-runtime` become `/usr`. Lines 197-198 and 219-220 then invoke/forward that system interpreter. The standard-library vendor check may pass even though the subsequent actual journey lacks its installed dependencies. Preserve the supplied absolute executable path when invoking Python; validate existence/executability without dereferencing away its venv entry point. Add a symlinked-venv regression.

3. **Ready-only documentation/central wiring needs actual inputs.** The prep command hardcodes `/home/user/work/wt/rt-m2-pin-2c4ac180`; that path does not exist at review time. The wrapper itself correctly has no producer-path default and refuses an absent path. Replace the stale command input with an explicitly supplied retained producer path whose HEAD is exactly the published SHA. Also, `request-test` serializes target/suite/files, not caller environment; `test-run` inherits the dispatcher environment. Merely exporting final variables in the requesting worker does not supply them to the named suite. Arrange concrete exact inputs in the central executor before requesting it. Bind them into the central command/cache identity (or deliberately bypass an obsolete cached result); the current cache key does not include these environment variables. Do not guess a replacement checkout or final Agent/App revision.

## Checks that are sound, within the limits above

- All eight identity/path inputs are required; SHA syntax is full lowercase 40-character hex. Runtime SHA must be `2c4ac180c2220bdad966bc01e95ad230e99ce26a`. App root is the current absolute checkout, not an inferred external checkout.
- App snapshot identity is deliberately by TREE, not expected App commit. Agent, Runtime, and Runtime producer HEADs are checked exactly. This is compatible with a different central App snapshot commit having the same tree; no branch-head substitution is made.
- BOTH normal consumer locks must name Runtime source `2c4ac180...` and artifact version `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`. Both generated metadata files must carry schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4` and component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`; App contract version is explicitly `0.2.13`. Agent client bytes/version are covered through its normal producer-backed vendor check. Producer manifest version/count are checked against artifact6f0/75. Existing vendor checks verify selected normal consumer bytes against the committed producer manifest, rather than a shadow client.
- Both immutable Composition public12 archives must hash to `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` and have 77 unique safe package members. Independently, the App and integration Agent archives both have that hash; the App archive has 77 regular members and zero nonregular members. This does not certify installed dependencies or runtime parity.
- Preflight and postflight fingerprint metadata, lock bytes, producer manifest and archive identities. Agent/Runtime/producer cleanliness and exact HEAD checks are repeated. App working bytes remain the exception described above.
- Delegation is exactly `npm run test:e2e:three-products`, using the existing config, default hosted build freshness helper and original journey. All seven current `test(...)` bodies, including actual M1 renderer-off and M2 Gate-5 cases, are unchanged against the base. The prep prose's “six” is a stale count.
- `ASTRID_APP_DIRECT_DIST` overrides are refused. Existing global setup checks source/config/vendor timestamps and hosted origin, rebuilding stale dist with `build:hosted`; no alternate build or shadow suite was introduced. Actual stale-dist/build execution was not run.
- Child nonzero exit is retained, null status becomes failure, and postflight throws are not caught or swallowed. `finally` has no success-return override. No manufactured browser pass is present.

## Exact validation

Commands ran from `/home/user/work/wt/app-m3-current013-wrapper-independent-review` unless stated otherwise:

```sh
node --test scripts/testing/current013-integration.test.mjs
node scripts/testing/current013-integration.test.mjs
node --check scripts/testing/current013-integration.mjs
node --check scripts/testing/current013-integration.test.mjs
git diff --exit-code 0ea988bdd HEAD -- tests/e2e playwright.three-products.config.ts playwright.direct.config.ts package.json scripts/vendor-lock.mjs
```

All exit 0. The direct Node run reports **3 passed, 0 failed**; the `--test` run reports its one file passed. The diff is empty: original tests/helpers/config/package script are byte-unchanged.

```sh
node --experimental-vm-modules /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-wrapper-independent-review/review-probes.mjs
```

Exit 0, **18 review checks completed**: missing inputs, abbreviated identities, wrong Runtime release, relative/absent paths, caller dist refusal, both Python path regressions, missing App status query, absent documented producer path. The App-dirty probe substitutes only git responses, retains actual files, and ends at the real stale App-lock refusal; it never constructs a successful exact-pair/browser fixture. No subprocesses are launched by the final probe. An initial subprocess-based version exited 1 with sandbox `spawnSync git EPERM`, despite git stdout being returned; it was replaced with this subprocess-free review probe. That sandbox error is not a wrapper qualification failure.

```sh
env -u TIMELINE_CURRENT013_RUN node scripts/testing/current013-integration.mjs
```

Expected exit 1, explicitly requiring `TIMELINE_CURRENT013_RUN=1`, before any child launch.

```sh
/home/user/work/venv-agent/bin/python -I -B -c 'import sys; print(sys.executable, sys.prefix)'
/home/user/work/venv-runtime/bin/python -I -B -c 'import sys; print(sys.executable, sys.prefix)'
/usr/bin/python3.13 -I -B -c 'import sys; print(sys.executable, sys.prefix)'
sha256sum vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz /home/user/work/agent/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz
tar -tvzf vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz | awk '{total++; if (substr($1,1,1) != "-") other++} END {print "archive members=" total ", non-regular=" (other+0)}'
```

Exit 0: prefixes are the two distinct venv roots and `/usr`, respectively; archive hashes both match public12; `archive members=77, non-regular=0`.

No browser, socket, build, tsc, full suite, install, or central test request was run. Shared dependencies were read only. Current reviewed App still has Runtime lock94114269/client0.2.9, as the prep doc anticipated; there is no matching final-pair acceptance claim. Source integrity and command flow beyond the tiny probes were inspected statically, including `finally` failure propagation; no actual successful child/postflight execution is claimed.

## Deferred ready command

**Do not execute while HOLD applies.** After fixes are independently reviewed, the manager must supply the actual final App tree, Agent SHA, absolute checkout paths and existing venv executable paths. The central executor outside this sandbox may then run this exact template, with all required variables concretely supplied; it is not a worker-local browser instruction:

```sh
cd "${FINAL_APP_CHECKOUT:?supply absolute final App checkout}"
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  TIMELINE_CURRENT013_RUN=1 \
  TIMELINE_CURRENT013_APP_TREE="${FINAL_APP_TREE:?supply final App tree}" \
  TIMELINE_CURRENT013_AGENT_SHA="${FINAL_AGENT_SHA:?supply final Agent SHA}" \
  TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT="${FINAL_RUNTIME_PRODUCER_CHECKOUT:?supply retained exact producer checkout}" \
  ASTRID_CHECKOUT="${FINAL_AGENT_CHECKOUT:?supply exact Agent checkout}" \
  ASTRID_RUNTIME_CHECKOUT="${FINAL_RUNTIME_CHECKOUT:?supply exact published Runtime checkout}" \
  ASTRID_PYTHON="${FINAL_AGENT_PYTHON:?supply Agent venv executable}" \
  ASTRID_RUNTIME_PYTHON="${FINAL_RUNTIME_PYTHON:?supply Runtime venv executable}" \
  node scripts/testing/current013-integration.mjs
```

For named central suite `e2e-current013-integration`, first have the orchestrator bind the same concrete inputs in its executor/command with appropriate cache identity; an environment-prefixed `request-test` alone is insufficient. The request then remains the existing service interface:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$("$O/bin/request-test" "$FINAL_APP_WORKER" e2e-current013-integration) && "$O/bin/wait-test" "$R"
```

No ready command can truthfully contain literal final consumer identities yet. This review authorizes neither M1/Gate-5 execution nor pixels/audio parity. Recommended next step: a narrowly scoped wrapper-fix worker for findings 1-2, correct the stale ready inputs/central binding, then rerun small guard regressions and independent review before the final exact-pair central lane.
