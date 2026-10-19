# Getting Started with Astrid

Install Astrid on this computer, then use it at
[astrid.haus](https://astrid.haus). Do not install or clone `astrid-app` to use
Astrid; that repository is for app developers.

On macOS or Linux, run:

```sh
curl -fsSL https://astrid.haus/install | sh
```

On Windows, open PowerShell and run:

```powershell
irm https://astrid.haus/install.ps1 | iex
```

Then open [astrid.haus](https://astrid.haus) and follow the on-screen steps.
For help, see [Troubleshooting](setup/troubleshooting.md).

Astrid Runtime runs on this computer and owns workspace projects, media,
timelines, tasks, and run records. Use Astrid at astrid.haus to work with them.

If an operator needs to restart the installed Runtime manually, use
`astrid-runtime up --profile astrid`. This is an operator recovery command, not
an alternative installation path.

## Developer reference

The rest of this repository contains source code and developer documentation
for the Astrid toolkit, capability packs, and Runtime integration. These are
for building or contributing to Astrid; they are not user installation
instructions. Start with [AGENTS.md](../AGENTS.md) for repository guidance,
[creating packs](packs/creating-packs.md) for pack development, and the
[architecture documentation](architecture/) for system design.
