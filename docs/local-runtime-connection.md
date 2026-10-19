# Reuse an existing local Runtime from the hosted editor

## Connection screens

| # | Situation | Signal | Screen |
|---|---|---|---|
| 1 | First visit, never installed | `prompt` → Connect → Allow → 2× `silent` | permission → pending → set_up |
| 2 | Installed, never connected from this browser (a cleared browser, a private window, another browser) | as 1 | set_up. It says only "you might not be set up yet"; the setup block searches for an install, then a checkout, before installing. |
| 3 | Returning, Astrid stopped | `granted`, 2× `silent`, `connectedBefore` | not_running |
| 4 | Astrid starting | fewer than 2 failed readings | connecting → app. If slower, row 3 or row 1 until ready. |
| 5 | Launcher up, Runtime down | `down` | not_running, whatever the history |
| 6 | Permission not asked | `prompt` | permission |
| 7 | Chrome's prompt open | `prompt`, Connect probe in flight | pending |
| 8 | Prompt dismissed | still `prompt` | permission again |
| 9 | Permission denied | `denied`, nothing sent | blocked |
| 10 | Launcher started for another origin | 403 before CORS → `silent` | set_up or not_running. The agent's command then hits G2. |
| 11 | Another program on 17340 | `silent` | set_up or not_running. The launcher says "Another program is in the way"; the agent reports it. |
| 12 | Realm or identity changed, before connecting | `restart` | restart_needed |
| 13 | Phone or tablet | `isMobileDevice()` | phone |
| 14 | Safari or Firefox | scenario not `chromium` | rows 1–5, no permission screens (G5) |
| 15 | Connected, Astrid stops | 2 failed health readings | stopped card. It clears itself when the same instance answers. |
| 16 | Connected, Astrid restarts | new `runtime_instance_id` | restarted card → Reload |
| 17 | Connected, realm changes | 503 `realm_changed` | restarted card → Reload → row 12. Rare, and each step is true. |
| 18 | Timeline won't load | load error | loadFailed. It retries a few times when Astrid answers; Try again always works. |
| 19 | Connected, no projects | — | EmptyWorkspaceGuidance |

The page polls every three seconds and on focus. A `restart` signal shows immediately; otherwise it stays on
`connecting` until two readings in a row fail. Then it shows `not_running` if this browser connected before or any
probe gave a `down` reading, and `set_up` otherwise. Background checks do not change visible content until
the screen itself changes. Non-Chromium desktop browsers skip the Chrome permission step.

Both agent blocks (`copy.ts`, `AGENT_SEARCHES`) look before they act: first for an install folder (its
`install.json` carries `astrid.local-source-install`; it starts with `<folder>/start`), then, only if there is none,
for an astrid-app checkout (`scripts/dev-local-workspace.mjs`; `npm run dev:local`). More than one: ask which. The
setup block installs only when it finds nothing and no sign that Astrid ran here before; the start block asks.

Run `npm run dev:local` from this App checkout, then open
`https://astrid.haus/tools/video-editor`. The local gateway on port 17340 connects
the hosted page to the selected Runtime. Runtime credentials stay on this
computer; the browser receives no product token.

For an existing installation, inspect its saved Runtime selection and source
profile before launching. Keep its support root, realm, profile and credential.
Do not infer the selected workspace from a checkout name or substitute an empty
default root. `astrid doctor --json` reports Astrid's resolved selection, and
`astrid-runtime workspace inspect --data-root <existing-root> --json` checks the
explicit installation.

Persist the verified selection in this checkout's ignored `.env.local`:

```dotenv
ASTRID_RUNTIME_DATA_ROOT="/absolute/existing/support-root"
ASTRID_RUNTIME_CHECKOUT="/absolute/existing/Runtime-checkout"
ASTRID_RUNTIME_PYTHON="/absolute/existing/environment/bin/python"
ASTRID_CHECKOUT="/absolute/existing/Astrid-checkout"
ASTRID_APP_ACP_ENABLED=1
```

`ASTRID_APP_ACP_ENABLED=1` explicitly enables the existing local agent connection
for the hosted origin, equivalent to `--acp`. Omit it to leave that connection
disabled. The launcher reads only its documented Runtime path settings and this
agent switch from `.env.local`; it does not import unrelated app credentials or
port settings. Shell variables take precedence over the local file, and explicit
launcher path arguments take precedence over both. Keep secrets out of `VITE_`
variables. `ASTRID_SUPPORT_ROOT`, `ASTRID_WORKSPACE_DISCOVERY`, and
`ASTRID_RUNTIME_SOURCE_MANIFEST` are also supported local launcher settings.
When the installation already uses a credential file or a specific pack-host
interpreter, preserve those paths with `ASTRID_ENV_FILE` and
`ASTRID_PACK_HOST_PYTHON`. The launcher passes paths, never reads or copies the
credential values. Existing credentials remain managed by Astrid's resolver.

The same one-command restart reuses the configured Runtime, starts the local App
and gateway, and passes that exact root and discovery path to the agent. Stop
the App launcher with Ctrl+C before restarting it; a separately running Runtime
remains owned by its existing launcher.

Verify `/api/runtime/v1/health`, realm identity, projects and timelines through
the gateway using the configured hosted Origin. Verify the selected agent by a
small read-only prompt. A connection can be healthy while a workspace is empty;
never create demo records to hide a wrong selection.

If a saved source profile points to a deleted temporary checkout, preserve its
original configuration and update its source paths to the actual current
installation through the Runtime's supported source-manifest/lifecycle flow.
Run supported `upgrade` for schema changes and honor its integrity checks.
An editable installation whose package was renamed may need its existing
editable finder mappings repaired to the current package paths; record exactly
which environment and aliases changed, rather than reinstalling or silently
changing interpreters. Preserve the installed named agent profile and verify its
instructions hash before and after recovery.

## Managed media requests

A successful object GET from a terminal does not prove that browser playback can
read it. The hosted page must send its exact Origin on native media requests,
and browser fetches must omit credentials. The gateway adds the Runtime token
on this computer; it rejects browser cookies and authorization. Keep its strict
Origin rule instead of adding credentialed CORS to work around a renderer bug.

The canonical rendering pack owns one managed-object URL recognizer and the
`ManagedImg`, `ManagedOffthreadVideo`, and `ManagedVideo` primitives. They apply
anonymous native CORS and credential-free decoder fetches only to managed object
routes on loopback origins or the same-origin proxy, preserving external and
signed URL options. Pack effects, image readiness, video readiness, and the App's
audio cache must reuse that boundary. Do not add request policy separately to
each effect. Refresh the browser source with
`scripts/astrid-landing/refresh-vendor.mjs` and verify its recorded provenance.

Regression coverage includes `ManagedMedia.hosted.test.tsx` (managed URLs,
encoded IDs, ports/hosts, native attributes, refs/readiness callbacks, decoder
and fallback options), `AudioAnalysisProvider.test.tsx` (credential-free cache
warming), and `astrid-loopback-gateway.test.ts` (Origin refusal and ranged byte
responses). Browser QA must also cover a pack-owned animated image/video,
backward and forward seeking, and transition boundaries; ordinary seeded media
alone does not exercise pack-owned native requests. Inspect the browser's actual
request and console when an image fails, not only a server-side GET.

## Saved chat after a bridge restart

An ACP connection ID belongs to one bridge process. If that process restarts,
the client retires a missing connection and retries the read-only saved
transcript load once with a fresh connection. This includes the older bridge's
specific `not_found` / `ACP connection is not available; reconnect` response;
an unknown saved session remains an error. Prompts are never automatically
resent by this recovery. Restored unconfirmed messages stay paused until the
user explicitly retries delivery after checking saved history.

`useAgentSession.test.tsx` covers both transcript-load and event-poll connection
loss, plus unknown-session isolation. `AgentChat.projectContract.test.tsx`
exercises the real panel/hooks/transport and verifies that a fresh connection
preserves the draft and queued message without calling the prompt endpoint.
