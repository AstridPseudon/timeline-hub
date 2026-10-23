# P3 OPS quoting correction

READY for the manager's one meaningful changed P3 service run. Only `ORCH/tests/suites.conf` row 36, `app ap2-P3-gate5-h6-0348`, changed. No App source delta; worktree remains clean at App411. KEEP is set and the P3 OPS commit message is recorded; no Git writes were performed.

The exact correction removes one obsolete backslash from each of ten doubled-backslash JavaScript quote escapes across the three preflight `node -e` commands. Bash previously consumed the unescaped quotes as shell delimiters and left literal backslashes in Node's payload. Global setup actually received argv `["--import", "tsx", "--input-type=module", "-e", "import setup from \\./tests/e2e/local/global-setup.ts\\; await setup()"]`. Its payload has no JavaScript string quotes; actual-beforeAll and trivialboot additionally split the error messages into extra argv entries. Corrected global-setup argv: `["--import", "tsx", "--input-type=module", "-e", "import setup from \"./tests/e2e/local/global-setup.ts\"; await setup()"]`. Each corrected preflight now has exactly one complete `-e` argument. Full old/new actual Bash-parsed argv for all five embedded Node commands is retained in `/tmp/w-f896c740fc/{before,after}-syntax.json`.

Diagnostics replace the three stage `/dev/null` redirections with private `global-setup.log`, `actual-beforeAll.log`, and `trivialboot.log`; selector output is also retained as `selector-collection.log`. Each real run creates a distinct mode-0700 directory under this worker's `p3-preflight.XXXXXX` and prints only its path to stderr. No environment or credential dump was added. Normal globalSetup/build-before-nativeboot ordering and failure gates remain unchanged.

Commands and results:

- `python /tmp/w-f896c740fc/p3_ops.py` — exit 0. Captured the real outer Bash `-c` argument using a private stub, then used Bash and a harmless Node stub for actual argv extraction. Pinned Node v20.19.4 `--check --input-type=module` on stdin: old three preflight payloads correctly refused (exit 1 each), old two tail payloads passed, corrected five payloads passed (exit 0 each). No imports or setup execution. Applied the one-row edit only after checks passed.
- `bash -n /tmp/w-f896c740fc/p3-row.sh` — exit 0, PASS, repeated after edit.
- `bash /tmp/w-f896c740fc/p3-static.sh` — exit 0, PASS, repeated after edit. Exact extracted current P3 prefix with real receipts, source/tree/body/toolchain/import-metadata guards, stopping before diagnostic creation/global setup.
- `python /tmp/w-f896c740fc/p3_finish.py` — exit 0. Four harmless stage-failure injections each returned exit 2, retained causal stderr in its stage log, and reported original-body-NOTRUN. Verified 48 literal hash guards, real identities, clean repositories, byte-identical post-preflight tail, and byte-identical outside-row content.
- `/home/user/work/runtimes/agent-remotion-ap2-current-8c-cfa-1415/.toolchain/node-v20.19.4-linux-x64/bin/node --version` — v20.19.4, exit 0. `git diff --stat` and `git status --short` — empty.

Identities and hashes:

- App: `411ff10bd7043d55b4d83f2dfbbbd841af7b4806` / tree `0b19a5a9e33165b5fabe7d0425ae755aa58adfa2`, clean.
- Agent: `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe` / tree `c4d72b065d6e68c92e4335120cc016cadf53b06a`, clean.
- Runtime: `cfa0af0d476e6954df041c08d7ef378fd6782932` / tree `3675f446c82c455ef5635ae725409eb6076a4f83`, clean.
- Original Gate5 body blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`; SHA-256 `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`.
- P3 row before `aff4a679ca9e4a125826102465fb2c5248f0e64baff5bc6cb1a3a416c5df598d`; after `53118de6a2a88b3d21496f47049b01bb188870c253cc990b2defda265b021d7d` (SHA-256 including newline).
- Outside the one row, before = after: `c4f2ea9a2941f575dbd6961e664458aaa518150b7a4386eb08ccca287df53c1e`.
- Entire post-preflight tail, before = after: `0ac582bcd3d248e7cde1c666f56837ea5bab0e63315b4b1f235eb0aad1594768`. Every selector, source/body/receipt/identity/metadata/lock guard is preserved; P1/P2 rows are byte-identical.
- Prior32246 failure log remains `193aa6cdc83fdf59e71d5a884c039cb676249b4fa429619243312e4a012e48c6` and retains its original global-setup FAIL. It is not reclassified.

Actual child `venv-agent-child-ap2-current-8c-cfa-1415` and Remotion `agent-remotion-ap2-current-8c-cfa-1415` receipts and installed identities pass the existing static predicates. Original 1410/1417 list1/typedsource evidence is reused; no collection/typecheck rerun or broader proof claim.

No blocker. Decision: correct only demonstrated shell escaping and retain stage output privately; no test-body/helper fix, toolchain/dependency change, or guard relaxation. No hosted build, globalSetup execution, HTTP, nativeboot, browser, body, service, full suite, P1/P4/corpus/native14, provisioning, or shared dependency mutation occurred. Runtime vendor-lock semantics and later executable guards were preserved but not executed. Syntax/static success is not live Gate5 qualification. Manager owns the next serialized changed P3 service; any later TEST-helper issue remains Sol1424's separate scope.
