# Plan A: same machine plus the hosted domain, zero-click (16 Oct 2026, revision 2)

**Goal (version 1).** Someone runs Reigh on their computer and opens the hosted app (e.g. `https://reigh.app`) in a browser on that computer. It connects to their local Runtime by itself, with nothing to paste and no link to click. Projects, timelines, saves and media come straight from the computer; our servers only serve the app. If it can't connect, the page says so kindly. The person gets a one-line instruction they can hand to their agent to get it running, and the page connects on its own as soon as it is.

**Builds toward Plan B** (`2026-10-16-plan-b-cross-device-relay.md`, any device through the relay). Everything below except the gateway transport is shared, so B only adds a second transport.

**Revision 2:** zero-click replaces the `#localRuntime` link (the owner's decision). Three searches of the App, Astrid and Runtime repos confirmed there is no existing auto-connect path to duplicate.

## 1. Where it stands (code evidence)

| Piece | State |
|---|---|
| Runtime | Has no browser-facing layer: no CORS, OPTIONS returns 501, no Origin or Host checks (`runtime_protocol/server.py:170-196, 974-990`). Its port is ephemeral and changes on every restart (`daemon.py:55`, `banodoco_local/bootstrap.py:1128-1141`). The product token has fixed scopes, no admin or worker access, and never expires (`server.py:242-255`, `bootstrap.py:509-521`). So the page must never hold it, and a gateway in front is required. |
| Local gateway `scripts/reigh-loopback-gateway.ts` | **Built, and careful.** It binds 127.0.0.1 (`:184`) and accepts only the configured hosted origin, using the Referer for media requests that send no Origin (`:72-78`). It answers CORS and Private Network Access preflights (`:79-93`) and forwards only the App's route table (`:64`). It streams with backpressure, allows up to 5 GiB (`:4-10`) and has a 60 s idle timeout (`:141`). It holds the product token server-side after verifying it (`:160-170`). It uses a random port and a random capability with an 8 h expiry (`:47-50`). |
| Launcher `npm run dev:local` (`scripts/dev-local-workspace.mjs`) | **The everyday hook point.** It verifies the Runtime (health, handshake, realm, schema digest, scoped credential; `:198-270`) and starts the discovery proxy, ACP bridge and Vite. It starts the gateway only with `--hosted-origin` (`:70-91, 373-385`), on port 0. It opens no browser. Astrid's `scripts/local_install.py` runs it for fresh installs and prints `http://localhost:2222`. |
| App | Always calls same-origin `/api/runtime` (`src/integrations/runtime/client.ts:30-33`). Many call sites build clients ad hoc with that default and compare against it (`useFinalVideoAvailable.ts:272`, `useActiveTaskClips.ts:157`, `ReighTimelineEditor.tsx:441`); ACP and discovery use `/api/astrid`. **Nothing finds or uses a local gateway.** The gateway prints a `#localRuntime=` link (`:188`) that no App code reads. |
| Precedent | A dormant probe of a fixed localhost port (`src/shared/lib/localWorker/config.ts:6-13`, `localhost:8765`, with a 250 ms health check) is the only existing case of the page reaching localhost directly. |
| Ports in use | 2222 (Vite), 8765 (local worker), 17333 (Astrid bridge), 17335 (ACP), 17336 (discovery proxy), 54321 (Supabase). |
| Tests | Unit tests only: `scripts/reigh-loopback-gateway.test.ts`. Nothing drives a built App in a browser against the gateway and a real Runtime. |

## 2. Design

### Shared foundations (Plan B reuses these unchanged)

- **F1. One Runtime connection resolver** (`src/integrations/runtime/connection.ts`). It answers "where is the Runtime, and how do I reach it?" with three bases: one for API calls, one for media URLs, and one for Astrid/ACP. Every client, media URL and "is runtime mode" check goes through it, replacing the ad-hoc defaults and the `=== RUNTIME_BASE_URL` comparisons. Transports plug in behind it: `same-origin` (today's dev proxy, and later the relay) and `direct` (the gateway).
- **F2. Connection states with one action each.** connected, connecting, Reigh not running on this computer, the browser blocked the local connection, Runtime restarted, and wrong or missing setup. A small status pill shows the state; the "not connected" panel is described in D3.
- **F3. Safe retry.** Reads retry. Writes retry with the same `Idempotency-Key` and `expected_version`, which the Runtime already requires. Unsaved edits survive a gap.
- **F4. Journey harness** (§3), parametrised by transport.

### Direct-path specifics

- **D1. Zero-click connect.** The gateway listens on one fixed default port, 17340, which is configurable and clear of the ports above. On load the hosted app calls `GET http://127.0.0.1:17340/v1/connect`. The gateway answers only when the `Origin` header is the configured hosted origin and `Host` is `127.0.0.1:17340` or `localhost:17340`, which defeats DNS rebinding. Its answer is the session base, the realm and the Runtime instance. The App then routes everything through the resolver. Nothing is pasted, nothing goes in the URL, and no secret is stored in the page.
  - **What this trusts:** any page served from the hosted origin can reach the local Runtime, within the product route table (no admin, no worker, no credential routes). That is the zero-click trade.
  - **What protects it:** the exact-origin check (other sites are refused; browsers do not let pages forge `Origin`), the Host check, the route allowlist, the size limits, and ACP being off unless chosen (decision 2).
- **D2. A stable gateway.** It uses the fixed port. It re-reads discovery and the token when the Runtime refuses a connection or returns 401, because the Runtime's port changes on restart. It waits for the Runtime instead of exiting, and drops the 8 h expiry. If the port is taken, it says so clearly and exits; it never silently moves.
- **D3. The "not connected" panel.**
  - It says plainly what is wrong, in one sentence per state (F2). It always has a **Copy instructions for your agent** button with a ready-made prompt, e.g.: "Start Reigh on this computer: run `banodoco-local up --profile astrid`, then in the reigh-app folder run `npm run dev:local`. Tell me when it reports the workspace is healthy."
  - It re-checks every few seconds and when the tab regains focus, and connects with no reload once Reigh is running.
  - If the browser blocks localhost (a denied permission prompt, an extension, Safari), it says that instead, with a short fix.
- **D3a. First time or returning.** After the first successful connection, the App remembers on its origin that this computer and realm have connected before. The panel then has four states:

  | Situation | Panel |
  |---|---|
  | Never connected and nothing answers | **Set up Reigh on this computer**, with install instructions for the agent, plus "Already installed? Start it" |
  | Connected before, nothing answers | **Reigh isn't running**, with start instructions |
  | The gateway answers but the Runtime is down | **Reigh is starting or the Runtime stopped** |
  | A different realm than last time | Say so; offer to switch |

  A different browser or cleared site data looks like a first time, so the first-time panel always includes the start path too.
- **D3b. Permissions.** No file or folder permission is ever requested: the browser never touches files, and the Runtime reads and writes its own files and SQLite. The only browser prompt is Chrome's one-time local-network access. The App explains it just before the first probe, and recognises a refusal ("browser blocked" state) with how to undo it. Uploads use the normal file picker.
- **D4. Runtime restarts.** If the same realm comes back under a new instance id, the App re-handshakes and continues, keeping drafts. A different realm stays fenced, as today, and offers "Reconnect"; it never silently rebinds.
- **D5. Big files.** Uploads and downloads stream through the gateway with backpressure, up to 5 GiB. Video seeks use Range requests. Media elements use `crossorigin="anonymous"`, so the browser sends `Origin`. The 60 s timeout is an idle timeout, so a slow transfer that keeps moving completes.
- **D6. One command starts everything.** `npm run dev:local` starts the gateway by default whenever a hosted origin is configured (`REIGH_HOSTED_ORIGIN`, defaulting to the production domain), on the fixed port. It prints "Open https://reigh.app". Astrid's `local_install.py` prints the same.

## 3. Testing

| Layer | Proves | Runs |
|---|---|---|
| Unit | Gateway rules: exact origin, Host check, route allowlist, size limits, `/v1/connect`. Resolver, connection states and retry logic. | `npm test`, every push |
| Journey `tests/e2e/local/direct-journey.spec.ts` | The real production build served from a hosted-style HTTPS domain (test certificate plus host mapping, so the browser applies public-site rules: mixed content, CORS and Private Network Access preflights), with the real gateway, a real Runtime daemon on SQLite and Chromium | Integration lane; before any merge touching the gateway, resolver or `dev-local-workspace.mjs` (R-11); `npm run test:e2e:direct` locally |
| Manual checklist, about 10 min per browser release | Things automation can't fake (below) | By hand, on the real domain |
| Live diagnostics | The "not connected" panel names the failing step | Every real visit |

**Journey cases.** Only a hang or one of these fails the run; durations are reported, never judged (R-10):
1. **Zero-click:**
   - opening the hosted origin connects with nothing in the URL;
   - a first visit with nothing running shows the set-up panel, and after one successful connection a later visit with nothing running shows the start panel;
   - a reload stays connected;
   - with the gateway stopped, the panel shows the agent instructions, then connects by itself, with no reload, once the gateway starts.
2. **Core:**
   - open a seeded project and read its timeline;
   - edit and save with the expected version;
   - a reload is byte-identical;
   - a second writer's save shows the conflict and keeps the draft.
3. **Media:**
   - an image and a video thumbnail load;
   - a video seek is a 206 Range read;
   - a 200 MB upload and a 60 MB download keep matching digests, with gateway memory bounded.
4. **Restarts:**
   - a Runtime restart on a new port continues, with drafts kept;
   - a gateway restart reconnects by itself.
5. **Security:**
   - another origin is refused;
   - a rebinding Host is refused;
   - admin, worker and credential routes are refused.
6. **Speed table** (reported, never judged): each step through the gateway against the Runtime directly; median, p95, MB/s and machine load.

**Manual checklist** (real domain, real browsers):
- Chrome or Edge stable: the local-network permission prompt appears once and is explained by the panel, and the journey's core steps work.
- Firefox: the same.
- Safari: record whether a public HTTPS page may call `http://127.0.0.1`. If not, the panel's "browser blocked" message must say so.
- The production domain's Content-Security-Policy, if the host or CDN sets one, allows `connect-src` and `img-src`/`media-src` to `http://127.0.0.1:17340`. The repo sets no CSP.
- Brave's shields, and one common ad blocker: note the result.

## 4. Phases

| Phase | Delivers | Size |
|---|---|---|
| A0 | Journey harness and cases; today's failures recorded (expected: every App-side case) | 0.5–1 d |
| A1 | Resolver (F1) used by every client and media URL; gateway `/v1/connect` with origin and Host checks and a fixed port (D1); the App connects with zero clicks; core journey green | 1–1.5 d |
| A2 | Stable gateway (D2); Runtime-restart continuation (D4); connection states, pill and "not connected" panel with agent instructions (F2, D3); safe retry (F3); restart cases green | 1–1.5 d |
| A3 | Media and big files (D5); security cases green; the manual checklist run once | 0.5–1 d |
| A4 | `npm run dev:local` starts the gateway by default and prints the hosted URL; `local_install.py` the same (D6) | 0.5 d |

About 4–5 days in total. Plan B then adds only the relay transport behind F1.

## 5. Decisions for the owner

1. **Settled: zero-click.** Any page on the hosted origin can reach the local Runtime's product routes; see D1 for the safeguards.
2. **ACP over the direct path.** The ACP agent's tool calls are auto-approved and it can open terminals. Off by default in version 1 (recommended), or on?
3. **Browsers for version 1.** Chromium-based browsers and Firefox (recommended), with Safari after the checklist says what it allows?
4. **The hosted origin(s)** the gateway accepts: production only, or also a staging domain?
5. **Port 17340:** acceptable?

## Master checklist

- [ ] A0 journey harness and cases; today's failures recorded
- [ ] A1 resolver used by every client, media URL and runtime-mode check
- [ ] A1 gateway `/v1/connect`, exact origin, Host check, fixed port; zero-click connect; core journey green
- [ ] A2 stable gateway (re-read discovery and token, wait for the Runtime, no 8 h expiry)
- [ ] A2 restart continuation; states, pill, "not connected" panel with agent instructions; safe retry
- [ ] A3 media and big files; security cases; manual checklist run once (including the production CSP)
- [ ] A4 `npm run dev:local` starts the gateway by default and prints the hosted URL; `local_install.py` the same
