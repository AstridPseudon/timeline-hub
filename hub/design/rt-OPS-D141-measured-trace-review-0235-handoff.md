# OPS D141 measured-trace handoff

## Disposition

**FAIL / hold.** Do not install the candidate, attach a receipt, or submit the targeted15/P5 bodies from this source. The first proved seam is the exact full-ID mismatch in the production caller. The P5 exact-full-ID binding is a second blocking mismatch.

The independent review did not edit source, queue, registry, kit, product/test files, pins, environments or generated files.

## Required correction and re-review

1. Correct or independently prove the held/cancelled guards against these exact full IDs through the normal caller:

   - `rt-pin-fa9cd546-full-d141-pristine-1026005231-8912`
   - `agent-p4-current-becfe-http-3legs-1026012948-19479`

   Both must fail closed without reissue, suffix matching, direct `--run`, environment bypass or alternate body.

2. Bind P5 to exactly `runtime-d141-p5-cut-1026013331-6934`, never bare `6934` and never an arbitrary name ending in `6934`. Re-run receipt validation and the normal dispatcher path with the existing request ID.

3. Re-run this independent full-ID subprocess review and preserve the separate Luna0247 targeted-row fail-closed review; do not combine or duplicate that finding here.

## Exact supported targeted15 route

The corrected supported suite name is:

`full-d141-pristine-targeted15`

The source-prep shorthand `full-d141-targeted15` is not the kit allowlist name. The exact target is Runtime worker `rt-pin-fa9cd546`, Runtime `fa9cd5464a8b37b02f971de375e56be846cd69e2` / tree `124e10dbcd54fb90219e783ec11aa34f8c91590c`, with Agent `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` / tree `0a3691a49b63fd7b0c22fb3478e9cf1947f266ed`.

## Next normal commands (only after independent correction review and CAS)

```sh
# Install exactly one disjoint row through the reviewed CAS installer.
# Preserve old full-d141-pristine, queued 8912, P5 6934, and all outside bytes.
D141_RESULT=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-pin-fa9cd546 full-d141-pristine-targeted15 --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$D141_RESULT"
```

The returned request ID must remain bound through terminal state, with source/origin/argv/XML/disk trace/runner-exit/KEEP retained. Do not use `--run`, an environment bypass, queue edits, a reissue, or the old 8912 request.

## CAS/install manifest to preserve

From the reviewed targeted15 return: registry preimage `0e8e74b787633867a8d5d7cbbc59d2fb0928431419563eaa594693823c839081` (156690 bytes); retain old `full-d141-pristine` row hash `c12d0642b9f57ed008cc042b296b5432d5b88c3edccc5bbb63c9281c67b59f99`; append one row hash `c58378a2036cca8d188447fd49abdd1b0b3be5765d9a252485b4f784b865314e`; expected postimage `7b1ffdd7225ad9db6a21dd3f2ced1ae7aa3335249ae9994f529aec6d15fd98df`; outside-row hash `33890fb74b6dde004fd8767e853be38f06bd872b4d829cc85667800fa7942e07`.

The P5 row/request remains the exact existing `runtime-d141-p5-cut-1026013331-6934` and must not be duplicated or generalized.
