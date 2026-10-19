# Reuse an existing local Runtime from the hosted editor

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
