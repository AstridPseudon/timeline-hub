# Astrid App local Astrid ACP bridge

The Astrid App ACP bridge is a user-machine process. It keeps only ephemeral
connection handles in memory; each selected agent remains the authority for its
profiles, opaque session IDs, and session storage. The browser never receives the bearer
token or starts a child process.

The service belongs to [astrid-agent](https://github.com/banodoco/astrid-agent/blob/main/docs/reference/services.md).
The Runtime starts and supervises it from the agent's service declaration. It
runs with Bun 1.3.14, registers its loopback endpoint and private credential in
`chat.json` beside Runtime discovery, and removes its own registration on exit.
The bridge launches the installed `astrid` command; Astrid owns the packaged
profile, OMP build, credentials, and session identity.

For app development, use `npm run dev:local` with the configured Runtime.
`--astrid /absolute/path/to/astrid-agent` selects a local agent checkout for
app source resolution; the Runtime's source profile selects the services.
`--acp` remains accepted for existing launcher scripts. Chat starts with the
Runtime regardless of that flag. The app never launches an ACP bridge.

`ASTRID_ACP_SESSION_DIR` is optional. When omitted, the installed OMP build
owns its canonical cwd-derived session directory, allowing ACP session
listing/loading/resume to discover the same opaque session ID after a fresh
process starts with the same profile and cwd. An explicit absolute
`ASTRID_ACP_SESSION_DIR` remains a supported legacy override; existing data is
left in place, but OMP 17.3.5 ACP discovery does not search that arbitrary
directory in a new process, so use it only when the original process remains
live.

The local app's discovery proxy re-reads the agent's `chat.json` for every
ACP request, including after chat restarts or credential rotation. Missing or
invalid registration returns `acp_unavailable`. The hosted page reaches chat
through the Runtime door; both paths retain the credential and protocol header.

The existing `/api/astrid` REST routes remain on the Astrid bridge port. ACP
requests use `/api/astrid/acp`, which the Vite proxy forwards to the local ACP
bridge with the existing bearer boundary and protocol header. The browser
controls create, resume, cancel, close, and reconnect sessions, but do not
persist connection or session IDs. Reconnect while the host is live reuses the
same ACP process and opaque session authority; it does not create a second
session registry.

## Agent readiness and selection

The New chat menu reads `GET /acp/agents` whenever it opens and when the window
regains focus. The bridge finds `claude` and `codex` on the person's login-shell
PATH (`$SHELL -lic`), then falls back to its own PATH. It asks
`claude auth status` (with a text fallback) and `codex login status` whether
each is signed in. Claude Code uses your Claude login; Codex uses your Codex
CLI login, including ChatGPT. Unknown sign-in counts as ready. Status errors
and child diagnostics never cross into the App.

The service reports one state per agent: **Ready**, **Sign in**, or
**Not installed**. A ready row starts a chat. Clicking either other row copies
its displayed recovery line and shows **Copied**. The lines are:

- Claude Code sign-in: Run `claude auth login`, then come back.
- Claude Code not installed: Install with `curl -fsSL https://claude.ai/install.sh | bash`.
- Codex sign-in: Run `codex login`, then come back.
- Codex not installed: Install with `npm install -g @openai/codex`.
- Astrid without a signed-in provider: Run `omp`, then `/login`.

OpenAI documents the Codex CLI install command in its [Codex setup guide](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex).
Use the same `--profile` as the bridge when configured.

The bridge launches each ACP adapter through Bun, pinned in
the agent’s `astrid/chat/astrid-local-agent-adapters.ts`:

```sh
bun x --bun @agentclientprotocol/claude-agent-acp@0.93.0
bun x --bun @agentclientprotocol/codex-acp@2.2.2
```

The first chat caches the adapter (about 250 MB for Claude Code and 330 MB for
Codex with native binaries). Bun's `--bun` runtime handles Claude's Node 22
requirement. The bridge passes the detected Claude executable as
`pathToClaudeCodeExecutable` and Codex as `CODEX_PATH`, so both adapters use the
person's installed CLI and login. The app does not install either CLI. While a
chat starts, the menu reports **Getting Claude Code ready…** (or the chosen
agent); a failed start shows **Claude Code didn't start.**, its details, and
**Try again**.

The header shows plain text such as `Claude Code · Sonnet 4.5`, with the
tooltip “To use another model, start a new chat.” Model choice is available in
the New chat menu. Existing model-list plumbing remains in place: Astrid's
provider catalog is loaded from `astrid agent models --json`, and Claude Code
and Codex lists are remembered after a session reports them.

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

The ACP adapters are resolved with Bun at the pinned versions in the bridge
launch path; no separate adapter install is needed. Live verification on the
owner's Mac: reopen the picker and start a prompt with each signed-in agent.

The installed OMP build does not make sessions stored under a custom
`--session-dir` discoverable to a newly spawned ACP process. Astrid App therefore
does not emulate a registry or migrate those files; the canonical no-override
launch is the supported fresh-process path, while custom-directory sessions
remain an explicit same-process limitation.

## Sharing a chat between tabs

The bridge keeps one native ACP session for every live chat, across all three
agents. A second tab loading that chat follows the existing host's transcript
and updates without opening another native writer. Each browser connection
has its own event queue, so polling one tab never drains another tab's stream.

The follower shows **Active in another tab — take over**. Takeover transfers
write permission immediately; a running turn continues on the same native
session. The former writer becomes a follower, and the new writer waits for
the running turn to finish before sending another message. Only the current
writer can change session settings or cancel its turn. A submitted request ID
is retained with its native operation, so a retry joins that operation instead
of sending it again.

The shared state reports the running request ID separately from a durable
history receipt. A saved queued row for that request shows **In progress in
another tab**, and cannot be retried while it is running. Following a turn or
taking over never automatically dispatches saved queued messages.

Closing the original tab retains its native host while other tabs still use
the session. The bridge releases it when no attached client or running request
needs it. This sharing is scoped to one bridge process; native agents continue
to own durable transcripts after a bridge restart.

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
