# Current Agent public10 Node qualification

## Result

Qualified the current Agent source at `384918908aa8c75229c2b6ccdd8fda03b7ce24a1` against an isolated staged Remotion project. No product files were changed; the worktree is clean.

The current committed Composition artifact is the exact 77-member archive:

```text
remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz
sha256 cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7
sha512/base64 SmJAoem9f+86D+eO+PvBAz3JydlefpUUwcOOkG7SU9k2ZPKpjXLWKHm/N4424TO5HNQtCHMt5T6Jy2Y5zA6Ycg==
members 77
```

The staged project used current source/locks, the exact archive extracted with safe member/path validation, symlinked read-only peers from `/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`, and an exact local copy of only the CLI package because the readiness binder correctly refuses a CLI symlink whose real path escapes the project. No install, package mutation, source alias, fake fixture, network, browser, render, socket, or full suite was used.

## Pins and graph

```text
current SHA                         384918908aa8c75229c2b6ccdd8fda03b7ce24a1
Node                                v20.19.4 (/tmp/vw-m3-agent-gate-node20.19.4/bin/node)
npm                                 10.8.2
package                             @banodoco/timeline-composition 0.0.10
React / React DOM                   18.3.1 / 18.3.1
Remotion / media / layout-utils     4.0.509 / 4.0.509 / 4.0.509
```

The lock records the local Composition tarball and its exact SHA-512 integrity, plus the official npm registry records for the five pinned peers. The six historical target hashes from the earlier approval were checked against the borrowed graph:

```text
@remotion/player/dist/cjs/PlayerUI.js             5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb
@remotion/player/dist/cjs/use-player-methods.js   ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46
@remotion/player/dist/cjs/use-playback.js         6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0
@remotion/player/dist/esm/index.mjs                d3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12
remotion/dist/esm/index.mjs                        9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8
remotion/dist/cjs/audio/shared-audio-tags.js       471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c
```

Pre/post manifests were identical for all 21,455 borrowed graph files, all 2,900 tracked current-source files, the extracted 77 Composition files, and the archive. `tar --compare` also passed over all 77 archive members.

## Checks

All logs and staging are outside the product repo. The primary stage was `/tmp/vw-m3-current-public10-node-qualification.E8KI5k`.

| Check | Result |
|---|---|
| `remotion_install_problem(staged_project)` | PASS: `None` |
| `_runtime_inputs(staged_project, exact Node, installed schema, empty closure)` | PASS: 21,463 bound files; closure SHA `142fa3d2dbfd7189c3b28630ac6c0af85b7ff74d66aa1518126c746325bb23a2` |
| Existing pure Agent readiness/generator lane (`test_composition_package.py`, `test_remotion_v3_aliases.py`, element generation/target/coherence) | **16 passed, 2 deselected**, 9.97s |
| Actual ESM imports of `.`, `/evaluation`, `/theme-api`, `/registry.generated`, `/effects.generated`, `/animations.generated`, `/transitions.generated`, `/registries`; public scene preparation and React SSR | PASS under Node 20.19.4 |
| Actual current generated Root bundle with `@remotion/bundler`, current `src/index.ts`, generated host registries, and normal `remotionPrimitiveAliasesFor` | PASS; bundle `/tmp/remotion-webpack-bundle-qJ8RKg` |
| Strict NodeNext consumer (`tsc --noEmit --strict --skipLibCheck --module NodeNext --moduleResolution NodeNext --target ES2022`) importing the real public entries | PASS |
| Source/graph/archive postflight | PASS: identical manifests; clean `git status` |

## Honest limits

- The existing `remotion/__smoke__/bundle.mjs` reached the actual generated Root bundle but failed its pre-existing snapshot assertion because current generated types include `derivedFrom`, `media_id`, and `origin` in `_ASSET_ENTRY_ALLOWED`, while that smoke snapshot expects the older list. I did not alter the product or rewrite the test; the separate actual Root bundle probe passed.
- An exploratory `selectComposition` invocation was not used as evidence. Remotion entered its browser/server path and stopped on the sandbox's `uv_interface_addresses` error before completion, after printing its browser-download notice. No browser/render/socket qualification was attempted or claimed.
- No official launch-validation receipt, live Runtime admission, browser, renderer, audio/pixel, or full-suite evidence is claimed. Missing coherent live context remains unqualified rather than receiving a fallback grant.

## Exact commands

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= -m 'not integration' --basetemp=/tmp/vw-m3-current-public10-pure-pytest tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_remotion_v3_aliases.py tests/packs/rendering/test_remotion_element_generation.py tests/packs/rendering/test_effect_registry_target.py tests/core/test_pack_coherence_elements.py
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/vw-m3-current-public10-node-qualification.E8KI5k/remotion/public-exports-ssr.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --preserve-symlinks-main /tmp/vw-m3-current-public10-node-qualification.E8KI5k/remotion/root-bundle-probe.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/vw-m3-current-public10-node-qualification.E8KI5k/remotion/node_modules/typescript/bin/tsc --noEmit --strict --skipLibCheck --module NodeNext --moduleResolution NodeNext --target ES2022 /tmp/vw-m3-current-public10-node-qualification.E8KI5k/remotion/consumer.ts
tar --compare --file remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz --directory /tmp/vw-m3-current-public10-node-qualification.E8KI5k/remotion/node_modules/@banodoco
```
