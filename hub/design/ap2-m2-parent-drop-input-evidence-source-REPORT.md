# AP2 M2 parent drop input and evidence-source candidate

## Result

The committed positive input path is now evidence-bearing, with no product
behavior change. The mounted journey still uses the existing seeded immutable
Runtime object and normal `File`/`DataTransfer` producer path, but it now proves
the source before attempting the drop:

- Runtime object bytes have the seeded object digest, exact size, and WebM EBML
  header.
- The seed must be the normal decodable `video/webm` fixture. The harness's
  ffmpeg-generated VP8 WebM is the valid positive fixture; its explicitly
  marked non-decodable MP4 fallback is refused by this positive test rather
  than being treated as success.
- A browser `File` made from those exact bytes has the expected MIME/size and
  successfully passes the same HTML5 metadata decode used by
  `uploadVideoGeneration` before `prepareMediaImport`.
- The imported entry and original selection are checked against the immutable
  stored object's object ID, digest, size, and media type. The verified
  five-field selection equality and all existing native placement assertions
  remain intact.

No mismatch was found, so no fixture, media authority, catalog identity, or
producer behavior was fabricated or bypassed.

## Evidence capture

`tests/e2e/local/three-products.spec.ts` now records bounded, credential-free
diagnostics for the mounted case: selected request URLs/methods, response
status and safe `code`/`message` summaries, filtered console lines, and page
errors. Reopened pages are included. Secret-like keys are redacted in the
summary projection.

The candidate driver is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-drop-input-evidence-source/run-parent-manual-drop-evidence.sh`

It owns the disposable normal014 run root, copies the Playwright trace and
error context plus a bounded request/console/native-refusal summary and source
tree identity outside that root, then removes the root. It retains no App
copy. Its `probe` mode passed without starting a browser.

## Validation

Passed directly:

```text
./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts
npx tsc --noEmit --pretty false --incremental false
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts
git diff --check
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-drop-input-evidence-source/run-parent-manual-drop-evidence.sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-drop-input-evidence-source/run-parent-manual-drop-evidence.sh probe
```

Results: lint, TypeScript, diff check, shell syntax, and retention probe
passed; Playwright collection found exactly one mounted manual-drop test. No
browser, localhost/socket, central request, or full suite was run.

## Next step

After the harness commits this candidate, run exactly one central gate:

```sh
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-drop-input-evidence-source/run-parent-manual-drop-evidence.sh run "$PWD"
```

The retained evidence directory is printed by the driver. Credentials remain
private to the runner; only bounded summaries are copied.
