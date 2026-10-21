# App pack-host failure payload preservation — 0344

## Result

Implemented the bounded App harness fix on exact App base `909d2bfa186985db9791be0ab090b9f4e7824f9b` (tree `79728118ec633070581beff0e283fdff1a74f2d2`). A valid helper `status:"failed"` line now preserves only the immutable helper's existing `error_type` and `error_location` values through the existing startup error. If cleanup also fails, the existing `pack-host startup cleanup failed` suffix remains separate and the original safe cause is retained. Unknown JSON fields, stderr, raw exception text, and planted secret text are not read or exposed.

## Exact patch

- Patch SHA-256: `c1a71bf0a217e7390f79705f4166b8bf82d2730a3b0830571778742ccddd1cc0`
- Patch bytes: `5885`
- Files changed:
  - `tests/e2e/timeline/viewing-parity/bootstrap.ts`
  - `tests/e2e/timeline/viewing-parity/harness.test.ts`
- Diff check: passed.

The immutable helper used by the stub test is b70 commit `b70b9d569b2c80885d72734c61cd57e64c3715a8`, tree `687f077c4771e3dbb66bfb7ff2b98f310ac054b6`, helper SHA-256 `bc75d73f21c6310efad7fc41e4a3d790bfe3a8975e0eb96c08c3dec63e62961b`.

## Tests

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/timeline/viewing-parity/bootstrap.ts tests/e2e/timeline/viewing-parity/harness.test.ts` — passed.
- `env ASTRID_CHECKOUT="$PWD" ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_PYTHON=/usr/bin/python ASTRID_PACK_HOST_HELPER_CHECKOUT=/home/user/work/wt/agt-pin-b70b9d56 node --import tsx tests/e2e/timeline/viewing-parity/harness.test.ts` — passed, 10 tests, 0 failures.

The new stub sends `error_type`, `error_location`, an unknown `secret`, and secret-bearing stderr, then makes cleanup exit unsuccessfully. The assertion confirms both safe fields and the cleanup suffix, and confirms the planted secret is absent.

No Runtime/host/browser, localhost/socket, rendering/export, token/grant/marker, physical rerun, full suite, or central live suite was run. Historical case28523 remains pre-Chrome and unqualified; this patch does not recover or reinterpret it. No release14 ordering or pin claim is made.

## Review status

Not blocked. Recommended next step: independent custody review of this two-file patch, followed by the App owner light gate. Any future physical run remains separately authorized work.
