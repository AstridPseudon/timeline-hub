# ap2-m2 ordinary structural batch review

Source verdict: **REQUEST CHANGES** for real-project type qualification. The
compound behavior is correct, and the current six-command TS→Agent parity
artifact passes records, bundle, replay, and guarded inverse, but
`tsconfig.app.json` reports new partial-row projection type errors at
`genericPatchCapture.ts:574,577` and `ordinaryStructuralMember.ts:438,441`.

Current adoption: **HOLD**. `tl/integration` and
`tl/ap2-m2-ordinary-members-current-forward` are both `f30187d7f`; the
candidate is three commits ahead and its HEAD commit is limited to the two
generic files plus the two structural files. No old App sections are touched
by that commit. Adoption waits for the type repair and current-pair
qualification.

Evidence: configured cache-free Vitest **8 files / 177 passed** (the two
changed files alone **16 passed**); ESLint **PASS**; strict-island project
typecheck **PASS**; `tsconfig.app.json` project typecheck **FAIL** as above;
`git diff --check` **PASS**. Native Agent parity with explicit
`/home/user/work/venv-app2-native/bin/python` and asserted current Agent
imports **PASS** for six commands, six records, replay, bundle equality, and
guarded inverse. Artifact:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-ordinary-structural-compose-native-parity.json`.

No source, test, shared dependency, pin, Git, ledger, full, browser, socket,
or Runtime-door changes were made or run. Recommended next step: repair the
strict structural projection row types, rerun `tsconfig.app.json`, then repeat
current-pair adoption qualification.
