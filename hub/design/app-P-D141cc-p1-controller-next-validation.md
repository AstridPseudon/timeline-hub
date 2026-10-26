# D141cc P1 controller validation

- Original JSON: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141cc-submit-owner-sol-1047/evidence/dispatch-recipes.json`; loaded `dispatches[5]` (`p1`, `original`) programmatically.
- Recipe SHA-256: `d665c4907abd063edc9da0f29c887b56f7b66fb80febbe52f14732ea66e95d0d`. Builder SHA-256/blob: `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f` / `59b65214bc74c1ca118b097bc3b13c0ffe480a93`.
- Read-only custody command: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141cc-submit-owner-sol-1047/evidence/candidate/controller.py p1 --owner-state not-started` → `FIRST_NATIVE_INVOCATION_ONLY` immediately before the one native invocation.
- Native invocation: exact JSON `argv`/`cwd`/recipe environment loaded from `dispatches[5]`; inherited `TEST_KEEP=D141hh p1`; one retained native session `9556` → exit `0`.
- Native artifact: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141cc-submit-owner-sol-1047/evidence/future-native/full-d141-p1-82e9e13d-submit/submit-plan.json`; authentic preflight `app-pin-82e9e13d-full-d141-p1-82e9e13d-submit-preflight-1026121110-31121` and normal `app-pin-82e9e13d-full-d141-p1-82e9e13d-submit-1026121140-32161`. Both raw `KEEP` files existed at first observation.
- Same-ID service wait: artifact-derived `wait-test app-pin-82e9e13d-full-d141-p1-82e9e13d-submit-1026121140-32161` → `pass exit=0 in 200s`.
- Service evidence: preflight `pass/0`, `trace PASS: 3 actual samples`; normal `pass/0`, `trace PASS: 42 actual samples`; readiness plus both P1 chain tests passed.
- Sampler: foreground 5-second session `73741`, `64` samples, minimum available `4855148544` bytes; no 4GB stop. Explicit SIGINT, wait, and reap completed (reap exit 1 from SIGINT); no backfill.
- No local suite/typecheck/lint/browser run; no product/test/generated/pin/registry/queue source edit.
