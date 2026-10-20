# current013 wrapper final independent review

**Verdict: APPROVE — repaired wrapper source only.** The two blocking source defects in the prior HOLD are repaired. Exact-pair browser/Gate-5 qualification remains pending actual final Agent publication and manager-owned central binding. No code edits, project decision changes, or successful cross-product proof are claimed.

## Exact reviewed source

- App worktree: `/home/user/work/wt/app-m3-current013-wrapper-final-review`.
- HEAD: `cee35da4b1ed653db50dd9d5c26693fab00f04ad`.
- TREE: `2b304de3a92faa011b289cd99859c5e43c57e8fe`, matching the repair report's calculated tree.
- Base: `171a259acbeb3ced855ca8f72fed0943a2f5a5cb` (approved normal013 root).
- Diff: exactly two added files, 465 lines: `scripts/testing/current013-integration.mjs` (240) and `scripts/testing/current013-integration.test.mjs` (225). All other base bytes are unchanged.
- Wrapper SHA-256: `82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901`.
- Test SHA-256: `d0196c5ae92f8164996229d0b17c21ad2b199eaef222b7b148e2549461fd93e8`.

Read PLAN.md, `design/app-current013-wrapper-independent-review.md` (HOLD), `design/app-current013-wrapper-fix-compose.md`, updated browser-gate preparation, both complete wrapper files, unchanged normal vendor/build helpers and central request/execution source. These design paths are under ORCH. No settled decision is disputed.

## Findings

1. **App source cleanliness repaired.** Wrapper lines 114–116 use porcelain status covering tracked, staged and untracked source; line 189 adds App to the same check as Agent/Runtime/producer. The launcher invokes the full source check before delegation and in `finally` afterward (217, 232). Normal ignored outputs remain allowed. Tests cover modified, staged and untracked App refusal before delegation, postflight mutation, and two status queries. The ignored-output control mocks Git's clean response; a separate real `git check-ignore` confirms `dist/current013-smoke` is ignored without creating it. Actual review worktree tracked/staged/untracked status was empty at both start and end.
2. **Central snapshot compatibility retained.** App root and `HEAD^{tree}` are checked (181–182); App commit equality is intentionally absent. The launcher control accepts a different App commit with the same TREE. Other three checkout HEADs remain exact, including the producer. No actual snapshot/browser was created in this review.
3. **Python venv identity repaired.** `requiredExecutable` (61–68) requires an absolute existing executable file and returns the supplied path, without realpath dereferencing. Directory normalization remains unchanged. Both vendor invocation and journey environment use that path (202, 223–224). The focused test creates two private symlinked venvs and invokes each to assert its actual `sys.prefix`; independent shared-venv read-only probes also preserve both prefixes.
4. **Failures remain failures.** Child status 7 is preserved; null status becomes 1. A thrown child launch still propagates through `finally`. Postflight check/fingerprint exceptions escape, including after a failing child; no return or catch converts them to success (228–236). Focused controls cover child 7/null, postflight dirty source after child success, metadata failure after child 7, and changed fingerprint bytes with unchanged metadata fields.
5. **Exact normal guards retained.** The wrapper's diff against the prior reviewed wrapper changes only executable validation/path preservation, App cleanliness, and exporting the existing launcher for unit controls. Both normal consumer locks still require Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` and artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`. Both generated metadata checks require schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4` and component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`; App contract is explicitly 0.2.13. Producer manifest version and 75-entry count remain required. The existing producer-backed App/Agent vendor checks remain mandatory at both boundaries, covering selected normal client bytes. This review did not execute a successful paired vendor check or certify a final Agent pin.
6. **Public12 guards retained.** Both consumer archives require SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 unique safe package members. The actual App archive independently matches and has 77 regular members, zero nonregular. Immutable hash equality anchors the member-type claim; the wrapper's listing itself does not inspect tar entry types. No installed-package or pixel/audio parity claim follows.
7. **No fabricated paired proof.** Test fixtures deliberately provide synthetic identities/locks/metadata/75 placeholder manifest entries, copy the actual public12 archive, substitute Git and vendor/browser child results, and assert launcher controls. Their comments explicitly limit their purpose. Their success logs are mocked launcher output, not a browser result. Private fixtures are cleaned. The original seven journey bodies, helpers, configs, package script and vendor checker are byte-unchanged from the previous review and base. Delegation remains exactly `npm run test:e2e:three-products`; caller dist overrides still refuse and the original hosted freshness helper remains authoritative.

## Exact validation

Commands ran from the reviewed App worktree. `O` denotes `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.

```sh
node --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs
node --experimental-vm-modules "$O/workers/app-m3-current013-wrapper-final-review/notes/review-probes.mjs"
```

Both exit 0: **15 passed / 0 failed / 0 skipped**, and **18 review checks completed**, respectively. The retained repair review probe was copied to this worker's notes with only its two worktree-path occurrences redirected. All 18 assertions are unchanged; the original independent and repair probe files were not modified. Retained repair probe SHA-256 is `f507508847f9086407318af96a00e5a322b2ff24dcbf20c14f972730e26db2b4`; redirected copy is `69ec9323cb3c4247fdc3174d08f07ceaf48ce50fb80aa4cc54d0b5ab162c2be3`. It launches no subprocess and stops the dirty-App probe before lock/vendor/browser execution.

```sh
node --check scripts/testing/current013-integration.mjs
node --check scripts/testing/current013-integration.test.mjs
git diff --exit-code 171a259acbeb3ced855ca8f72fed0943a2f5a5cb HEAD -- . ':!scripts/testing/current013-integration.mjs' ':!scripts/testing/current013-integration.test.mjs'
git diff --exit-code ba8ae7228b460b0188170276e6711725d45c352c HEAD -- tests/e2e playwright.three-products.config.ts playwright.direct.config.ts package.json scripts/vendor-lock.mjs
git diff --check
git diff --exit-code
git diff --cached --exit-code
git ls-files --others --exclude-standard
git status --porcelain=v1 --untracked-files=all
git check-ignore --no-index dist/current013-smoke
```

All exit 0. Diffs and tracked/staged/untracked lists are empty; check-ignore prints the expected ignored path. One exploratory `rg` used an absent `helpers*` path and exited 2 after successful syntax/diff checks; the corrected search used `tests/e2e/local/support/astrid.ts` and exited 0. It was not a test failure.

```sh
/home/user/work/venv-agent/bin/python -I -B -c 'import sys; print(sys.executable, sys.prefix)'
/home/user/work/venv-runtime/bin/python -I -B -c 'import sys; print(sys.executable, sys.prefix)'
sha256sum scripts/testing/current013-integration.mjs scripts/testing/current013-integration.test.mjs vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
tar -tvzf vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz | awk '{total++; if (substr($1,1,1) != "-") other++} END {print "archive members=" total ", non-regular=" (other+0)}'
env -u TIMELINE_CURRENT013_RUN node scripts/testing/current013-integration.mjs
```

Prefix/hash/archive commands exit 0: prefixes `/home/user/work/venv-agent` and `/home/user/work/venv-runtime`; hashes as above; `archive members=77, non-regular=0`. The last command intentionally exits 1 requiring explicit manager input before child launch.

## Central binding and remaining limits

Verified directly: `bin/request-test` serializes target/repo/suite/files/nocache, not requester environment. `bin/test-run` selects the registered complete command, keys cache by repo + App TREE + suite + files + command (plus cross-product integration refs), then runs it in its own App snapshot. The existing `e2e-current013-integration` suite is still an incomplete placeholder and must not be used as qualification. Changing requester exports or dispatcher environment does not establish the exact pair/cache identity.

The repair report's future recipe is appropriate: after actual matching Agent publication, the manager registers ONE new named command with the literal full actual Agent SHA, verified final App TREE, retained absolute Agent/Runtime/producer paths, executable venv paths and private cache/output paths. The producer path must exist and both Runtime and producer HEADs must be exactly `2c4ac180c2220bdad966bc01e95ad230e99ce26a`; no moving-main default or previously absent hardcoded checkout is accepted. The new complete literal command and name establish a fresh cache identity. The central snapshot stays the App cwd. Confirm TREE `2b304de3a92faa011b289cd99859c5e43c57e8fe` only if no source changes intervene. Request only that newly bound suite through the existing service.

The documentation correctly distinguishes npm cache configuration from Vite cache placement. Manager must ensure the unchanged normal runner's tool/config caches remain private and shared dependencies remain read-only before the eventual central execution. No central bins, suite registrations or dependencies were changed here.

No actual browser, build, localhost/socket, full suite, tsc, install, central request, pixel/audio proof or final-pair acceptance was run. Shared node_modules, caches, venvs and runtimes were read only. No build/temp output was left in the App worktree. No local review blocker remains; actual matching Agent identity, retained producer checkout and central qualification are future manager work, not approval implied by this report.
