# Viewing build instructions

These are the stable, user-facing commands for the Composition package. They
do not publish a package, certify a viewer, or close the physical parity gate.

## Supported setup

Use the existing supported environment request
`agent-remotion-viewing13-d0a5072b` for Node.js 20.19.4 and npm 10.8.2. Keep
shared installs read-only; use a private checkout/cache for any local work.
The immutable consumer artifact is Composition 0.0.13, 77 files, SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
Do not repack it or create a 0.0.14 archive in a consumer.

## Composition checks

From a clean Composition checkout:

```sh
cd /home/user/work/composition
make build
make test
npm run test:package -- /absolute/path/to/banodoco-timeline-composition-0.0.13.tgz
```

`make build` runs the generated-registry check, strict TypeScript/declaration
checks, and the ESM build. `make test` runs the repository suite. The package
smoke must receive the exact immutable 0.0.13 artifact; it checks public Node
imports, scoped registration/capabilities, peer identity, declarations, and
installed-file immutability. It does not prove browser pixels, Player audio,
or film parity.

The focused registry/test commands remain available when changing the package:

```sh
npm run gen-registry:check
npm run build:test
node --import ./typescript/tests/register-extensionless.mjs --test \
  typescript/test-dist/tests/registries.test.js \
  typescript/test-dist/tests/animations.test.js \
  typescript/test-dist/tests/scene-evaluation.test.js \
  scripts/gen-registry.test.mjs
```

`npm test` is equivalent to `make test`. Builds regenerate only the package's
own generated outputs; do not write through a shared `node_modules` or cache.

## Source-bound viewing route

The normal host route is:

```text
inherited_source(timeline_path, assets_path)
  -> _prepared_remotion_root
  -> prepareCompositionScene
  -> Root / querySceneFrame
```

The host supplies the accepted or candidate timeline and asset closure,
resolved theme/registries, canvas, and rational frame rate. Composition does
not load Runtime state or certify source authority. The private advisory Scene
path reports `UNAVAILABLE` for missing, stale, forged, or malformed source;
that result must not block save or rewrite authored data.

Saving remains renderer-free: commit, reload, retry, rebase, undo, and history
acceptance must work with Node, Root, and the renderer stopped. Preview and
Scene availability are separate reports.

These commands and route notes do not claim physical frame/audio parity,
macOS playback, owner-film viewing, or whole-project ZIP delivery. The explicit
normalized-mouth public13 physical case passed, but omitted-mouth default
compatibility is unproved and the private fallback remains. The old
independent-fade assertion remains live until public14 and the AM capability
are adopted as a qualified pair. Gate 6 request
`vw-m3-gate6-isolation-cleared-one-run-0251-e2e-viewing-gate6-built909-0240-1021025417-32009`
stopped before issuance at the central 10 GiB staging guard and is not parity
evidence.
Those limits are recorded in `design/viewing.md`.
