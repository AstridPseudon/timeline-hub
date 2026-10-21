# Parent central keeper command preflight 0508

## Result

The final central source-only preflight passed. The owned gate admits the
central service snapshot by tree only, requires the protected original keeper
by exact HEAD/tree and clean status, binds the approved helper and existing
0323 driver hashes, runs the existing source-only preflight, checks the four
requested refusals, and lists exactly one parent test.

No assertion, product source, shared helper, existing driver, or live caller
was changed. The App worktree is clean.

## Exact registered commands

The new literal suite entries are:

```text
app ap2-m2-parent-central-keeper-command-preflight-0508-preflight /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh preflight
app ap2-m2-parent-central-keeper-command-preflight-0508-actual /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh run
```

The exact central request and wait commands used for the final evidence were:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-central-keeper-command-preflight-0508 ap2-m2-parent-central-keeper-command-preflight-0508-preflight --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-parent-central-keeper-command-preflight-0508-ap2-m2-parent-central-keeper-command-preflight-0508-preflight-1021051417-15272
```

Final result: `PASS`, exit `0`, 8 seconds, central captured tree
`a3c82aa91f1336b86491191acf857d88c56179b2`.

The gate's source-only invocation was:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  NORMAL014_USE_BASE_PYTHON=1 NORMAL014_RUN_ROOT="$RUN_ROOT" TMPDIR="$TMP_ROOT" \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh \
  preflight /home/user/work/wt/ap2-m2-parent-complete-current-proof-source-0455
```

The exact one-test list command was:

```sh
cd /home/user/work/wt/ap2-m2-parent-complete-current-proof-source-0455
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR="$LIST_TMP" \
  node node_modules/playwright/cli.js test \
  --config playwright.three-products.config.ts \
  --grep 'M2 real mounted manual video drop' --list
```

It reported `Total: 1 test in 1 file` and
`three-products.spec.ts:1440`.

The separately registered actual command was not run:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh run
```

That preserves the existing driver invocation as `run APP_ROOT`; no browser,
hosted build, mounted actual, or full suite ran.

## Source, cohort, and evidence tuple

- Protected source keeper: `/home/user/work/wt/ap2-m2-parent-complete-current-proof-source-0455`
- App HEAD/tree: `a304dce02a185a4774ff514d5aa451c9702aa46f` /
  `a3c82aa91f1336b86491191acf857d88c56179b2`; clean
- Profile/role: `final95` / `parent`
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
- Runtime and producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`
- Artifact: `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`
- Manifest: `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, 76 artifacts
- Schema: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- Wire: `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`
- Private graph archive: `sha256:895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- Composition archive: `sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Helper: `normal014-source-common.sh`, SHA-256
  `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`
- Existing driver: `run-parent-manual-drop-evidence.sh`, SHA-256
  `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`
- Owned evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/preflight`

Evidence records:

- source preflight: passed; `verified artifacts=76`, expected manifest/schema,
  d05e marker, imports, collection, graph, and shell guards
- wrong captured tree: refused
- wrong keeper: refused
- wrong helper hash: refused
- wrong argv: refused with the existing driver's usage failure
- list: passed with exactly one collected case

## Decisions and corrections

The central service's synthetic commit SHA was intentionally not compared to
the keeper SHA; only its captured tree was required to equal `a3c82…`. The
original keeper path was passed to the existing driver root argument.

The task text's abbreviated driver value was verified against the approved
0501 record and corrected to the full 64-character hash ending in `3867f0`.
The first gate run also exposed shell expected-failure functions that could
continue after a failed `test`; those functions now return failure atomically.
Neither correction changes product behavior or the existing driver.

No blockers remain. The actual/browser command remains registered but
intentionally unverified pending the separately authorized final independent
review.
