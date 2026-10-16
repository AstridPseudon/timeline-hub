# Astrid naming: execution plan

Status: ready to execute (v1; a simplicity review is being folded in). Drafted 2026-10-17 against `main` of Astrid `e766a7d8`, Runtime `569412c`, App `67f16daca`. Evidence tables are in [inventory.md](inventory.md); every old-name token is in [old-tokens.txt](old-tokens.txt) and the 79 collisions in [collisions.tsv](collisions.tsv).

This plan renames the three Astrid repositories and every name derived from the old ones. `peteromallet/Astrid-agent` becomes `peteromallet/astrid-agent`. `banodoco/reigh-app` becomes `banodoco/astrid-app`. `banodoco/banodoco-workspace-runtime` becomes `banodoco/astrid-runtime`. In code, "Reigh" becomes "Astrid" (or "App" where both exist), and "Banodoco" as a product name for the Runtime becomes "Astrid Runtime".

**Clean-break rule.** No aliases, shims, dual reads, fallback env vars, re-exports or compatibility periods. After cutover no file in any repo contains an old name. The only exceptions are two temporary migration modules and this plan, all deleted later.

**Complexity verdict.** Moderate: big but mostly mechanical. A script does the bulk; the hard parts are a short list of persisted data and lockstep cross-repo names.

The plan names the old names, so it is itself residue. The last task deletes it.

## Contents

1. Names and 2. Scope: what counts as an old name
3. How hard is this? (verdict, hard parts, effort, "Complexity you might be missing")
4. Approach
5. Mapping rules
6. Sequencing and the cutover window
7. How to run this
8. Tasks (Phase 0 prep, Phase 1 cutover, Phase 2 after)
9. Owner checklist
10. Done when
11. Open questions

---

## 1. Names

| Today | New | Note |
|---|---|---|
| `peteromallet/Astrid-agent` (the old `peteromallet/Astrid` already redirects to it) | `peteromallet/astrid-agent` | Case-only change, for family consistency. Moving it into the `banodoco` org is the owners' call and out of scope. |
| `banodoco/reigh-app` | `banodoco/astrid-app` | |
| `banodoco/banodoco-workspace-runtime` | `banodoco/astrid-runtime` | |

**Why `astrid-runtime` and not `astrid-workspace-runtime`.**
- No recorded reason for "workspace" exists. The earlier Codex plan (10 to 11 Oct) proposed `astrid-workspace-runtime`, but its rationale was never written down. The only hint is the seed commit `ba511c4f79` calling it a "neutral workspace runtime for Astrid and Reigh".
- "Workspace" meant the Runtime was neutral between two products. Reigh is now the Astrid App, so that no longer motivates the repo name.
- The user-facing command is already `astrid-runtime`. Runtime `pyproject.toml:15` maps it to the launcher, and Astrid runs `astrid-runtime up` (`astrid/setup.py:291`).
- The neutral protocol keeps its names: `workspace.v1`, `WorkspaceClient`, `runtime_protocol`, `/v1/` routes. Only product packaging changes: distributions, launcher package, client packages, CLI, env vars, support folder.
- The Runtime's neutrality tests do not stop this. `tests/test_contract_fixtures.py:13` scans only `conformance/fixtures/*.json` and `:60` scans only `conformance/fake-second-product.ts`. Neither reads `pyproject.toml`, `README.md` or package names (verified). The `forbidden_symbols` line in `conformance/second-client-core-v1.yaml:7` is documentation and is not enforced. The Runtime `README.md` already says "Astrid" and "REIGH" (lines 3, 11, 12, 96), so N-MAP and C-RT must keep that sentence true: the protocol and fixtures stay product-free, the packaging may say Astrid.

**Why `astrid-agent` and not `astrid`.** The repo holds the `astrid` Python package and CLI, but also `scripts/`, `planning/`, `evals/`, `remotion/` and docs. The GitHub URL is already `Astrid-agent`, and `docs/setup/release-recipe.md` calls it the "Astrid client/toolkit". The inside names (package `astrid`, CLI `astrid`) do not change, so `astrid-agent` costs one case change and avoids a second rename.

## 2. Scope: what counts as an old name

**Old (the zero check fails on these, case-insensitive unless noted):**
- `reigh` in any case and any position (`Reigh`, `REIGH`, `ReighExtension`, `useReighShotsHost`, `reigh_live_scene_request`).
- `banodoco-workspace-runtime`, `banodoco-workspace-client`, `banodoco_workspace` (covers `banodoco_workspace_client` and `banodoco_workspace_runtime`).
- `banodoco_local`, `banodoco-local`, `banodoco-runtime`.
- Env vars containing `BANODOCO_`, including `ASTRID_BANODOCO_*`.
- `@banodoco/workspace-client`.
- `Application Support/Banodoco`, `Banodoco Workspace`.
- `peteromallet/Astrid` not followed by `-agent`.
- The bare key `workspace-runtime` used as a repo name (App `scripts/quality/lib/astrid-contract-schema.mjs:10`). N-MAP decides each hit; protocol names such as `WORKSPACE_RUNTIME_URL` are not repo names.

**Not old (the zero check must not flag these):**
- The GitHub org `banodoco` in URLs of repos that keep their names: `banodoco-workspace`, `timeline-composition`, `timeline-schema`, `timeline-theme-2rp`, `hivemind`, `runpod-lifecycle`, `Wan2GP`, `Banodoco-website`, `ArtAgents`.
- The `@banodoco/timeline-*` package scope, and `banodoco-timeline-schema` (`astrid/pyproject.toml:53`).
- The Banodoco community, `public/banodoco-gold.png`, and the `banodoco-workspace` repo name (the community workspace, live: Astrid imports `banodoco_social` from it).
- Files such as `astrid/core/timeline/banodoco_schema.py` and `executor/banodoco_catalog.py`: a bare `banodoco` is not an old name. Their env vars (`ASTRID_BANODOCO_*`) are renamed; the module names stay. See Open questions.
- `astrid.haus`: already the new domain.

The zero check therefore uses exact patterns (section 4), never a bare `banodoco`.

## 3. How hard is this?

**Verdict: moderate. Big but mostly mechanical.** About 13k old-name lines and about 2,600 distinct tokens across the three repos (App 5,193 lines in 957 files; Astrid 5,597 in about 698, of which 4,333 are history; Runtime 24 `reigh` lines plus about 400 `banodoco`), plus the satellites.

**The genuinely hard parts**
1. "Reigh" and "Astrid" are today two different things. A blanket `reigh` to `astrid` makes 79 tokens collide with names that already exist (`reighCommit` next to `astridCommit`, `REIGH_ROOT` next to `ASTRID_ROOT`).
2. Users' persisted data: browser storage, realm timelines, Supabase rows, the support folder.
3. Lockstep cross-repo wire names and three generated copies of one client.
4. Hash-chained fixtures and evidence.
5. Deployed infra and secrets.
6. Satellite repos and CI pins.
7. The plan and its tools must disappear at the end.

**Effort (agent time unless stated)**

| Block | Estimate |
|---|---|
| Phase 0 prep, all tasks in parallel | about 1 day |
| Cutover window (freeze, apply, land, deploy, migrate) | hours to 1 day |
| Phase 2 cleanup | about 1 day |
| Owner time | 1 to 2 hours (GitHub, Supabase, Railway, secrets) |
| Waiting | a 30 day window before the migration modules are deleted |

### Complexity you might be missing

- **Satellite repos.** `reigh-worker` is still fetched by Astrid CI jobs `m7-release-candidate` and `python` at `efc2276d`, and `tests/integrations/test_c12_cpu_runtime_harness.py` imports its code. `m7-release-candidate` gates `m8-publication`. `reigh-worker-orchestrator`, `reigh-workspace` and `banodoco-workspace` also carry or are referenced by old names. (N-SAT)
- **"Banodoco" is the Runtime's product name well beyond the repo name.** Env vars (`BANODOCO_LOCAL_*`, `BANODOCO_RUNTIME_*`, `ASTRID_BANODOCO_*`: 27 names), the support folder, the launcher package `banodoco_local` (12 files), three client packages, two console scripts, and 418 `banodoco` lines in the Runtime.
- **Browser data and the same-origin constraint.** About 20 localStorage keys and 5 IndexedDB databases, including extension settings. Code on a new origin cannot read them. This project therefore must not change the App's origin.
- **Saved timelines and extension ids.** The clip type `com.reigh.astrid.liveScene` is validated by the Runtime on stored timelines (`runtime_protocol/store.py:1559`). Extension ids `com.reigh.*` (about 150 literals) key saved state and a Supabase CHECK constraint.
- **Agent-facing names.** 22 capability ids `reigh.*` in `config/astrid-capability-census.lock.json`, the wire tags `<reigh_live_scene_request>`, and skill text under `~/.local/state/astrid/skills`.
- **Local folders and agent configs.** `astrid-local/reigh-app`, `~/.codex/config.toml` trust keys, Hivemind scripts, review-tooling scripts.
- **R4 docs and Otto records.** About 90 old-name lines in R4 planning docs, which R4 workers will read.
- **Generated and digest-bound artifacts.** `SCHEMA_DIGEST`, pinned digests in the parity test, the capability census lock, and the registry hash in `release_identity.py`.
- **A tracked build artifact.** `banodoco_workspace_runtime.egg-info/` (5 files) is tracked in the Runtime.
- **The plan's own deletion.**
- **Hivemind knowledge content** probably mentions Reigh. Out of scope beyond its scripts. Flagged in Open questions.

## 4. Approach

### 4.1 The map is data
One machine-readable file, `tools/astrid-rename/rename-map.tsv` (in the Astrid repo), maps old token to new token, plus path renames. N-MAP produces it with every collision resolved by hand. Workers never invent names. A missing name is a change to the map, made by the map owner only.

Columns: `kind` (`token`, `path`, `regex`), `old`, `new`, `scope` (`all`, or a repo), `note`.

### 4.2 `rename.py`
`tools/astrid-rename/rename.py --repo <path> [--apply]`. It applies the map to file contents and to paths (`git mv`). It is:
- longest-match-first, case-aware (`reigh`, `Reigh`, `REIGH`, `ReighFoo`);
- idempotent (a second run changes nothing);
- dry-run by default, printing a diff summary;
- skipping binary files, `.git`, and an allowlist of temporary migration modules (section 4.7).

### 4.3 `check-zero`
`tools/astrid-rename/check-zero --repo <path> [--allow allowlist.txt]`. It fails on any old-name pattern in file contents or in tracked paths. Exact patterns (PCRE, case-insensitive):

```
reigh
banodoco[-_]workspace[-_](runtime|client)
banodoco_workspace
banodoco[-_]local
banodoco-runtime
\w*BANODOCO_
@banodoco/workspace-client
Application Support/Banodoco
Banodoco Workspace
peteromallet/Astrid(?!-agent)
```
plus the repo-key hits N-MAP lists for bare `workspace-runtime`. It never uses a bare `banodoco`. It has profiles: `main` (the three repos), `keep` (kept satellites such as `banodoco-workspace`, where only references to renamed repos count: it omits `BANODOCO_`), `local` (local tooling). The final allowlist is empty.

### 4.4 Regenerate, do not edit
Generated and digest-bound artifacts are regenerated from their source after `rename.py`. They are never hand-renamed:
- Runtime OpenAPI to clients: `contract/openapi/workspace-v1.yaml` through `generators/generate.py` (output paths hard-coded at `generate.py:23`). `SCHEMA_DIGEST` changes. Regenerate the Runtime copies, then the Astrid vendored copy and the App copy (`src/integrations/runtime/generated.ts`, `generated-contract-metadata.ts`) all from one Runtime SHA.
- `config/astrid-capability-census.lock.json` through `python -m astrid.core.execution.capability_ledger approve` (`capability_ledger.py:636-665`).
- The hash-chained fixture `tests/fixtures/timeline_visualize/desert_slice/assembly.jsonl` (N-CHAIN).
- `release_identity.py` registry digests: recomputed, not pinned as literals (verified: `component_registry_sha256` has no literal pin in Astrid; Runtime has a duplicate definition at `runtime_protocol/release_identity.py:107` and `:194`, the second shadows the first).
- The pinned values in `tests/stage1/test_vendored_workspace_client_parity_luna.py:35-39` and `banodoco_workspace_client/contract_metadata.py:4-5`.

### 4.5 Why this is merge-safe against R4 and Codex branches
R4 (`timeline-platform-r4`, projects A to J, 95 cards) has not started and has no branches on any origin. The rename lands before R4 wave 0, so nothing in flight conflicts. Any other branch open at cutover (Codex's, for example) runs `rename.py --apply` on itself, then merges. Because the rename is a script, there are no textual conflicts to resolve by hand, and a branch that adds new old-name text after the cutover is caught by `check-zero` in CI.

### 4.6 History policy
- Before cutover, tag the last pre-rename commit in every repo `pre-astrid-rename` and push the tag. That tag is the archive.
- History in the working tree is **deleted, not rewritten**. That covers `.oracle/`, `.megaplan/` done initiatives, dated plans, run logs, audits, release evidence of shipped releases, failed rc folders, `docs/slot-first-audits/`, `docs/local-runtime/reviews/`. Rewriting dated evidence would falsify it.
- If a live gate, test or script reads a history item, it is regenerated, or deleted together with the gate when the gate guards a finished release. The N-HIST task for each repo decides per item and lists it.
- Git history itself stays. It is not residue in the tree.
- GitHub redirects from old repo names stay. They are invisible in code, and the only way to kill them is a placeholder repo under the old name, which is worse residue.

### 4.7 Persisted-data policy
Migrate once, then delete the migration. A clean break without a migration silently loses user data.
- **Browser storage (App).** One isolated module `src/migrations/astridRenameBrowserMigration.ts` (final path set by N-BROWSER) runs at App start: copy old to new, verify, delete old. The zero check allowlists that one file for a window (default 30 days after deploy), then P-WINDOW deletes it. The service worker deletes the `reigh-v3` cache once inside the same module.
- **Runtime realms.** A one-time migration, run per realm at upgrade, rewrites current-state records only. Append-only ledgers, receipts and event history stay as they are. The code must not need to read old names from them. Deleted after the window.
- **Supabase rows.** A one-off SQL script, run once by the owner (N-SQL).
- **Support folder.** Moved with the Runtime's `relocate` command (and `backup`/`restore`), once per machine, as an operator step. No code fallback.
- **Env vars and secrets** on dev machines, CI and deployments: set under the new names in the cutover window (owner checklist).

### 4.8 How the plan deletes itself
P-FINAL runs the final `check-zero --allow /dev/null` on all repos and local tooling, tags every repo `astrid-rename-done`, then in one commit deletes `docs/plans/astrid-naming/` and `tools/astrid-rename/`. The tag keeps the plan reachable in history. After that deletion `check-zero` no longer exists, so P-FINAL records the passing output in the commit message.

---

## 5. Mapping rules

These are the binding rules. N-MAP turns them into `rename-map.tsv`.

1. **Reigh means the App.** Default: `reigh` to `astrid`, case preserved (`Reigh` to `Astrid`, `REIGH` to `ASTRID`).
2. **Collisions use `app`.** 79 tokens already exist with the new name and a different meaning (full table: [inventory.md section 7](inventory.md#7-collision-table)). Wherever the App and the agent repo are distinct concepts in the same context, the App becomes `app` / `App` / `ASTRID_APP_` / `astrid-app`. Examples: `reighCommit` to `appCommit`, `REIGH_ROOT` to `ASTRID_APP_ROOT`, `--reigh-commit` to `--app-commit`, `integrations/reigh` to `integrations/app`, `ReighElementKind` to `AppElementKind`, `checkReigh` to `checkApp`, `github.com/banodoco/Reigh` to `github.com/banodoco/astrid-app`. Repo references: `reigh-app` to `astrid-app`.
3. **Env vars.** `REIGH_*` to `ASTRID_APP_*`, `VITE_REIGH_*` to `VITE_ASTRID_APP_*` (collision-safe everywhere; 58 + 1 names). `BANODOCO_LOCAL_*` and `BANODOCO_RUNTIME_*` to `ASTRID_RUNTIME_*`. `ASTRID_BANODOCO_CATALOG_URL` to `ASTRID_RUNTIME_CATALOG_URL`.
   - Same-suffix pairs N-MAP must resolve (verified): `BANODOCO_LOCAL_OWNER_TOKEN` and `BANODOCO_RUNTIME_OWNER_TOKEN`; `BANODOCO_LOCAL_RUNTIME_CHECKOUT` and `BANODOCO_RUNTIME_CHECKOUT`. `ASTRID_RUNTIME_ENDPOINT` already exists (`astrid/packs/runpod/worker_process.py:1049`) and meets `BANODOCO_RUNTIME_ENDPOINT`. `ASTRID_RUNTIME_CUSTODY_*` exists and is kept.
   - The other five `ASTRID_BANODOCO_*` names (`AGENT_EXECUTORS`, `DEFAULT_EXECUTORS`, `EXECUTOR_CACHE`, `MANDATORY_EXECUTORS`, `REFRESH`) follow the same rule (`ASTRID_RUNTIME_*`) unless it collides. Flagged in Open questions.
   - `BANODOCO_URL` (App `HeroSection.tsx:15`), `BANODOCO_ASTRID_SOURCE_CHECKOUT`, `BANODOCO_RELEASE_RECEIPT_ROOT`, `BANODOCO_TIMELINE_SCHEMA_ROOT`: N-MAP decides. If a meaning is unclear, escalate; do not guess.
4. **Prose.** "Reigh" to "Astrid", or "the Astrid App" where the distinction matters.
5. **Specific names**
   - `ReighExtension` to `AstridExtension`; `@reigh/editor-sdk` to `@astrid/editor-sdk` (tsconfig alias: `tsconfig.json:15`, `tsconfig.app.json:23`, `config/vite/vite.config.ts:170`); `reigh-extension.json` to `astrid-extension.json` (21 example manifests, 5 fixtures, `config/contracts/reigh-extension.schema.json`).
   - Extension ids `com.reigh.*` to `haus.astrid.*` (reverse DNS of astrid.haus). `com.reigh.astrid.liveScene` to `haus.astrid.liveScene`. `com.reigh.astrid.live-scenes` to `haus.astrid.live-scenes`. The Supabase CHECK `^com[.]reigh[.]` becomes `^haus[.]astrid[.]`.
   - Wire tags `<reigh_live_scene_request|result|context>`, `<reigh_editor_context>`, `<reigh_element_operation>`, `<reigh_element_result>` to `<astrid_...>`. Schema ids `reigh.<x>/v1` to `astrid.<x>/v1` (keep `/v1`; after a lockstep cutover no reader of the old id exists).
   - Runtime control version `reigh.local-worker-control/v1` to `workspace.local-worker-control/v1` (neutral protocol family, `local_worker_composition.py:43`). It is sent and compared on a local control socket and not stored (verified).
   - Fingerprint prefix `reigh-fnv1a64-v1:` to `astrid-fnv1a64-v1:`. Verified: the prefix is prepended after hashing (`src/sdk/video/timeline/sourceMap.ts:223`), so the hash input is unchanged and migration only rewrites the stored string. Equality checks at `:315-316` compare full strings.
   - Runtime packaging: distribution `banodoco-workspace-runtime` to `astrid-runtime`; launcher package `banodoco_local` to `astrid_runtime`; Python client `banodoco_workspace_client` to `astrid_runtime_client` (distribution `banodoco-workspace-client` to `astrid-runtime-client`) in every copy: Runtime `packages/python/`, Astrid root `banodoco_workspace_client/`, generated code; TS client `@banodoco/workspace-client` to `@astrid/runtime-client`.
   - CLI: keep `astrid-runtime` (launcher). Delete `banodoco-local`, which maps to the same entry point (`pyproject.toml:14-15`). Rename `banodoco-runtime` (`runtime_protocol.cli:main`) by the rule "one command per entry point, prefixed `astrid-runtime`": `astrid-runtime-protocol`.
   - Support folder `~/Library/Application Support/Banodoco/` to `~/Library/Application Support/Astrid Runtime/` (`banodoco_local/paths.py:41,53,73`).
   - Actor ids `reigh-browser` (App `src/integrations/runtime/client.ts:349`), `reigh-product-connector`, `reigh-app:local-editor`, idempotency-key prefixes (`reigh.task.cancel-`, `reigh.render:v1/v2:`, `reigh.runtime.*`), CustomEvent names, `window.__REIGH_*` globals, localStorage keys and IndexedDB names follow rules 1 and 2.
   - Files: `scripts/reigh-acp-bridge.ts` to `scripts/astrid-acp-bridge.ts` (pin this name now for R4 project H), and the other `scripts/reigh-*` files; `adapters/reigh/` to `adapters/app/` (collision rule: `integrations/reigh` exists beside `integrations/astrid`).
   - Edge function `reigh-data-fetch`: deleted if no caller exists, else `astrid-data-fetch` (N-SAT/N-INFRA confirm). `project_id = "reigh"` in `supabase/config.toml:3` becomes `astrid-app` (local id only).
   - Capability ids `reigh.*` (22 in the census lock, 71 live refs in `capability_ledger.py:234-291`) become `astrid.*` unless a collision exists; N-MAP checks each.
   - Composition package `@banodoco/timeline-composition` is **unchanged** (not an old name). R4 project G pins it as is.
6. **The map is data** (section 4.1).

---

## 6. Sequencing and the cutover window

**This revises the 11 Oct order.** On 11 Oct the plan was "naming last, after R4 is completed and accepted" (`production/review/merge/CODEX-REPLY.md:321-325`). The user has now decided to do the rename first by asking for this plan. The reasons: R4 has not started and has no branches (inventory.md), so there is nothing to conflict with; doing it after R4 is the same work plus more old names written in the meantime.

**Cutover window.** A short merge freeze on the three mains, hours rather than days. Order:

1. Pre-checks pass (all Phase 0 tasks done).
2. Freeze. Tag `pre-astrid-rename` everywhere.
3. GitHub renames (owner). They come first because redirects make them zero-downtime.
4. Per-repo apply, three in parallel.
5. Cross-repo integration check.
6. Lockstep land: **Runtime, then Astrid, then App.** Pins updated in lockstep.
7. Deploy App, Supabase, Railway, secrets (owner), in the same window.
8. Run the realm and support-folder migrations.
9. Unfreeze.

**Why this landing order.** Astrid's vendored client and the App's generated copy derive from the Runtime SHA. Astrid CI fetches the Runtime by URL and SHA (`ci.yml:61,220`). The App CI checks out Astrid and the App by name (`bridge-latency.yml:34-39`). So the Runtime must exist first, then Astrid pins to it, then the App.

**Phase 2** follows: local tooling, R4 docs, satellite archiving, the post-window deletion of migration modules, the final zero check.

---

## 7. How to run this

This section is for the manager agent.

### 7.0 Models

| Use | Model | Where |
|---|---|---|
| **Normal** tasks: all `Route: normal` work, and every fan-out worker inside any task | **Haiku 5.5** (`claude-haiku-5-5`) | Most of the plan: the tools, the history lists, the per-repo apply and failure triage, local tooling |
| **XHARD** tasks | **Sonnet 5.5** (`claude-sonnet-5-5`) as the lead, handing the legwork to parallel Haiku workers and reviewing every diff against the invariant | N-MAP, N-BROWSER, N-REALM, N-CHAIN |
| Work that needs **taste or thoroughness** | **Opus 5.5** (`claude-opus-5-5`) | Reviewing the name map and `map-notes.md` before any apply (names are taste); all user-visible text: UI strings, README and install text, extension-author docs; the final pre-landing review of the three `rename/astrid` diffs in C-INT |
| `Route: owner` | a human with credentials | GitHub, Supabase, Railway, secrets, archiving |

The manager itself can be Haiku. Opus is used for judgment and review, not for bulk edits: brief it with the evidence, and have it fan out its own legwork to Haiku workers.

### 7.1 Phases and parallelism

| Phase | Tasks | Parallel? |
|---|---|---|
| 0 Prep, no freeze | N-MAP, N-TOOL, N-HIST-ASTRID, N-HIST-RUNTIME, N-HIST-APP, N-BROWSER, N-REALM, N-SQL, N-CHAIN, N-SAT, N-INFRA, N-LOCAL | All parallel except: N-TOOL needs the first map draft from N-MAP only for its tests (develop with a stub map); N-BROWSER, N-REALM, N-CHAIN and N-SQL start when N-MAP publishes the first map commit (they read it, never write it) |
| 1 Cutover, freeze | C-TAG, O-GITHUB, then C-RT, C-AS, C-APP (parallel), C-INT, C-LAND, O-DEPLOY, C-MIGRATE | Sequential gates; C-RT, C-AS, C-APP run in parallel after O-GITHUB, with a Runtime SHA hand-off (7.5) |
| 2 After | P-LOCAL, P-R4, P-SAT, P-WINDOW, P-FINAL | P-LOCAL, P-R4, P-SAT in parallel; P-WINDOW needs 30 days; P-FINAL last |

Phase 0 may start now. Nothing in it touches the three mains except by reviewed PRs to Astrid's `tools/astrid-rename/` and `docs/plans/astrid-naming/`.

### 7.2 Briefing a worker
The task block is the brief. Give the worker its block verbatim, plus: the path to this README, the path to `rename-map.tsv`, and the repo checkout it works in. Do not summarise the block. Workers see nothing else, so every block names its own paths, commands and stop conditions.

### 7.3 Fan-out inside a task
Route `normal` means one Haiku worker. A task may fan out many Haiku workers when it says so (for example the C-APP failure triage). Rules:
- Split by folder, one folder per worker, using the folder lists in the block. Never two workers on the same file.
- Workers fix only failures in their folder. A failure that needs a map change is returned to the task owner, not fixed.
- The task owner (the manager for `normal`, the Sonnet lead for `XHARD`) reviews every diff before it is committed.
- Route `XHARD` means a Sonnet lead who keeps the design and invariant, hands searching, reading, running and simple edits to as many parallel Haiku workers as the work splits into, and reviews every diff against the invariant. The lead lists each sub-agent in its report.

### 7.4 Stop rules
Stop and escalate to a human when:
- a name has no entry in the map and is not obviously covered by a rule in section 5;
- a collision is found that the map does not list;
- a check that "must be green" turns red after one correction cycle (two failed cycles mean a root-cause decision, not a third try);
- a task would delete a file that a live gate reads and the block does not authorise it;
- the Supabase CLI turns out to checksum migration file contents (N-SQL);
- any step would touch the `banodoco` org name, a kept satellite name, `workspace.v1` or the `@banodoco/timeline-*` scope.

Never guess a name. Never add an alias, shim, dual read, fallback env var or re-export, even temporarily, even "just for tests". Never edit a generated file by hand. Never rewrite dated evidence.

### 7.5 One writer per file
Each file or area has exactly one owner task (the **Owns** line). Tasks that share a file are ordered by **Depends on**, never run in parallel. Only N-MAP writes `rename-map.tsv`. Only N-TOOL writes `rename.py` and `check-zero`. Only the apply task of a repo writes that repo's tree during the freeze. Phase 0 tasks that produce modules for a repo (N-BROWSER, N-REALM, N-SQL) write only their own new files and commit them to a prep branch `prep/astrid-rename-<task>`; the apply task merges them.

**Runtime SHA hand-off.** C-RT ends by pushing its renamed branch and reporting `RUNTIME_SHA`. C-AS and C-APP regenerate their client copies from that SHA only. If the Runtime changes afterwards, both regenerate again.

### 7.6 Status
Keep one table in the manager's notes: task, state (`todo`, `doing`, `done (commit)`, `blocked (dep)`), commit. This plan is not edited while running; the status lives with the manager.

---

## 8. Tasks

Template: **ID**, **Route** (`normal`, `XHARD`, `owner`), **Depends on**, **Owns**, **Outcome**, **Steps**, **Acceptance**. XHARD adds **Invariant**, **Plausible mistake**, **Why it looks right**. In commands, `$ASTRID`, `$RUNTIME`, `$APP` are the three working checkouts and `$TOOLS` is `$ASTRID/tools/astrid-rename`.

### Phase 0: prep

#### N-MAP
- **Route:** XHARD
- **Depends on:** none
- **Owns:** `tools/astrid-rename/rename-map.tsv`, `tools/astrid-rename/map-notes.md` (Astrid repo)
- **Outcome:** the complete map, every collision resolved, every token in `inventory.md` covered or explicitly kept.
- **Steps:**
  1. Load `old-tokens.txt` (2,602 tokens) and `collisions.tsv` (79 collisions), both in this folder, as input.
  2. Write the rules of section 5 as `regex`/`token` rows, longest match first. Resolve all 79 collisions one by one using rule 2. A blanket `reigh` to `astrid` row exists only as the last row, scope `all`, after every collision is covered.
  3. Resolve the env var pairs listed in rule 3 by reading each use (`generic_host.py:7377-7378`, `tests/stage1/test_final_cold_launch_matrix_luna.py:1377`, Runtime `banodoco_local/cli.py:196,203,417`). Where the two names mean the same value, merge; where they differ, give them different `ASTRID_RUNTIME_*` suffixes.
  4. Add path rows for the old paths in inventory section 2 (`banodoco_local/` to `astrid_runtime/`, `adapters/reigh/` to `adapters/app/`, 21 `reigh-extension.json`, `scripts/reigh-*`, `ReighLoading.tsx`, and so on).
  5. Add the repo-key rows (`'reigh-app'`, `'Astrid'`, `'workspace-runtime'` in `scripts/quality/lib/astrid-contract-schema.mjs:10`, `check-astrid-contract-freeze.mjs:71,96,218`, `config/contracts/astrid-plan-a-c1.json`/`c2.json`): `astrid-app`, `astrid-agent`, `astrid-runtime`.
  6. Add the `Astrid-agent` to `astrid-agent` row, scope URLs only (7 lines in Astrid).
  7. Run a dry run: `rename.py` (from N-TOOL's stub) over copies of all three repos; run `check-zero` on the result. Zero residue except the files in the allowlist. Review the 200 most frequent output tokens for nonsense (`astrid-astrid`, `AstridAstrid`, a name that now equals an existing one).
  8. Write `map-notes.md`: every judgment call and every token deliberately left out, with the reason.
- **Invariant:** after the map is applied, no two distinct old names produce the same new name, and no new name equals a pre-existing different name in the same scope.
- **Plausible mistake:** accepting the blanket `reigh` to `astrid` for a token that has an `astrid` twin in a context where both appear (a struct with both `astridCommit` and `reighCommit`, a path with both `integrations/astrid` and `integrations/reigh`). The result compiles, the tests pass, and two things have silently merged.
- **Why it looks right:** the collisions are only visible by joining the old-token list against the new-token set per scope. Each hit reads fine alone.
- **Acceptance:**
  - `python3 $TOOLS/map_selfcheck.py` (written by N-MAP) exits 0: no duplicate `new` values from different `old` values within a scope, and every token in `12-old-tokens.txt` matches at least one row or appears in `map-notes.md`.
  - `awk -F'\t' 'NR>1{print $4}' $TOOLS/rename-map.tsv | sort | uniq -d` prints nothing.
  - Dry-run `check-zero` over the three renamed copies prints only allowlisted files.
  - An Opus 5.5 reviewer has read `rename-map.tsv` and `map-notes.md`, and every name it questioned is resolved and noted in `map-notes.md`.

#### N-TOOL
- **Route:** normal
- **Depends on:** none (stub map); final tests after N-MAP
- **Owns:** `tools/astrid-rename/rename.py`, `tools/astrid-rename/check-zero`, `tools/astrid-rename/tests/`, `tools/astrid-rename/allowlist.txt`
- **Outcome:** the two scripts described in section 4.2 and 4.3.
- **Steps:**
  1. `rename.py`: read the map, sort token rows longest first, compile case variants, apply to every tracked text file (`git ls-files`), skip binaries by NUL-byte sniff and the allowlist, then `git mv` path rows deepest first. `--apply` writes; the default prints counts per file. Print a per-repo summary line.
  2. `check-zero`: the patterns of section 4.3, over `git ls-files` contents and path names; `--profile main|keep|local`; `--allow file`; non-zero exit and `path:line:match` output on any hit. In `local` profile it walks given directories without git.
  3. `allowlist.txt` initial entries: `docs/plans/astrid-naming/`, `tools/astrid-rename/`, and (added later by their tasks) the browser and realm migration modules.
  4. Tests in `tools/astrid-rename/tests/`: idempotence (apply twice, second diff empty), case preservation, longest-match (`reigh-app` before `reigh`), path moves, allowlist skip, no change to `@banodoco/timeline-schema`, `banodoco-workspace` (the repo), `banodoco-timeline-schema`, `astrid-agent`, `peteromallet/Astrid-agent`.
- **Acceptance:**
  - `python3 -m pytest -q $TOOLS/tests` passes.
  - `printf 'banodoco-workspace @banodoco/timeline-schema banodoco_social\n' | $TOOLS/check-zero --stdin` exits 0.
  - `printf 'banodoco-workspace-runtime BANODOCO_LOCAL_HOME\n' | $TOOLS/check-zero --stdin` exits 1.

#### N-HIST-ASTRID
- **Route:** normal
- **Depends on:** none
- **Owns:** `tools/astrid-rename/history/astrid.txt` (deletion list), and during the freeze the deletions themselves in `$ASTRID`
- **Outcome:** an exact list of paths to delete in Astrid, and for each live reader of a deleted path, the fix.
- **Steps:**
  1. Start from `inventory.md` section 6. Candidate deletions: `.oracle/` (534 files, 4,097 old-name lines; no verified reader), `.megaplan/` done initiatives (27 files), `receipts/` (8), `findings/` (5), `docs/projects/` (58 files; handover and publication docs), `docs/plans/` (26), `docs/megaplan/loose-work-consolidation-plan.md`, `.astrid-convergence/` (3), `artifacts/` old-name files (`artifacts/m4/reigh-external-gate-disposition.json` and the six others).
  2. For every candidate, `git grep -nF '<path>'` outside the folder. Known live readers to handle: `scripts/reshape/check_repo_hygiene.py:37-39,82-84` (`ROOT_DIR_ALLOWLIST`, `.megaplan` paths), `scripts/reshape/m4_gate.py:75`, `m7_gate.py:43` (`DEFAULT_PLAN`), `scripts/reshape/stage1_acceptance.py:19-20` (`.astrid-convergence/stage1-evidence`), `tests/reshape/test_repo_hygiene.py:64,139,150,187`, `.github/workflows/ci.yml:34,35,42,91,97` (`artifacts/m7/`), `pyproject.toml:196`, `installed_artifact.py:458`.
  3. For each reader choose: (a) keep the folder and remove only the old-name files inside it; (b) delete folder and edit the reader; (c) delete folder and the gate, only if the gate guards a finished release. Record the choice and why. If (c) is chosen for anything under `m4`, `m7` or `m8`, stop and escalate.
  4. Write the list as `delete <path>` / `edit <path>: <what>` lines.
  5. List any remaining old-name file that is neither deleted nor handled by `rename.py` (for example `tests/fixtures/runaway_release/audio-reactive-v1.json:467`, an absolute `/Users/peteromalley/.../reigh-workspace/...` path: replace with a relative path).
- **Acceptance:**
  - Dry run: apply the list to a throwaway copy (`git worktree` or `cp -R`), then `python3 -m pytest -q tests/reshape` passes and `$TOOLS/check-zero --repo <copy>` reports only files that `rename.py` fixes.
  - Every `delete` line has a "readers: none" or the matching `edit` line.

#### N-HIST-RUNTIME
- **Route:** normal
- **Depends on:** none
- **Owns:** `tools/astrid-rename/history/runtime.txt`
- **Outcome:** the list for the Runtime.
- **Steps:**
  1. `git rm -r banodoco_workspace_runtime.egg-info/` (5 tracked files: PKG-INFO, SOURCES.txt, dependency_links.txt, entry_points.txt, top_level.txt), and add `*.egg-info/` to `.gitignore`.
  2. `CHECKPOINT.md`, `LOCAL_REVIEW_CHECKPOINT.json` (GitHub URLs to the old repos, branch `codex/combined-local-review-20261014`): delete both unless a reader exists; `git grep -n 'LOCAL_REVIEW_CHECKPOINT\|CHECKPOINT.md'` first.
  3. `contract/schemas/timeline-config.schema.provenance.json:12` (path `reigh-main-role-slice-20261009`, a historical receipt path): decide delete or replace with a neutral path; check `git grep` for the schema's readers first.
  4. `tests/test_astrid_activation_join.py:44-45`: hard-coded `/Users/peteromalley/Documents/reigh-workspace/...` path. Replace with a `tmp_path` fixture.
- **Acceptance:** dry-run copy, then `python3 -m pytest -q` in the copy passes; `$TOOLS/check-zero --repo <copy>` reports nothing outside what `rename.py` fixes.

#### N-HIST-APP
- **Route:** normal
- **Depends on:** none
- **Owns:** `tools/astrid-rename/history/app.txt`
- **Outcome:** the list for the App.
- **Steps:**
  1. Candidates (inventory section 6): `docs/extensions/evidence/` (137 files, 206 old-name lines; rc1 to rc3 are `failed-*.json` only, rc4 and rc5 are superseded), `docs/slot-first-audits/` (8 files, 256 lines), `docs/local-runtime/reviews/` (2), dated 2026-09 files in `docs/local-runtime/` (`02-reigh-plan.md`, `04e-reigh-worker-cutover-lane.md`, `2026-09-09-state-audit.md`, `05-next-stage-execution-20260909.md`), `docs/video-editor/reigh-branch-census-and-convergence.md`, and the old plans `docs/state_management_context_audit.md`, `docs/sqlite-only-local-runtime-plan.md`, `docs/video-editor-sprint3-followups.md`.
  2. Live readers to handle: `.github/workflows/slot-first-quality.yml:11` (path filter `docs/slot-first-audits/**`: remove the filter or the job if it only guards that folder), `scripts/quality/check-extension-ship-evidence.mjs:393-439` (sha256 against committed HEAD blob), `scripts/quality/lib/extension-external-evidence.mjs`, `scripts/quality/capture-extension-external-evidence.mjs:287`, `scripts/quality/check-extension-release-preflight.mjs:161`, `scripts/release/verify-rc4*`/`verify-rc6*` verifiers and their tests (8 + 3 + 2 hits), `.gitattributes:6`, `.gitignore:69,70`, `config/contracts/astrid-plan-a-c1.json:1222` (references `docs/plans/astrid-default-packs-and-skills/PLAN.md`).
  3. Decide per reader as in N-HIST-ASTRID. The `verify-paired-release-e2e.mjs:3892` generator writes `reigh-build.log`, `reigh-npm-ci.log` and `extension-ship-quality-rc*` names that the rc verifiers and tests read: either rename generator and readers together (the map handles it) or delete the finished-release verifiers and their tests. Record which.
  4. `docs/design/*-2026-10-05.md` (7 files, live-ish): keep and rename by `rename.py`; they are not history.
- **Acceptance:** dry-run copy; `npm run test:extension-ship-verifier` (script at `package.json:56`) passes or is removed with its verifiers, `npx vitest run src/sdk` passes, and `$TOOLS/check-zero --repo <copy>` reports nothing `rename.py` cannot fix.

#### N-BROWSER
- **Route:** XHARD
- **Depends on:** N-MAP (first map commit)
- **Owns:** new file `src/migrations/astridRenameBrowserMigration.ts` plus its test and one call site in the App entry (`src/main.tsx`, verify the entry file) on branch `prep/astrid-rename-browser`; `public/sw.js` cache cleanup lines
- **Outcome:** a one-time App-start migration that copies every old persisted browser key to its new name, verifies, deletes the old, and removes the `reigh-v3` cache.
- **Steps:**
  1. Build the key table from `inventory.md` section 3 and re-verify each `path:line` against `$APP`. Read the new names from the map (do not compute them).
  2. Implement per store:
     - localStorage: copy exact keys and every key under the prefixes `reigh.ext.<id>.` (note the extension id inside the key also changes: `com.reigh.*` to `haus.astrid.*`), `reigh.ext-state.`, `reigh-hidden-shots:`, `reigh:transcript-draft:`, `reigh.runtime.media-import.v1:`; the 6 `reigh.ext.state.*` keys; `reigh.dev-extensions.disabled` (a JSON array of extension ids: rewrite the ids inside the value).
     - The `showDataLanesByKind` preference value containing kind id `reigh.transcript` (`useEditorPreferences.ts:64,141`): trace its backend first (unverified), rewrite the id inside the value.
     - IndexedDB: `reigh.extension-state`, `reigh.timeline-drafts`, `reigh.sync-ledger`, `reigh.ext-proposals`, `reigh.local-media` (store `reigh.local-media-handles`). Copy records to the new DB with the same store layout. `reigh.local-media` holds `FileSystemHandle`s: structured-clone them into the new DB and verify each still resolves (`queryPermission`); if a handle cannot be cloned, keep the user's media list and mark the entries as needing re-import. Never drop silently.
     - Cache Storage: `caches.delete('reigh-v3')` once. Update `public/sw.js:1,14,63,74,90`, `index.html:141` and `src/test/serviceWorkerRegistration.test.ts:53` to the new cache name.
  3. Order per store: read old, write new, read new back and compare, delete old, only then record a completion marker `astrid.rename-migration.v1` (itself a new-name key). If any step fails, leave old data in place and retry on next start. No dual read: after the marker is set, no code reads an old name.
  4. Test with jsdom and `fake-indexeddb`: a populated old state migrates to equal new state; running twice is a no-op; a failure mid-way leaves old data intact; extension settings (which may hold API keys) survive byte-for-byte.
  5. Add the module and its test to `tools/astrid-rename/allowlist.txt` with the removal date in a comment.
  6. The App's origin must not change in this release. Add an assertion test that `PREVIEW_ALLOWED_HOSTS` still contains `astrid.haus` and write the same-origin constraint into the module header comment.
- **Invariant:** every value a user stored under an old name is readable under the new name after the first start, and no code path reads an old name after the marker is set.
- **Plausible mistake:** renaming the key constants (which `rename.py` does anyway) and writing the migration to read the "old key" from those same constants, so the migration reads the new names and copies nothing. Second: migrating keys but not the extension id embedded inside keys and values, so settings sit under `haus.astrid.x` keys that the extension never finds under its old `reigh.ext.com.reigh.x.` pattern.
- **Why it looks right:** the tests pass if they seed the new names. The migration file is the one place that must hold old names as string literals, which is why it is allowlisted and excluded from `rename.py`.
- **Acceptance:**
  - `npx vitest run src/migrations` passes.
  - `$TOOLS/check-zero --repo $APP --allow $TOOLS/allowlist.txt` passes after `rename.py` on a copy, and the migration file is the only allowlisted file containing `reigh`.
  - `git grep -n "reigh" -- src ':!src/migrations'` on the renamed copy prints nothing.

#### N-REALM
- **Route:** XHARD
- **Depends on:** N-MAP (first map commit)
- **Owns:** new files in the Runtime: `banodoco_local/` (after rename `astrid_runtime/`) `astrid_rename_realm_migration.py`, its tests, and a branch `prep/astrid-rename-realm`
- **Outcome:** a one-time migration, run per realm at upgrade, that rewrites current-state records and nothing else.
- **Steps:**
  1. Inventory what each realm stores (verified starting points): `com.reigh.astrid.liveScene` in `project_documents.content_json` (`canonical_schema.py:125`) via validation at `store.py:1550-1565` and `visual_seam.py:23`; extension ids and `reigh.transcript_segment/v1` keys (`sourceItemsBySchemaRef`) inside timeline JSON; fingerprint prefix `reigh-fnv1a64-v1:` inside stored provenance (`sourceFingerprint`, `outputFingerprint`); `project_selections.actor_id` and `command_idempotency` rows containing `reigh-browser` or `reigh.*` keys; `reigh.editor.timeline.<hex>` ids (`dataProvider.ts:1593`, unverified whether persisted).
  2. Classify every table (see `canonical_schema.py`): append-only and hash-chained (`events` `:54`, `timeline_events` `:276`, `timeline_revisions` `:153`, `internal_timeline_revisions` `:322` content-addressed by `content_digest`), versus current state (`tasks`, `runs`, `timelines` `:112`, `project_documents` `:125`, `user_preferences` `:131`, `project_selections` `:240`, `command_idempotency` `:194`, and the rest).
  3. Rewrite current-state rows only, in a single transaction per realm, after taking a verified backup with the existing `backup` command (`banodoco_local/cli.py:95-101`). Never edit hash-chained or content-addressed rows: that would break their hashes. Where the current head of a timeline is a content-addressed revision containing an old name, write a new revision through the Runtime's normal commit path so the head moves forward and the chain stays valid.
  4. Check whether any state is rebuilt by replaying events. The audit found no projector (`store.py` reads of `events` at `:2722, :2918-2919, :2949, :5357, :5786, :5795-5797` look like integrity checks; unproven). If replay exists anywhere, the migration must also rewrite what replay produces, or replay will resurrect old names. Report the result explicitly.
  5. Wire it to the existing `upgrade` command (`cli.py:108-111`) so it runs once per realm at upgrade and records a done marker. After it, no code reads an old name, including from ledgers.
  6. Tests: build a realm in a fixture with old names in every location above, run the migration, assert the new names in current state, assert untouched ledger rows are byte-identical, assert hash-chain verification (`store.py:5786` area) still passes, assert a second run is a no-op.
  7. Add the module and test to `allowlist.txt`.
- **Invariant:** after migration, a realm validates, renders and continues its hash chains, and no current-state record holds an old name. Ledgers are untouched.
- **Plausible mistake:** a global `UPDATE ... SET content_json = replace(content_json, 'com.reigh', 'haus.astrid')` that also hits content-addressed revision payloads or event rows. Every digest then fails verification, or worse, passes because the digest is recomputed over rewritten history.
- **Why it looks right:** the old name disappears from every row and `grep` is happy. The damage shows only in chain verification and replay.
- **Acceptance:**
  - `python3 -m pytest -q tests/test_astrid_rename_realm_migration.py` passes in the Runtime (after the C-RT rename of the package folder).
  - The test's chain-verification assertion passes on a migrated fixture realm.
  - `sqlite3 <fixture.db> "select count(*) from events where payload_json like '%reigh%'"` is unchanged before and after.

#### N-SQL
- **Route:** normal
- **Depends on:** N-MAP (first map commit)
- **Owns:** `supabase/migrations/20260823100000_create_extension_operational_analytics.sql` (edit in place), and the new one-off script `supabase/one-off/2026-astrid-rename.sql` (App, prep branch `prep/astrid-rename-sql`)
- **Outcome:** old names removed from the five migration files that contain them; a one-off production SQL script; confirmation about how the Supabase CLI treats edited migration files.
- **Steps:**
  1. **First verify** that the Supabase CLI tracks applied migrations by version only and does not checksum file contents. Evidence in the repo is only: apply method is `npx supabase db push --linked` (`CLAUDE.md:18`, `README.md:22`); no text mentions repair or checksums; the only reference to `schema_migrations` is `scripts/quality/check-schema-drift.mjs:133`. Read the CLI source for the installed version (`npx supabase --version`; read `internal/migration` in the CLI repo) and run `npx supabase db push --linked --dry-run` against a throwaway branch/local stack after editing a comment in a copy. If the CLI compares content hashes, **stop and report**.
  2. Edit in place: `20260506115000_seed_section3a_mode_aware_route_metadata.sql` (lines 4, 25, 26, 79, 80: comment and seed text; check that the seed strings are not looked up by value elsewhere), `20260524000000_revert_route_backend_gating_in_claim_and_counts.sql:44,49`, `20260524010000_drop_tasks_assert_claimable_trigger.sql:12`, `20260918000000_retire_legacy_generation_methods.sql:1,3`, and the CHECK at `20260823100000_create_extension_operational_analytics.sql:31`: `^com[.]reigh[.]` to `^haus[.]astrid[.]`. Fresh databases then get the new constraint.
  3. One-off script for production, run once by the owner: in one transaction, drop the old CHECK on `extension_operational_events.extension_id`, `UPDATE` rows `set extension_id = regexp_replace(extension_id, '^com\.reigh\.', 'haus.astrid.')`, re-add the CHECK with the new prefix. Print row counts before and after. The script uses the old name as a string, so it lives in the temporary migration area (allowlisted until P-WINDOW).
  4. `supabase/config.toml:3` `project_id` and the `[functions.reigh-data-fetch]` section (`:128`) are handled by C-APP (rename or delete with the function).
- **Acceptance:**
  - `git grep -niE 'reigh' -- supabase/migrations` on the edited copy prints nothing.
  - On a local Supabase stack (`npx supabase start`, `npx supabase db reset` on the throwaway copy only): `insert ... extension_id = 'haus.astrid.x'` succeeds and `'com.reigh.x'` fails.
  - The report states the checksum finding in one sentence with its evidence.

#### N-CHAIN
- **Route:** XHARD
- **Depends on:** N-MAP (first map commit)
- **Owns:** `tools/astrid-rename/regen_desert_slice.py` (Astrid), and during the freeze the fixture files under `tests/fixtures/timeline_visualize/desert_slice/` and the frozen constants in `tests/core/timeline/test_timeline_visualize_hashes.py:42-44`
- **Outcome:** a script that rewrites the 145 old-name event lines of `assembly.jsonl` with the new actor id and recomputes `prev_hash` and `hash` for every line using the real hash code, plus updated companion files.
- **Steps:**
  1. Read the canonical hash code: `astrid/core/timeline/events/schema/serialize.py` (`canonical_json_bytes`, `sha256_hex` `:60-61`, `hash_embedded` `:64-77`, `with_event_hash` `:80-82`). Confirm in `types.py:360` (`to_json_obj`) whether `actor` is emitted and so hashed (unverified; assume yes).
  2. Write `regen_desert_slice.py`: parse each line into the event type, replace `actor` (`reigh-app:local-editor` to the map's new id) and display name (`Reigh local editor`), reset `prev_hash` to the chain's genesis or the previous line's new hash, recompute `hash` with `with_event_hash`, emit the line in the same canonical form. Use the library; never reimplement the hash.
  3. Update `assembly.head.json` (`head_last_hash`) and `assembly.identity.json`, and any digest the tests freeze (`test_timeline_visualize_hashes.py:42-44`; canonical digests of `assembly.json` and `registry.json` at `:66-79`). Search the other fixtures sharing the timeline ULID `01KYPVKMW5STB4W6FE05ED8242` (`desert_truth.json`, `adversarial/*/case.json`, `negative/*/fixture.json`, `tests/fixtures/v10/m7_representative.json`) for hash values derived from the chain.
  4. Verify the whole chain, not just the last hash: write an assertion (in the script and as a new test) that recomputes every `hash` and `prev_hash` from line 1. The existing test checks only the last hash (`:84-98`), so it would pass over a broken middle.
  5. `rename.py` must skip these fixture files (add the paths to its content-skip list); only this script changes them.
- **Invariant:** every line's `hash` equals the hash of its content and every `prev_hash` equals the previous line's `hash`, from genesis to head.
- **Plausible mistake:** string-replacing the actor in the file and fixing only the last hash and the frozen constants so `test_timeline_visualize_hashes.py` goes green, leaving 145 broken inner hashes.
- **Why it looks right:** the existing test does not recompute the chain, so it passes.
- **Acceptance:**
  - `python3 tools/astrid-rename/regen_desert_slice.py --check` exits 0 (recomputes the full chain).
  - `python3 -m pytest -q tests/core/timeline tests/packs/rendering -k "timeline_visualize or snapshot"` passes.
  - `grep -ci reigh tests/fixtures/timeline_visualize/desert_slice/assembly.jsonl` prints 0.

#### N-SAT
- **Route:** normal
- **Depends on:** none
- **Owns:** `tools/astrid-rename/satellites.md`; prep branches in Astrid and App that remove references
- **Outcome:** a verdict for each satellite and the reference-removal diffs.
- **Steps:**
  1. **`banodoco/reigh-worker`.** Decide whether any live deployment still uses it. Check: RunPod templates and images that clone it; the orchestrator's pod startup (`reigh-worker-orchestrator/gpu_orchestrator/runpod/worker_startup.template.sh:254-266` clones `banodoco/Reigh-Worker`); the user (ask via the manager; the user believes it is deprecated). Evidence so far: Astrid CI fetches it at `efc2276d30c22ac0cbe54f735a1129cef79583ef` in `ci.yml:64` (job `m7-release-candidate`) and `:223` (job `python`), with `REIGH_WORKER_CHECKOUT` at `:52,211`; `tests/integrations/test_c12_cpu_runtime_harness.py:36,44-45` imports `source.runtime.supervisor` and `source.runtime.worker.preflight` with no skip guard.
     - If **nothing live** uses it: prepare a branch that deletes `tests/integrations/test_c12_cpu_runtime_harness.py`, the two fetch steps and the `REIGH_WORKER_CHECKOUT` env lines (`ci.yml:52,63-65,211,222-224`), the comment at `astrid/packs/wan2gp/src/compiler.py:26`, and any remaining `REIGH_WORKER_CHECKOUT` use (9 lines). Check that no `needs:` in `ci.yml` (notably `m8-publication` at line 740) depends on a job that this empties. The repo is then archived (P-SAT, owner).
     - If **something live** uses it: rename it to `banodoco/astrid-worker`, treat it as a fourth repo in the codemod run, and update the pod template URL, the `REIGH_*` pod env contract (about 40 names) together with the orchestrator, RunPod volume names (`reigh-livetest-prebuilt-*`) and Astrid's pin. Escalate: this adds a C-WORKER task and the plan must be extended.
  2. **`banodoco/reigh-worker-orchestrator` and `banodoco/reigh-workspace`:** deprecated. Remove references: App `README.md:31` (links to both worker repos), Astrid `planning/gen_fal_storyboard.py:23` and `planning/gen_park24_storyboard.py:26` (read a key from a `reigh-workspace/reigh-worker/this.env` path: repoint or delete the scripts), `planning/build_park24_slice.py`, `astrid/packs/blender/deploy.py:391`, and the absolute `/Users/peteromalley/Documents/reigh-workspace/...` paths in `tests/integrations/test_generic_host_*.py`. Orchestrator is only blocked from archiving if `banodoco-workspace/banodoco-worker/` is still deployed on Railway: ask the manager to ask the owner.
  3. **`banodoco/banodoco-workspace`:** live, name stays. List its old-name hits that refer to renamed repos (`REIGH_SUPABASE_URL` in `banodoco-worker/README.md:33` and `worker_jwt.py:9`, `banodoco-worker/README.md:4-6`, stale Reigh-DB deployment docs, `README.md:82`). Prepare a PR to scrub them. Do not touch `BANODOCO_*` env vars that belong to the community workspace itself.
  4. **`timeline-schema`, `timeline-composition`, `timeline-theme-2rp`:** names stay. Scrub the comment hits (`timeline-schema/typescript/src/schemas.ts:118`, `tests/test_materialize_output.py:105`, `typescript/tests/resolveTheme.test.ts:58`; `timeline-composition/scripts/gen-registry.ts:13,38,55,184`; `timeline-theme-2rp` README:31). `provider: "reigh"` in timeline-schema is a data value: check whether anything persists it before changing it; if so, escalate.
  5. Wan2GP submodule branch `reigh-sprint-3` (`reigh-worker/.gitmodules`): list it; only matters if the worker is kept.
- **Acceptance:**
  - `satellites.md` has one verdict per satellite with `path:line` evidence.
  - On the prep branch: `git -C $ASTRID grep -nE 'reigh-worker|REIGH_WORKER_CHECKOUT|reigh-workspace' -- . ':!.oracle' ':!.megaplan'` prints nothing (if the worker is retired), and `python3 -m pytest -q tests/integrations` passes.
  - The ci.yml diff keeps `m8-publication` reachable: `grep -n "needs:" .github/workflows/ci.yml` shows no dangling job name.

#### N-INFRA
- **Route:** normal
- **Depends on:** none
- **Owns:** `docs/plans/astrid-naming/owner-checklist.md` input (the manager folds it into section 9), and the code references listed below on prep branches
- **Outcome:** an exact list of every deployed or external name, with the code change that goes with it, in cutover order.
- **Steps:**
  1. Confirm there is no live caller of the Supabase edge function `reigh-data-fetch` (`supabase/functions/reigh-data-fetch/`, `config.toml:128`, `functionName` at `index.ts:575`, `LOG_PREFIX` at `:8`): `git grep -n 'reigh-data-fetch'` in Astrid, Runtime, App and the satellites (previous result: only `.oracle/` history in Astrid, none in Runtime or App). If a caller turns up, the name becomes `astrid-data-fetch`. Otherwise the directory, config section, tests and `_shared` helpers are deleted.
  2. List env vars/secrets set outside the repos: Supabase secrets `REIGH_APPEND_SERVICE_URL`, `REIGH_APPEND_SERVICE_INTERNAL_TOKEN` (`supabase/functions/_shared/reighAppendService.ts:7-8`); Railway build var `VITE_REIGH_APPEND_SERVICE_URL`; any `VITE_*` and `REIGH_*` the owner has (the repo shows only `Dockerfile:31 ARG VITE_APP_ENV`); CI variables `BANODOCO_RUNTIME_CHECKOUT`, `REIGH_WORKER_CHECKOUT`; shell and launch-config `BANODOCO_*`.
  3. Railway: service `reigh-production` (host `reigh-production.up.railway.app` in `config/vite/policy.ts:7` `PREVIEW_ALLOWED_HOSTS`). Prepare the policy change to the new host. Domains `reigh.art`/`www.reigh.art` (`policy.ts:10-11`), `reigh.ai` (`supabase/functions/huggingface-upload/index.ts:594`, `config/contracts/reigh-extension.schema.json:3` `$id`), `reigh.app` (`config/contracts/astrid-plan-a-diagnostic-c2.schema.json:3` `$id`) are removed from code. What the domains themselves do is the owners' call.
  4. Public install surface: `src/pages/Home/publicAstridLinks.ts:4` (`REPOSITORY_URL`), `PublicAstridHeroCta.tsx:8` (`git clone https://github.com/banodoco/reigh-app.git`), `HeroSection.tsx:13` (`https://github.com/banodoco/Reigh`, capital R, probably dead), `README.md:16-17` (`git clone https://github.com/peteromallet/reigh`), `scripts/astrid-landing/prepare.py:249,306`, `prepare-public.py:132` (pinned `APP_COMMIT`). List each with the new URL.
  5. Supabase hosted project: confirm its ref is not named after the old name (only the local `project_id` is). It is not renamed.
  6. GitHub: for each of the three renames list what must be re-pointed after: workflow `uses:` (actions are not redirected on rename; there are none today to old repos, verify with `grep -rn 'uses: *\(banodoco\|peteromallet\)/' .github`), webhooks, deploy keys, Railway's GitHub link, Supabase's GitHub integration (reconnect), branch protection, and `gh repo view` confirming the target names are free (`banodoco/astrid-app`, `banodoco/astrid-runtime`, `peteromallet/astrid-agent` returned 404 unauthenticated; private repos would also 404).
- **Acceptance:** a Markdown checklist where every line is: system, exact old value, exact new value, who, order, verification command. `grep -c '^- \[ \]' owner-checklist.md` is at least 25.

#### N-LOCAL
- **Route:** normal
- **Depends on:** none
- **Owns:** `tools/astrid-rename/local-tooling.md`
- **Outcome:** an exact list of local files and folders that need changing after cutover, with the command for each.
- **Steps:** verify and extend this list (all paths are on the owner's Mac):
  - Skills: `~/.local/state/astrid/skills/claude/` and `.../codex/` (5 files each, identical): `packs/rendering/references/live-scenes-authoring.md` (12 hits), `pack-builder/SKILL.md` (9, links to `github.com/peteromallet/Astrid/blob/main/...`), `packs/rendering/SKILL.md` (3), `references/document-checkout.md` (2), `references/placeholder-voiceover.md` (1). These are generated from the Astrid repo (`astrid/skills/view.py:43` `_PACK_BUILDER_DOC_PREFIX`): the fix is to rebuild them from the renamed Astrid, not to edit them. Find the rebuild command in `astrid/skills/` and record it. `~/.codex/skills/astrid` is a symlink to the codex tree.
  - `~/.codex/config.toml` project-trust keys at lines 170, 188, 362, 401, 425 (`[projects."…/reigh-…"]`), keyed on directory paths: update when the folders are renamed.
  - Hivemind (`~/Developer/hivemind`): `hivemind_scripts/rehearse_embedding_pilot.py:47` and `rehearse_historical_backfill.py:90` (default `VIBECOMFY_ROOT=/Users/peteromalley/Documents/reigh-workspace/vibecomfy`, a path that does not exist: pre-existing bug, fix to an env var required). History files there stay.
  - `~/Developer/astrid-video/astrid-local/`: directory `reigh-app` (rename to `astrid-app`), `live-main/Runtime/` and `live-main/Astrid/` `LOCAL_REVIEW_CHECKPOINT.json` URLs, `live-main/Runtime/contract/manifest.json`, `contract/component-manifest.json`, `clients/typescript/component-manifest.json` (generator config), `labs/*/app/supabase/config.toml` and `vendor/timeline-schema/python/pyproject.toml` (vendored copies: regenerate from source), `env.sh` (no hits today, but it may set `BANODOCO_*` in the shell; check), top-level `*.sh`.
  - Review tooling: `~/Developer/astrid-video/production/review/merge/watch-codex.sh`, `watch-codex-once.sh`, and 9 of 11 `*.md` notes there.
  - Otto/portfolio records and `~/Developer/otto-program` projects that name the repos: list only; Otto records are not edited by this plan (see Open questions).
  - Shell profiles: `~/.zshrc`, `~/.zprofile`, `~/.config` for `BANODOCO_*` and `REIGH_*`.
- **Acceptance:** each entry has path, old text, new text, command. `grep -c '^|' local-tooling.md` is at least 20.

### Phase 1: cutover (freeze)

#### C-TAG
- **Route:** normal (needs push rights; if the agent lacks them, owner)
- **Depends on:** all Phase 0 tasks done and merged to their prep branches; freeze declared
- **Owns:** git tags only
- **Outcome:** `pre-astrid-rename` pushed on all three repos (and on every satellite that will be changed).
- **Steps:** for each repo `git fetch origin && git tag pre-astrid-rename origin/main && git push origin pre-astrid-rename`. Record the three SHAs; they must equal the checkout SHAs the prep tasks were verified against, or the manager reruns N-TOOL dry runs on the newer SHA.
- **Acceptance:** `git ls-remote --tags origin pre-astrid-rename` in each repo prints one line; the SHA equals `git rev-parse origin/main` at freeze.

#### O-GITHUB
- **Route:** owner
- **Depends on:** C-TAG
- **Owns:** GitHub settings
- **Outcome:** the three repos renamed. See the Owner checklist (section 9), items G1 to G6.
- **Acceptance:** `gh repo view banodoco/astrid-app --json name,url`, `gh repo view banodoco/astrid-runtime --json name,url`, `gh repo view peteromallet/astrid-agent --json name,url` succeed; `git ls-remote https://github.com/banodoco/reigh-app.git` still answers (redirect).

#### C-RT
- **Route:** normal (fan-out by folder allowed)
- **Depends on:** O-GITHUB, N-TOOL, N-MAP, N-HIST-RUNTIME, N-REALM, N-SAT
- **Owns:** the whole `$RUNTIME` tree during the freeze
- **Outcome:** the Runtime renamed, regenerated, tests green, pushed on a branch `rename/astrid`, `RUNTIME_SHA` reported.
- **Steps:**
  1. `git switch -c rename/astrid`; apply the history list (`history/runtime.txt`, including `git rm -r banodoco_workspace_runtime.egg-info`).
  2. `python3 $TOOLS/rename.py --repo $RUNTIME --apply`. This renames `banodoco_local/` to `astrid_runtime/`, `packages/python/banodoco_workspace_client/` to `packages/python/astrid_runtime_client/`, and rewrites `pyproject.toml` (`:3` name, `:12-15` scripts, `:15,21` packages), `packages/python/pyproject.toml:2`, `packages/typescript/package.json:2`, env vars, paths (`paths.py:41,53,73`), `CONTROL_VERSION` (`local_worker_composition.py:43`), the clip type (`store.py:1559`, `visual_seam.py:23`), and `README.md` (keep the neutrality sentence true).
  3. Delete the `banodoco-local` script line; rename `banodoco-runtime` per rule 5.
  4. Merge `prep/astrid-rename-realm` (N-REALM) and keep it allowlisted.
  5. Regenerate: update `generators/generate.py` output paths (`:23`, `:178-190`) via the map, then run it. Regenerate `runtime_protocol/contract_metadata.py`, `packages/python/astrid_runtime_client/{generated,contract_metadata}.py`, `packages/typescript/src/{generated,contract-metadata}.ts`, `clients/typescript/{generated,contract-metadata}.ts`. Never edit them by hand. Update `contract/manifest.json`, `contract/component-manifest.json` and `clients/typescript/component-manifest.json` generator config via the map.
  6. Fix tests (`tests/test_astrid_activation_join.py` etc.).
  7. Commit, push `rename/astrid`, report `RUNTIME_SHA`.
- **Acceptance:**
  - `python3 -m pytest -q` passes in `$RUNTIME`.
  - `python3 generators/generate.py && git diff --exit-code` (regeneration is a no-op).
  - `$TOOLS/check-zero --repo $RUNTIME --allow $TOOLS/allowlist.txt` passes.
  - `git ls-files | grep -iE 'egg-info|banodoco_local|reigh'` prints nothing.
  - `grep -n 'astrid-runtime\|banodoco' pyproject.toml` shows one `astrid-runtime` script and no `banodoco-local`.

#### C-AS
- **Route:** normal (fan-out by folder allowed)
- **Depends on:** C-RT (`RUNTIME_SHA`), N-CHAIN, N-HIST-ASTRID, N-SAT, N-SQL (none), N-MAP
- **Owns:** the whole `$ASTRID` tree during the freeze
- **Outcome:** Astrid renamed, pinned to `RUNTIME_SHA`, tests green, branch `rename/astrid` pushed.
- **Steps:**
  1. Apply `history/astrid.txt` deletions and edits.
  2. `python3 $TOOLS/rename.py --repo $ASTRID --apply` (skips the desert_slice fixture files). This moves `banodoco_workspace_client/` to `astrid_runtime_client/`, rewrites 37 importing `.py` files, `pyproject.toml:84` (`include = ["astrid*", "astrid_runtime_client*"]`), `ci.yml`, env vars (`journey.py:599,617`, `generic_host.py:13497`, `autobootstrap.py:127,143`, `docs/reference/env-vars.md:15`, `.env.example:20-21`), `release_identity.py:81,183`, `skills/view.py:43`, capability ids, docs and SKILL text.
  3. Re-vendor the client: copy `astrid_runtime_client/{__init__,generated,contract_metadata}.py` from the Runtime at `RUNTIME_SHA` (`cmp` must show identical). Update pinned values at `tests/stage1/test_vendored_workspace_client_parity_luna.py:35-39` and `astrid_runtime_client/contract_metadata.py:4-5` (renamed file) from the regenerated output.
  4. CI: in `ci.yml`, set the Runtime fetch URL to `https://github.com/banodoco/astrid-runtime.git` and the SHA to `RUNTIME_SHA` (lines 61, 220); rename env `BANODOCO_RUNTIME_CHECKOUT` as the map says; remove or rename the worker fetch as N-SAT decided (lines 52, 63-65, 211, 222-224).
  5. Regenerate `config/astrid-capability-census.lock.json` with `python -m astrid.core.execution.capability_ledger approve`. Update `tests/stage1/test_reigh_authority_absence.py` literals at `:15-17,36,39,79` in the same commit (it guards absence of the old integration; keep the guard, with new literals; rename the file via the map).
  6. Run N-CHAIN's `regen_desert_slice.py` and commit the fixture changes.
  7. `ASTRID_RUNTIME_CUSTODY_*` stay (both ends in this and the Runtime repo; no old name).
  8. Fix failures by folder (fan-out). Do not change assertions to pass; fix the code or the map.
  9. Commit and push `rename/astrid`.
- **Acceptance:**
  - `python3 -m pytest -q` passes (or the same subset CI runs; copy it from `ci.yml` job `python`).
  - `python3 -m pytest -q tests/stage1/test_vendored_workspace_client_parity_luna.py tests/core/timeline/test_timeline_visualize_hashes.py` passes.
  - `python3 tools/astrid-rename/regen_desert_slice.py --check` exits 0.
  - `$TOOLS/check-zero --repo $ASTRID --allow $TOOLS/allowlist.txt` passes.
  - `cmp -s $ASTRID/astrid_runtime_client/generated.py $RUNTIME/packages/python/astrid_runtime_client/generated.py && echo same` prints `same`.

#### C-APP
- **Route:** normal (fan-out by folder: the failure triage is the large part)
- **Depends on:** C-RT (`RUNTIME_SHA`), N-HIST-APP, N-BROWSER, N-SQL, N-INFRA, N-SAT, N-MAP
- **Owns:** the whole `$APP` tree during the freeze
- **Outcome:** the App renamed, typed, tested, built; branch `rename/astrid` pushed.
- **Steps:**
  1. Apply `history/app.txt`.
  2. `python3 $TOOLS/rename.py --repo $APP --apply`. This covers the 71 renamed paths (inventory section 2), identifiers (`ReighExtension` 283 uses, `ReighRuntimeClient` 146), tsconfig aliases, `vite` and vitest aliases (`config/vite/vite.config.ts:170`, `config/testing/*`), wire tags, schema ids, extension ids, env vars, storage keys, workflow, contracts, README.
  3. Copy the regenerated TS client from the Runtime at `RUNTIME_SHA` into `src/integrations/runtime/generated.ts` and `generated-contract-metadata.ts` (regenerate; do not hand-edit).
  4. Merge `prep/astrid-rename-browser` and `prep/astrid-rename-sql`.
  5. Edge function: delete `supabase/functions/reigh-data-fetch/` and the `config.toml` section if N-INFRA found no caller (else rename to `astrid-data-fetch`). Rename `_shared/reighAppendService.ts` and its env vars (`ASTRID_APP_APPEND_SERVICE_URL`, `ASTRID_APP_APPEND_SERVICE_INTERNAL_TOKEN`; the map is authoritative). Set `project_id` in `supabase/config.toml:3`.
  6. `config/vite/policy.ts:6-11`: the new Railway host from N-INFRA; remove `reigh.art` and `www.reigh.art`; keep `astrid.haus`.
  7. `.github/workflows/bridge-latency.yml:34-39,47,53`: `repository: banodoco/astrid-app` with `path: astrid-app-main`, `repository: peteromallet/astrid-agent`.
  8. Contracts: `config/contracts/astrid-plan-a-c1.json`, `c2.json` repository keys and `scripts/quality/lib/astrid-contract-schema.mjs:10` enum, `check-astrid-contract-freeze.mjs:71,96,218`. These are gate inputs; change the enum and the data together.
  9. Run `npx tsc -p tsconfig.app.json --noEmit`, `npx vitest run`, `npm run build` in the background and triage failures by folder with parallel Haiku workers (`src/tools/video-editor/runtime`, `components`, `examples`, `hooks`, `lib`, `contexts`, `data`, `dev`; then `src/sdk`, `src/integrations`, `scripts`, `docs`, `supabase`). Workers fix only their folder.
  10. Commit and push `rename/astrid`.
- **Acceptance:**
  - `npx tsc -p tsconfig.app.json --noEmit` exits 0.
  - `npx vitest run` passes; `npm run build` exits 0.
  - `node scripts/quality/check-astrid-contract-freeze.mjs` exits 0.
  - `$TOOLS/check-zero --repo $APP --allow $TOOLS/allowlist.txt` passes.
  - `git ls-files | grep -i reigh` prints nothing.

#### C-INT
- **Route:** normal
- **Depends on:** C-RT, C-AS, C-APP
- **Owns:** nothing (read-only checks on the three `rename/astrid` branches)
- **Outcome:** proof the three renamed repos work together before anything lands.
- **Steps:**
  1. Run Astrid's tests with its CI pins pointing at the `rename/astrid` Runtime SHA.
  2. Start the renamed Runtime (`astrid-runtime up`, fresh data root), run the App against it, exercise the handshake with actor id `astrid-browser`, a live-scene request/result with the `<astrid_live_scene_*>` tags, and a timeline commit.
  3. Check `SCHEMA_DIGEST` equal across all three copies: `grep -rn SCHEMA_DIGEST` in each.
  4. Run `check-zero` on all three with the allowlist; run the cross-repo greps below.
- **Acceptance:**
  - `for r in $ASTRID $RUNTIME $APP; do $TOOLS/check-zero --repo $r --allow $TOOLS/allowlist.txt || exit 1; done` exits 0.
  - Astrid's cold-launch tests (`tests/stage1/test_cold_launch_autobootstrap.py`, `test_final_cold_launch_matrix_luna.py`) pass against the renamed Runtime.
  - The three `SCHEMA_DIGEST` values are identical.
  - An Opus 5.5 reviewer has read the three `rename/astrid` diffs, sampled by area with Haiku helpers. It reported no merged concepts, no wrong product name in user-visible text, and no alias or fallback. Every finding is fixed before C-LAND.

#### C-LAND
- **Route:** owner (merge rights) or manager with credentials
- **Depends on:** C-INT
- **Owns:** the three mains
- **Outcome:** `rename/astrid` merged into `main`: Runtime first, then Astrid (its CI pin now points at the merged Runtime SHA), then App.
- **Steps:** merge Runtime. If Astrid's pinned `RUNTIME_SHA` was a branch SHA and the merge changed it (squash), update the pin and the three parity constants, rerun C-AS acceptance, then merge Astrid. Merge App. No squash if it can be avoided, so SHAs stay valid.
- **Acceptance:** `git -C <each> log -1 origin/main` shows the merge; Astrid CI green on `main`; App CI green on `main`.

#### O-DEPLOY
- **Route:** owner
- **Depends on:** C-LAND
- **Owns:** Supabase, Railway, secrets, CI variables
- **Outcome:** deployed under the new names. Owner checklist items D1 to D8.
- **Acceptance:** the App loads on the production host; a request to the append service succeeds with the new secrets; no request hits an old function URL.

#### C-MIGRATE
- **Route:** owner (runs commands), agent prepares exact command lines
- **Depends on:** O-DEPLOY
- **Owns:** per-machine data
- **Outcome:** each machine's support folder moved, each realm migrated, the Supabase one-off applied. Owner checklist items M1 to M5.
- **Acceptance:** `astrid-runtime status` is healthy; `ls "$HOME/Library/Application Support/Astrid Runtime"` shows `runtime/` and `credentials/`; the old folder is gone; the SQL script's printed counts show zero rows with `com.reigh.%`.

### Phase 2: after

#### P-LOCAL
- **Route:** normal
- **Depends on:** C-LAND, N-LOCAL
- **Owns:** the local files listed in `local-tooling.md`
- **Outcome:** local tooling uses the new names.
- **Steps:** execute `local-tooling.md` entry by entry. Rebuild skill trees from the renamed Astrid. Rename `astrid-local/reigh-app` to `astrid-app`, update `~/.codex/config.toml` trust keys and `env.sh`.
- **Acceptance:** `$TOOLS/check-zero --profile local --dir ~/.local/state/astrid/skills --dir ~/.codex/config.toml --dir ~/Developer/hivemind/hivemind_scripts --dir ~/Developer/astrid-video/astrid-local/live-main` exits 0. Dated history files in those trees are listed in an allowlist file that must be empty for P-FINAL, so each is either deleted or fixed.

#### P-R4
- **Route:** normal
- **Depends on:** C-LAND
- **Owns:** `~/Developer/astrid-video/.otto/runs/timeline-platform-r4/` planning docs
- **Outcome:** R4 workers write the new names from day one.
- **Steps:** apply `rename.py` to the doc files (about 90 lines): `cards.md` lines 145, 299, 480, 1065, 1078, 1091 (start-from paths `banodoco_workspace_client/generated.py`, `P/scripts/reigh-acp-bridge.ts`), `spec-rendering.md`, `briefs/WS-SAVE.md` (`BANODOCO_LOCAL_DATA_ROOT`, `banodoco-local`), `agent_goal.md`, `status.md`, `open-questions.md`, `northstar.md`, `manager-brief.md`. `reviews/*.md` quote review history: delete the files that no card cites, rewrite the ones workers read. Pin the names R4 introduces: `scripts/astrid-acp-bridge.ts`, composition package `@banodoco/timeline-composition` (unchanged).
- **Acceptance:** `git grep -niE 'reigh|banodoco-workspace-(runtime|client)|banodoco_workspace|banodoco[-_]local|peteromallet/Astrid($|[^-])' -- .otto/runs/timeline-platform-r4` prints nothing.

#### P-SAT
- **Route:** owner
- **Depends on:** N-SAT, C-LAND
- **Owns:** GitHub settings of satellites
- **Outcome:** per N-SAT: `reigh-workspace` and `reigh-worker-orchestrator` archived; `reigh-worker` archived or renamed. Merge the `banodoco-workspace` and `timeline-*` scrub PRs. Owner checklist S1 to S5.
- **Acceptance:** `gh repo view banodoco/reigh-workspace --json isArchived` prints `true`; scrub PRs merged.

#### P-WINDOW
- **Route:** normal
- **Depends on:** 30 days after O-DEPLOY and C-MIGRATE, and the owner's confirmation that every machine and realm migrated
- **Owns:** the migration modules and their allowlist entries
- **Outcome:** the browser migration module, the realm migration module and the one-off SQL script deleted.
- **Steps:** delete `src/migrations/astridRenameBrowserMigration.ts` (and its call site and test), `astrid_runtime/astrid_rename_realm_migration.py` (and its test, and its hook in `upgrade`), `supabase/one-off/2026-astrid-rename.sql`. Empty `allowlist.txt` of their entries.
- **Acceptance:** `git grep -il reigh` in the three repos prints nothing; tests still pass.

#### P-FINAL
- **Route:** normal (the manager runs it)
- **Depends on:** P-LOCAL, P-R4, P-SAT, P-WINDOW
- **Owns:** `docs/plans/astrid-naming/`, `tools/astrid-rename/`, tags
- **Outcome:** the final zero, the completion tags, the plan deleted.
- **Steps:** see section 10.
- **Acceptance:** section 10.

---

## 9. Owner checklist

All items are human actions with credentials. Do them in this order; the manager pastes the exact commands from N-INFRA's output.

**GitHub (before applying, during the freeze)**
- [ ] G1. As org admin of `banodoco`: rename `banodoco/reigh-app` to `astrid-app`. Settings, General, Repository name. Or `gh repo rename astrid-app -R banodoco/reigh-app`.
- [ ] G2. Rename `banodoco/banodoco-workspace-runtime` to `astrid-runtime`.
- [ ] G3. As owner of `peteromallet/Astrid-agent`: rename to `astrid-agent` (case-only; unverified that GitHub accepts a case-only change in one step. If not, rename via a temporary name, then back; do not create a repo at the old name).
- [ ] G4. Confirm the targets were free first: `gh repo view banodoco/astrid-app`, `banodoco/astrid-runtime`, `peteromallet/astrid-agent` must report not found before the rename.
- [ ] G5. Do not create any repo under an old name; that would kill the redirect. Leave redirects alone.
- [ ] G6. Re-check integrations bound to the old repos: Railway's GitHub connection for the App, Supabase's GitHub integration, webhooks, deploy keys, branch protection, Actions secrets and variables (secrets stay with the repo on rename; reconfirm).

**Deploy (after landing)**
- [ ] D1. Supabase secrets: set `ASTRID_APP_APPEND_SERVICE_URL` and `ASTRID_APP_APPEND_SERVICE_INTERNAL_TOKEN` (new names, map-authoritative) with the values of `REIGH_APPEND_SERVICE_URL` / `_INTERNAL_TOKEN`; deploy; then unset the old ones.
- [ ] D2. Supabase: deploy the App's edge functions. Delete the edge function `reigh-data-fetch` (or deploy `astrid-data-fetch` first if N-INFRA found a caller, switch the caller, then delete the old). `npx supabase functions delete reigh-data-fetch --project-ref <ref>`.
- [ ] D3. Supabase: run `supabase/one-off/2026-astrid-rename.sql` once in the SQL editor or `psql`, in the cutover window. Keep the printed counts.
- [ ] D4. Supabase: `npx supabase db push --linked`. It should report nothing new if only comments and the in-place CHECK edit changed (the CLI tracks versions; see N-SQL's finding).
- [ ] D5. Railway: set `VITE_ASTRID_APP_APPEND_SERVICE_URL` (value of `VITE_REIGH_APPEND_SERVICE_URL`), remove the old one, redeploy. Rename the service `reigh-production` or add a new domain; put the new host into `PREVIEW_ALLOWED_HOSTS` (already in the landed code). Keep the public origin `astrid.haus` unchanged: the browser migration cannot move data across origins.
- [ ] D6. GitHub Actions / CI variables and secrets: rename `BANODOCO_RUNTIME_CHECKOUT` and `REIGH_WORKER_CHECKOUT` if they are set as repository variables (the repo sets them in the workflow `env`, so likely nothing to do; verify).
- [ ] D7. Domains: `reigh.art`, `reigh.ai`, `reigh.app` are removed from code. Decide what they do (redirect, keep, let lapse). This plan does not need an answer to finish, but check-zero will ignore them only because they are gone from code.
- [ ] D8. Verify production: load the App, create and save a timeline, open an extension with saved settings.

**Per machine (migrations)**
- [ ] M1. Update shells and launch configs: `BANODOCO_LOCAL_*` and `BANODOCO_RUNTIME_*` to `ASTRID_RUNTIME_*`, `REIGH_*` to `ASTRID_APP_*`, per `map-notes.md`.
- [ ] M2. Stop the Runtime: `astrid-runtime down`.
- [ ] M3. Move the support folder with the Runtime's own commands, once: `astrid-runtime backup --destination <dir>`, then `astrid-runtime relocate --plan --destination "$HOME/Library/Application Support/Astrid Runtime"`, review, then `relocate --confirm "RELOCATE <selected-realm-id>"`. Verify that `credentials/owner.token`, `discovery.json` and the catalog moved (N-REALM verifies this in its test; unverified for the real tree).
- [ ] M4. `astrid-runtime upgrade` (runs the realm migration per realm).
- [ ] M5. Open the App once in each browser profile used with Astrid so the browser migration runs. Check extension settings are present.

**Satellites (Phase 2)**
- [ ] S1. Archive `banodoco/reigh-workspace` (Settings, Danger zone, Archive).
- [ ] S2. Archive `banodoco/reigh-worker-orchestrator` (after the owner confirms `banodoco-worker/` is not deployed on Railway).
- [ ] S3. `banodoco/reigh-worker`: archive if N-SAT found nothing live; otherwise rename to `astrid-worker` and extend the plan.
- [ ] S4. Merge the scrub PRs in `banodoco-workspace`, `timeline-schema`, `timeline-composition`, `timeline-theme-2rp`.
- [ ] S5. Optional and the owners' call: delete instead of archive. Archiving is reversible and is the default.

**Final**
- [ ] F1. Confirm 30 days have passed and every machine ran M1 to M5. Tell the manager to run P-WINDOW.
- [ ] F2. Approve P-FINAL (it deletes the plan).

---

## 10. Done when

All of these hold:
1. `P-WINDOW` is complete: no migration module remains.
2. `check-zero` with an **empty allowlist** passes on every repo: `for r in astrid runtime app; do tools/astrid-rename/check-zero --repo <checkout of $r> || exit 1; done`, and passes with profile `keep` on `banodoco-workspace`, `timeline-schema`, `timeline-composition`, `timeline-theme-2rp`, and with profile `local` on the local tooling listed in `local-tooling.md`.
3. Every old name is gone from file names too: `git ls-files | grep -iE 'reigh|banodoco_local|banodoco_workspace'` prints nothing in each repo.
4. Tests and builds pass on `main` in all three repos; deployed App, Supabase and Railway run under the new names.
5. The owner has finished D1 to D8, M1 to M5 and S1 to S5.
6. Tags `astrid-rename-done` pushed on the three repos at the commit that follows steps 1 to 5.
7. One final commit in Astrid deletes `docs/plans/astrid-naming/` and `tools/astrid-rename/`. Its message contains the final `check-zero` output. After it, `git grep -il reigh` in Astrid prints nothing.

The pre-rename tags `pre-astrid-rename` stay. They are the archive.

---

## 11. Open questions

1. **Satellite conflict with the user's belief.** Finding 11 says `reigh-worker` is live (Astrid CI imports it) and `reigh-worker-orchestrator` is a live Railway service that clones `Reigh-Worker` into pods (`worker_startup.template.sh:254-266`). The decision treats both as deprecated. N-SAT checks; if a deployment is live, the plan gains a C-WORKER task.
2. **Migration checksums.** Finding 03 says applied migration files cannot be edited without a checksum mismatch. The decision edits them in place. N-SQL verifies the CLI behaviour first. If wrong, stop; the fallback is to leave the comments and add a new migration for the CHECK, which leaves residue.
3. **Support folder name.** Decision: `Astrid Runtime`. Unverified: that `relocate` moves the whole tree (`credentials/`, `discovery.json`, locks) rather than only realm data. N-REALM tests it.
4. **`ASTRID_BANODOCO_*` module name.** The env vars are renamed to `ASTRID_RUNTIME_*`, but the module `astrid/core/execution/executor/banodoco_catalog.py` keeps the community-facing `banodoco` name. Owner to confirm the catalog is Banodoco-community content.
5. **Kept satellites and `BANODOCO_`.** `banodoco-workspace` has 31 `BANODOCO_` lines and the orchestrator 28 that are its own env vars. The `keep` profile omits that pattern. If the owners want the `BANODOCO_` pattern enforced there, they must say so.
6. **`reigh-product-connector`.** App findings place it at `client.ts:371` and `dataProvider.test.ts:761`; the later audit found no hits in any repo. N-MAP re-greps before relying on either.
7. **Neutrality wording.** Runtime `README.md` and `conformance/second-client-core-v1.yaml:7` (`forbidden_symbols` lists `astrid`) describe a product-free contract. Naming the repo `astrid-runtime` is consistent with the enforced tests but not with that sentence. Decision stands; the sentence is reworded in C-RT.
8. **`astrid-runtime` command ownership.** The command `astrid-runtime` is defined by the Runtime (`pyproject.toml:15`, mapping to `banodoco_local.cli`), but Astrid also has `astrid/runtime_cli.py` with `prog="astrid-runtime"` (`:319`) and no console-script entry of its own. Which implementation `astrid-runtime up` reaches depends on the install. N-MAP must decide whether they are one command or two, before C-RT deletes `banodoco-local`.
9. **Capability ids and saved agent transcripts.** Old `reigh.*` capability ids and wire tags remain inside stored agent transcripts and prompts. The clean break leaves them unreadable by new code; this plan does not migrate transcripts. Confirm that is acceptable.
10. **Hivemind and Otto content.** Hivemind's knowledge content and Otto's project records probably mention Reigh. Out of scope beyond Hivemind's scripts (N-LOCAL). Decide whether to rewrite them.
11. **Dated design docs** `docs/design/*-2026-10-05.md` in the App are treated as live docs and renamed, not deleted. Confirm.
12. **`com.reigh.*` extension ids** are treated as a brand and renamed to `haus.astrid.*`, with data migrated. If no installed user has saved extension state, N-BROWSER's extension-id rewriting could be dropped; the decision keeps it.
13. **Browser local-media handles** (`reigh.local-media`) may not survive a structured-clone to a new database. N-BROWSER decides per case and must not drop them silently.
