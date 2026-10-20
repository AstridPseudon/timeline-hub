# Astrid App

The public app is at [astrid.haus](https://astrid.haus/). This repository contains the developer source for the web app.

## Develop the app

Use Node.js 20.19 or newer and install the repository's dependencies. Start the app with a compatible `astrid-runtime` available on `PATH`:

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
