---
name: astrid-setup
description: Set up Astrid on a new or existing machine, verify its Runtime connection, and help the user begin.
---

# Set up Astrid

Help the user install Astrid on this computer and open the product at
[astrid.haus](https://astrid.haus). Do not ask them to clone, build, or install
`astrid-app`; that repository is for developers.

First identify the operating system and check whether an Astrid installation
already exists. Preserve existing work. For a new installation, give the user
the matching command from [Getting Started](../getting-started.md):

- macOS or Linux: `curl -fsSL https://astrid.haus/install | sh`
- Windows PowerShell: `irm https://astrid.haus/install.ps1 | iex`

Then have them open [astrid.haus](https://astrid.haus) and follow its setup
steps. Carry out requested checks, report their actual results, and do not
claim a check passed when it could not be run. Do not provide a separate
manual install route or ask the user to install Astrid from a source checkout.

Once setup is complete, follow [Astrid’s core skill](../../astrid/packs/_core/docs/SKILL.md)
and the relevant pack for the work they want to do. Guide any provider
credential entry locally.
