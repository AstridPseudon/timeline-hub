# Astrid App

The public app is at [astrid.haus](https://astrid.haus/). This repository contains the developer source for the web app.

## Run Astrid fully on your computer

Use this route to change the editor itself. The editor runs from source, with live updates when you edit it. Once dependencies are installed, it can open offline; online models and providers still need internet.

First install or repair Astrid with the official installer. Read the script before running it. It keeps existing projects, media, credentials and agent instructions.

macOS or Linux, in Terminal:

```sh
curl -fsSL https://astrid.haus/install | sh
```

Windows, in PowerShell:

```powershell
irm https://astrid.haus/install.ps1 | iex
```

Install Git and Node.js **20.19 or newer in the Node 20 release line**, then run these commands in Terminal or PowerShell:

```sh
git clone https://github.com/banodoco/astrid-app.git
cd astrid-app
npx -y npm@11 ci
npm run dev:local
```

Open **http://127.0.0.1:5180/tools/video-editor?connect=1** and confirm it shows Connected. Keep the terminal open. The launcher checks the Runtime's identity and compatibility, then proxies the editor's requests on the same address. Credentials stay in the local server; the browser needs no local-network permission. The existing Runtime door remains available to astrid.haus on the same computer.

- **Start later:** in this clone, run `npm run dev:local`. The launcher attaches to the installed Runtime or starts it using its recorded Python environment. If it asks for a repair, rerun the official installer.
- **Stop:** press Ctrl+C in that terminal. It stops the editor and its proxy, and any Runtime it started. A Runtime already running through the installer's login service keeps running, so astrid.haus remains usable.
- **Update the editor:** stop it, save or commit your source changes, then run `git pull --ff-only origin main`, `npx -y npm@11 ci` and `npm run dev:local`. If Git reports a conflict or divergence, keep your changes and resolve it before continuing.
- **Update the Runtime and agent:** use the [official update command](https://github.com/banodoco/astrid-agent/blob/main/docs/setup/troubleshooting.md#update-astrid), then restart the editor. Never delete the workspace to resolve a version mismatch.

Your clone is the editor's code. Edit it while the dev server runs to see changes through Vite's normal development workflow. If port 5180 is occupied, the launcher reports it; stop the program that owns it before starting Astrid.

## Develop the app

Use Node.js 20.19 or newer in the Node 20 release line and install the repository's dependencies. Start the app with an official Astrid installation, or a compatible `astrid-runtime` available on `PATH`:

```sh
npm install
npm run dev:local
```

The launcher attaches to a compatible Runtime or starts one, then prints the URL to open. Press Ctrl-C to stop the app and any Runtime it started. To select an existing workspace and checkout explicitly:

```sh
npm run dev:local -- --data-root <path> --runtime <astrid-runtime-checkout> --astrid <astrid-agent-checkout>
```

Use `--source-manifest <path>` to select an explicit Runtime source manifest. The corresponding environment settings are `ASTRID_RUNTIME_DATA_ROOT`, `ASTRID_RUNTIME_CHECKOUT`, `ASTRID_RUNTIME_PYTHON`, and `ASTRID_CHECKOUT`. For a paired relay session, add `--paired` (and optionally `--reset-pairing`) and configure `ASTRID_APP_PAIRED_RELAY_ORIGIN`, `ASTRID_APP_PAIRED_PRODUCT_ACTOR`, `ASTRID_APP_PAIRED_REALM_ID`, `ASTRID_PRODUCT_TOKEN_FILE`, and `ASTRID_APP_PAIRED_CONNECTOR_STATE`. For an isolated timeline preview with demo clips and a fake Runtime, use `npm run dev:editor`.

## Project documentation

- [Architecture overview](structure.md)
- [Compatibility and migration contracts](docs/governance/contracts/compatibility-shims.md)
- [Astrid public boundary](docs/governance/contracts/astrid-plan-a.md)
- [Video editor SDK](docs/video-editor-sdk/README.md)
- [Code quality guide](docs/code_quality_audit.md)
- [Agent instructions](CLAUDE.md)

## Contract and quality checks

Run the mapped checks with the repository's Node.js 20.19+ environment:

| Gate | Command | Live mapped surfaces |
|---|---|---|
| Contracts | `npm run test:contracts` | [`src/sdk/index.ts`](src/sdk/index.ts), [`src/tools/video-editor/index.ts`](src/tools/video-editor/index.ts), [`src/tools/video-editor/browser.ts`](src/tools/video-editor/browser.ts), [`src/tools/video-editor/testing.ts`](src/tools/video-editor/testing.ts), [`src/shared/components/ui/contracts/cn.ts`](src/shared/components/ui/contracts/cn.ts), [`src/shared/lib/errorHandling/runtimeError.ts`](src/shared/lib/errorHandling/runtimeError.ts), [`src/domains/generation/types/index.ts`](src/domains/generation/types/index.ts) |
| Architecture | `npm run test:arch` | [`scripts/quality/check-video-editor-sdk-imports.mjs`](scripts/quality/check-video-editor-sdk-imports.mjs), [`scripts/quality/check-sdk-no-barrel-imports.mjs`](scripts/quality/check-sdk-no-barrel-imports.mjs), [`config/governance/video-editor-sdk-import-allowlist.json`](config/governance/video-editor-sdk-import-allowlist.json), [`src/shared/lib/errorHandling/runtimeError.ts`](src/shared/lib/errorHandling/runtimeError.ts), [`src/integrations/supabase/client.ts`](src/integrations/supabase/client.ts), [`docs/governance/contracts/compatibility-shims.md`](docs/governance/contracts/compatibility-shims.md) |
| Integrated quality | `npm run quality:check` | [`src/sdk/index.ts`](src/sdk/index.ts), [`src/tools/video-editor/index.ts`](src/tools/video-editor/index.ts), [`src/tools/video-editor/browser.ts`](src/tools/video-editor/browser.ts), [`src/tools/video-editor/testing.ts`](src/tools/video-editor/testing.ts), [`scripts/quality/check-video-editor-sdk-imports.mjs`](scripts/quality/check-video-editor-sdk-imports.mjs), [`scripts/quality/check-sdk-public-exports.mjs`](scripts/quality/check-sdk-public-exports.mjs), [`scripts/quality/check-sdk-no-barrel-imports.mjs`](scripts/quality/check-sdk-no-barrel-imports.mjs), [`config/governance/video-editor-sdk-import-allowlist.json`](config/governance/video-editor-sdk-import-allowlist.json), [`config/governance/sdk-public-export-allowlist.json`](config/governance/sdk-public-export-allowlist.json), [`src/integrations/supabase/client.ts`](src/integrations/supabase/client.ts), [`src/shared/lib/errorHandling/runtimeError.ts`](src/shared/lib/errorHandling/runtimeError.ts), [`src/shared/components/ui/contracts/cn.ts`](src/shared/components/ui/contracts/cn.ts) |
| Family conformance (`quality:extension-family-conformance`) | `npm run check:extension-family-conformance` (also included by `npm run quality:check`) | [`src/sdk/video/families/familyDefinitions.ts`](src/sdk/video/families/familyDefinitions.ts), [`src/sdk/video/families/familyDefinitions.test.ts`](src/sdk/video/families/familyDefinitions.test.ts), [`src/sdk/video/families/conformanceGate.test.ts`](src/sdk/video/families/conformanceGate.test.ts), [`src/sdk/core/families/maturity.ts`](src/sdk/core/families/maturity.ts), [`src/sdk/core/families/conformance.ts`](src/sdk/core/families/conformance.ts) |
| Astrid conformance | `npm run check:astrid-conformance` | [`config/astrid-cli-surface/vendor.lock.json`](config/astrid-cli-surface/vendor.lock.json), [`config/astrid-public-boundary/bundle.json`](config/astrid-public-boundary/bundle.json), [`scripts/quality/lib/astrid-public-boundary.mjs`](scripts/quality/lib/astrid-public-boundary.mjs), [`scripts/quality/astrid-public-boundary.test.mjs`](scripts/quality/astrid-public-boundary.test.mjs), [`docs/governance/contracts/astrid-plan-a.md`](docs/governance/contracts/astrid-plan-a.md) |
