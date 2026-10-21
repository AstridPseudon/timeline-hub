# AP2-M2 parent newborn current proof source

## Result

Composed one frozen parent proof source on current `hub/tl/integration`.
The source is the current integration tree plus the exact reviewed parent
spec/body from `tl/ap2-m2-parent404-door-body-exact-correction-0604`; no HOME
service was reimplemented and no actual was run.

HOME's reviewed newborn hold fix is already present through merged
`6bdb7dfadb5218d00cb04db45f67468609b0a1c6` / tree
`4ee81f8a438a60bd470ded1462f47b21d7552ba6` (source
`0a3b3eb790db4cd4754af9aa03adb9dc1b94bed7`). The accepted newborn row gains
only detached `hold = to - from`; the raw generated row remains unchanged.
HOME's independent r2 review is APPROVE with 134 targeted tests and the
meaningful regression green.

## Source delta and identity

Only `tests/e2e/local/three-products.spec.ts` changed. The later relaxed
wrong-selection assertion was restored to the reviewed strict contract:

```ts
expect(wrongVerified.status()).toBe(404);
await expect(wrongVerified.json()).resolves.toEqual({
  code: 'not_found',
  message: 'selected media is not a managed project generation/variant/object',
  request_id: expect.stringMatching(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$/),
});
```

This preserves the full reviewed parent body: import/selection/verified
reads, strict 404 body and request ID, native `clip.add-media`, V1/at
placement, raw/opaque/order checks, no `afterClipId`/`removeClipId`/
`replaceClipId`, lost ACK, exact retry body/key, reload, Runtime restart,
undo, and zero legacy traffic. SWAP and after-anchor paths remain dormant.

Hashes:

```text
HEAD before edit:       0c9b7bf01a694856a4a5e75a46161b115c600763
HEAD tree before edit:  424aa4d9a923e43b18f1425c27d4b9193f603a7d
spec before edit:       56560d53aecf1d1ad2fce737e3955b20d35792bde3115da6f0df51913bc87bb5
reviewed 0604 spec:     5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603
candidate spec:         5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603
candidate whole tree:   00bce13c888dda845b69a944c71aae7142e2e21e
```

The candidate spec is byte-identical to the reviewed 0604 spec. No live
caller changed. The existing callers remain `commitSession.ts` and
`useTimelineCommandSession.ts`; the HOME-owned service carrier is present
only through the already-merged integration ancestry.

## Cheap complete preflight

Executed read-only, with no build, browser, daemon, localhost/live socket,
install, full suite, or actual. The exact list command collected one test:

```sh
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=/tmp \
  node node_modules/playwright/cli.js test \
  --config playwright.three-products.config.ts \
  --grep 'M2 real mounted manual video drop' --list
```

Result: `three-products.spec.ts:1440:1`, `Total: 1 test in 1 file`.

Preflight results:

- ancestry `5d36b0e5`, `968bbad0`, and HOME `6bdb7df` — PASS;
- current pin014/Agent6ef/Runtime95/all76/Composition13 checksum 9412/all77 — PASS;
- exact normal Node/Vite graph — PASS (`node v22.22.0`, Vite `5.4.21`,
  Playwright `1.60.0`, shared graph resolves to `/home/user/work/app/node_modules`);
- helper role `final95:parent` — PASS as a closed role, but its source tuple
  is stale for this candidate (see proposal below);
- final argv/config/list1, short child paths, and shell guards — PASS;
- local browser lock — PASS, nonblocking and idle;
- disk — PASS, `14,404,588 KiB` available on `/tmp` (above 10 GiB);
- private copies — PASS, zero created;
- admission/discovery/credential FILE static guards — PASS; the existing
  `WORKSPACE_RUNTIME_TOKEN_FILE`, discovery `worker_credential_file`, and
  runtime discovery proxy paths remain in place.

Aggregated failures, once:

1. Candidate worktree is intentionally dirty with the one source edit; the
   harness must commit it.
2. The read-only shared helper still binds `final95:parent` to
   `acb582c2c3b08481d43853b8526894ac60d074bc` / tree
   `141724b56736be40a269f60aa8bfc060914ebd29`, not the candidate tree.

## Source/test-role custody proposal — not applied

The shared helper was not mutated. Its current whole-file SHA-256 is
`d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848`.
After the exact two-line replacement below, the prospective whole-file SHA-256
is `c23a6b8d64f38ca5f020ba506b03e019465bd03d9cc4d3b1099cd9d15b324f1c`:

```diff
-APP_ROOT_SHA=acb582c2c3b08481d43853b8526894ac60d074bc
-APP_ROOT_TREE=141724b56736be40a269f60aa8bfc060914ebd29
+APP_ROOT_SHA=0c9b7bf01a694856a4a5e75a46161b115c600763
+APP_ROOT_TREE=00bce13c888dda845b69a944c71aae7142e2e21e
```

This uses the immutable current HEAD as the source ancestor and the exact
candidate tree; the harness's final commit SHA was not available before exit.
The delegated updater must refuse a collision unless the helper hash is
exactly the old hash above, then verify the new hash, source ancestry, and
candidate tree. No other helper line, role, pin, guard, or live caller may
change. The final committed SHA/tree should be recorded by the dispatcher when
the harness commit becomes available.

The existing eventual actual command remains, unexecuted here:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh run "$PWD"
```

## Verification boundary

No browser or actual result is claimed. The earlier actual11497 failure remains
the pre-HOME-fix failure before outbox submission because the generated video
lacked hold. This worker made no product/service change beyond restoring the
reviewed proof source assertion and did not claim parent success or writer
deletion.
