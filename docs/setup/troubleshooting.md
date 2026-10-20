# Get help

Astrid is used at [astrid.haus](https://astrid.haus). If setup does not finish,
keep the message shown by the installer and the page, then follow the
instructions there or contact the person who provided the installer.

The supported setup commands are listed in [Getting Started](../getting-started.md).
Do not clone or install `astrid-app` to troubleshoot a user installation.

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

The command prints the bundle path. If Astrid has not finished installing or
has already been removed, attach the install log instead.

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
