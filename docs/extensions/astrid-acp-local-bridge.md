# Astrid App local Astrid ACP bridge

The Astrid App ACP bridge is a user-machine process. It keeps only ephemeral
connection handles in memory; each selected agent remains the authority for its
profiles, opaque session IDs, and session storage. The browser never receives the bearer
token or starts a child process.

In one terminal, start the bridge with explicit host-owned paths. The bridge
launches the real `astrid` command, not a separate raw `omp` profile; Astrid
therefore remains the authority for the named agent, system prompt, branded
OMP build, credentials, and session identity:

```sh
export ASTRID_BRIDGE_TOKEN='use-the-same-local-token-as-vite'
ASTRID_ACP_CWD="$PWD" \
npm run dev:astrid-acp

# Optional: set ASTRID_ACP_PROFILE to use an isolated Astrid/OMP profile. By
# default the real `astrid` launcher uses the machine's normal configuration.
ASTRID_ACP_CWD="$PWD" ASTRID_ACP_PROFILE='isolated' \
npm run dev:astrid-acp
```

`ASTRID_ACP_SESSION_DIR` is optional. When omitted, the installed OMP build
owns its canonical cwd-derived session directory, allowing ACP session
listing/loading/resume to discover the same opaque session ID after a fresh
process starts with the same profile and cwd. An explicit absolute
`ASTRID_ACP_SESSION_DIR` remains a supported legacy override; existing data is
left in place, but OMP 17.3.5 ACP discovery does not search that arbitrary
directory in a new process, so use it only when the original process remains
live.

In a second terminal, start Astrid App and point the ACP proxy at its separate
loopback port:

```sh
export ASTRID_BRIDGE_TOKEN='use-the-same-local-token-as-vite'
VITE_ASTRID_ACP_BRIDGE_PORT=17335 npm run dev
```

The existing `/api/astrid` REST routes remain on the Astrid bridge port. ACP
requests use `/api/astrid/acp`, which the Vite proxy forwards to the local ACP
bridge with the existing bearer boundary and protocol header. The browser
controls create, resume, cancel, close, and reconnect sessions, but do not
persist connection or session IDs. Reconnect while the host is live reuses the
same ACP process and opaque session authority; it does not create a second
session registry.

The agent header's model chip uses `astrid agent models --json` to list
providers and usable models, including providers that need no sign-in.
Sign in to another provider in a terminal: run
`omp`, then `/login` (use the same `--profile` as the bridge when configured).
Choose **ChatGPT Plus/Pro (Codex Subscription)** for the `openai-codex` route.
Reopen the picker after signing in. Provider billing, authentication and quota
errors also offer **Switch model** beside the failed turn.

The authenticated `/acp/models` and `/acp/model` routes share the existing
bridge token and protocol boundary. The bridge calls the same configured
Astrid command for ACP and model management, using `OMP_PROFILE` for model
commands when an isolated profile is configured. `astrid agent use PROVIDER/MODEL`
owns validation and persistence of OMP's `modelRoles.default`. Listing the
saved default leaves existing chat models and project defaults unchanged.
After an explicit App selection, the bridge restarts ACP to discover newly
authenticated providers, then loads the same
conversation ID and applies the chosen model before the next prompt. Switching
waits until the current request finishes. The browser receives provider/model
metadata and usage limits, never credentials or account tokens.

## Other agents already on this computer

The picker has an **Agent** section above Astrid's OMP models. It detects
`claude` and `codex` on the bridge process's PATH, then asks only
`claude auth status --text` and `codex login status` whether each is signed in.
Claude Code uses your Claude login; Codex uses your Codex CLI login (including
ChatGPT). These are separate from OMP's provider logins. Status errors appear as
unknown, and child diagnostics and credential files never cross into the App.

Neither CLI currently exposes a native ACP mode. Install its standard adapter
explicitly in a terminal if the picker says **Available to install**:

```sh
npm install -g @agentclientprotocol/claude-agent-acp
npm install -g @agentclientprotocol/codex-acp
```

These are the current packages maintained at
[Claude Agent ACP](https://github.com/agentclientprotocol/claude-agent-acp) and
[Codex ACP](https://github.com/agentclientprotocol/codex-acp), successors to the
Zed-scoped packages. The bridge runs the installed `claude-agent-acp` or
`codex-acp` executable directly, pins it to the detected CLI, and never invokes
an installer or `npx`. To sign in, run `claude auth login` or `codex login`, then
reopen the picker. Restart the bridge if its PATH needs updating.
The current Claude adapter requires Node 22 or newer on that PATH; the App's
Node 20 checks use fake adapters and do not establish live adapter compatibility.

The choice is saved in this App origin's local settings and applies to new
chats. Existing project chats keep their original agent. Only external session
IDs are prefixed (`claude-code:` or `codex:`) at the bridge boundary, so native
IDs from different stores cannot collide; the prefix never reaches an adapter.
OMP's IDs and model default are unchanged. External agents use their own
default model; the OMP model list applies only to Astrid.

Every external turn receives the installed Astrid packaged profile from
`astrid --agent-profile-file`, the editor integration instructions, and the same
scoped editor context. Astrid skills installed by the setup guide remain
available to the local agent; chat never installs skills or changes global
agent configuration. Project associations, replay, cancellation, and terminal
and permission callbacks use the existing ACP bridge.

The external profile and media policy are prompt context, rather than an
adapter-enforced system policy. The OMP overlay that disables native image
tools applies to Astrid only. Permission requests retain the bridge's existing
host-side decisions; this change does not add an approval dialog.

Live verification after explicitly installing the adapters: reopen the picker,
start a new chat with each signed-in agent, read a disposable project's timeline
through Astrid, exercise a tool approval and cancellation, then reload and
continue each saved chat after selecting a different default agent.

The installed OMP build does not make sessions stored under a custom
`--session-dir` discoverable to a newly spawned ACP process. Astrid App therefore
does not emulate a registry or migrate those files; the canonical no-override
launch is the supported fresh-process path, while custom-directory sessions
remain an explicit same-process limitation.

## Editor context passed to Astrid

The launcher is deliberately project-agnostic. Astrid App does not put the selected
project or timeline in a process flag because one bridge process can serve
multiple tabs and the selection can change while a conversation remains open.

Each submitted editor turn contains a bounded, machine-readable
`<astrid_editor_context>` block with schema `astrid.editor-context/v1`. It carries
the current project ID/slug, timeline ID/name, the Astrid App deep link, a revision
for the captured selection snapshot, and selected clip/asset references. It
does not copy the full asset registry or private media URLs into the prompt.
Astrid should use its project, timeline, media, task, and run tools to read
fresh state before editing and saving. The block is refreshed on submission so
a project or timeline switch cannot leave the next request using stale editor
context.

## Canonical Runtime editor entry

The editor's canonical local data path is the existing authenticated Runtime
proxy, not the legacy Astrid REST timeline route. Start Astrid App with
`VITE_WORKSPACE_RUNTIME_URL` and `WORKSPACE_RUNTIME_TOKEN_FILE`, then open:

`/tools/video-editor?runtime=1&runtimeProject=<Runtime project_id>&runtimeTimeline=<timeline_id>`

For disposable Runtime setup, use the generated client's atomic
`createTimelineDocument` operation with the chosen project and timeline IDs.
Do not create the same timeline first with `createTimeline`; the Runtime
contract treats `createTimelineDocument` as the create-timeline-plus-document
operation and returns `409 timeline already exists` for a pre-created shell.
The ACP controls are available alongside this Runtime editor entry; their
connection and opaque session IDs remain tab-local.
