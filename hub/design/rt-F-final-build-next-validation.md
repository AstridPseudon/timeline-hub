# F-final validation

Status: BLOCKED at the sole authorized service startup. No product source was changed.

Preflight PASS:

- Final source tuple, gate tuple, four heads/trees, accepted caller, lifecycle helper, D68 wrapper, and builder hashes were read back.
- All 11 accepted installed candidate files matched their recorded SHA256 digests and modes.
- Pre-dispatch available space was 5,148,094,464 bytes; the durable five-sample trace recorded a minimum of 5,149,528,064 bytes, above the 4,000,000,000-byte stop line.
- Request directory was protected at creation by `TEST_KEEP='F-final actual delivery original raw and continuous trace'`.

Actual service:

- Command: `request-test integration:runtime delivery-v2-final --no-cache`
- Service: `runtime-delivery-v2-final-1026171722-10589`
- Result: exit 1; `wait-test` exit 1.
- Failure: the registered Python launcher executed the accepted `run-final-delivery.py`, which failed at line 23 importing `delivery_lifecycle`.
- The delivery builder was not invoked, so no staging, patch, bundle, ZIP, ZIP hash, per-repository applied-patch result, or archive inspection exists.
- No retry, direct run, alias, route change, registry change, or alternate build was attempted.

Not run because the caller failed before the body:

- lifecycle process-group stop/source-descendant reap and durable service trace;
- four-repository patch/tree/bundle equality;
- checksum/manifest/archive checks and secret scan;
- product typecheck, lint, or tests.

Raw service evidence remains at the normal test-service paths in `request-receipt.json`.
