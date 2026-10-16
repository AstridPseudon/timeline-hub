# Plan A: same machine plus the hosted domain, direct (16 Oct 2026)

**Goal (version 1).** Someone opens the hosted Reigh app (e.g. `https://reigh.app`) in a browser on the same computer where their Runtime runs, and it uses that local Runtime: projects, timelines, saves and media, read straight from the computer. They link it once, and it keeps working across reloads, Runtime restarts and reboots. Big files work. Nothing goes through our servers except the app itself.

**Builds toward Plan B** (`2026-10-16-plan-b-cross-device-relay.md`, any device through the relay). Everything here except the gateway transport is shared, so B only adds a second transport.

## 1. Where it stands (code evidence)

| Piece | State |
|---|---|
| Local gateway `scripts/reigh-loopback-gateway.ts` | **Exists and is careful.** Binds 127.0.0.1 only (`:184`). Accepts only the configured hosted origin, and for media elements without an Origin header it checks the Referer (`:72-78`). Sends CORS and Private Network Access headers (`:79-93`). Forwards only the App's route table (`:64`, shared `pairedRoutePolicy`). Streams with Node backpressure. Allows objects up to 5 GiB (`:4-10`). Upstream idle timeout is 60 s (5 min for ACP; `:141`). Verifies it holds a product-scoped Runtime identity before serving (`:168-170`). |
| Linking | The gateway prints `open_url = <hosted origin>/#localRuntime=<base>` (`:188`). **Nothing in the App reads it**: no `localRuntime` handling in `src/`. |
| App base URL | Always same-origin `/api/runtime` (`src/integrations/runtime/client.ts:33`, by design, so a proxy injects the credential). Many call sites build clients ad hoc with that default and compare against it (`useFinalVideoAvailable.ts:272`, `useActiveTaskClips.ts:157`, `ReighTimelineEditor.tsx:441`). ACP and discovery use `/api/astrid` (`nativeEditorConnection.ts:6`). |
| Gateway lifetime | A random capability and port each start, with an 8 h expiry (`:49-50`). So it would need re-linking every start and every 8 hours. |
| Runtime restart | The gateway reads discovery and the token once, at start (`:160-170`). The App fences a changed Runtime instance and asks for a relaunch (`client.ts`, "Runtime restarted—relaunch workspace"). |
| Tests | Unit-level only: `scripts/reigh-loopback-gateway.test.ts` (origin and host policy, 413; now in `npm test`). Nothing runs a built App in a browser against the gateway and a real Runtime. |

**Verdict:** the local half is built and well guarded; the App half (find it, use it everywhere, keep it) is missing. So version 1 is mostly App wiring plus making the gateway stable, then proving it end to end.

## 2. Design

### Shared foundations (Plan B reuses these unchanged)

- **F1. One Runtime connection resolver.** A single module (`src/integrations/runtime/connection.ts`) answers "where is the Runtime, and how do I reach it?". It returns a base URL for API calls, a base for media URLs and a base for Astrid/ACP. Every client, media URL builder and "is runtime mode" check goes through it. That replaces the ad-hoc `new ReighRuntimeClient()` defaults and the `=== RUNTIME_BASE_URL` comparisons. Transports plug in behind it: `same-origin` (today's proxy, and later the relay) and `direct` (the gateway).
- **F2. Connection states.** connected, reconnecting, computer not running Reigh, Runtime restarted, link invalid or expired. One small status pill with one action per state.
- **F3. Safe retry.** Reads retry. Writes retry with the same `Idempotency-Key` and `expected_version`, which the Runtime already requires. Unsaved edits survive a gap.
- **F4. Journey harness.** A real production build on a hosted-style HTTPS origin, a real Runtime daemon on a throwaway SQLite realm, and Chromium. It is parametrised by transport: `direct` now, `relay` in Plan B.

### Direct-path specifics

- **D1. Link once.** On load the App reads `#localRuntime=<base>`. It validates the value: `http:`, loopback host, explicit port, and the path `/session/<capability>/api/runtime`. It stores it per origin in localStorage and removes the fragment with `history.replaceState`. The fragment never reaches our server. From then on the resolver returns `direct`.
- **D2. Stable gateway.**
  - The gateway runs at a fixed, configurable port with a capability persisted locally (file mode 0600).
  - There is no 8 h expiry; "Forget browsers" rotates the capability.
  - It re-reads discovery and the token when the Runtime refuses a connection or returns 401.
  - It waits for the Runtime instead of exiting.
  - A gateway or Runtime restart then needs no re-linking.
- **D3. Runtime restarts.** If the same realm comes back under a new instance id, the App re-handshakes and offers one-click "Reconnect", keeping drafts. A different realm stays fenced, as today, so the App never silently rebinds.
- **D4. Browser rules** (verified by the journey where Chromium can, and by a short manual checklist for others):
  - An HTTPS page may call `http://127.0.0.1`, because it is a potentially trustworthy origin.
  - The gateway answers the Private Network Access preflight.
  - Chrome's local-network permission prompt appears once.
  - Media elements send Origin when they carry `crossorigin="anonymous"`; otherwise the gateway falls back to Referer.
  - Safari's handling of a public HTTPS page calling localhost must be checked by hand before we claim Safari support.
- **D5. Big files.** Uploads and downloads stream through the gateway with backpressure, up to 5 GiB. Video seeks use Range. The 60 s timeout is idle, not total, so a slow but moving transfer completes.
- **D6. Start with the computer.** Astrid's local install (`astrid-agent/scripts/local_install.py`) starts and supervises the gateway next to the Runtime, and offers an "Open Reigh" link that carries the fragment.

## 3. Proof (testing plan F2; rule R-10: durations reported, never judged)

`tests/e2e/local/direct-journey.spec.ts` runs on Linux in CI's integration lane and locally via `npm run test:e2e:direct`. The App's build is served at a hosted-style HTTPS origin, using a test certificate and host mapping, so mixed-content and Private Network Access rules apply. It talks to the real gateway and a real Runtime daemon on SQLite (started directly, with discovery written by the harness).

Only a hang or one of these behaviours fails the run:
1. **Linking:**
   - opening the link stores it and strips the fragment;
   - after a reload the App is still linked;
   - a malformed or non-loopback link is refused.
2. **Core journey:**
   - open a seeded project;
   - read its timeline;
   - edit and save with the expected version;
   - reload and get a byte-identical document;
   - after a second writer saves first, the App shows the conflict and keeps the draft.
3. **Media:**
   - an image and a video thumbnail load;
   - a video seek is a 206 Range read;
   - a 200 MB upload and a 60 MB download complete with matching digests;
   - gateway memory stays bounded.
4. **Restarts:**
   - the Runtime restarts mid-session, and the App reconnects with one click, keeping its drafts;
   - the gateway restarts, and the App reconnects with no re-link;
   - the gateway is stopped, and the App shows "start Reigh on your computer".
5. **Security:**
   - a request from another origin is refused;
   - a missing or wrong capability is refused;
   - admin and worker routes are refused.

Every run also prints a table of each step through the gateway against the Runtime directly (median, p95, MB/s, machine load) so overhead is visible. Today's failures go in as owned known failures first and come out as each piece lands.

## 4. Phases

| Phase | Delivers | Size |
|---|---|---|
| A0 | Journey harness (F4) and its cases; today's failures recorded (expected: linking fails) | 0.5–1 d |
| A1 | Connection resolver (F1) used by every client and media URL; link consumption (D1); core journey green | 1–1.5 d |
| A2 | Stable gateway (D2); Runtime-restart reconnect (D3); connection states, pill and safe retry (F2, F3); restart cases green | 1 d |
| A3 | Media and big files (D5, D4): `crossorigin` media, Range seeks, 200 MB upload; the manual browser checklist | 0.5–1 d |
| A4 | Started with the computer by Astrid's local install, with an "Open Reigh" link (D6) | 0.5–1 d |

About 4–5 days in total. Plan B then adds only the relay transport behind F1.

## 5. Decisions for the owner

1. **Link once by clicking "Open Reigh" (recommended), or link automatically?** In the automatic option, the hosted app asks the gateway at its fixed port, and the gateway answers only the configured hosted origin. It is zero-click, but any page on that origin (including an injected script) could then reach the local Runtime without a step the person took.
2. **ACP over the direct path.** The gateway can forward to the Astrid ACP bridge, whose tool calls are auto-approved and which can open terminals. Should version 1 include ACP, or projects, timelines and media only?
3. **Safari:** required for version 1, or Chromium-based browsers and Firefox first?
4. **Capability lifetime:** no expiry, rotated by "Forget browsers" (recommended), or a long sliding expiry?
5. **The fixed port number,** and what happens when it is taken (fall back and re-link, or fail clearly).

## Master checklist

- [ ] A0 direct journey harness with today's failures recorded
- [ ] A1 connection resolver used by every Runtime client, media URL and runtime-mode check
- [ ] A1 `#localRuntime` link: validate, store, strip; core journey green
- [ ] A2 gateway: fixed port, persisted capability, re-read discovery and token, wait for the Runtime
- [ ] A2 Runtime-restart reconnect keeping drafts; connection states and pill; safe retry
- [ ] A3 `crossorigin` media, Range seeks, 200 MB upload, bounded memory; manual browser checklist
- [ ] A4 started by Astrid's local install; "Open Reigh" link
