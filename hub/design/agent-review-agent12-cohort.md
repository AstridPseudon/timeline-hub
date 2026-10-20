# Agent review: tl/vw-m3-agent12-presenter-cohort (ce251003)

Reviewer: agt-review-agent12-cohort (read-only; no repo changes, no commit-msg, no test runs).
Subject: `tl/vw-m3-agent12-presenter-cohort` at `ce2510034`, supersedes `f29a9475` (Composition 0.0.12 pin) and `tl/vw-m3-agent-consume12`.
Merge base with `tl/integration` (0e951d68): `6c5aab20`. Branch = `6c5aab20` + `f29a9475` (adopt 0.0.12) + `ce251003` (presenter pairing). 33 paths, +1554 / −54.

## Verdict: REJECT (this revision), narrow

One requirement fails: the theme-constant equality test is not real. Everything else checked is sound, and the fix is small. Re-review after R1 is fixed; no other rework is needed.

### Blocking

**R1. The theme-constant test uses a copied literal, not the Agent host constant.**
`tests/packs/rendering/presenter_scene_capability.mjs` lines 50–59 do `assert.deepEqual(DEFAULT_THEME, {id: 'banodoco-default', visual: {...}})` with the navy values typed in by hand. Nothing compares against Agent's `BUILTIN_DEFAULT_THEME` (`astrid/core/theme/_schema.py:174`). `grep BUILTIN_DEFAULT_THEME tests/` returns nothing on the branch. I compared the values by eye: the literal matches both `BUILTIN_DEFAULT_THEME` and the 0.0.12 package's `DEFAULT_THEME` (`dist/chunk-GWYPEUCA.js`). That agreement is not guarded by any test, so a future drift on either side goes unnoticed.

Required change (small):
- In the Python fixture, serialise `astrid.core.theme._schema.BUILTIN_DEFAULT_THEME` (for example `json.dumps` into a file or argv next to `query.mjs`).
- In the mjs, `assert.deepEqual(DEFAULT_THEME, <that parsed value>)`.
- Keep the explicit historical black/Georgia `theme` block and its comment; that part is correct and is what keeps the 286 SSR hashes stable.

### Non-blocking

- N1. `tests/packs/rendering/test_presenter_scene_capability.py` has `assert hashlib.sha256(...).hexdigest() in {SHA256, "0a7b…"}`: the set holds the same value twice. Use `== SHA256`.
- N2. The handoff's test commands set `ASTRID_COMPOSITION_TEST_NODE_MODULES` to another worker's worktree (`/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`). That is a borrowed read-only dependency, not a clean provision. The default `ROOT/remotion/node_modules` does not exist in this worktree. Evidence for the merge should come from the central test service on the merged tree, not from that run.

## Checks (what I verified, and how)

| Area | Result | How |
|---|---|---|
| Tarball identity | PASS | `git show ce251003:remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz` → sha256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 58,444 bytes. Equals the `SHA256` constant in `test_composition_package.py`, `test_scene_answers.py`, `test_scene_host.py`, and the presenter test. |
| sha512 pin / lock integrity | PASS | SRI computed over the blob = `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`. Matches `remotion/package-lock.json` `integrity` and the `INTEGRITY` constant. |
| Composition provenance | PASS | Composition repo `5e06f40` (merge of `tl/vw-m3-release12`), prep commit `4b9f2ee`: `package.json` version `0.0.12`; source `DEFAULT_THEME` uses `#050814`. |
| Lock diff scope | PASS | `remotion/package-lock.json`: 4 lines changed (version, resolved, integrity). Nothing else moves. |
| Peer deps | PASS (unchanged) | 0.0.10 and 0.0.12 `package.json` both declare `@remotion/layout-utils`, `@remotion/media` 4.0.509, `react`/`react-dom` 18.3.1, `remotion` 4.0.509. Lock peer entries unchanged. `remotion/package.json` changes only the tarball path. |
| `artifacts.json` regenerated | PASS | Exported `ce251003` with `git archive` to scratch, ran `scripts/artifact_manifest.py --check` → `artifacts.json is current`. Presenter entries (`component.tsx`, `element.yaml`, `motion.ts`, new `scene.ts`) are identical to tl/integration. Only the `version` line and those entries differ from the base. |
| Presenter bytes | PASS | `astrid/packs/astrid_motion/**` is byte-identical between `ce251003` and `tl/integration`. |
| Old 0.0.10 tarball | PASS | Removed on the branch (f29). No remaining references to `timeline-composition-0.0.10.tgz` in the branch tree. Deletion is correct. |
| No schema / provider / compiler change | PASS | Changed paths: `astrid/core/rendering/remotion_runtime.py` (one constant), `astrid/packs/astrid_motion/` (presenter + pack.yaml), `remotion/` package files, `artifacts.json`, and tests/fixtures. None under `astrid/core/timeline/schema`, `astrid/sdk`, providers, or the compiler. |
| No crop deletion | PASS | `git diff` has no removed line containing "crop". Presenter `motion.ts`/`component.tsx` changes are moves (`anchorOr`, `mouthEraseRect`, `pixelGeometry`) into `motion.ts`/`scene.ts`. |
| No skip / xfail added | PASS | Added-line grep for skip/xfail/fails/todo: only a `skipLibCheck` tsconfig option. |
| Runtime tarball | PASS | `runtimes/agent-remotion-0012/artifacts/banodoco-timeline-composition-0.0.12.tgz` is byte-equal to the branch's tarball. Installed `node_modules/@banodoco/timeline-composition/package.json` version `0.0.12`. |
| Runtime lock byte-equality | **FAIL on the runtime side** | `runtimes/agent-remotion-0012/package-lock.json` is NOT byte-equal to `remotion/package-lock.json`. The runtime lock equals the Agent lock except that 8 `"libc": [...]` blocks are missing (glibc/musl entries for native optional packages). `remotion/package.json` is byte-equal. The Agent lock is the correct one (npm output; equals base + composition-only change). The runtime lock looks hand-derived or re-written without npm's `libc` fields. `remotion_runtime.py` (around line 405) hashes the project `package-lock.json` into a render fingerprint, so this mismatch matters. This is not a branch defect. See the merge plan, step 0. |

Not verified by me: the 33 targeted tests the handoff reports. Running tests was not part of this read-only review. I did not reproduce them.

## Merge plan

Current state, from `git` and the orchestrator notes:
- `tl/integration` = `0e951d68`. It already has the identical presenter source (`80266992`, "expose current presenter scene capability"). It is still pinned to Composition 0.0.10, has the 0.0.10 lock and `package.json`, and has an `artifacts.json` with a changed `cli-surface.json` entry.
- `tl/vw-m3-agent12-presenter-cohort` (`ce251003`) carries the 0.0.12 pin plus the series/selected-cut query helpers and tests that integration lacks.

### Step 0: precondition, runtime side (orchestrator)
Re-materialise `runtimes/agent-remotion-0012` from the reviewed `remotion/package-lock.json` (with the `libc` fields) and re-check its lock bytes. Do not hand-edit the shared runtime; it is read-only to workers.

### Step 1: fix R1 on the branch (owner of `tl/vw-m3-agent12-presenter-cohort`)
Apply R1 and N1, then regenerate `artifacts.json` (`scripts/artifact_manifest.py`, then `--check`). Re-review the delta only.

### Step 2: land Composition unit onto `tl/integration`
Expected merge result against integration:

| File | Git result | Action |
|---|---|---|
| `artifacts.json` | **conflict** (integration changed `cli-surface.json` and `version`; branch changed presenter entries and `version`) | Do not hand-merge. Take either side, then regenerate with `scripts/artifact_manifest.py` after step 2 and again after step 3. |
| `tests/packs/rendering/presenter_scene_capability.mjs` | **conflict** (integration keeps `theme = DEFAULT_THEME` and no historical theme block) | Take branch version. Integration's variant drops the explicit historical theme that keeps the SSR hashes stable. |
| `tests/packs/rendering/presenter_crop_geometry.mjs` | **conflict** (branch adds the `seriesInspection` helper and the `prepareRoot` export; integration lacks both) | Take branch version. Integration's lack of `seriesInspection` is the series regression the branch restores. |
| `tests/packs/rendering/test_presenter_scene_capability.py` | **conflict** (integration: 0.0.10 artifact, `public10` names, `SHA256` imported from `test_composition_package`) | Take branch version, which is the 0.0.12 test with its own `SHA256`. Its tests and names are a superset. |
| `remotion/package.json`, `remotion/package-lock.json`, `astrid/core/rendering/remotion_runtime.py` | clean (integration still at base here) | Take branch. Integration's `_COMPOSITION_PACKAGE_VERSION` moves 0.0.10 → 0.0.12. |
| `tests/packs/rendering/test_composition_package.py`, `test_scene_host.py`, `test_scene_answers.py`, `test_render_export_task_adapter.py`, `tests/core/timeline/test_clip_fields.py`, `tests/journeys/test_journey_plumbing.py` | clean | Take branch. After this, no `0.0.10` pin remains except the historical key in `test_capture_scene_labels.py`, which is harmless and already expects 0.0.12's hash. |
| Presenter source, `pack.yaml`, `presenter_ssr_before.json`, `test_presenter_crop_equivalence.py`, selected-cut fixtures | identical on both sides | No action. |
| Series/selected-cut helpers and tests (`presenter_series_inspection.mjs`, `presenter_selected_cut_query.mjs`, `test_presenter_series_inspection.py`, `test_presenter_selected_cut_aggregate.py`) | branch-only additions | Keep. These restore regressions integration lacks. |
| `remotion/__smoke__/bundle.mjs` | integration-only change | Keep. Not touched by the branch. |

After step 2: run the presenter targeted set on the merged tree through the central test service, not in-sandbox. Expect `presenter_scene_capability`, `presenter_crop_equivalence`, `presenter_series_inspection`, `presenter_selected_cut_aggregate`, `test_composition_package`, `test_artifact_manifest`. Then regenerate `artifacts.json`.

### Step 3: Runtime pin unit (`tl/agt-m2-runtime-pin-current`)
Status: BLOCKED, per the worker's `BLOCKED` file. It needs a Runtime producer checkout at exactly `94114269` (`/home/user/work/runtime` is at `6023cfb`, a descendant). Orchestrator should create a detached worktree at `94114269`.

Important: `tl/agt-m2-runtime-pin-current` (`b7789c19`) is not a pin-only branch. It is a merge stack (`shot-settings`, `clip-set-element`, `stack-sync-3`, …). Cut the pin unit fresh from `tl/integration` after step 2, not from that branch.

Files the pin unit touches (per brief): `runtime.lock.json`, `astrid_runtime_client/*` (4 files), `tests/fixtures/runtime-responses/*`, `tests/fixtures/visual-boundary-v1.json`, `tests/editing_conformance/test_commit_runtime_m1.py`, `tests/sdk/test_capture_source_runtime.py`, `artifacts.json` (regenerated).

Overlap with the Composition unit: **`artifacts.json` only**. None of the others appear in the branch's 33 paths or in the integration deltas I checked.

### Step 4: final
Regenerate `artifacts.json` on the final tree and run `scripts/artifact_manifest.py --check`. Then App pins the same pair.

## Not in scope, and not claimed
- No activation of normal callers, no production source or custody qualification, no private crop or statistics retirement, no physical render capture, no parity or Gate 6 claim. Those remain as the handoff says.
- The handoff describes a 22-path delta (f29→ce251). The full branch diff against the merge base is 33 paths. I checked both.
