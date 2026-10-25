# D127 retention path

Read-only trace against Runtime `453b3e6f92045980219ec4948419ee5ad25c817d`, App `84857c45347539c7820bb054b69e2e5ad4079081`, and helper SHA-256 `6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`.

## Source and caller

1. `app/src/tools/video-editor/commands/commitOutbox.ts:464-530` is the persisted browser funnel. It writes `pending` to IndexedDB (`astrid.command-outbox`) before transmission, sends the exact serialized body and idempotency key, and keeps that exact request on retry/uncertain transport.
2. `app/src/tools/video-editor/commands/commitSession.ts:238-249` supplies the existing `send`/operation transport to the outbox. It classifies transport uncertainty as retry and does not rebuild the request.
3. `app/src/integrations/runtime/dataProvider.ts:751-767` is the registered Runtime provider caller. It validates project/timeline and verified base identities, calls the generated client, rejects preview as non-accepted, and returns the accepted closure.
4. `app/src/integrations/runtime/generated.ts:202-204` emits the canonical timeline commit POST and `Idempotency-Key`. No new caller or collector is needed for this diagnostic.
5. The App harness (`tests/e2e/local/support/harness.ts:719-733, 775-785`) opt-in mounts the existing helper through `sitecustomize`, with the helper SHA checked by the harness and the sink selected only when `D66_RUNTIME_LOG_DIR` is configured. The normal product launcher remains uninstrumented.

## Existing helper lifetime

- `tests/helpers/p2_commit_phase_capture.py:304-375` samples active Runtime request threads every 20 ms. It increments bounded per-request sample counters and safe-frame counts; it never retains body, header, credential, URL, identifier, or exception text.
- `:496-575` keeps a bounded rolling event ring (`max_events=128`) and a request-local deque bounded by `max_bytes=65536`. The request-local buffer is the source for a final failed or pending request; the rolling ring is the fallback/context view.
- `:649-717` produces phase summaries. The dispatch boundary is `_dispatch`; arrival, body-read time, exact lock wait, and caller receipt are explicitly unsupported/UNKNOWN.
- `:731-834` selects the newest non-complete request at shutdown, gives its retained events priority, then fills remaining output from the rolling ring. `stop()` (`:238-274`) stops sampling, cancels watchdog timers, summarizes requests, finalizes the snapshot, writes the bounded event set, flushes, and closes both sinks.
- `:836-974` maps only existing Runtime trace seams: dispatch, handler, authorization, coordinator admission/lock, dynamic provider, accept, receipt, and response. The current dynamic provider and phase tracing are existing-helper behavior, not a new Runtime writer.

## Actual 10721 result

The browser element request joins exactly to the Runtime capture by the locally computed lowercase UTF-8 idempotency-key SHA-256 and process namespace/PID birth/request tuple. The joined request retained 352 samples and 3 lost samples, ended its retained observation at `authorization`, and remained `PENDING` when the capture was stopped. Its handler end, provider completion, response, request-wall denominator, and final duration are all UNKNOWN.

The helper retained 22 request events for that pending request and reported them byte-complete within the 64 KiB request buffer. That is buffer completeness only; it is not request lifecycle completion. The overall output was 128 events / 40,763 bytes with 7 rolling-capacity drops. The ten-row inclusive projection is occupied by shared door/dispatch routing frames, so no provider-dominant leaf was retained. This is projection censorship, not evidence that the provider was dominant or absent.

The other captured launches are not assigned to the joined element request. A separate completed request has measured handler/provider spans, but is a distinct request and cannot supply the element result. The SWAP browser join remains UNKNOWN. No response, wall denominator, native comparison, or cost attribution is inferred.

## Custody and privacy

The sink is created with exclusive creation and mode `0600`; the containing App diagnostic directory is a private `0700` child of `TMPDIR`. App teardown waits for the Runtime process and records its streams beside the externally supplied diagnostic directory, then removes only the harness-owned temporary directory. Without `D66_RUNTIME_LOG_DIR`, no phase sink is created. The retained evidence is therefore an explicitly requested diagnostic artifact, not normal product persistence.

The reviewed packet contains only safe phase fields, counters, relative safe-frame labels, and hashes. No raw stack blob, body, key preimage, auth header, credential, or private URL is published. The normal IndexedDB outbox retains the exact user commit request for product recovery; the Runtime helper does not read or duplicate that payload.

