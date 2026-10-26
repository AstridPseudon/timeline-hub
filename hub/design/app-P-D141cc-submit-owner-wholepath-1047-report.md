# D141cc independent whole-path report

## Result

Completed one independent, read-only native-path investigation after the second failed private fix. No product change and no body claim.

The supported future path is:

`caller/client + one tool session → unchanged d66 builder → existing submit artifact file lock → genuine request-test preflight/normal IDs → daemon registry-row admission and test-run snapshot → durable status/summary/receipt → wait → original body`

The native builder is exact and unchanged: `/home/user/work/app/scripts/testing/d66-plain-stack.mjs`, blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`.

## Native path map

- `serviceRecipe` lines 375–395 materializes all pinned D66 source SHA/tree/checkout bindings and the actual node command.
- `registerSubmitRecipes` lines 407–425 appends exactly preflight and normal rows, preserving old registry bytes and refusing duplicate names or concurrent registry changes.
- Lines 638–660 adopt an existing artifact; a durable normal ID is returned without another request, and a preflight-only artifact waits its recorded preflight before requesting one normal ID.
- Lines 663–701 build the new exact tuple, wait for checkout receipts, register rows, persist the artifact, request preflight, wait, request normal once, and persist that normal ID.
- Lines 704–710 wrap the submit path in the in-process and artifact file lock; the lock is a serialization mechanism for the builder, not an authorization to make a second manual normal request.
- `request-test` writes the durable result request and queue item. The dispatcher admits the registered row, creates the result snapshot, and records status/log/summary/exit. `wait-test` polls status and returns only a terminal summary/exit.

The C0 v2 request/reply shape is preserved exactly as required by the brief; ordinary request metadata is not Runtime v2 wire and no wire change is proposed.

## Evidence comparison

Placement `9168` is a bounded PASS: preflight `6758` passed, normal `9168` passed with exit 0 in 259 seconds. Popup preflight `437` passed, but normal `13234` was cancelled with exit 130 and normal `20413` was queued/cancelled as an identical in-flight run. Both popup IDs remain cancelled custody records with UNKNOWN body verdict. Six selectors are NOTRUN. No D141j diagnostic was triggered.

The original 1026 evidence shows the first divergence was overlapping worker/controller invocations before the first normal ID was proven durable/dead. It does not show a native internal retry or an independent production caller. Preserve this native implementation and ownership rule.

## Private candidate findings

Review-next found three blocking, intrinsic candidate defects:

1. The authorized popup retry uses synthetic command/row bytes instead of the unchanged builder output (builder command/row hashes differ from candidate hashes).
2. A FakeService preflight-to-normal interleaving makes `normal_calls=2`; the candidate does not re-inspect or lock at that boundary.
3. A same-source wrong command/row candidate is silently ignored and causes a new request instead of a fail-closed refusal; digest-to-byte binding is not validated.

The 1032 model therefore cannot qualify the native route. It never invokes the genuine builder, real artifact lock, registry, request-test, daemon snapshot, or wait/receipt path. Its 12 private controls remain model-only evidence.

## Safe finite handoff

Use one owner/tool session and the unchanged builder. Inspect authoritative same-target/same-suite/source request and artifact state before any create or relaunch; adopt exact IDs under the existing lock. Never repeat a normal request because an artifact is incomplete. Stop finitely on unknown owner, mismatch, ambiguity, missing receipt, or safety refusal. Do not resume `13234` or `20413`, backfill a body verdict, or reopen popup ADD. Any future remaining-selector work must be one selector at a time and retain the 4 GB stop.

See `source-map.json`, `source-manifest.json`, `findings.md`, and `validation.md` for absolute citations and hashes.
