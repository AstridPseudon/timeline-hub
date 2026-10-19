# Set up Astrid

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

Then open [astrid.haus](https://astrid.haus) and follow the on-screen setup
steps. The [setup checklist](SKILL.md) gives agents the same instructions.

Developers building Astrid's toolkit, packs, Runtime integration, or local app
should use the developer documentation in the relevant repository. Those build
instructions are not user installation paths.
