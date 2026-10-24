# Get help

Astrid is used at [astrid.haus](https://astrid.haus). If setup does not finish,
read the log at the installer's `Details:` path. Open Terminal on macOS or
Linux, or PowerShell on Windows, when you run an installer command below.

The supported setup commands are listed in [Getting Started](../getting-started.md).
For the default hosted route, cloning `astrid-app` is not a repair step.
For a source editor, follow the [fully local route](../getting-started.md#run-everything-on-your-computer).

## Asking for help

For help, open [Astrid issues](https://github.com/banodoco/astrid-agent/issues)
and attach the doctor bundle. By default, it is saved to your Desktop (or
Downloads if Desktop is unavailable) and its folder opens in Finder or File
Explorer. It contains installer logs and service states, with home paths, user
names, and secrets redacted. It excludes Runtime, chat, and service logs.

## Update Astrid

macOS and Linux, in Terminal:

```sh
curl -fsSL https://astrid.haus/install | sh -s -- --update
```

Windows, in PowerShell:

```powershell
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --update
```

## Make a support bundle

macOS and Linux, in Terminal:

```sh
curl -fsSL https://astrid.haus/install | sh -s -- --doctor
```

Windows, in PowerShell:

```powershell
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --doctor
```

The command prints the bundle path and opens its folder. If Astrid has not
finished installing or has already been removed, attach the install log
instead.

## Uninstall Astrid

macOS and Linux, in Terminal:

```sh
curl -fsSL https://astrid.haus/install | sh -s -- --uninstall
```

Windows, in PowerShell:

```powershell
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --uninstall
```

Uninstall keeps your workspace. Add `--delete-data` only when you intend to delete it too.

Developers working on the Python toolkit or Runtime can use the developer
commands in [Getting Started](../getting-started.md#developer-reference).
