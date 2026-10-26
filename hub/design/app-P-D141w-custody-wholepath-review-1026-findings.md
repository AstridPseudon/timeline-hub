# Findings

## 1. Source and placement authentication

The retained source tuple is exact and clean: App `82e9e13d`, Agent `ecdc242e`, Runtime `95d98f03`, Composition `635f4de0`; the base Composition is `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`. The reviewed builder is `/home/user/work/app/scripts/testing/d66-plain-stack.mjs`, blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, 49,914 bytes.

The retained registry rows 417–420 are the exact `full-d141` preflight/normal pairs for placement and popup ADD. The placement submit plan, actual request, snap, manifest, status, and exit all bind to the exact App tree. Its body log records native readiness plus the placement gesture, and its actual test manifest records readiness exit 0 and original exit 0. It is a bounded PASS only for that selector and predicates retained in the original body; it is not a global journey or ZIP claim.

## 2. Failed return whole path

The reviewed 0747 packet says `--submit` owns source preflight, registration, derived preflight request/wait, normal request, and artifact persistence. The unchanged source has two relevant branches:

- `d66-plain-stack.mjs:691-699`: a new invocation requests preflight, saves its ID, waits, requests normal, then saves the normal ID.
- `d66-plain-stack.mjs:643-660`: a prior artifact with preflight but no normal ID waits the retained preflight and requests normal, then saves the normal ID.

The actual controller log shows the initial popup invocation at lines 2460–2521 and a second invocation at lines 2579–2641. At `10:21:34.151` the artifact had preflight `...437` and no normal field. The worker treated the lock owner as gone and launched a second `--submit`; the original invocation had not been proven dead. The trace then records `10:21:49.224` with only the preflight ID, resume at `10:21:49.227`, normal ID `...2149-13234` at `10:21:54.262`, and normal ID `...2155-20413` at `10:21:59.291`.

The request files prove both IDs used the same target, suite, App tree and snap key. The second request's `why` says `identical run ...2149-13234 in flight`. Therefore this was not native source reissue: each caller invocation reached one normal request call. It was not an independent service caller: both invocations were launched by the same worker/controller path. It was a worker procedural overlap after an artifact/runner custody loss. A process/tool resume is distinct from creating another service request; this resume did create another request.

The prior worker's initial progress/KEEP obligation failure is retained as a custody limitation. No missing progress, KEEP, or body evidence is reconstructed or backfilled here.

## 3. Cancellation and sampler coverage

The first request `...13234` was running with a build log and no completed body verdict. The second `...20413` remained queued and had no body log; the retained `why` marks it as identical while `...13234` was in flight. `request-stop-test` was issued for both; the retained controller stop log shows both cancellations queued. The retained wait logs and statuses show both reached terminal `cancelled`. The first has exit 130. The queued second has no body exit/summary and wait exited 1 after terminal cancellation; this is a queued-cancel/no-exit case, not a test failure.

The original five-second traces cover 63 placement samples, 36 popup samples, and remain above the 4-GB standing stop: placement minimum 5,622,292,480 bytes; popup minimum 5,776,478,208 bytes. No standing-stop cancellation occurred. The review's own two-sample five-second `df` trace is separate and read-only; it is not substituted for the original service trace and does not backfill missing service samples.

## 4. Contract and limits

C0 v2 was not changed. The preserved request fields are `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands`, `label`, `steps`, `merge`, `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, and `group_id`; command fields are `schema_version`, `op`, `version`, `select`, `args`, and `created`; step fields are `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, and `reads`; merge values remain `fields|atomic`. Preserved reply surfaces are accepted/merged `data`, `receipt`, `canonical_document`, `document_digest`, `provider_version`, `compiler_version`, `normalized_commands`, `idmap`, `base`, `previous`, accepted revision-publication pairs, `rebased_onto`, `merge_mode`, `steps`, `records`, `bindings`, `effects`, `dependencies`, `history`, `undo_steps`, `publisher`, and `annotations`; conflict `reason|head`; invalid `code|path|hint|suggested_command`; preview `would_status|null_receipt`.

D130 remains absolute. D141s-c paired kit is dropped. IDs 8912 and 19479 remain held; 18617 remains the cancelled original. No alternate route, new author/body, source fix, diagnostic, product claim, or future ID was invented.

## 5. Bounded next step

Treat the popup result as cancelled custody, not a functional popup failure. Preserve both cancelled IDs and their raw protected originals. Continue with the original reviewed remaining-selector packet at `p2-parent-move`, then the already ordered remaining selectors, under one submit owner. On any artifact loss, inspect the existing request/artifact state and stop with the first custody error; never rerun `--submit`, repeat printed request lines, or reopen popup ADD in this continuation.
