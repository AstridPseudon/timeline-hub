# AP2 M2 selected failure retention — owned runner 0903

## Result

Copied the immutable 0858 selected runner into the owned durable artifact
directory and changed only that runner's output, retention, and EXIT cleanup:

```text
runner: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-failure-retention-owned-0903/artifacts/run-owned-selected-final95.sh
KEEP:   /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-failure-retention-owned-0903/artifacts/KEEP
0858 source SHA-256: b3fb1336b36bd3703e3fc460ca9fe0932e9601b39c721215e07c5ca35bf535e5
owned runner SHA-256: 4459f2c9acd7ce411f92beab33c216e549c98fe1fad996706998e6c5aaab85a3
```

The 0858 source remains byte-identical and immutable. No App source/spec,
harness, selector, budget, authority, pin, source helper, or launcher was
changed. The selected case was not executed.

## Actual path traced

The existing run path is:

```text
run-owned-selected-final95.sh MODE=run
  -> source-common.sh read-only source/graph preparation
  -> run_actual
  -> APP_OVERLAY private copy
  -> PLAYWRIGHT_OUTPUT_DIR=$RUN_ROOT/browser-output
  -> npm run build:hosted
  -> flock ... npm run test:e2e:three-products -- --grep "$TEST_TITLE"
  -> runner EXIT trap
  -> rm -rf "$RUN_ROOT"
```

`playwright.three-products.config.ts` consumes `PLAYWRIGHT_OUTPUT_DIR` as its
`outputDir`; the selected test's `three-products-summary.json` is written
beside Playwright output by the test's `afterAll`. The previous EXIT trap
deleted this complete root without retaining the child log or Playwright
failure artifacts.

The owned runner now redirects only the existing child command's stdout/stderr
to `$RUN_ROOT/selected-child.log`, retains before cleanup on nonzero status,
and then removes the disposable root. Retention copies only:

```text
child.log
browser-output/dom.html       (from dom.html, dom-snapshot.html, or *.html)
browser-output/error-context.md
browser-output/trace.zip
identity.txt
SHA256SUMS
```

It never copies the overlay, caches, runtime data, source checkouts,
credentials, environment dumps, summaries, or the rest of the run tree. The
run root is passed to retention as `realpath "$RUN_ROOT"`; the durable root is
resolved physically and must be outside it. Existing 0822 physical-root,
bounded-copy, identity, and SHA-manifest patterns were reused where they fit;
the 0822 ordinary helper was not called because it copies the whole browser
output tree and requires an ordinary-mode contract, which would violate this
selected allowlist.

Failed child status is preserved. A retention failure is visible and changes
the outer result to status 1. An empty browser-output directory is treated as
startup `PREBODY`: available child log, identity, and SHA manifest survive,
and identity explicitly records `trace_retained=false`. Nonempty browser
output requires DOM, error-context, and trace; missing output or a destination
collision refuses visibly.

## Bounded real run-mode seam

The real selected `MODE=run` path was invoked with the existing
`SELECTED_FINAL95_LAUNCH_STUB` seam and `NORMAL014_USE_BASE_PYTHON=1` to avoid
installation. The stub was the only child; it planted representative DOM,
error-context, and trace files under the runner-exported Playwright output
directory, then exited 17. No browser, build, daemon, socket, install,
actual selected test, full suite, or central service was run.

Observed result:

```text
child/outer status: 17 / 17
child invocation count: 1
phase: BODY
retained: DOM, error-context, trace, child.log, identity.txt, SHA256SUMS
SHA256SUMS verification: PASS
temporary RUN_ROOT after EXIT cleanup: absent
```

Additional controls through the same real run-mode seam:

```text
PREBODY startup stub: status 19 preserved; identity/SHA/log retained; no trace claimed
nonempty missing-output stub: visible trace-missing refusal; outer status 1
pre-existing durable destination: visible destination refusal; outer status 1
success stub: status 0; durable evidence absent; temporary root removed
```

## Exact checks

All passed:

```sh
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-failure-retention-owned-0903/artifacts/run-owned-selected-final95.sh
```

The central handoff command was syntax-checked without submitting it:

```sh
APP_KEEPER_ROOT="$PROTECTED_APP_KEEPER" SELECTED_FINAL95_MODE=run "$RUNNER" "$SERVICE_CAPTURED_APP_ROOT"
```

The immutable 0858 source hash was rechecked as `b3fb1336…`. Reversing the
complete owned diff reproduced the old source exactly:

```text
reverse SHA-256: b3fb1336b36bd3703e3fc460ca9fe0932e9601b39c721215e07c5ca35bf535e5
old SHA-256:     b3fb1336b36bd3703e3fc460ca9fe0932e9601b39c721215e07c5ca35bf535e5
```

The run-mode guard path also passed the existing exact custody checks,
including parent helper SHA `96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109`,
selected App `a50ca4a0172cce9c73ce3c040290bf9479098b0f` / tree
`92391f9a57dd38ce327b0a63990725053ea34601`, selected spec SHA
`10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1`,
final95 76-artifact manifest, locked Composition 0.0.13 graph, Node/Vite/
Vitest/Playwright versions, exact list1, argv/title, zero-test refusal,
short physical paths, credential-file/origin guards, and cleanup controls.

## Handoff

Independent process-custody review should inspect the owned runner artifact and
the bounded controls above. No selected actual run was registered or executed
by this worker. The repo worktree itself is unchanged; the harness may commit
the empty worktree contribution if required by orchestration.
