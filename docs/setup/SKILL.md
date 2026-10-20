---
name: astrid-setup
description: Set up Astrid on a new or existing machine, verify its Runtime connection, and help the user begin.
---

# Set up Astrid

Help the user install Astrid on this computer and open the product at
[astrid.haus](https://astrid.haus). Do not ask them to clone, build, or install
`astrid-app`; that repository is for developers.

Run the install line for this operating system. It installs Astrid on a new
machine, repairs or restarts an existing installation, and keeps existing
work. Open Terminal on macOS or Linux, or PowerShell on Windows. Use the line
from [Getting Started](../getting-started.md):

- macOS or Linux: `curl -fsSL https://astrid.haus/install | sh`
- Windows PowerShell: `irm https://astrid.haus/install.ps1 | iex`

Then open [astrid.haus](https://astrid.haus) and follow its setup steps. Carry
out requested checks, report their actual results, and do not claim a check
passed when it could not be run.

If the installer fails, read the log at the printed `Details:` path. For help,
run the same install line with `--doctor`, attach the bundle, and follow
[Troubleshooting](troubleshooting.md#asking-for-help). For updates, see
[Troubleshooting](troubleshooting.md#update-astrid).

Once setup is complete, follow [Astrid’s core skill](../../astrid/packs/_core/docs/SKILL.md)
and the relevant pack for the work they want to do. Guide any provider
credential entry locally; never ask the user to paste a secret into chat.
