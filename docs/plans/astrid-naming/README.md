# Astrid naming: execution plan

Status: ready to execute (v2, simplicity review folded in). Drafted 2026-10-17 against `main` of Astrid `e766a7d8`, Runtime `569412c`, App `67f16daca`. Evidence tables are in [inventory.md](inventory.md); every old-name token is in [old-tokens.txt](old-tokens.txt) and the 79 collisions in [collisions.tsv](collisions.tsv).

This plan renames the three Astrid repositories and every name derived from the old ones. `peteromallet/Astrid-agent` becomes `peteromallet/astrid-agent`. `banodoco/reigh-app` becomes `banodoco/astrid-app`. `banodoco/banodoco-workspace-runtime` becomes `banodoco/astrid-runtime`. In code, "Reigh" becomes "Astrid" (or "App" where both exist), and "Banodoco" as a product name for the Runtime becomes "Astrid Runtime".

## Summary

- **Security fix first.** A third party now holds `reigh.art` (created 2026-09-23, 302-redirects to an unrelated domain), and the App still sends users there (README, the allowed preview hosts, and every LoRA README the `huggingface-upload` function writes). Removing every `reigh.art`, `reigh.ai` and `reigh.app` reference is the first PR of Phase 0 (D-APP, step 1). It does not wait for the rename.
- **21 tasks:** 1 XHARD (N-MAP), 15 normal, 5 owner. Plus one standalone follow-up (F-WINDOW) that needs neither the plan nor its tools.
- **Lifetime: about 3 days**, then the plan and its tools are deleted (P-FINAL). The only thing left afterwards is the three-line follow-up F-WINDOW, about 30 days after deploy.
- **Shape.** Phase 0 lands every pure deletion on `main` as ordinary PRs and renames the GitHub repos, while the tools and the map are built. Phase 1 is a short freeze: the Runtime lands first on its own, then Astrid and the App pin its merged SHA once. Phase 2 cleans up local tooling, R4 docs and satellites, then deletes the plan.
- **No data migrations except one.** No Runtime realm migration (a byte census on every machine confirms it is not needed). One small browser-storage copier in the App. One forward Supabase migration.

**Clean-break rule.** No aliases, shims, dual reads, fallback env vars, re-exports or compatibility periods. After cutover no file in any repo contains an old name. The only exceptions are the temporary browser migration module (and its test) and this plan, both deleted later.

**Complexity verdict.** Moderate: big but mostly mechanical. A script does the bulk; the hard parts are the name map and lockstep cross-repo names.

The plan names the old names, so it is itself residue. P-FINAL deletes it.

## Contents

1. Names and 2. Scope: what counts as an old name
3. How hard is this? (verdict, hard parts, effort, "Complexity you might be missing")
4. Approach
5. Mapping rules
6. Sequencing and the cutover window
7. How to run this
8. Tasks (Phase 0 prep, Phase 1 cutover, Phase 2 after, the standalone follow-up)
9. Owner checklist
10. Done when
11. Open questions

---

## 1. Names

| Today | New | Note |
|---|---|---|
| `peteromallet/Astrid-agent` (the old `peteromallet/Astrid` already redirects to it) | `peteromallet/astrid-agent` | Case-only change, for family consistency. `https://github.com/peteromallet/astrid-agent` already returns 200. Moving it into the `banodoco` org is the owners' call and out of scope. |
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
- Env vars containing `BANODOCO_`, **matched case-sensitively**, including `ASTRID_BANODOCO_*`. Lowercase `banodoco_schema`, `banodoco_timeline_schema`, `banodoco_config`, `banodoco_root`, `banodoco_composer`, `banodoco_worker`, `banodoco_catalog`, `banodoco_social` are not env vars and are not old (about 570 lines in Astrid).
- `@banodoco/workspace-client`.
- `Application Support/Banodoco`, `Banodoco Workspace`. Two hits in `astrid/core/timeline/banodoco_schema.py` (lines 6 and 89) mean the community repo, not the Runtime: N-MAP maps those two by hand.
- `peteromallet/Astrid` not followed by `-agent`, and, case-sensitively, `/Astrid-agent` with a capital A (so the six lines that must become `astrid-agent` cannot survive the final check).
- The bare key `workspace-runtime` used as a repo name (App `scripts/quality/lib/astrid-contract-schema.mjs:10`). N-MAP decides each hit; protocol names such as `WORKSPACE_RUNTIME_URL` are not repo names.
- The domains `reigh.art`, `reigh.ai`, `reigh.app` (covered by `reigh`; named here because they are a security matter, see the Summary).

**Not old (the zero check must not flag these):**
- The GitHub org `banodoco` in URLs of repos that keep their names: `banodoco-workspace`, `timeline-composition`, `timeline-schema`, `timeline-theme-2rp`, `hivemind`, `runpod-lifecycle`, `Wan2GP`, `Banodoco-website`, `ArtAgents`.
- The `@banodoco/timeline-*` package scope, and `banodoco-timeline-schema` (`astrid/pyproject.toml:53`).
- The Banodoco community, `public/banodoco-gold.png`, and the `banodoco-workspace` repo name (the community workspace, live: Astrid imports `banodoco_social` from it).
- Files such as `astrid/core/timeline/banodoco_schema.py` and `executor/banodoco_catalog.py`: a bare `banodoco` is not an old name. Their env vars (`ASTRID_BANODOCO_*`) are renamed; the module names stay. See Open questions.
- `astrid.haus`: already the new domain.

The zero check therefore uses exact patterns (section 4.3), never a bare `banodoco`.

## 3. How hard is this?

**Verdict: moderate. Big but mostly mechanical.** About 13k old-name lines and about 2,600 distinct tokens across the three repos (App 5,193 lines in 957 files; Astrid 5,597 in about 698, of which 4,333 are history; Runtime 24 `reigh` lines plus about 400 `banodoco`), plus the satellites. The history part is deleted in Phase 0 before any rename runs.

**The genuinely hard parts**
1. "Reigh" and "Astrid" are today two different things. A blanket `reigh` to `astrid` makes 79 tokens collide with names that already exist (`reighCommit` next to `astridCommit`, `REIGH_ROOT` next to `ASTRID_ROOT`). This is the one XHARD task (N-MAP).
2. Lockstep cross-repo wire names and three generated copies of one client.
3. Escaped and regex forms of the extension-id prefix that a plain token row misses.
4. Deployed infra and secrets.
5. Satellite repos and CI pins.
6. The plan and its tools must disappear at the end.

**Effort (agent time unless stated)**

| Block | Estimate |
|---|---|
| Phase 0 prep, all tasks in parallel | about 1 day |
| Cutover window (freeze, apply, land, deploy, migrate) | hours to 1 day |
| Phase 2 cleanup and P-FINAL | about 1 day |
| Owner time | 1 to 2 hours (GitHub, Supabase, Railway, secrets) |
| Waiting | none for the plan. F-WINDOW is a standalone follow-up about 30 days after deploy. |

The plan lives about 3 days.

### Complexity you might be missing

- **Satellite repos.** `reigh-worker` is still fetched by Astrid CI jobs `m7-release-candidate` and `python` at `efc2276d`, and `tests/integrations/test_c12_cpu_runtime_harness.py` imports its code. `m7-release-candidate` gates `m8-publication`. `reigh-worker-orchestrator`, `reigh-workspace` and `banodoco-workspace` also carry or are referenced by old names. (N-SAT)
- **"Banodoco" is the Runtime's product name well beyond the repo name.** Env vars (`BANODOCO_LOCAL_*`, `BANODOCO_RUNTIME_*`, `ASTRID_BANODOCO_*`: 27 names), the support folder, the launcher package `banodoco_local` (12 files), three client packages, two console scripts, and 418 `banodoco` lines in the Runtime.
- **Browser data and the same-origin constraint.** About 20 localStorage keys and 5 IndexedDB databases. Code on a new origin cannot read them. This project therefore must not change the App's origin.
- **Extension ids.** `com.reigh.*` (about 150 literals) becomes `haus.astrid.*`. The id appears in plain form, in three escaped regex forms and in a Supabase CHECK constraint. A plain row misses the escaped forms and the result is silent: the client drops every analytics event and the edge validator rejects them (gap E3, handled by N-MAP).
- **The live film stack.** `astrid-local/live-main/env.sh` points the Runtime at the 1.4 GB film realm through `BANODOCO_LOCAL_DATA_ROOT`. Renamed code ignores that variable and would fall back to the default support folder and an empty realm. The env file and the code must switch in one step (C-MIGRATE M4).
- **Agent-facing names.** The wire tags `<reigh_live_scene_request>`, and skill text under `~/.local/state/astrid/skills`. The 22 retired capability ids `reigh.*` are deleted, not renamed (D-AS).
- **Local folders and agent configs.** `astrid-local/reigh-app`, `~/.codex/config.toml` trust keys, Hivemind scripts, review-tooling scripts.
- **R4 docs and Otto records.** About 90 old-name lines in R4 planning docs, which R4 workers will read.
- **Generated and digest-bound artifacts.** `SCHEMA_DIGEST`, pinned digests in the parity test and in the App's `client.test.ts:384`, the capability census lock, and the registry hash in `release_identity.py`.
- **A tracked build artifact.** `banodoco_workspace_runtime.egg-info/` (5 files) is tracked in the Runtime.
- **The plan's own deletion.**
- **Hivemind knowledge content** probably mentions Reigh. Out of scope beyond its scripts. Flagged in Open questions.

## 4. Approach

### 4.1 The map is data
One machine-readable file, `tools/astrid-rename/rename-map.tsv` (in the Astrid repo), maps old token to new token, plus path renames. N-MAP produces it with every collision resolved by hand. Workers never invent names. A missing name is a change to the map, made by the map owner only.

Columns: `kind` (`token`, `path`, `regex`), `old`, `new`, `scope` (`all`, or a repo), `note`.

### 4.2 `rename.py`
`tools/astrid-rename/rename.py (--repo <path> | --dir <path>) [--apply] [--report-merges]`. It applies the map to file contents and to paths. It is:
- longest-match-first, case-aware (`reigh`, `Reigh`, `REIGH`, `ReighFoo`);
- idempotent (a second run changes nothing);
- dry-run by default, printing a diff summary;
- skipping binary files, `.git`, and the allowlisted files (the browser migration module and its test, the desert_slice fixture files that N-CHAIN owns).

Modes:
- `--repo <path>`: a git repo. Uses `git ls-files` and `git mv`.
- `--dir <path>`: a plain directory, no git (plain renames). Used for P-R4, P-LOCAL and the satellite scrubs, so they are not hand edits.
- `--report-merges`: for each repo, computes the distinct identifier set before and after the rename and lists every post-rename token that already existed before with a different source. This is how N-MAP checks its invariant mechanically.

### 4.3 `check-zero`
`tools/astrid-rename/check-zero --repo <path> [--allow allowlist.txt]`. It fails on any old-name pattern in file contents or in tracked paths. Patterns (PCRE). Case-insensitive unless marked:

```
reigh
banodoco[-_]workspace[-_](runtime|client)
banodoco_workspace
banodoco[-_]local
banodoco-runtime
@banodoco/workspace-client
Application Support/Banodoco
Banodoco Workspace
peteromallet/Astrid(?!-agent)
case-sensitive:  \w*BANODOCO_
case-sensitive:  /Astrid-agent
```
plus the repo-key hits N-MAP lists for bare `workspace-runtime`. It never uses a bare `banodoco`. It has profiles: `main` (the three repos), `keep` (kept satellites such as `banodoco-workspace`, where only references to renamed repos count: it omits `BANODOCO_`), `local` (local tooling, takes `--dir`). The final allowlist is the browser migration module and its test only (until F-WINDOW deletes them).

### 4.4 Regenerate, do not edit
Generated and digest-bound artifacts are regenerated from their source after `rename.py`. They are never hand-renamed:
- Runtime OpenAPI to clients: `contract/openapi/workspace-v1.yaml` through `generators/generate.py` (output paths hard-coded at `generate.py:23`). `SCHEMA_DIGEST` changes (the OpenAPI `title` is renamed and the file's bytes are hashed, `generate.py:51-60`; `COMPONENT_MANIFEST_SHA256` also changes because `contract/component-manifest.json:6-8` holds the client package paths). Regenerate the Runtime copies in C-RT. Astrid's vendored copy and the App's copy (`src/integrations/runtime/generated.ts`, `generated-contract-metadata.ts`) are copied once from the merged Runtime SHA.
- `config/astrid-capability-census.lock.json` through `python -m astrid.core.execution.capability_ledger approve` (`capability_ledger.py:636-665`). Regenerated twice: in D-AS after the retired rows are deleted, and in C-AS after the rename.
- The hash-chained fixture `tests/fixtures/timeline_visualize/desert_slice/assembly.jsonl` (N-CHAIN).
- `release_identity.py` registry digests: recomputed, not pinned as literals (verified: `component_registry_sha256` has no literal pin in Astrid; Runtime has a duplicate definition at `runtime_protocol/release_identity.py:107` and `:194`, the second shadows the first).
- The pinned values in `tests/stage1/test_vendored_workspace_client_parity_luna.py:35-39`, `banodoco_workspace_client/contract_metadata.py:4-5`, and **the App's `src/integrations/runtime/client.test.ts:384`** (a literal `SCHEMA_DIGEST` pin). All three take the regenerated value.

### 4.5 Why this is merge-safe against R4 and Codex branches
R4 (`timeline-platform-r4`, projects A to J, 95 cards) has not started and has no branches on any origin. The rename lands before R4 wave 0, so nothing in flight conflicts. The Phase 0 deletion PRs land first and tag `pre-astrid-rename` before the first of them, so a Codex branch that touches a deleted file gets a trivial delete conflict and the archive tag has the old content. Until P-FINAL, `check-zero` catches a branch that adds new old-name text.

**The rename commit is pure.** In each repo, C-RT, C-AS and C-APP commit the raw `rename.py --apply` output as one commit of its own, titled `Apply the Astrid rename (rename.py)`, before any fix-up commit. History deletions are in the earlier D-* commits; tests, regeneration and fixes come in later commits. All three rename branches (C-RT's included) land with a merge commit, never a squash, so that commit survives on `main`. The catch-up recipe depends on this.

**Catching up a branch that was open before the rename** (an R4 branch, a Codex branch, anything). Do not hand-merge the rename. Re-run it on the branch:

```
git fetch origin
git merge <R>~1                                   # main up to just before the rename commit R; ordinary merge
python3 tools/astrid-rename/rename.py --repo . --apply
git commit -am "Apply the Astrid rename (rename.py)"
git merge -X ours <R>                             # see below
git merge origin/main                             # the fix-ups after R; ordinary merge
tools/astrid-rename/check-zero --repo .           # then the repo's tests
```

Why `-X ours` is safe on `R`, and only on `R`:
- After the branch has run the rename itself, `R` and the branch make the identical change to every line the branch didn't otherwise touch, so those merge cleanly.
- The only conflicts are lines that the branch edited **and** that held an old name. In those, `R`'s side is just the rename, which the branch's side already contains. Keeping the branch's side is therefore correct.
- Paths renamed on both sides are the same rename, so git pairs them.
- Never use `-X ours` on any other commit.

Real conflicts are left only where the branch introduced a name the map doesn't know. That is a map change, per stop rule 7.4. Expect minutes per branch, not a hand merge of a 13k-line commit.

After P-FINAL deletes the tools, the tag `astrid-rename-done` still holds them: `git show astrid-rename-done:tools/astrid-rename/rename.py`.

### 4.6 History policy
- Before the first deletion PR in each repo, tag the last pre-deletion commit `pre-astrid-rename` and push the tag. That tag is the archive.
- History in the working tree is **deleted, not rewritten**, by ordinary PRs on `main` in Phase 0 (D-APP, D-AS, D-RT). That covers `.oracle/`, `.megaplan/` done initiatives, dated plans, run logs, audits, release evidence of shipped releases, failed rc folders, `docs/slot-first-audits/`, `docs/local-runtime/reviews/`. Rewriting dated evidence would falsify it.
- If a live gate, test or script reads a history item, the reader is edited in the same PR, or deleted together with the gate when the gate guards a finished release.
- Git history itself stays. It is not residue in the tree.
- GitHub redirects from old repo names stay. They are invisible in code, and the only way to kill them is a placeholder repo under the old name, which is worse residue.

### 4.7 Persisted-data policy
Migrate only what the evidence says users have. Everything else is an accepted, stated effect.
- **Browser storage (App).** One small isolated module `src/migrations/astridRenameBrowserMigration.ts` (N-BROWSER) runs at App start. It is a generic copier: for each key under a short literal list of old prefixes it copies old to new, verifies, deletes old. Same for three IndexedDB databases. The zero check allowlists the module and its test. F-WINDOW deletes them about 30 days after deploy.
- **Runtime realms. No migration.** Evidence: there is no public Runtime install (the only path is a producer wheelhouse, both wheel names `PENDING_PRODUCER_HANDOFF`, `astrid:docs/setup/README.md:49-50`, `:23` forbids public registries). This Mac has 4 realms, none containing `com.reigh.`, `reigh-fnv1a64-v1:`, `reigh.transcript` or `reigh-browser` (byte census). The other targets do not need one: idempotency rows expire after 24 h (`runtime_protocol/store.py:41`); a lost `project_selections` row for actor `reigh-browser` only forgets which project was selected (`store.py:1385-1409`); a clip whose `clipType` does not match is skipped, not failed (`store.py:1559-1560`). Each team machine runs the byte census at cutover (C-MIGRATE M1). If it finds a targeted string, an operator script is written then, in `tools/astrid-rename/`, and deleted with the plan. Append-only ledgers, receipts and event history are never edited.
- **Supabase rows.** A forward migration (N-SQL), no old name in it. A one-off operator script only if `extension_operational_events` has rows.
- **Support folder.** Moved with the Runtime's `relocate` command, run by the **old** install while it is still running, once per machine. No code fallback.
- **Env vars and secrets** on dev machines, CI and deployments: set under the new names in the cutover window (owner checklist).

**Accepted effects (decided, not open):**
- Old `reigh.editor.timeline.<hex>` revision ids sit inside the film realm's hash-chained ledgers and are not touched. Astrid labels a revision's source by prefix (`astrid:astrid/sdk/timeline/revisions.py:18`, `astrid/packs/timeline/cli_history.py:23`). After the rename, old revisions show source "other" instead of "app". Recognising the old prefix would be a dual read.
- Dev-only extension settings stored in browsers (the extension-state stores, the dev-disable list, extension ids inside keys) are not migrated. Production has the extension host off, so only team members lose anything.
- The per-user preference that holds the `reigh.transcript` data-lane kind id resets to default.
- A Runtime clip of type `com.reigh.astrid.liveScene` saved before the cutover is skipped by the new Runtime, not failed.
- Old capability ids and wire tags remain inside stored agent transcripts (see Open questions).

### 4.8 How the plan deletes itself
P-FINAL runs the final `check-zero` (allowlist: the browser migration module and its test only) on all repos and local tooling, tags every repo `astrid-rename-done`, records the F-WINDOW follow-up as a GitHub issue in the App repo, then in one commit deletes `docs/plans/astrid-naming/` and `tools/astrid-rename/`. The tag keeps the plan reachable in history. After that deletion `check-zero` no longer exists, so P-FINAL records the passing output in the commit message.

---

## 5. Mapping rules

These are the binding rules. N-MAP turns them into `rename-map.tsv`.

1. **Reigh means the App.** Default: `reigh` to `astrid`, case preserved (`Reigh` to `Astrid`, `REIGH` to `ASTRID`).
2. **Collisions use `app`.** 79 tokens already exist with the new name and a different meaning (full table: [inventory.md section 7](inventory.md#7-collision-table)). Wherever the App and the agent repo are distinct concepts in the same context, the App becomes `app` / `App` / `ASTRID_APP_` / `astrid-app`. Examples: `reighCommit` to `appCommit`, `REIGH_ROOT` to `ASTRID_APP_ROOT`, `--reigh-commit` to `--app-commit`, `integrations/reigh` to `integrations/app`, `ReighElementKind` to `AppElementKind`, `checkReigh` to `checkApp`, `github.com/banodoco/Reigh` to `github.com/banodoco/astrid-app`, `peteromallet/reigh` to `banodoco/astrid-app` (it redirects to the App today; the blanket rule would give `peteromallet/astrid`, which is the agent repo). Repo references: `reigh-app` to `astrid-app`.
3. **Env vars.** `REIGH_*` to `ASTRID_APP_*`, `VITE_REIGH_*` to `VITE_ASTRID_APP_*` (collision-safe everywhere; 58 + 1 names). `BANODOCO_LOCAL_*` and `BANODOCO_RUNTIME_*` to `ASTRID_RUNTIME_*`. `ASTRID_BANODOCO_CATALOG_URL` to `ASTRID_RUNTIME_CATALOG_URL`.
   - Same-suffix pairs N-MAP must resolve (verified): `BANODOCO_LOCAL_OWNER_TOKEN` and `BANODOCO_RUNTIME_OWNER_TOKEN`; `BANODOCO_LOCAL_RUNTIME_CHECKOUT` and `BANODOCO_RUNTIME_CHECKOUT`. `ASTRID_RUNTIME_ENDPOINT` already exists (`astrid/packs/runpod/worker_process.py:1049`) and meets `BANODOCO_RUNTIME_ENDPOINT`. `ASTRID_RUNTIME_CUSTODY_*` exists and is kept.
   - The other five `ASTRID_BANODOCO_*` names (`AGENT_EXECUTORS`, `DEFAULT_EXECUTORS`, `EXECUTOR_CACHE`, `MANDATORY_EXECUTORS`, `REFRESH`) follow the same rule (`ASTRID_RUNTIME_*`) unless it collides. Flagged in Open questions.
   - `BANODOCO_URL` (App `HeroSection.tsx:15`), `BANODOCO_ASTRID_SOURCE_CHECKOUT`, `BANODOCO_RELEASE_RECEIPT_ROOT`, `BANODOCO_TIMELINE_SCHEMA_ROOT`: N-MAP decides. If a meaning is unclear, escalate; do not guess.
   - `BANODOCO_LOCAL_DATA_ROOT` is read by the live film stack's `env.sh`. Its new name must be recorded in `map-notes.md` first, because C-MIGRATE M4 needs it.
4. **Prose.** "Reigh" to "Astrid", or "the Astrid App" where the distinction matters.
5. **Specific names**
   - `ReighExtension` to `AstridExtension`; `@reigh/editor-sdk` to `@astrid/editor-sdk` (tsconfig alias: `tsconfig.json:15`, `tsconfig.app.json:23`, `config/vite/vite.config.ts:170`); `reigh-extension.json` to `astrid-extension.json` (21 example manifests, 5 fixtures, `config/contracts/reigh-extension.schema.json`).
   - Extension ids `com.reigh.*` to `haus.astrid.*` (reverse DNS of astrid.haus). `com.reigh.astrid.liveScene` to `haus.astrid.liveScene`. `com.reigh.astrid.live-scenes` to `haus.astrid.live-scenes`. The Supabase CHECK `^com[.]reigh[.]` becomes `^haus[.]astrid[.]`. **Escaped forms get their own rows** (a plain `com.reigh.` row does not match them): `com\.reigh\.` to `haus\.astrid\.`, `com[.]reigh[.]` to `haus[.]astrid[.]`, `com\\.reigh\\.` to `haus\\.astrid\\.`. Known hits: App `extensionOperationalAnalytics.ts:43` and `supabase/functions/extension-operational-events/validator.ts:36` (`/^com\.reigh\.[a-z0-9.-]{1,100}$/`), the CHECK at migration `20260823100000...sql:31`, `ExtensionManager.test.tsx:3574-3687`, `scripts/runtime/verify-extension-runtime-rollout.test.mjs:43`, `tests/e2e/timeline/extension-performance-budget.spec.ts:146`.
   - Wire tags `<reigh_live_scene_request|result|context>`, `<reigh_editor_context>`, `<reigh_element_operation>`, `<reigh_element_result>` to `<astrid_...>`. Schema ids `reigh.<x>/v1` to `astrid.<x>/v1` (keep `/v1`; after a lockstep cutover no reader of the old id exists).
   - Runtime control version `reigh.local-worker-control/v1` to `workspace.local-worker-control/v1` (neutral protocol family, `local_worker_composition.py:43`). It is sent and compared on a local control socket and not stored (verified).
   - Fingerprint prefix `reigh-fnv1a64-v1:` to `astrid-fnv1a64-v1:`. Verified: the prefix is prepended after hashing (`src/sdk/video/timeline/sourceMap.ts:223`), so the hash input is unchanged. Equality checks at `:315-316` compare full strings. Stored fingerprints with the old prefix are not migrated (4.7).
   - Runtime packaging: distribution `banodoco-workspace-runtime` to `astrid-runtime`; launcher package `banodoco_local` to `astrid_runtime`; Python client `banodoco_workspace_client` to `astrid_runtime_client` (distribution `banodoco-workspace-client` to `astrid-runtime-client`) in every copy: Runtime `packages/python/`, Astrid root `banodoco_workspace_client/`, generated code; TS client `@banodoco/workspace-client` to `@astrid/runtime-client`.
   - CLI: keep `astrid-runtime` (launcher). Delete `banodoco-local`, which maps to the same entry point (`pyproject.toml:14-15`). Rename `banodoco-runtime` (`runtime_protocol.cli:main`) by the rule "one command per entry point, prefixed `astrid-runtime`": `astrid-runtime-protocol`.
   - Support folder `~/Library/Application Support/Banodoco/` to `~/Library/Application Support/Astrid Runtime/` (`banodoco_local/paths.py:41,53,73`).
   - Actor ids `reigh-browser` (App `src/integrations/runtime/client.ts:349`), `reigh-product-connector`, `reigh-app:local-editor`, idempotency-key prefixes (`reigh.task.cancel-`, `reigh.render:v1/v2:`, `reigh.runtime.*`), `reigh.editor.timeline.*` revision ids (`dataProvider.ts:1593`, with the label code at `revisions.py:18` and `cli_history.py:23`), CustomEvent names, `window.__REIGH_*` globals, localStorage keys and IndexedDB names follow rules 1 and 2.
   - Files: `scripts/reigh-acp-bridge.ts` to `scripts/astrid-acp-bridge.ts` (pin this name now for R4 project H), and the other `scripts/reigh-*` files; `adapters/reigh/` to `adapters/app/` (collision rule: `integrations/reigh` exists beside `integrations/astrid`).
   - Edge function `reigh-data-fetch` has no caller and is deleted in D-APP (so it needs no map row). `project_id = "reigh"` in `supabase/config.toml:3` becomes `astrid-app` (local id only).
   - **Retired capability ids `reigh.*` are deleted, not renamed** (D-AS). They are marked dead in code (`capability_ledger.py:234-261`, `:455-457`). Renaming them would invent ids that never existed (`astrid.open_in_astrid`) inside the namespace agents see. So the map has no `reigh.*` capability rows.
   - Composition package `@banodoco/timeline-composition` is **unchanged** (not an old name). R4 project G pins it as is.
6. **The map is data** (section 4.1).

---

## 6. Sequencing and the cutover window

**This revises the 11 Oct order.** On 11 Oct the plan was "naming last, after R4 is completed and accepted" (`production/review/merge/CODEX-REPLY.md:321-325`). The user has now decided to do the rename first by asking for this plan. The reasons: R4 has not started and has no branches (inventory.md), so there is nothing to conflict with; doing it after R4 is the same work plus more old names written in the meantime.

**Phase 0 (now, no freeze).** D-APP first (its step 1 is the security fix). Then the other deletion PRs, the GitHub renames (redirects make them zero-downtime whenever they happen, and doing them early surfaces Railway, Supabase and webhook breakage days before the freeze), and the prep tasks.

**Cutover window.** A short merge freeze on the three mains, hours rather than days. Order:

1. Pre-checks pass (all Phase 0 tasks done and merged).
2. Freeze starts.
3. **C-RT: the Runtime lands first, on its own**, as soon as it is green. Report the merged `RUNTIME_SHA`.
4. C-AS and C-APP, in parallel, each pinned once to the merged `RUNTIME_SHA`.
5. C-INT: the live handshake check against the merged Runtime, and the Opus 5.5 final review of the diffs. This is the pre-merge check for Astrid and the App.
6. C-LAND: merge Astrid, then the App.
7. Deploy App, Supabase, Railway, secrets (owner), in the same window.
8. Per-machine migration steps (census, relocate, switch code and env together, film stack).
9. Unfreeze.

**Why the Runtime can land alone.** Consumers take the Runtime only by pinned SHA and copied generated files (`astrid:.github/workflows/ci.yml:61,220`; the App CI checks out Astrid and the App by name, `bridge-latency.yml:34-39`). Old pins stay fetchable through the GitHub redirect. Landing the Runtime early breaks nobody, and Astrid and the App pin the final SHA once. There is no re-regenerate loop and no squash-pin loop.

**Phase 2** follows: local tooling, R4 docs, satellite archiving, then P-FINAL right after (final zero check, tags, the follow-up issue, plan deleted). F-WINDOW is separate and later.

---

## 7. How to run this

This section is for the manager agent.

### 7.0 Models

| Use | Model | Where |
|---|---|---|
| **Normal** tasks: all `Route: normal` work, and every fan-out worker inside any task | **Haiku 5.5** (`claude-haiku-5-5`) | Most of the plan: the tools, the three deletion PRs, the browser copier, the SQL, the fixture chain, the per-repo apply and failure triage, satellites, local tooling, R4 docs |
| **XHARD** tasks | **Sonnet 5.5** (`claude-sonnet-5-5`) as the lead, handing the legwork to parallel Haiku workers and reviewing every diff against the invariant | N-MAP only |
| Work that needs **taste or thoroughness** | **Opus 5.5** (`claude-opus-5-5`) | Reviewing the name map and `map-notes.md` before any apply (names are taste); all user-visible text: UI strings, README and install text, extension-author docs; the final pre-merge review of the Astrid and App `rename/astrid` diffs (and the merged Runtime diff) in C-INT |
| `Route: owner` | a human with credentials | GitHub, Supabase, Railway, secrets, merges, archiving, per-machine commands |

The manager itself can be Haiku. Opus is used for judgment and review, not for bulk edits: brief it with the evidence, and have it fan out its own legwork to Haiku workers.

### 7.1 Phases and parallelism

| Phase | Tasks | Parallel? |
|---|---|---|
| 0 Prep, no freeze | D-APP (step 1, the security PR, first), D-AS, D-RT, O-GITHUB, N-MAP, N-TOOL, N-BROWSER, N-SQL, N-CHAIN, N-SAT | All parallel except: D-APP step 1 merges before anything else lands in the App; N-TOOL needs the first map draft from N-MAP only for its tests (develop with a stub map); N-BROWSER, N-SQL and N-CHAIN start when N-MAP publishes the first map commit (they read it, never write it); N-SQL also waits for the two owner queries (section 9, Q1 and Q2) |
| 1 Cutover, freeze | C-RT, then C-AS and C-APP (parallel), C-INT, C-LAND, O-DEPLOY, C-MIGRATE | Sequential gates. The Runtime merges first; Astrid and the App pin its merged SHA (7.5) |
| 2 After | P-LOCAL, P-R4, P-SAT, then P-FINAL | P-LOCAL, P-R4, P-SAT in parallel; P-FINAL last, right after |
| Later, standalone | F-WINDOW | About 30 days after deploy. Needs neither the plan nor its tools |

Phase 0 may start now. The D-* tasks are ordinary reviewed PRs to the three mains. The tools and the map go to Astrid's `tools/astrid-rename/` and `docs/plans/astrid-naming/` by reviewed PRs.

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
- `supabase_migrations.schema_migrations` turns out to have a content-hash column (N-SQL);
- a byte census finds a targeted string in a realm (C-MIGRATE M1): write the operator script only after the manager has seen the counts;
- any step would touch the `banodoco` org name, a kept satellite name, `workspace.v1` or the `@banodoco/timeline-*` scope;
- any step would run renamed code with the old env file, or write to or clean up the film's realm (`astrid-local/Astrid/.astrid-data`), or anything under `~/Developer/astrid-video/production/`.

Never guess a name. Never add an alias, shim, dual read, fallback env var or re-export, even temporarily, even "just for tests". Never edit a generated file by hand. Never rewrite dated evidence. Never touch `.github/workflows/slot-first-quality.yml` (D-APP): it is the App's only test CI.

### 7.5 One writer per file
Each file or area has exactly one owner task (the **Owns** line). Tasks that share a file are ordered by **Depends on**, never run in parallel. Only N-MAP writes `rename-map.tsv`. Only N-TOOL writes `rename.py` and `check-zero`. The D-* tasks own only the paths they delete or edit in Phase 0. Only the apply task of a repo writes that repo's tree during the freeze. Phase 0 tasks that produce modules for the App (N-BROWSER, N-SQL) write only their own new files and commit them to a prep branch `prep/astrid-rename-<task>`; C-APP merges them.

**Runtime SHA, once.** C-RT merges to Runtime `main` and reports `RUNTIME_SHA` (the merged commit). C-AS and C-APP copy their client files from that SHA and pin that SHA. It does not change afterwards. If it somehow does, that is a stop rule trigger, not a loop.

### 7.6 Status
Keep one table in the manager's notes: task, state (`todo`, `doing`, `done (commit)`, `blocked (dep)`), commit. This plan is not edited while running; the status lives with the manager.

---

## 8. Tasks

Template: **ID**, **Route** (`normal`, `XHARD`, `owner`), **Depends on**, **Owns**, **Outcome**, **Steps**, **Acceptance**. XHARD adds **Invariant**, **Plausible mistake**, **Why it looks right**. In commands, `$ASTRID`, `$RUNTIME`, `$APP` are the three working checkouts and `$TOOLS` is `$ASTRID/tools/astrid-rename`.

### Phase 0: prep

#### D-APP
- **Route:** normal
- **Depends on:** none. Do this first.
- **Owns:** the deleted and edited paths below in `$APP`
- **Outcome:** two ordinary PRs merged to App `main`. PR 1 removes every reference to the three dead domains (a security fix). PR 2 deletes the App's history and dead code. Tag `pre-astrid-rename` exists on the App before PR 1.
- **Steps:**
  0. Tag: `git fetch origin && git tag pre-astrid-rename origin/main && git push origin pre-astrid-rename`. Do this before any PR.
  1. **PR 1: the domains (security, merge first).** A third party holds `reigh.art`. Remove every `reigh.art`, `reigh.ai` and `reigh.app` reference:
     - `README.md:3` ("For usage, go to reigh.art"): the production URL becomes `https://astrid.haus`.
     - `config/vite/policy.ts:6-11` (`PREVIEW_ALLOWED_HOSTS`): remove `reigh.art` and `www.reigh.art`. Keep `astrid.haus` and, for now, the Railway host (the new Railway host comes in C-APP).
     - `supabase/functions/huggingface-upload/index.ts:594`: it writes `https://reigh.ai/` into every uploaded LoRA README. Replace with `https://astrid.haus/`.
     - `config/contracts/reigh-extension.schema.json:3` and `config/contracts/astrid-plan-a-diagnostic-c2.schema.json:3` (`$id` hosts `reigh.ai` and `reigh.app`): replace the host with `astrid.haus` and update every reference by `$id` found by `git grep`.
     - Any other hit from `git grep -niE 'reigh\.(art|ai|app)' -- . ':!docs'`.
     The README's other lines (`:16-17`, `git clone https://github.com/peteromallet/reigh`) are mapped by `rename.py` later, not here.
  2. **PR 2: deletions.** Start from `inventory.md` section 6. Delete:
     - `docs/extensions/evidence/` (137 files; rc1 to rc3 are `failed-*.json` only, rc4 and rc5 are superseded);
     - `docs/slot-first-audits/` (8 files), `docs/local-runtime/reviews/` (2), dated 2026-09 files in `docs/local-runtime/` (`02-reigh-plan.md`, `04e-reigh-worker-cutover-lane.md`, `2026-09-09-state-audit.md`, `05-next-stage-execution-20260909.md`), `docs/video-editor/reigh-branch-census-and-convergence.md`, `docs/state_management_context_audit.md`, `docs/sqlite-only-local-runtime-plan.md`, `docs/video-editor-sprint3-followups.md`;
     - the finished-release verifiers `scripts/release/verify-rc4*` and `verify-rc6*` with their tests, and their `package.json` scripts (`package.json:29,56,58,98`). No workflow runs them (no `.github/` file references them);
     - the edge function `supabase/functions/reigh-data-fetch/`, its `[functions.reigh-data-fetch]` section (`supabase/config.toml:128`), its test glob entry (`vitest.edge.config.ts:35`) and tests, and `_shared` helpers used only by it. It has no caller: confirm with `git grep -n 'reigh-data-fetch'` in all three repos and the satellites first; if a caller turns up, stop and report;
     - other readers: edit them in the same PR. Known: `scripts/quality/check-extension-ship-evidence.mjs:393-439` (sha256 against committed HEAD blob), `scripts/quality/lib/extension-external-evidence.mjs`, `scripts/quality/capture-extension-external-evidence.mjs:287`, `scripts/quality/check-extension-release-preflight.mjs:161`, `.gitattributes:6`, `.gitignore:69,70`, `config/contracts/astrid-plan-a-c1.json:1222` (references `docs/plans/astrid-default-packs-and-skills/PLAN.md`). For each, choose: (a) keep the folder and remove only the old-name files; (b) delete the folder and edit the reader; (c) delete the reader too, only when it guards a finished release. Record the choice in the PR description. The generator `verify-paired-release-e2e.mjs:3892` writes `reigh-build.log` and similar names; with the verifiers gone, `rename.py` renames its output names later.
  3. **Do not touch `.github/workflows/slot-first-quality.yml`.** It is not a docs guard: it runs `make slot-first-audit` (vitest unit, edge, db and Playwright e2e; `Makefile:124`) on `src/**`, `supabase/**` and more. The `docs/slot-first-audits/**` entry in its path filters has no old name and may stay as a dead filter.
  4. Keep `docs/design/*-2026-10-05.md` (7 files, live-ish): `rename.py` renames them; they are not history.
- **Acceptance (run locally; App CI runs no `tsc`, build or full vitest, so a green check proves little):**
  - After PR 1: `git grep -niE 'reigh\.(art|ai|app)' -- . ':!docs'` prints nothing.
  - After PR 2: `git grep -niE 'reigh\.(art|ai|app)'` prints nothing; `npx tsc -p tsconfig.app.json --noEmit` exits 0; `npx vitest run src/sdk` passes; `npm run test:extension-ship-verifier` passes or is removed together with its verifiers.
  - `git diff origin/main -- .github/workflows/slot-first-quality.yml` is empty on both PRs.
  - `git ls-remote --tags origin pre-astrid-rename` prints one line.

#### D-AS
- **Route:** normal
- **Depends on:** none (the `reigh-worker` CI removal belongs to N-SAT)
- **Owns:** the deleted and edited paths below in `$ASTRID`
- **Outcome:** one ordinary PR merged to Astrid `main`: history deleted, the retired Reigh capability rows deleted, the Reigh absence assertions deleted, hard-coded home-directory paths replaced. Tag `pre-astrid-rename` exists on Astrid before the PR.
- **Steps:**
  0. Tag: `git fetch origin && git tag pre-astrid-rename origin/main && git push origin pre-astrid-rename`.
  1. **History.** Start from `inventory.md` section 6. Delete: `.oracle/` (534 files, 4,097 old-name lines; no verified reader), `.megaplan/` done initiatives (27 files), `receipts/` (8), `findings/` (5), `docs/projects/` (58 files; handover and publication docs), the dated or finished plans under `docs/plans/` that contain old names (about 26 files; live plans stay and are renamed by `rename.py`; never delete `docs/plans/astrid-naming/`, which is this plan), `docs/megaplan/loose-work-consolidation-plan.md`, `.astrid-convergence/` (3), `artifacts/` old-name files (`artifacts/m4/reigh-external-gate-disposition.json` and the six others). For every candidate, `git grep -nF '<path>'` outside the folder. Known live readers to handle: `scripts/reshape/check_repo_hygiene.py:37-39,82-84` (`ROOT_DIR_ALLOWLIST`, `.megaplan` paths), `scripts/reshape/m4_gate.py:75`, `m7_gate.py:43` (`DEFAULT_PLAN`), `scripts/reshape/stage1_acceptance.py:19-20` (`.astrid-convergence/stage1-evidence`), `tests/reshape/test_repo_hygiene.py:64,139,150,187`, `.github/workflows/ci.yml:34,35,42,91,97` (`artifacts/m7/`), `pyproject.toml:196`, `installed_artifact.py:458`. Per reader choose (a) keep the folder and remove only the old-name files, (b) delete the folder and edit the reader, or (c) delete the reader too, only if it guards a finished release. If (c) is chosen for anything under `m4`, `m7` or `m8`, stop and escalate. Record each choice in the PR description.
  2. **Retired capability rows.** Delete the `reigh.*` rows of `_HISTORICAL_EXECUTOR_ROWS` (`astrid/core/execution/capability_ledger.py:234-261`), `_LEGACY_REIGH_IDS` (`:280-299`) and its `_legacy_ids` use (`:445-458`, called at `:523`). First `git grep -n 'historical_only\|_legacy_ids' tests` and fix any count assertion. Then regenerate the lock with `python -m astrid.core.execution.capability_ledger approve`. Only `capability_ledger.py` reads the lock (`:21`).
  3. **Absence test.** In `tests/stage1/test_reigh_authority_absence.py` delete the Reigh-specific assertions (`:12-41`). Keep the non-Reigh markers (`:63-86`). (The file's own name is renamed later by the map.)
  4. **Hard-coded home paths.** `tests/fixtures/runaway_release/audio-reactive-v1.json:467` and the `/Users/peteromalley/.../reigh-workspace/...` paths in `tests/integrations/test_generic_host_*.py`: replace with relative or `tmp_path` paths.
- **Acceptance:**
  - `python3 -m pytest -q tests/reshape` and the subset CI runs in job `python` (copy it from `ci.yml`) pass.
  - `grep -ci reigh config/astrid-capability-census.lock.json` prints 0, and a second `approve` run leaves `git diff --exit-code config/astrid-capability-census.lock.json` clean.
  - `git ls-remote --tags origin pre-astrid-rename` prints one line.
  - Every deleted path has "readers: none" or a matching edit in the PR description.

#### D-RT
- **Route:** normal
- **Depends on:** none
- **Owns:** the deleted and edited paths below in `$RUNTIME`
- **Outcome:** one ordinary PR merged to Runtime `main`. Tag `pre-astrid-rename` exists on the Runtime before the PR.
- **Steps:**
  0. Tag: `git fetch origin && git tag pre-astrid-rename origin/main && git push origin pre-astrid-rename`.
  1. `git rm -r banodoco_workspace_runtime.egg-info/` (5 tracked files: PKG-INFO, SOURCES.txt, dependency_links.txt, entry_points.txt, top_level.txt), and add `*.egg-info/` to `.gitignore`.
  2. `CHECKPOINT.md`, `LOCAL_REVIEW_CHECKPOINT.json` (GitHub URLs to the old repos, branch `codex/combined-local-review-20261014`): delete both unless a reader exists; `git grep -n 'LOCAL_REVIEW_CHECKPOINT\|CHECKPOINT.md'` first.
  3. `contract/schemas/timeline-config.schema.provenance.json:12` (path `reigh-main-role-slice-20261009`, a historical receipt path): delete or replace with a neutral path; `git grep` the schema's readers first.
  4. `tests/test_astrid_activation_join.py:44-45`: hard-coded `/Users/peteromalley/Documents/reigh-workspace/...` path. Replace with a `tmp_path` fixture.
- **Acceptance:** `python3 -m pytest -q` passes; `git ls-files | grep -i egg-info` prints nothing; `git ls-remote --tags origin pre-astrid-rename` prints one line.

#### O-GITHUB
- **Route:** owner
- **Depends on:** none (do it now; the D-* tasks do not depend on it)
- **Owns:** GitHub settings
- **Outcome:** the three repos renamed. See the Owner checklist (section 9), items G1 to G6.
- **Acceptance:** `gh repo view banodoco/astrid-app --json name,url`, `gh repo view banodoco/astrid-runtime --json name,url`, `gh repo view peteromallet/astrid-agent --json name,url` succeed; `git ls-remote https://github.com/banodoco/reigh-app.git` still answers (redirect).

#### N-MAP
- **Route:** XHARD
- **Depends on:** none
- **Owns:** `tools/astrid-rename/rename-map.tsv`, `tools/astrid-rename/map-notes.md` (Astrid repo)
- **Outcome:** the complete map, every collision resolved, every token in `inventory.md` covered or explicitly kept or marked deleted.
- **Steps:**
  1. Load `old-tokens.txt` (2,602 tokens) and `collisions.tsv` (79 collisions), both in this folder, as input. The D-* PRs delete many occurrences (history, the `reigh.*` capability ids, `reigh-data-fetch`). A token that now occurs only in paths those PRs delete is listed in `map-notes.md` as `deleted` and needs no row.
  2. Write the rules of section 5 as `regex`/`token` rows, longest match first. Resolve all remaining collisions one by one using rule 2. A blanket `reigh` to `astrid` row exists only as the last row, scope `all`, after every collision is covered.
  3. Resolve the env var pairs listed in rule 3 by reading each use (`generic_host.py:7377-7378`, `tests/stage1/test_final_cold_launch_matrix_luna.py:1377`, Runtime `banodoco_local/cli.py:196,203,417`). Where the two names mean the same value, merge; where they differ, give them different `ASTRID_RUNTIME_*` suffixes. Record the new name of `BANODOCO_LOCAL_DATA_ROOT` in `map-notes.md` first (C-MIGRATE M4 needs it).
  4. Add path rows for the old paths in inventory section 2 (`banodoco_local/` to `astrid_runtime/`, `adapters/reigh/` to `adapters/app/`, 21 `reigh-extension.json`, `scripts/reigh-*`, `ReighLoading.tsx`, `tests/stage1/test_reigh_authority_absence.py` to a neutral name, and so on).
  5. Add the repo-key rows (`'reigh-app'`, `'Astrid'`, `'workspace-runtime'` in `scripts/quality/lib/astrid-contract-schema.mjs:10`, `check-astrid-contract-freeze.mjs:71,96,218`, `config/contracts/astrid-plan-a-c1.json`/`c2.json`): `astrid-app`, `astrid-agent`, `astrid-runtime`.
  6. Add the `Astrid-agent` to `astrid-agent` row, scope URLs only (the six remaining lines in Astrid: `CHECKPOINT.md` is gone after D-AS or D-RT as applicable; `README.md:19`, `docs/getting-started.md:42`, `docs/setup/README.md:31`, `docs/setup/release-recipe.md:35` and any other `git grep -n '/Astrid-agent'` hit).
  7. Add the rows that a token row would miss: the three escaped extension-id forms (rule 5), `peteromallet/reigh` to `banodoco/astrid-app` (rule 2), and the hand mappings of `Banodoco Workspace` at `astrid/core/timeline/banodoco_schema.py:6,89` (community repo: leave as `banodoco-workspace`, mark kept).
  8. Run a dry run: `rename.py --report-merges` (from N-TOOL's stub) over copies of all three repos taken after the D-* PRs; run `check-zero` on the result. Every merge `--report-merges` flags is either resolved by a row or recorded as intended in `map-notes.md`. Zero residue except the allowlisted files. (This replaces eyeballing the most frequent output tokens.)
  9. Write `map-notes.md`: every judgment call, every token deliberately left out or deleted, with the reason.
- **Invariant:** after the map is applied, no two distinct old names produce the same new name, and no new name equals a pre-existing different name in the same scope.
- **Plausible mistake:** accepting the blanket `reigh` to `astrid` for a token that has an `astrid` twin in a context where both appear (a struct with both `astridCommit` and `reighCommit`, a path with both `integrations/astrid` and `integrations/reigh`). The result compiles, the tests pass, and two things have silently merged.
- **Why it looks right:** the collisions are only visible by joining the old-token list against the new-token set per scope. Each hit reads fine alone.
- **Acceptance:**
  - `python3 $TOOLS/map_selfcheck.py` (written by N-MAP) exits 0: no duplicate `new` values from different `old` values within a scope, and every token in `old-tokens.txt` matches at least one row or appears in `map-notes.md` as kept or deleted.
  - `awk -F'\t' 'NR>1{print $4}' $TOOLS/rename-map.tsv | sort | uniq -d` prints nothing.
  - `python3 $TOOLS/rename.py --repo <copy> --report-merges` reports no unresolved merge on each of the three renamed copies.
  - Dry-run `check-zero` over the three renamed copies prints only allowlisted files.
  - An Opus 5.5 reviewer has read `rename-map.tsv` and `map-notes.md`, and every name it questioned is resolved and noted in `map-notes.md`.

#### N-TOOL
- **Route:** normal
- **Depends on:** none (stub map); final tests after N-MAP
- **Owns:** `tools/astrid-rename/rename.py`, `tools/astrid-rename/check-zero`, `tools/astrid-rename/tests/`, `tools/astrid-rename/allowlist.txt`
- **Outcome:** the two scripts described in sections 4.2 and 4.3, with `--dir` and `--report-merges`.
- **Steps:**
  1. `rename.py`: read the map, sort token rows longest first, compile case variants, apply to every tracked text file (`git ls-files`), skip binaries by NUL-byte sniff and the allowlist, then `git mv` path rows deepest first. `--apply` writes; the default prints counts per file. Print a per-repo summary line.
  2. `rename.py --dir <path>`: the same without git (walks the directory, plain renames).
  3. `rename.py --report-merges`: compute the distinct identifier set of each repo before and after, list every post-rename token that already existed before with a different source, as `new <- old1, old2` lines. Exit non-zero if any is not marked intended in a file passed with `--intended`.
  4. `check-zero`: the patterns of section 4.3 (with `BANODOCO_` and `/Astrid-agent` case-sensitive), over `git ls-files` contents and path names; `--profile main|keep|local`; `--allow file`; non-zero exit and `path:line:match` output on any hit. In `local` profile it walks given `--dir` directories without git.
  5. `allowlist.txt` initial entries: `docs/plans/astrid-naming/`, `tools/astrid-rename/`, and (added by N-BROWSER and N-CHAIN) the browser migration module and its test, and the desert_slice fixture files.
  6. Tests in `tools/astrid-rename/tests/`: idempotence (apply twice, second diff empty), case preservation, longest-match (`reigh-app` before `reigh`), path moves, allowlist skip, `--dir` on a non-git folder, `--report-merges` flags a seeded collision, no change to `@banodoco/timeline-schema`, `banodoco-workspace` (the repo), `banodoco-timeline-schema`, `banodoco_social`, `astrid-agent`; and `peteromallet/Astrid-agent` **is** rewritten to `peteromallet/astrid-agent` (this agrees with N-MAP step 6).
- **Acceptance:**
  - `python3 -m pytest -q $TOOLS/tests` passes.
  - `printf 'banodoco-workspace @banodoco/timeline-schema banodoco_social banodoco_schema banodoco_timeline_schema\n' | $TOOLS/check-zero --stdin` exits 0.
  - `printf 'astrid-agent peteromallet/astrid-agent\n' | $TOOLS/check-zero --stdin` exits 0.
  - `printf 'banodoco-workspace-runtime BANODOCO_LOCAL_HOME\n' | $TOOLS/check-zero --stdin` exits 1.
  - `printf 'https://github.com/peteromallet/Astrid-agent\n' | $TOOLS/check-zero --stdin` exits 1.

#### N-BROWSER
- **Route:** normal
- **Depends on:** N-MAP (first map commit)
- **Owns:** new file `src/migrations/astridRenameBrowserMigration.ts` plus its test, the fixture list `tools/astrid-rename/browser-old-prefixes.txt`, and one call site in the App entry (`src/main.tsx`, verify the entry file), on branch `prep/astrid-rename-browser`
- **Outcome:** a small one-time App-start migration that copies the old persisted browser keys and databases to their new names, verifies, and deletes the old.
- **Steps:**
  1. Build `browser-old-prefixes.txt` from `inventory.md` section 3 and re-verify each `path:line` against `$APP`. It lists only: the exact localStorage keys and the prefixes `reigh-hidden-shots:`, `reigh:transcript-draft:`, `reigh.runtime.media-import.v1:`, plus the three IndexedDB names `reigh.timeline-drafts`, `reigh.sync-ledger`, `reigh.local-media` (store `reigh.local-media-handles`). Read the new names from the map (do not compute them).
  2. Implement:
     - **localStorage:** for each key that starts with a listed old prefix (or equals a listed key), copy to the new name, read back and compare, delete the old key.
     - **IndexedDB:** one generic copier (schema plus records) for the three databases. `reigh.local-media` holds `FileSystemHandle`s: structured-clone them as they are stored. If a handle cannot be cloned, keep the entry and mark it as needing re-import (the user is already told to drop the file again, `resolveTaskInputMedia.ts:50-60`). Never drop silently.
     - **Not migrated (accepted, section 4.7):** extension-id rewriting inside keys and values, the extension-state stores, `reigh.ext-proposals`, `reigh.dev-extensions.disabled`, the `showDataLanesByKind` value, the Cache Storage `reigh-v3`. The service worker already deletes every cache whose name differs from `CACHE_NAME` on activate (`public/sw.js:89-93`), so the renamed `CACHE_NAME` removes `reigh-v3` for free.
  3. Order per store: read old, write new, read new back and compare, delete old, only then record a completion marker `astrid.rename-migration.v1` (itself a new-name key). If any step fails, leave old data in place and retry on next start. No dual read: after the marker is set, no code reads an old name.
  4. Tests with jsdom and `fake-indexeddb`: seed **every** literal from `browser-old-prefixes.txt`; a populated old state migrates to equal new state; running twice is a no-op; a failure mid-way leaves old data intact.
  5. Add the module and its test to `tools/astrid-rename/allowlist.txt` with the removal date in a comment.
  6. The App's origin must not change in this release. Add an assertion test that `PREVIEW_ALLOWED_HOSTS` still contains `astrid.haus` and write the same-origin constraint into the module header comment.
- **Invariant:** every value a user stored under a listed old name is readable under the new name after the first start, and no code path reads an old name after the marker is set.
- **Plausible mistake:** writing the migration to read the "old key" from the key constants that `rename.py` rewrites, so the migration reads the new names and copies nothing.
- **Why it looks right:** the tests pass if they seed the new names. The mistake is mechanically caught: the literal grep and the seeded test below fail if the module does not hold the old literals.
- **Acceptance:**
  - `npx vitest run src/migrations` passes.
  - `while read p; do grep -qF -- "$p" src/migrations/astridRenameBrowserMigration.ts || echo "MISSING $p"; done < $TOOLS/browser-old-prefixes.txt` prints nothing.
  - `$TOOLS/check-zero --repo $APP --allow $TOOLS/allowlist.txt` passes after `rename.py` on a copy, and the migration file and its test are the only allowlisted files containing `reigh`.
  - `git grep -n "reigh" -- src ':!src/migrations'` on the renamed copy prints nothing.

#### N-SQL
- **Route:** normal
- **Depends on:** N-MAP (first map commit); owner queries Q1 and Q2 (section 9)
- **Owns:** the new forward migration `supabase/migrations/<timestamp>_astrid_extension_id_prefix.sql` and a second forward migration for the route prose (App, prep branch `prep/astrid-rename-sql`); in the rows-exist case only, the operator script `tools/astrid-rename/extension-id-rows.sql`
- **Outcome:** old names removed from the five migration files that contain them (by `rename.py` through the map), the CHECK and the production prose changed by forward migrations that contain no old name, and the CLI question settled with one query.
- **Steps:**
  1. **Checksum question, one read-only query.** The owner runs `\d supabase_migrations.schema_migrations` (Q1) and returns the output. No hash column means the CLI cannot compare file contents and in-place edits of old migrations are safe. A hash column: **stop and report**.
  2. **In-place edits come from `rename.py`,** not by hand: `20260506115000_seed_section3a_mode_aware_route_metadata.sql` (lines 4, 25, 26, 79, 80: comment and seed text; check that the seed strings are not looked up by value elsewhere), `20260524000000_revert_route_backend_gating_in_claim_and_counts.sql:44,49`, `20260524010000_drop_tasks_assert_claimable_trigger.sql:12`, `20260918000000_retire_legacy_generation_methods.sql:1,3`, and the CHECK at `20260823100000_create_extension_operational_analytics.sql:31` (`com[.]reigh[.]` to `haus[.]astrid[.]`, via the escaped-form map row). Fresh databases then get the new constraint.
  3. **Route prose (E11).** The seed inserted prose such as `'...through the Reigh travel child adapter...'` into `route_backend_capabilities` (`20260506115000...sql:25-26,79-80`). Editing the file leaves the production rows unchanged. Write a forward `UPDATE ... WHERE route_key = '<key>'` for each affected row, setting the text that the renamed seed now contains. The migration contains no old name.
  4. **Extension ids, by row count (Q2).** The owner runs `select count(*) from extension_operational_events where extension_id is not null;` and returns the number.
     - **0 rows (expected: the production host is off):** a forward migration drops the CHECK on `extension_operational_events.extension_id` and re-adds it with `^haus[.]astrid[.]`. It contains no old name and goes out through the normal `db push`.
     - **Rows exist:** the data `UPDATE` needs the old prefix as a literal, so it cannot live in a migration. Write `tools/astrid-rename/extension-id-rows.sql`, run once by the owner: one transaction that drops the old CHECK, runs `UPDATE ... SET extension_id = regexp_replace(extension_id, '^com\.reigh\.', 'haus.astrid.')`, re-adds the CHECK with the new prefix, prints row counts before and after. The script is deleted with the plan (P-FINAL). Never put it in a migration file. Owner step D3 becomes active.
  5. `supabase/config.toml:3` `project_id` is handled by C-APP. The `[functions.reigh-data-fetch]` section is already deleted by D-APP.
- **Acceptance:**
  - `git grep -niE 'reigh' -- supabase/migrations` on the renamed copy prints nothing.
  - The new migration files contain no old name: `grep -il reigh supabase/migrations/<new files>` prints nothing.
  - The report states the Q1 result and the Q2 count, each in one sentence.
  - If a local Supabase stack is already available: `insert ... extension_id = 'haus.astrid.x'` succeeds and `'com.reigh.x'` fails after the migration. Starting a stack just for this is not required.

#### N-CHAIN
- **Route:** normal
- **Depends on:** N-MAP (first map commit)
- **Owns:** `tools/astrid-rename/regen_desert_slice.py` (Astrid), and during the freeze the fixture files under `tests/fixtures/timeline_visualize/desert_slice/` and the frozen constants in `tests/core/timeline/test_timeline_visualize_hashes.py:42-44`
- **Outcome:** a script that rewrites the 145 old-name event lines of `assembly.jsonl` with the new actor id and recomputes `prev_hash` and `hash` for every line using the real hash code, plus updated companion files.
- **Steps:**
  1. Read the canonical hash code: `astrid/core/timeline/events/schema/serialize.py` (`canonical_json_bytes`, `sha256_hex` `:60-61`, `hash_embedded` `:64-77`, `with_event_hash` `:80-82`). Confirm in `types.py:360` (`to_json_obj`) whether `actor` is emitted and so hashed (unverified; assume yes).
  2. Write `regen_desert_slice.py`: parse each line into the event type, replace `actor` (`reigh-app:local-editor` to the map's new id) and display name (`Reigh local editor`), reset `prev_hash` to the chain's genesis or the previous line's new hash, recompute `hash` with `with_event_hash`, emit the line in the same canonical form. Use the library; never reimplement the hash.
  3. Update `assembly.head.json` (`head_last_hash`) and `assembly.identity.json`, and any digest the tests freeze (`test_timeline_visualize_hashes.py:42-44`; canonical digests of `assembly.json` and `registry.json` at `:66-79`). Search every consumer of the timeline ULID `01KYPVKMW5STB4W6FE05ED8242` and of the chain's hashes: `desert_truth.json`, `adversarial/*/case.json`, `negative/*/fixture.json`, `tests/fixtures/v10/m7_representative.json`, and **`tests/stage1/test_zero_shim_timeline_cutover_luna.py:100,112,151`**.
  4. Verify the whole chain, not just the last hash: write an assertion (in the script and as a new test) that recomputes every `hash` and `prev_hash` from line 1. The existing test checks only the last hash (`:82-97`), so it would pass over a broken middle. This `--check` is the guard: no whole-chain verifier exists in the repo, and a worker cannot pass it while leaving broken inner hashes.
  5. `rename.py` must skip these fixture files (add the paths to its content-skip list); only this script changes them.
- **Invariant:** every line's `hash` equals the hash of its content and every `prev_hash` equals the previous line's `hash`, from genesis to head.
- **Plausible mistake:** string-replacing the actor in the file and fixing only the last hash and the frozen constants so `test_timeline_visualize_hashes.py` goes green, leaving 145 broken inner hashes.
- **Why it looks right:** the existing test does not recompute the chain, so it passes.
- **Acceptance:**
  - `python3 tools/astrid-rename/regen_desert_slice.py --check` exits 0 (recomputes the full chain).
  - `python3 -m pytest -q tests/core/timeline tests/packs/rendering tests/stage1/test_zero_shim_timeline_cutover_luna.py -k "timeline_visualize or snapshot or zero_shim"` passes.
  - `grep -ci reigh tests/fixtures/timeline_visualize/desert_slice/assembly.jsonl` prints 0.

#### N-SAT
- **Route:** normal
- **Depends on:** none
- **Owns:** `tools/astrid-rename/satellites.md`; ordinary PRs in Astrid and App that remove references (merged to `main` in Phase 0 when the verdict says retire); prepared scrub PRs for the kept satellites (merged in P-SAT)
- **Outcome:** a verdict for each satellite and the reference-removal PRs.
- **Steps:**
  1. **`banodoco/reigh-worker`.** Decide whether any live deployment still uses it. Check: RunPod templates and images that clone it; the orchestrator's pod startup (`reigh-worker-orchestrator/gpu_orchestrator/runpod/worker_startup.template.sh:254-266` clones `banodoco/Reigh-Worker`); the user (ask via the manager; the user believes it is deprecated). Evidence so far: Astrid CI fetches it at `efc2276d30c22ac0cbe54f735a1129cef79583ef` in `ci.yml:64` (job `m7-release-candidate`) and `:223` (job `python`), with `REIGH_WORKER_CHECKOUT` at `:52,211`; `tests/integrations/test_c12_cpu_runtime_harness.py:36,44-45` imports `source.runtime.supervisor` and `source.runtime.worker.preflight` with no skip guard.
     - If **nothing live** uses it: open and merge an ordinary Astrid PR that deletes `tests/integrations/test_c12_cpu_runtime_harness.py`, the two fetch steps and the `REIGH_WORKER_CHECKOUT` env lines (`ci.yml:52,63-65,211,222-224`), the comment at `astrid/packs/wan2gp/src/compiler.py:26`, and any remaining `REIGH_WORKER_CHECKOUT` use (9 lines). Check that no `needs:` in `ci.yml` (notably `m8-publication` at line 740) depends on a job that this empties. The repo is then archived (P-SAT, owner).
     - If **something live** uses it: rename it to `banodoco/astrid-worker`, treat it as a fourth repo in the codemod run, and update the pod template URL, the `REIGH_*` pod env contract (about 40 names) together with the orchestrator, RunPod volume names (`reigh-livetest-prebuilt-*`) and Astrid's pin. Escalate: this adds a C-WORKER task and the plan must be extended.
  2. **`banodoco/reigh-worker-orchestrator` and `banodoco/reigh-workspace`:** deprecated. Remove references in ordinary PRs: App `README.md:31` (links to both worker repos), Astrid `planning/gen_fal_storyboard.py:23` and `planning/gen_park24_storyboard.py:26` (read a key from a `reigh-workspace/reigh-worker/this.env` path: repoint or delete the scripts), `planning/build_park24_slice.py`, `astrid/packs/blender/deploy.py:391`. (The hard-coded `/Users/peteromalley/...` test paths belong to D-AS.) Orchestrator is only blocked from archiving if `banodoco-workspace/banodoco-worker/` is still deployed on Railway: ask the manager to ask the owner.
  3. **`banodoco/banodoco-workspace`:** live, name stays. List its old-name hits that refer to renamed repos (`REIGH_SUPABASE_URL` in `banodoco-worker/README.md:33` and `worker_jwt.py:9`, `banodoco-worker/README.md:4-6`, stale Reigh-DB deployment docs, `README.md:82`). Prepare a PR to scrub them (with `rename.py --dir` where the map applies). Do not touch `BANODOCO_*` env vars that belong to the community workspace itself.
  4. **`timeline-schema`, `timeline-composition`, `timeline-theme-2rp`:** names stay. Scrub the comment hits (`timeline-schema/typescript/src/schemas.ts:118`, `tests/test_materialize_output.py:105`, `typescript/tests/resolveTheme.test.ts:58`; `timeline-composition/scripts/gen-registry.ts:13,38,55,184`; `timeline-theme-2rp` README:31). `provider: "reigh"` in timeline-schema is a data value: check whether anything persists it before changing it; if so, escalate.
  5. Wan2GP submodule branch `reigh-sprint-3` (`reigh-worker/.gitmodules`): list it; only matters if the worker is kept.
- **Acceptance:**
  - `satellites.md` has one verdict per satellite with `path:line` evidence.
  - After the Astrid PR (if the worker is retired): `git -C $ASTRID grep -nE 'reigh-worker|REIGH_WORKER_CHECKOUT|reigh-workspace' -- . ':!.oracle' ':!.megaplan'` prints nothing, and `python3 -m pytest -q tests/integrations` passes.
  - The ci.yml diff keeps `m8-publication` reachable: `grep -n "needs:" .github/workflows/ci.yml` shows no dangling job name.

### Phase 1: cutover (freeze)

Pre-condition: all Phase 0 tasks done and merged, O-GITHUB done. Tags `pre-astrid-rename` already exist (D-* step 0). There is no separate tag gate and no rule that SHAs must equal any prep SHA: the apply run is the real run and its acceptance is tests plus `check-zero`.

#### C-RT
- **Route:** normal (fan-out by folder allowed)
- **Depends on:** O-GITHUB, D-RT, N-TOOL, N-MAP, N-SAT
- **Owns:** the whole `$RUNTIME` tree during the freeze
- **Outcome:** the Runtime renamed, regenerated, tests green, **merged to Runtime `main` on its own**, `RUNTIME_SHA` reported.
- **Steps:**
  1. `git switch -c rename/astrid`.
  2. `python3 $TOOLS/rename.py --repo $RUNTIME --apply`. This renames `banodoco_local/` to `astrid_runtime/`, `packages/python/banodoco_workspace_client/` to `packages/python/astrid_runtime_client/`, and rewrites `pyproject.toml` (`:3` name, `:12-15` scripts, `:15,21` packages), `packages/python/pyproject.toml:2`, `packages/typescript/package.json:2`, env vars, paths (`paths.py:41,53,73`), `CONTROL_VERSION` (`local_worker_composition.py:43`), the clip type (`store.py:1559`, `visual_seam.py:23`), and `README.md` (keep the neutrality sentence true).
  3. Delete the `banodoco-local` script line; rename `banodoco-runtime` per rule 5.
  4. Regenerate: update `generators/generate.py` output paths (`:23`, `:178-190`) via the map, then run it. Regenerate `runtime_protocol/contract_metadata.py`, `packages/python/astrid_runtime_client/{generated,contract_metadata}.py`, `packages/typescript/src/{generated,contract-metadata}.ts`, `clients/typescript/{generated,contract-metadata}.ts`. Never edit them by hand. Update `contract/manifest.json`, `contract/component-manifest.json` and `clients/typescript/component-manifest.json` generator config via the map.
  5. Fix tests.
  6. Commit, open the PR, and merge when green. Report the merged commit as `RUNTIME_SHA`.
- **Acceptance:**
  - `python3 -m pytest -q` passes in `$RUNTIME`.
  - `python3 generators/generate.py && git diff --exit-code` (regeneration is a no-op).
  - `$TOOLS/check-zero --repo $RUNTIME --allow $TOOLS/allowlist.txt` passes.
  - `git ls-files | grep -iE 'egg-info|banodoco_local|reigh'` prints nothing.
  - `grep -n 'astrid-runtime\|banodoco' pyproject.toml` shows one `astrid-runtime` script and no `banodoco-local`.
  - `git -C $RUNTIME log -1 origin/main` shows the merge.

#### C-AS
- **Route:** normal (fan-out by folder allowed)
- **Depends on:** C-RT (`RUNTIME_SHA`, merged), N-CHAIN, D-AS, N-SAT, N-MAP
- **Owns:** the whole `$ASTRID` tree during the freeze
- **Outcome:** Astrid renamed, pinned once to `RUNTIME_SHA`, tests green, branch `rename/astrid` pushed.
- **Steps:**
  1. `python3 $TOOLS/rename.py --repo $ASTRID --apply` (skips the desert_slice fixture files). This moves `banodoco_workspace_client/` to `astrid_runtime_client/`, rewrites 37 importing `.py` files, `pyproject.toml:84` (`include = ["astrid*", "astrid_runtime_client*"]`), `ci.yml`, env vars (`journey.py:599,617`, `generic_host.py:13497`, `autobootstrap.py:127,143`, `docs/reference/env-vars.md:15`, `.env.example:20-21`), `release_identity.py:81,183`, `skills/view.py:43`, docs and SKILL text.
  2. Re-vendor the client: copy `astrid_runtime_client/{__init__,generated,contract_metadata}.py` from the Runtime at `RUNTIME_SHA` (`cmp` must show identical). Update the pinned values at `tests/stage1/test_vendored_workspace_client_parity_luna.py:35-39` and `astrid_runtime_client/contract_metadata.py:4-5` (renamed file) from the regenerated output.
  3. CI: in `ci.yml`, set the Runtime fetch URL to `https://github.com/banodoco/astrid-runtime.git` and the SHA to `RUNTIME_SHA` (lines 61, 220); rename env `BANODOCO_RUNTIME_CHECKOUT` as the map says. The worker fetch is already gone if N-SAT retired it.
  4. Regenerate `config/astrid-capability-census.lock.json` with `python -m astrid.core.execution.capability_ledger approve`. There are no `reigh.*` rows left to rename (D-AS).
  5. Run N-CHAIN's `regen_desert_slice.py` and commit the fixture changes.
  6. `ASTRID_RUNTIME_CUSTODY_*` stay (both ends in this and the Runtime repo; no old name).
  7. Fix failures by folder (fan-out). Do not change assertions to pass; fix the code or the map.
  8. Commit and push `rename/astrid`. Do not merge yet (C-INT first).
- **Acceptance:**
  - `python3 -m pytest -q` passes (or the same subset CI runs; copy it from `ci.yml` job `python`).
  - `python3 -m pytest -q tests/stage1/test_vendored_workspace_client_parity_luna.py tests/core/timeline/test_timeline_visualize_hashes.py` passes.
  - `python3 tools/astrid-rename/regen_desert_slice.py --check` exits 0.
  - `$TOOLS/check-zero --repo $ASTRID --allow $TOOLS/allowlist.txt` passes.
  - `cmp -s $ASTRID/astrid_runtime_client/generated.py $RUNTIME/packages/python/astrid_runtime_client/generated.py && echo same` prints `same`.

#### C-APP
- **Route:** normal (fan-out by folder: the failure triage is the large part)
- **Depends on:** C-RT (`RUNTIME_SHA`, merged), D-APP, N-BROWSER, N-SQL, N-SAT, N-MAP
- **Owns:** the whole `$APP` tree during the freeze
- **Outcome:** the App renamed, typed, tested, built; branch `rename/astrid` pushed.
- **Steps:**
  1. `python3 $TOOLS/rename.py --repo $APP --apply`. This covers the 71 renamed paths (inventory section 2), identifiers (`ReighExtension` 283 uses, `ReighRuntimeClient` 146), tsconfig aliases, `vite` and vitest aliases (`config/vite/vite.config.ts:170`, `config/testing/*`), wire tags, schema ids, extension ids in all four forms (plain and the three escaped), env vars, storage keys, workflow, contracts, README.
  2. Copy the regenerated TS client from the Runtime at `RUNTIME_SHA` into `src/integrations/runtime/generated.ts` and `generated-contract-metadata.ts` (regenerate; do not hand-edit). **Update the literal `SCHEMA_DIGEST` pin at `src/integrations/runtime/client.test.ts:384`** to the new value.
  3. Merge `prep/astrid-rename-browser` and `prep/astrid-rename-sql`.
  4. Rename `_shared/reighAppendService.ts` and its env vars (`ASTRID_APP_APPEND_SERVICE_URL`, `ASTRID_APP_APPEND_SERVICE_INTERNAL_TOKEN`; the map is authoritative). Set `project_id` in `supabase/config.toml:3`. (`reigh-data-fetch` is already deleted by D-APP.)
  5. `config/vite/policy.ts:6-11`: put in the new Railway host (from the owner checklist, section 9). `astrid.haus` stays. (The dead domains are already gone from D-APP.)
  6. `.github/workflows/bridge-latency.yml:34-39,47,53`: `repository: banodoco/astrid-app` with `path: astrid-app-main`, `repository: peteromallet/astrid-agent`.
  7. Contracts: `config/contracts/astrid-plan-a-c1.json`, `c2.json` repository keys and `scripts/quality/lib/astrid-contract-schema.mjs:10` enum, `check-astrid-contract-freeze.mjs:71,96,218`. These are gate inputs; change the enum and the data together.
  8. Run `npx tsc -p tsconfig.app.json --noEmit`, `npx vitest run`, `npm run build` in the background and triage failures by folder with parallel Haiku workers (`src/tools/video-editor/runtime`, `components`, `examples`, `hooks`, `lib`, `contexts`, `data`, `dev`; then `src/sdk`, `src/integrations`, `scripts`, `docs`, `supabase`). Workers fix only their folder.
  9. Commit and push `rename/astrid`. Do not merge yet (C-INT first).
- **Acceptance. This local run is the real gate.** App CI runs no `tsc`, no `npm run build` and no full vitest suite (the workflows are `bridge-latency`, `dockerfile-check` and `slot-first-audit`), so a green CI check does not prove these:
  - `npx tsc -p tsconfig.app.json --noEmit` exits 0.
  - `npx vitest run` passes; `npm run build` exits 0.
  - `node scripts/quality/check-astrid-contract-freeze.mjs` exits 0.
  - `$TOOLS/check-zero --repo $APP --allow $TOOLS/allowlist.txt` passes.
  - `git ls-files | grep -i reigh` prints nothing.

#### C-INT
- **Route:** normal (the review step runs on Opus 5.5)
- **Depends on:** C-RT (merged), C-AS, C-APP
- **Owns:** nothing (read-only checks)
- **Outcome:** proof that the renamed Astrid and App work with the merged Runtime, and an independent diff review, before Astrid and the App land. This is their pre-merge check.
- **Steps:**
  1. Live handshake: start the merged renamed Runtime (`astrid-runtime up`, fresh data root), run the App branch against it, and exercise the handshake with actor id `astrid-browser`, a live-scene request/result with the `<astrid_live_scene_*>` tags, and a timeline commit.
  2. **Opus 5.5 final review** of the Astrid and App `rename/astrid` diffs, plus the already-merged Runtime diff, sampled by area with Haiku helpers. Brief it with the evidence and the invariant of N-MAP, not with a conclusion. It reports: merged concepts, wrong product name in user-visible text, any alias or fallback. A Runtime finding is fixed forward in a new Runtime PR (and `RUNTIME_SHA` is then a stop-rule event, 7.5). Every finding in Astrid and the App is fixed before C-LAND.
  The parity test, `cmp` and `check-zero` are already C-AS and C-APP acceptance and are not repeated here.
- **Acceptance:**
  - Astrid's cold-launch tests (`tests/stage1/test_cold_launch_autobootstrap.py`, `test_final_cold_launch_matrix_luna.py`) pass against the renamed Runtime.
  - The handshake, live-scene round trip and timeline commit are recorded as succeeded.
  - The Opus 5.5 report lists no unresolved finding.

#### C-LAND
- **Route:** owner (merge rights) or manager with credentials
- **Depends on:** C-INT
- **Owns:** the Astrid and App mains
- **Outcome:** `rename/astrid` merged into Astrid `main`, then App `main`. The Runtime is already on `main` (C-RT).
- **Steps:** merge Astrid, then the App, each with a merge commit and **never a squash**, so the pure rename commit survives on `main` for the catch-up recipe (section 4.5). Re-run C-APP's acceptance commands once on the merged App `main`.
- **Acceptance:** `git -C <each> log -1 origin/main` shows the merge; Astrid CI green on `main`; C-APP's `tsc`, `vitest run` and `build` pass on the merged App `main`. A green App CI alone is not evidence (it does not run them).

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
- **Outcome:** each machine's support folder moved, the live film stack on renamed code with its env file switched, and the browser copier run once. Owner checklist items M1 to M5.
- **Steps (the agent prepares these for each machine; section 9 holds the checklist):**
  1. **Census.** On each machine, before anything moves, run the byte census over every realm: `for f in <each realm>/realm.sqlite3*; do LC_ALL=C grep -a -o -e 'com\.reigh\.' -e 'reigh-fnv1a64-v1:' -e 'reigh\.transcript' -e 'reigh-browser' "$f" | sort | uniq -c; done`. Expect empty output. If it finds a targeted string, write a one-off operator script in `tools/astrid-rename/` at that point (stop rule 7.4), not before.
  2. **Relocate with the old install, while it runs.** `relocate` requires a running owner (`banodoco_local/relocation.py:257-259`) and takes its source from the path the running code computes (`:250`). Renamed code would compute the new, empty path. So: `backup`, `relocate --plan`, `--confirm` all with the old install running. Keep `relocate` rather than `mv`: `catalog.json` stores absolute realm paths and relocate rewrites them (`:75`, `:322`). **First check whether one command does it:** `upgrade --destination` is a relocation cutover and requires an explicit data root (`cli.py:108-114`). On a scratch data root, determine whether it relocates and switches in one command. If yes, write that one command in the checklist and drop the separate steps.
  3. **Switch code and env names together** (after the relocation, not before): stop the old Runtime, install the renamed Runtime, update shells and launch configs (`BANODOCO_LOCAL_*` and `BANODOCO_RUNTIME_*` to `ASTRID_RUNTIME_*`, `REIGH_*` to `ASTRID_APP_*`, per `map-notes.md`), start it. Old code reads old names, so the env change must not precede the code change.
  4. **Live film stack.** `astrid-local/live-main/env.sh` sets `BANODOCO_LOCAL_DATA_ROOT` to the 1.4 GB film realm under `astrid-local/Astrid/.astrid-data`. Switch `env.sh` to the new variable name **in the same step** that moves the live stack onto renamed code. Never run renamed code with the old env file: it ignores the old variable, falls back to the default support folder (`paths.py:15,47,53`) and finds or creates a different, empty realm. No clean-up touches that realm.
  5. **Browser.** Open the App once in each browser profile used with Astrid so the copier runs.
- **Acceptance:** the census output is recorded for each machine; `astrid-runtime status` is healthy; `ls "$HOME/Library/Application Support/Astrid Runtime"` shows `runtime/` and `credentials/` and the old folder is gone; on the live film stack, `astrid-runtime status` reports the film data root and `du -sh astrid-local/Astrid/.astrid-data` is still about 1.4 GB, checked before any traffic.

### Phase 2: after

#### P-LOCAL
- **Route:** normal
- **Depends on:** C-LAND
- **Owns:** the local files listed below
- **Outcome:** local tooling uses the new names. (This merges the old list-and-execute pair: verify each entry, then do it in one pass.)
- **Steps:** all paths are on the owner's Mac. Verify each entry, then execute it. Use `rename.py --dir` where the map applies.
  - Skills: `~/.local/state/astrid/skills/claude/` and `.../codex/` (5 files each, identical): `packs/rendering/references/live-scenes-authoring.md` (12 hits), `pack-builder/SKILL.md` (9, links to `github.com/peteromallet/Astrid/blob/main/...`), `packs/rendering/SKILL.md` (3), `references/document-checkout.md` (2), `references/placeholder-voiceover.md` (1). These are generated from the Astrid repo (`astrid/skills/view.py:43` `_PACK_BUILDER_DOC_PREFIX`): rebuild them from the renamed Astrid, do not edit. Find the rebuild command in `astrid/skills/` and record it. `~/.codex/skills/astrid` is a symlink to the codex tree.
  - `~/.codex/config.toml` project-trust keys at lines 170, 188, 362, 401, 425 (`[projects."…/reigh-…"]`), keyed on directory paths: update when the folders are renamed.
  - Hivemind (`~/Developer/hivemind`): `hivemind_scripts/rehearse_embedding_pilot.py:47` and `rehearse_historical_backfill.py:90` (default `VIBECOMFY_ROOT=/Users/peteromalley/Documents/reigh-workspace/vibecomfy`, a path that does not exist: pre-existing bug, fix to a required env var). History files there stay.
  - `~/Developer/astrid-video/astrid-local/`: directory `reigh-app` (rename to `astrid-app`), `live-main/Runtime/` and `live-main/Astrid/` `LOCAL_REVIEW_CHECKPOINT.json` URLs, `live-main/Runtime/contract/manifest.json`, `contract/component-manifest.json`, `clients/typescript/component-manifest.json` (generator config), `labs/*/app/supabase/config.toml` and `vendor/timeline-schema/python/pyproject.toml` (vendored copies: regenerate from source), top-level `*.sh`. **`live-main/env.sh` follows the rule in C-MIGRATE M4:** if C-MIGRATE has not already switched it, it is switched in the same step that moves `live-main` onto renamed code, never later.
  - Review tooling: `~/Developer/astrid-video/production/review/merge/watch-codex.sh`, `watch-codex-once.sh`, and 9 of 11 `*.md` notes there. Edit those named files only. Do not delete or move anything under `production/`, any runtime data root, or the film.
  - Otto/portfolio records and `~/Developer/otto-program` projects that name the repos: list only; Otto records are not edited by this plan (see Open questions).
  - Shell profiles: `~/.zshrc`, `~/.zprofile`, `~/.config` for `BANODOCO_*` and `REIGH_*`.
- **Acceptance:** `$TOOLS/check-zero --profile local --dir ~/.local/state/astrid/skills --dir ~/.codex/config.toml --dir ~/Developer/hivemind/hivemind_scripts --dir ~/Developer/astrid-video/astrid-local/live-main` exits 0. Dated history files in those trees are listed in an allowlist file that must be empty for P-FINAL, so each is either deleted or fixed (never from `production/` or runtime data).

#### P-R4
- **Route:** normal
- **Depends on:** C-LAND
- **Owns:** `~/Developer/astrid-video/.otto/runs/timeline-platform-r4/` planning docs
- **Outcome:** R4 workers write the new names from day one.
- **Steps:** apply `rename.py --dir` to the cards and briefs workers execute (about 90 lines): `cards.md` lines 145, 299, 480, 1065, 1078, 1091 (start-from paths `banodoco_workspace_client/generated.py`, `P/scripts/reigh-acp-bridge.ts`), `spec-rendering.md`, `briefs/WS-SAVE.md` (`BANODOCO_LOCAL_DATA_ROOT`, `banodoco-local`), `agent_goal.md`, `status.md`, `open-questions.md`, `northstar.md`, `manager-brief.md`. **Delete `reviews/*.md`** instead of rewriting them: they quote dated review history (section 4.6). Pin the names R4 introduces: `scripts/astrid-acp-bridge.ts`, composition package `@banodoco/timeline-composition` (unchanged).
- **Acceptance:** `git grep -niE 'reigh|banodoco-workspace-(runtime|client)|banodoco_workspace|banodoco[-_]local|peteromallet/Astrid($|[^-])' -- .otto/runs/timeline-platform-r4` prints nothing.

#### P-SAT
- **Route:** owner
- **Depends on:** N-SAT, C-LAND
- **Owns:** GitHub settings of satellites
- **Outcome:** per N-SAT: `reigh-workspace` and `reigh-worker-orchestrator` archived; `reigh-worker` archived or renamed. Merge the `banodoco-workspace` and `timeline-*` scrub PRs. Owner checklist S1 to S5.
- **Acceptance:** `gh repo view banodoco/reigh-workspace --json isArchived` prints `true`; scrub PRs merged.

#### P-FINAL
- **Route:** normal (the manager runs it)
- **Depends on:** P-LOCAL, P-R4, P-SAT (right after Phase 2; it does not wait for any window)
- **Owns:** `docs/plans/astrid-naming/`, `tools/astrid-rename/`, tags, the follow-up issue
- **Outcome:** the final zero, the completion tags, the F-WINDOW issue recorded, the plan deleted.
- **Steps:** see section 10.
- **Acceptance:** section 10.

### Standalone follow-up

#### F-WINDOW
- **Route:** normal (a three-line job; schedule it as a reminder)
- **Depends on:** a date, about 30 days after O-DEPLOY and C-MIGRATE. It does **not** depend on the plan, the map, the tools or `check-zero`, which are gone by then.
- **Owns:** the browser migration module in the App
- **Outcome:** the browser copier is deleted.
- **Steps:** delete `src/migrations/astridRenameBrowserMigration.ts`, its call site in `src/main.tsx` and its test.
- **Acceptance:** `git -C <app> grep -il reigh` prints nothing; the App's tests still pass.
- **How it is recorded.** P-FINAL opens a GitHub issue in the App repo, worded without any old name, for example: "Delete `src/migrations/astridRenameBrowserMigration.ts`, its call site in `src/main.tsx` and its test after <date>. Then a case-insensitive grep for the App's old product name returns no files." The issue is the reminder.

---

## 9. Owner checklist

All items are human actions with credentials. Do them in this order. The manager pastes the exact commands. Phase 0 items can be done now.

**Phase 0 (now)**

*GitHub (O-GITHUB)*
- [ ] G1. As org admin of `banodoco`: rename `banodoco/reigh-app` to `astrid-app`. Settings, General, Repository name. Or `gh repo rename astrid-app -R banodoco/reigh-app`.
- [ ] G2. Rename `banodoco/banodoco-workspace-runtime` to `astrid-runtime`.
- [ ] G3. As owner of `peteromallet/Astrid-agent`: rename to `astrid-agent` (case-only; unverified that GitHub accepts a case-only change in one step. If not, rename via a temporary name, then back; do not create a repo at the old name).
- [ ] G4. Confirm the targets were free first: `gh repo view banodoco/astrid-app`, `banodoco/astrid-runtime`, `peteromallet/astrid-agent` must report not found before the rename.
- [ ] G5. Do not create any repo under an old name; that would kill the redirect. Leave redirects alone.
- [ ] G6. Re-check integrations bound to the old repos, now rather than in the freeze: Railway's GitHub connection for the App, Supabase's GitHub integration (reconnect), webhooks, deploy keys, branch protection, Actions secrets and variables (secrets stay with the repo on rename; reconfirm). Workflow `uses:` lines are not redirected on rename; there are none to the old repos today (verify with `grep -rn 'uses: *\(banodoco\|peteromallet\)/' .github`).

*Read-only queries for N-SQL*
- [ ] Q1. Against the linked Supabase project: `\d supabase_migrations.schema_migrations`. Return the output. (No hash column is expected.)
- [ ] Q2. `select count(*) from extension_operational_events where extension_id is not null;`. Return the number. (0 is expected.)

*Security follow-through for D-APP*
- [ ] Q3. After D-APP PR 1 merges: confirm Railway deployed `main`, and redeploy the edge function that wrote the dead domain: `npx supabase functions deploy huggingface-upload --project-ref <ref>`.
- [ ] Q4. Do not point anything at `reigh.art`, `reigh.ai` or `reigh.app`. A third party holds `reigh.art`; `reigh.ai` and `reigh.app` do not resolve. Their DNS and registration are the owners' call (D7), but no code references them any more.

**External names, in cutover order** (this replaces the old N-INFRA list; the manager pastes exact values)
- Supabase secrets: `REIGH_APPEND_SERVICE_URL`, `REIGH_APPEND_SERVICE_INTERNAL_TOKEN` (`supabase/functions/_shared/reighAppendService.ts:7-8`) become `ASTRID_APP_APPEND_SERVICE_URL`, `ASTRID_APP_APPEND_SERVICE_INTERNAL_TOKEN`.
- Railway: build var `VITE_REIGH_APPEND_SERVICE_URL` becomes `VITE_ASTRID_APP_APPEND_SERVICE_URL`; service `reigh-production` (host `reigh-production.up.railway.app`, `config/vite/policy.ts:7`) gets a new host that goes into `PREVIEW_ALLOWED_HOSTS`. The repo shows only `Dockerfile:31 ARG VITE_APP_ENV`, so list what the Railway dashboard holds.
- CI variables `BANODOCO_RUNTIME_CHECKOUT`, `REIGH_WORKER_CHECKOUT` (workflow `env`, so likely nothing to do), and shell and launch-config `BANODOCO_*`.
- Supabase hosted project: confirm its ref is not named after the old name (only the local `project_id` is). It is not renamed.
- Public install surface: URLs in `src/pages/Home/publicAstridLinks.ts:4` (`REPOSITORY_URL`), `PublicAstridHeroCta.tsx:8` (`git clone https://github.com/banodoco/reigh-app.git`), `HeroSection.tsx:13` (`https://github.com/banodoco/Reigh`, capital R, probably dead), `README.md:16-17` (`git clone https://github.com/peteromallet/reigh`), `scripts/astrid-landing/prepare.py:249,306`, `prepare-public.py:132` (pinned `APP_COMMIT`). Map rows rewrite them; the owner reviews the result in the C-APP diff.

**Deploy (after landing)**
- [ ] D1. Supabase secrets: set `ASTRID_APP_APPEND_SERVICE_URL` and `ASTRID_APP_APPEND_SERVICE_INTERNAL_TOKEN` (new names, map-authoritative) with the values of the old ones; deploy; then unset the old ones.
- [ ] D2. Supabase: deploy the App's edge functions. Delete the deployed edge function `reigh-data-fetch` (its code was deleted by D-APP; no caller): `npx supabase functions delete reigh-data-fetch --project-ref <ref>`.
- [ ] D3. **Only if Q2 returned rows:** run `tools/astrid-rename/extension-id-rows.sql` once in the SQL editor or `psql`, in the cutover window, and keep the printed counts. If Q2 returned 0, there is no D3.
- [ ] D4. Supabase: `npx supabase db push --linked`. It applies the new forward migrations (the CHECK change if Q2 was 0, and the route prose `UPDATE`). The in-place comment edits to old migrations are not re-run.
- [ ] D5. Railway: set `VITE_ASTRID_APP_APPEND_SERVICE_URL` (value of `VITE_REIGH_APPEND_SERVICE_URL`), remove the old one, redeploy. Rename the service `reigh-production` or add a new domain; put the new host into `PREVIEW_ALLOWED_HOSTS` (already in the landed code). Keep the public origin `astrid.haus` unchanged: the browser copier cannot move data across origins.
- [ ] D6. GitHub Actions / CI variables and secrets: rename `BANODOCO_RUNTIME_CHECKOUT` and `REIGH_WORKER_CHECKOUT` if they are set as repository variables (verify).
- [ ] D7. Domains: decide what `reigh.art`, `reigh.ai`, `reigh.app` do (the owners' call: redirect, keep, let lapse). Code no longer references them (D-APP), so the plan does not need an answer to finish.
- [ ] D8. Verify production: load the App, create and save a timeline. (The extension host is off in production, so there is no extension step.)

**Per machine (C-MIGRATE)**
- [ ] M1. Census: run the byte census over every realm (C-MIGRATE step 1). Record the output. If it shows a targeted string, stop and tell the manager.
- [ ] M2. Relocate the support folder with the **old** install still running: `astrid-runtime backup --destination <dir>`, then `astrid-runtime relocate --plan --destination "$HOME/Library/Application Support/Astrid Runtime"`, review, then `relocate --confirm "RELOCATE <selected-realm-id>"`. Verify that `credentials/owner.token`, `discovery.json` and the catalog moved (unverified for the real tree). If the agent has shown on a scratch root that `upgrade --destination` does M2 and M3 in one command, use that one command.
- [ ] M3. Stop the old Runtime, install the renamed one, and switch shells and launch configs to the new env names in the same step: `BANODOCO_LOCAL_*` and `BANODOCO_RUNTIME_*` to `ASTRID_RUNTIME_*`, `REIGH_*` to `ASTRID_APP_*`, per `map-notes.md`. Start it. `astrid-runtime status` must be healthy.
- [ ] M4. Live film stack: switch `astrid-local/live-main/env.sh` to the new data-root variable in the same step as moving the stack onto renamed code. Check the film data root and its size before any traffic (C-MIGRATE acceptance).
- [ ] M5. Open the App once in each browser profile used with Astrid so the browser copier runs.

**Satellites (Phase 2)**
- [ ] S1. Archive `banodoco/reigh-workspace` (Settings, Danger zone, Archive).
- [ ] S2. Archive `banodoco/reigh-worker-orchestrator` (after the owner confirms `banodoco-worker/` is not deployed on Railway).
- [ ] S3. `banodoco/reigh-worker`: archive if N-SAT found nothing live; otherwise rename to `astrid-worker` and extend the plan.
- [ ] S4. Merge the scrub PRs in `banodoco-workspace`, `timeline-schema`, `timeline-composition`, `timeline-theme-2rp`.
- [ ] S5. Optional and the owners' call: delete instead of archive. Archiving is reversible and is the default.

**Final**
- [ ] F1. Approve P-FINAL (it deletes the plan). It does not wait 30 days.
- [ ] F2. Put the F-WINDOW date in a calendar. The GitHub issue P-FINAL opens is the reminder.

---

## 10. Done when

Plan complete (P-FINAL), all of these hold:
1. `check-zero` passes on every repo with an allowlist of **only** the browser migration module and its test: `for r in astrid runtime app; do tools/astrid-rename/check-zero --repo <checkout of $r> --allow <module and test only> || exit 1; done`; passes with profile `keep` on `banodoco-workspace`, `timeline-schema`, `timeline-composition`, `timeline-theme-2rp`; and passes with profile `local` on the local tooling listed in P-LOCAL.
2. Every old name is gone from file names too: `git ls-files | grep -iE 'reigh|banodoco_local|banodoco_workspace'` prints nothing in each repo.
3. No `reigh.art`, `reigh.ai` or `reigh.app` reference remains in any repo: `git grep -niE 'reigh\.(art|ai|app)'` prints nothing.
4. Tests and builds pass on `main` in all three repos (App: `tsc`, full `vitest`, `build` run locally); deployed App, Supabase and Railway run under the new names.
5. The owner has finished D1 to D8 (D3 only if Q2 returned rows), M1 to M5 and S1 to S5.
6. Tags `astrid-rename-done` pushed on the three repos at the commit that follows steps 1 to 5.
7. The F-WINDOW issue exists in the App repo, with a date and no old name in it.
8. One final commit in Astrid deletes `docs/plans/astrid-naming/` and `tools/astrid-rename/` (including any operator script). Its message contains the final `check-zero` output. After it, `git grep -il reigh` in Astrid prints nothing.

Complete later, standalone: F-WINDOW. After it, `git grep -il reigh` in the App prints nothing and no allowlist exists.

The pre-rename tags `pre-astrid-rename` stay. They are the archive.

---

## 11. Open questions

1. **Satellite conflict with the user's belief.** `reigh-worker` is live as far as Astrid CI goes (it imports it), and `reigh-worker-orchestrator`'s pod template clones `Reigh-Worker` into pods (`worker_startup.template.sh:254-266`). Whether the orchestrator is still deployed (Railway) cannot be seen from the repos. The decision treats both as deprecated. N-SAT checks; if a deployment is live, the plan gains a C-WORKER task.
2. **Other team machines.** The byte census found nothing on this Mac. Another team machine (for example Peter's) may have saved live scenes or other targeted strings. C-MIGRATE M1 settles this per machine in seconds. Decision if it finds something: write an operator script then.
3. **Support folder relocation.** Decision: `Astrid Runtime`. Unverified: that `relocate` moves the whole tree (`credentials/`, `discovery.json`, locks) rather than only realm data, and whether `upgrade --destination` does relocate and switch in one command. C-MIGRATE checks on a scratch data root.
4. **`ASTRID_BANODOCO_*` module name.** The env vars are renamed to `ASTRID_RUNTIME_*`, but the module `astrid/core/execution/executor/banodoco_catalog.py` keeps the community-facing `banodoco` name. Owner to confirm the catalog is Banodoco-community content.
5. **Kept satellites and `BANODOCO_`.** `banodoco-workspace` has 31 `BANODOCO_` lines and the orchestrator 28 that are its own env vars. The `keep` profile omits that pattern. If the owners want the `BANODOCO_` pattern enforced there, they must say so.
6. **`reigh-product-connector`.** App findings place it at `client.ts:371` and `dataProvider.test.ts:761`; the later audit found no hits in any repo. N-MAP re-greps before relying on either.
7. **Neutrality wording.** Runtime `README.md` and `conformance/second-client-core-v1.yaml:7` (`forbidden_symbols` lists `astrid`) describe a product-free contract. Naming the repo `astrid-runtime` is consistent with the enforced tests but not with that sentence. Decision stands; the sentence is reworded in C-RT.
8. **`astrid-runtime` command ownership.** The command `astrid-runtime` is defined by the Runtime (`pyproject.toml:15`, mapping to `banodoco_local.cli`), but Astrid also has `astrid/runtime_cli.py` with `prog="astrid-runtime"` (`:319`) and no console-script entry of its own. Which implementation `astrid-runtime up` reaches depends on the install. N-MAP must decide whether they are one command or two, before C-RT deletes `banodoco-local`.
9. **Capability ids and saved agent transcripts.** Old `reigh.*` capability ids and wire tags remain inside stored agent transcripts and prompts. The clean break leaves them unreadable by new code; this plan does not migrate transcripts. Confirm that is acceptable.
10. **Hivemind and Otto content.** Hivemind's knowledge content and Otto's project records probably mention Reigh. Out of scope beyond Hivemind's scripts (P-LOCAL). Decide whether to rewrite them.
11. **Dated design docs** `docs/design/*-2026-10-05.md` in the App are treated as live docs and renamed, not deleted. Confirm.
12. **Accepted losses to confirm.** Stated in section 4.7: team members lose dev-only extension settings and the `showDataLanesByKind` preference resets; old revisions in the film realm show source "other"; a pre-cutover `com.reigh.astrid.liveScene` clip is skipped by the new Runtime. Say so now if any is not acceptable.
13. **Browser local-media handles** (`reigh.local-media`) may not survive a structured-clone to a new database. N-BROWSER marks such entries as needing re-import and must not drop them silently.
14. **Domains.** What `reigh.ai` and `reigh.app` should do (they do not resolve) and whether the owners want `reigh.art` back, are the owners' call (D7). The plan only removes the references.
15. **Merge rights for the D-* PRs.** If the manager lacks merge rights on the three repos, the owner merges D-APP PR 1 immediately and the others in order.
