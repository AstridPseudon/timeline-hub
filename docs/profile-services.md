# Profile services

The active source profile can set `service_declaration` to the absolute path of
one agent-owned JSON file matching [`services.json`](../contract/schemas/services.json).
No field (or `null`) means no services. An explicitly configured missing or invalid
file refuses startup; Runtime never scans for installations or imports agent code.
The installer already links the declaring installed environment with
`runtime_environment`; services use that same environment, without a second
interpreter setting. A profile without it uses the current installed interpreter.

For example, the agent installer may write these source-profile fields:

```json
{
  "profile": "astrid",
  "runtime_checkout": "/install/lib/python3.11/site-packages",
  "source_checkout": "/install/lib/python3.11/site-packages",
  "runtime_environment": "/install",
  "service_declaration": "/install/lib/python3.11/site-packages/agent/services.json"
}
```

The declaration is versioned independently of the HTTP protocol:

```json
{
  "version": 1,
  "services": [
    {
      "name": "example-service",
      "argv": ["{python}", "-m", "example.service", "--support-root", "{support_root}"],
      "env": {"PYTHONUNBUFFERED": "1"},
      "restart": "always",
      "ready": {"file": "example-ready.json", "timeout_seconds": 30}
    }
  ]
}
```

Names must be unique, including case, and readiness files must be unique.
Commands are argv arrays, passed directly to process creation with no shell.
Runtime substitutes only entire argv elements and entire env values equal to
`{python}`, `{source_checkout}`, `{support_root}`, `{realm_root}`, `{realm_id}`,
or `{runtime_endpoint}`. Other strings pass through literally; there is no shell
or environment-variable expansion. The Python path keeps its virtual-environment
spelling (`Scripts/python.exe` on Windows, `bin/python` elsewhere), even when it is
a symlink. The working directory is `source_checkout`. Children inherit the
Runtime's environment, with Python import overrides and Runtime custody/Job
handoff variables removed; the selected environment's scripts directory leads
`PATH`, and declaration `env` additions are applied last.

`ready` is optional. Without it, a live process is running. With it, the service
owns the named file directly inside Runtime support (no directories). Runtime
removes the old file before each launch and after stopping the tree. The service
writes it atomically when ready; until then its state is `restarting`. Runtime
checks only that it is a regular file, so endpoint consumers still validate the
handshake contents. Readiness timeout is a failure and restarts the tree.

Both `run` and `up` start services after Runtime admission, discovery publication,
and listener startup. Services can read discovery and wait for their scoped
credentials as needed. Runtime does not grant additional credentials or start
worker execution through this declaration. Services own their child protocols.
Chat continues to use the existing support-folder `chat.json` handshake, with no
registration API. An agent may declare `chat.json` as its readiness file.

`always` restarts any exit; `on-failure` restarts nonzero exits, launch errors and
readiness timeouts. A successful `on-failure` exit is terminal (`failed`, last
exit `0`). Retry delays are 1, 2, 4, 8, 16, then 30 seconds, resetting after a
minute of stable running. Old descendants are stopped before a replacement
starts. Shutdown interrupts backoff, sends graceful tree termination, waits up
to five seconds, then forces remaining processes through the platform module
(process sessions on POSIX, Job Objects on native Windows).
Windows service children are launched without a console window.
For profiles with services, the outer `up`/`down` owner stop allows twenty
seconds for the supervisor and listeners to finish before escalating against
the Runtime itself; profiles without a declaration keep the existing wait.

The existing health response includes `services`, an array of `{name, state,
last_exit}` records, with state `running`, `restarting`, or `failed` and a nullable
integer exit code. Records also include `restart_count` and an optional fixed
`reason` code. Health's top-level status continues to describe Runtime admission;
a failing optional service does not make the Runtime disappear. `status --json`
preserves the same records under `health.services`. Command arguments and env
values are never included in status.

Each service writes stdout and stderr to `service-<name>.log` beside
`runtime.log`. Both use the same rotation policy: 5 MiB per file and three
backups (`.1` through `.3`), closing before renaming and retrying temporary
Windows sharing violations for a bounded interval. Restart Runtime
to apply profile or declaration edits.
