# Astrid rename map decisions

## Required early decision for C-MIGRATE M4

`BANODOCO_LOCAL_DATA_ROOT` becomes `ASTRID_RUNTIME_DATA_ROOT`. It selects the launcher's support tree (`runtime:banodoco_local/paths.py:47`), including the live film realm. The protocol CLI's separate `BANODOCO_RUNTIME_ROOT` becomes `ASTRID_RUNTIME_ROOT`; it selects the protocol CLI's root (`runtime:runtime_protocol/cli.py:45`). These remain distinct.

## Command ownership

The Runtime launcher owns the `astrid-runtime` console script (`runtime:pyproject.toml:15`). The Runtime protocol CLI's old `banodoco-runtime` command becomes `astrid-runtime-protocol`. Astrid's `astrid/runtime_cli.py` supplies a parser with `prog="astrid-runtime"` but has no console-script registration; its help label is the launcher's command name, not a second installed command.

## Product and repository identities

The App release manifest key `reigh` becomes `app` beside the distinct `astrid` key. Its release verifier's local `reigh` binding and the App archive directory follow the same distinction. Astrid's pinned-group `source_key="reigh:..."` becomes `app:...` beside native `astrid:...` keys (`astrid/core/timeline/shot_composition_migration.py:770,848`). The Runtime second-client fixture drops the redundant `REIGH, reigh` forbidden-symbol entries and retains `Astrid, astrid` (`runtime/conformance/second-client-core-v1.yaml:7`). These are identifier decisions under rule 2, not prose substitutions.

The App release owner list contains `reigh-on-call` beside `astrid-on-call` in one array (`app:scripts/quality/check-extension-ship-evidence.test.mjs:147`), so the former becomes `app-on-call`. The App ACP bridge fixture's `/tmp/reigh-project` becomes `/tmp/astrid-app-project`, distinct from pre-existing `astrid-project` DOM/test IDs. Its `scripts/reigh-project-chat.ts` import still follows the planned script path move to `scripts/astrid-project-chat.ts`. The service-worker fake origin `reigh.example` becomes `astrid-app.example`, distinct from an existing `astrid.example` schema-reference fixture. `reigh-acp` labels become `astrid-acp`: they identify the same bridge launched by the existing `dev:astrid-acp` npm command. The reserved command ID `reigh.test` and the pre-existing `https://astrid.test` browser origin are different namespaces; `rename.py` compares their suffixes globally, so this lexical collision is recorded as intended with that evidence.

Repository keys are scoped to repository-valued literals in the App contract schema and checker. In particular, `'Astrid'` becomes `'astrid-agent'` only as a quoted repository key in those two scripts and as `repository` or `publicProjectionOwner` in the two contract JSON files. Live `Astrid Runtime` product prose is not rewritten by those rows. The `Astrid-agent` URL regex is restricted to `github.com/peteromallet/` URLs.

`reigh-product-connector` is present in App runtime integration tests (`src/integrations/runtime/createDefaultTimeline.test.ts:149,190` and other App tests), contrary to `inventory.md:155`. The existing explicit row maps it to `astrid-product-connector`.

## Runtime names and Banodoco classification

Astra settled both old Runtime contract URI hosts: `banodoco.dev/workspace/v1/` becomes `astrid.haus/workspace/v1/`, and `banodoco.local/schemas/` becomes `astrid.haus/schemas/`. The latter also applies to Astrid's retained `docs/contracts/stage1-acceptance-evidence-v1.schema.json`. Paths and protocol versions stay intact. Runtime `x-banodoco-*` extension metadata keys become `x-astrid-runtime-*`; their `@banodoco/timeline-schema` values remain community package references. The `workspace-runtime` owner values in `runtime:contract/schemas/shot-composition.json` and its test become `astrid-runtime`.

The `banodoco.<domain>.v1` framed-hash namespaces in Astrid and Runtime release identity code are Runtime product identifiers and become `astrid_runtime.<domain>.v1`. The row is split by repo scope so it does not mechanically collide with package names that also become `astrid_runtime`. This changes hash domain separators intentionally; cutover regenerates dependent identities and digests rather than preserving old identifiers.

The retained App vision documents' `banodoco.video.travel@2` and `banodoco.image.generate@3` are community/provider examples by Astra's decision. Community package, website catalog, Discord, GitHub organization, logo, and vendored composition names are covered with reasoned regexes in `kept-banodoco.txt`. `astrid/core/execution/executor/banodoco_catalog.py` stays community-named; its `ASTRID_BANODOCO_*` environment keys become `ASTRID_RUNTIME_*` under rule 3. App's `ClipTypeExportRoute` literal `banodoco` names the community composition exporter, so it is kept only in its exact type/test contexts. Runtime worker pools, task types, and `BANODOCO` service-role log label are Runtime product names and map to Astrid Runtime forms.

`Banodoco` in split `"Application Support" / "Banodoco"` or JavaScript `join(...)` expressions is the Runtime support folder and maps to `Astrid Runtime` in the exact source/test files. This complements the whole-path row `Application Support/Banodoco`. It does not authorize a second support-root read; C-AS and C-RT must remove any legacy-read behavior their post-rename tests expose.

## Distinct environment values and intentional merges

`BANODOCO_LOCAL_OWNER_TOKEN` and `BANODOCO_RUNTIME_OWNER_TOKEN` remain distinct: `astrid:tests/stage1/test_final_cold_launch_matrix_luna.py:1377` clears both. `BANODOCO_LOCAL_RUNTIME_CHECKOUT` and `BANODOCO_RUNTIME_CHECKOUT` remain distinct: `astrid:tests/stage1/test_cold_launch_autobootstrap.py:489-491` assigns different hostile paths. `BANODOCO_ASTRID_SOURCE_CHECKOUT` is a third hostile fixture key and does not merge with `ASTRID_SOURCE_CHECKOUT` in that same test.

`BANODOCO_RUNTIME_ENDPOINT` and existing `ASTRID_RUNTIME_ENDPOINT` represent the same endpoint: `astrid/core/execution/generic_host.py:7377` exports `self.client.endpoint` and `astrid/packs/runpod/worker_process.py:1049` reads the connection endpoint. `BANODOCO_RELEASE_RECEIPT_ROOT` and `ASTRID_RELEASE_RECEIPT_ROOT` are read in the same receipt-root environment search (`astrid/core/release_identity.py:36`, `runtime/runtime_protocol/release_identity.py:16`). Their merges are recorded in `intended-merges.txt`; the duplicate receipt-root fallback entry must be removed in cutover fix-up code so no dual read survives.

`rename.py --report-merges` reports both many-to-one mappings and a single old token colliding with a pre-existing new token. `intended-merges.txt` therefore has evidence-backed one-old entries for the latter category; `map_selfcheck.py` accepts them while still checking every multi-old map output. The pre-existing `astrid-runtime` console script, for example, is the target for the old distribution and launcher names, and the scoped `workspace-runtime` repository/owner key now shares that product identity.

## Path census

A fresh `git ls-files` scan of the current checkouts found 8 old-name paths in Astrid, 15 in Runtime, and 71 in the App. Path rows cover every current Runtime path and every live old-name path in the other two checkouts. The remaining 4 Astrid paths are `.oracle/` or `artifacts/m4/` deletion candidates; the remaining 10 App evidence paths and 2 `reigh-data-fetch` paths are D-APP deletion candidates. The App's five `useReigh*` hook files in `adapters/reigh/` need both the folder move and a basename move, so the `path useReigh -> useAstrid` row covers their relative imports as well.

## Pending after the deletion PRs

The current pre-deletion checkouts still contain `.oracle/` and `.megaplan/` dated material that D-AS deletes. `map_selfcheck.py` currently reports 14 bare Banodoco occurrences there. Do not mark tokens `deleted` from the dated 17 Oct inventory until D-APP, D-AS, and D-RT merge and the manager provides fresh main-based checkouts. No deleted-only token is asserted yet.

`astrid:docs/testing/astrid-b12-source-authority-forensic-20260901.md:148-149` is dated evidence with an old Runtime support path. It is not in D-AS's listed deletions. The manager must include this file in the dated-evidence deletion, or decide another deletion route before the zero check; rewriting it would violate the evidence rule. The final dry run also awaits the manager's `$WORK/dry/` copies, N-TOOL's scripts, and baseline results.
