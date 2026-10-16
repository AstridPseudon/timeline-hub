# Paired relay: pair once, update constantly, fast and reliable (16 Oct 2026)

**Goal.** A person connects the hosted Reigh app to the Runtime on their computer once. After that, it just works: across deploys, laptop sleep, Wi-Fi changes, Runtime restarts and app updates, with no re-pairing and no terminal commands. Big files and big saves work. We can ship the hosted app many times a day without breaking anyone's connection.

**Scope.** The hosted App's relay (`config/vite/pairedRelay.ts`, `config/vite/pairedRegistry.ts`, `config/vite/pairedRoutePolicy.ts`), the user-local connector (`scripts/reigh-local-connector.ts`), the App's connection UI, and the tests that prove all of it. The Runtime itself changes only where noted (§4).

## 1. Where it stands (code evidence)

| Area | Today | Effect on people |
|---|---|---|
| Pairing state | In-memory maps in the relay process (`pairedRegistry.ts:57-60`) | Every deploy or relay restart un-pairs everyone |
| Lifetimes | Session cookie and connector record expire after 8 h (`pairedRegistry.ts:4-5`; cookie `Max-Age=28800`, `pairedRelay.ts:151`) | Re-pair at least every 8 hours |
| Pairing flow | The connector prints a pairing URL in the terminal on every hello (`connector:136`) | A terminal step every time |
| Connector drop | Pending requests wait for the 30 s idle timeout, then 504 (`pairedRelay.ts:218`, `:276`) | 30 s freezes, then errors |
| Liveness | No heartbeat; fixed 1 s reconnect (`connector:156`) | Sleep and NAT drops go unnoticed |
| Runtime restart | Discovery is read once (`connector:49-50`) | 502 on every call until the connector restarts |
| Size limits | JSON 128 KiB, upload 64 MiB (`pairedRoutePolicy.ts:4-5`); Runtime allows 64 MiB JSON and 5 GiB objects | Big timeline saves and big videos fail |
| Throughput | Base64 inside JSON frames; no sender backpressure; one shared socket for everything (`connector:120,148,202`; `pairedRelay.ts:200,242,295-301`) | Small calls stall behind media (probe: 1.7 ms idle, 75 ms median during a 60 MB download); connector memory peaked at 250 MB |
| Version coupling | The connector enforces the App's full route table (`connector:12,163`) | Every new Runtime route the App uses needs every user's connector updated first |
| Distribution | The connector is a repo script run with `tsx` | Not something a person installs |

Probe numbers are from one loopback run of the real relay and connector against a fake Runtime (`scratchpad/relay-review/probe.mts`).

## 2. Design decisions

**D1. A pairing is a durable record, not process memory.** A pairing names a browser (and, for signed-in users, the Reigh account), a connector (machine) and a realm. It lives in a small table, read on connect and authorise and cached in the relay. The App already runs on Supabase, so use a `paired_devices` table with row-level security (`user_id`, `pair_id`, `connector_id`, `realm_id`, `label`, `created_at`, `last_seen_at`, `revoked_at`). The relay stores verifiers (hashes), never secrets. *Alternative, if the relay must stay database-free:* HMAC-signed session and connector tickets with key rotation (`kid`), plus a tiny durable revocation list. That still needs storage for revocation, so a table is simpler and also gives D6's device list.

**D2. Lifetimes match a "remember this device" product.** The session slides 30 days on use and the connector record slides 90 days; both are revocable from either side. The `generation` counter stays, but only to fence stale sockets and responses. A connector reconnect never invalidates a browser session.

**D3. Deploys are invisible.** On shutdown the relay:
1. sends `goaway` to every connector;
2. stops taking new browser requests;
3. finishes in-flight ones within a short drain window;
4. exits.

Connectors reconnect at once, with jittered backoff, to whichever instance is up. A browser request that arrives while its connector is between instances is parked for up to ~10 s waiting for that connector, instead of failing. Writes carry `Idempotency-Key` and `expected_version` already (the Runtime requires them), so the App can retry them safely. The UI shows "Reconnecting to your computer..." only if the gap is noticeable.

**D4. The connector is a dumb, stable pipe; the Runtime is the authority.** The connector keeps only coarse rules:
- loopback Runtime only, using a product-scoped Runtime token;
- method and size limits;
- no credentials from the browser.

It drops the App's fine-grained route table. Authorisation of each call stays where it already is, the Runtime's scoped bearer credentials (`runtime_protocol/auth.py`). New App features then need no connector update.
- The relay speaks a versioned protocol. The connector says its version in `connector_hello`, and the relay supports the current version and the one before it (N-1).
- If a connector falls out of that window, the App says so with one clear action.

**D5. The connector ships with the Runtime, not as a script.** The person installs one thing. Two options:
- (a) the Runtime launcher (`banodoco_local`) starts and updates the connector as a managed child;
- (b) the Runtime daemon itself dials out to the relay as a "remote access" module.

(b) has the fewest moving parts but puts a product-specific concern in the neutral Runtime. Recommend (a) now, with (b) as an option later.

**D6. One connection-status UI with one action per state.**

| State | Shown as | Action |
|---|---|---|
| Connected | machine label | none |
| Reconnecting | spinner | none |
| Computer offline | "Start Reigh on your computer" | none |
| Runtime stopped | message | none |
| Connector or Runtime too old | message | "Update" |
| Pairing revoked or expired | message | "Connect this computer" |

Settings lists paired devices, with last seen and Revoke.

**D7. Pairing is a device-code flow.** The hosted app shows "Connect your computer" with a short code. The local side opens the browser to confirm, or the person types the code. This replaces the terminal-printed URL as the primary path. Invitations stay single-use and short-lived (5 min).

**D8. Fast by construction.**
- Binary WebSocket frames with a small header (stream id, flags, length) replace base64-in-JSON.
- Per-stream credit-based flow control (window ~256 KiB–1 MiB) means the sender waits for credit and on `bufferedAmount`.
- Small and large streams are scheduled round-robin, so a small call never waits behind media.
- Limits match the Runtime: 64 MiB JSON and the Runtime's object maximum.
- Uploads stream end to end. Large downloads resume with `Range`.

**D9. Same-machine fast path is optional, later.** The loopback gateway already streams with backpressure and allows 5 GiB. A direct browser → localhost path depends on Chrome's local-network permission and Safari's mixed-content rules, so the relay stays the default. Revisit only if the measurements in §3 show the relay is the bottleneck for same-machine users.

## 3. How it is proven (testing plan F2, rule R-10: durations are reported, never judged)

One thin journey, `tests/e2e/paired/paired-journey.spec.ts`, runs on Linux:
- a production build served with the relay;
- the real connector;
- a real Runtime daemon on a throwaway SQLite realm, with `discovery.json` written by the harness;
- Chromium.

Each case runs direct and through the relay in the same run. Every run prints median and p95, MB/s and machine load. Nothing fails on time except a hang. These behaviour checks fail the run:
- pairing persists across a relay restart (the deploy simulation in D3) and a connector restart;
- a small call started during a 60 MB transfer completes before the transfer (head-of-line blocking);
- connector memory stays under a fixed bound with a stalled reader;
- byte counts and digests match for 5 MB and 60 MB objects;
- a 1 MB Range read returns 206;
- a save over 128 KiB succeeds;
- a killed connector socket mid-save gives the named error, then a reconnect, then the retry with the same idempotency key, and exactly one publication;
- a CAS 409 keeps the draft and shows the conflict;
- a Runtime restart reconnects without user action;
- an N-1 connector works, and an N-2 connector gets the "update" state;
- a revoked device gets the "connect this computer" state.

Cases that fail today go in as owned known failures and come out as each fix lands. Unit tests cover the frame codec, the flow-control window and the registry's persistence and lifetimes.

## 4. Phases (each ends with the journey green for its cases)

| Phase | Work | Size | Depends on |
|---|---|---|---|
| P0 | Thin journey harness, the measurement table, today's failures recorded | 1.5–2 d | none |
| P1 | Reliability quick wins: fail pending requests at once on connector close; heartbeat ping/pong 15 s with jittered backoff; re-read discovery on ECONNREFUSED; limits matching the Runtime; ACP long-poll keepalive | 1–1.5 d | P0 |
| P2 | Durable pairing (D1, D2) and invisible deploys (D3) | 2–3 d | P0; the Supabase table |
| P3 | Fast transport (D8): binary frames, credit flow control, fair scheduling | 2–3 d | P0, P1 |
| P4 | Decoupling and skew (D4): coarse connector policy, protocol versioning N-1 | 1–2 d | P2 |
| P5 | People-facing: status UI (D6), device list and revoke, device-code pairing (D7) | 2–3 d | P2 |
| P6 | Distribution (D5a): the launcher runs and updates the connector | 1–2 d (Runtime and Astrid repos) | P4 |
| Later | Multi-replica routing by `pair_id`; the same-machine fast path (D9) | only if needed | |

## 5. Decisions for the owner

1. Are hosted users signed in to a Reigh account (so a pairing binds to `user_id` and devices can be listed), or is the browser the only identity?
2. Lifetimes: are 30-day sliding sessions and 90-day connectors acceptable, given that a stolen cookie reaches a local Runtime until revoked?
3. Where the connector lives: the launcher's managed child (D5a) or a Runtime module (D5b)?
4. Hosting: a single instance with rolling deploys (D3's parking covers that), or several replicas (needs sticky routing)?
5. Moving per-route authorisation from the connector to the Runtime's scoped tokens (D4) is a security-boundary change; it needs your sign-off.

## Master checklist

- [ ] P0 journey harness with measurement table; known failures recorded
- [ ] P1 fail-fast on connector close
- [ ] P1 heartbeat and jittered reconnect
- [ ] P1 re-read discovery on Runtime restart
- [ ] P1 limits match the Runtime (JSON 64 MiB, object max)
- [ ] P1 ACP long-poll keepalive
- [ ] P2 `paired_devices` table, relay cache, sliding lifetimes
- [ ] P2 goaway, drain and request parking; deploy simulation green
- [ ] P3 binary frames, credit flow control, fair scheduling; head-of-line and memory checks green
- [ ] P4 coarse connector policy; protocol version N-1
- [ ] P5 status UI, device list, device-code pairing
- [ ] P6 connector shipped and updated by the launcher
