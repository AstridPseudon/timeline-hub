# Immutable Agent public10 composition-consumer review

**PASS for this bounded consumer review; final source/adoption approval remains UNCERTAIN.** Reviewed only pinned imported commit `fc6c1f2615b1b37ae6bc2121397e64ee9d8061f5`, parent `4a75f68f32049a69fd86135c645fa64c51175c14`. This is not adoption or final owner publication. Native commands/provider, generated Runtime client and official Runtime pin review belong to their owners. The task explicitly says owner publication and Runtime confirmation are outstanding; lock contents are not confirmation.

No repository writes or git mutations. All review files are here in own ORCH. Agent worktree remains clean at the exact parent; no M1 files changed. Read PLAN first; actual absolute Viewing QUIET marker was absent before CPU checks (the ORCH root alias is dangling). No installation, network, browser, socket, full suite, or central test request.

## Findings

- Exact public10 artifact matches the immutable ORCH artifact byte-for-byte: **77 members, 58,008 bytes**, SHA256 `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`; computed SHA512 matches the new lock integrity. Full file size/hash manifests `public10-77-pre.txt` and `public10-77-post.txt` are identical (manifest SHA256 `9cce39da565f23fa820d9cb5bc77bd3ab8269bbb270d745365e182cd2dbb29d3`). `archives-pre.json` / `archives-post.json`: all **10** recorded original global/worker 8/9/10/11 archives unchanged, including global 8/9/11. `sparse-inputs.json`: all 113 imported files still equal pinned git blobs.
- Package spec, installed lock record and readiness version agree on 0.0.10. The lock graph is otherwise identical to parent. Exact peers in artifact, lock and reused read-only install agree: Remotion/media/layout-utils **4.0.509**, React/react-dom **18.3.1**. Public smoke confirms host/package peer identity. No shared Composition package was substituted for the extracted artifact.
- Readiness is unchanged except the version constant. Real 8 with baseline and real 10 with candidate both pass; each refuses the other version, and both refuse a removed evaluation entry. Original tests also prove package.json-only installation, removed/missing/escaping built targets, and launch-input binding fail closed. Readiness checks all eight required built JS/type export targets; it does not itself execute them. Separate actual Node imports cover their emitted JS graph.
- All eight required public entries resolve to this scratch artifact's `dist/`. Checked all 17 emitted JS files: imports resolve to built local chunks or declared exact peers; the evaluator's three-file closure has no runtime peers. No vendored Composition source, checked-in stale dist, private source imports, or separate npm timeline-schema/theme dependency was introduced. The existing Python schema admission requirement remains unchanged.
- Actual host imports remain small: Root/Three use `TimelineComposition`, `DEFAULT_THEME`, `getTimelineDurationInFrames`, `TimelineCompositionProps`; host maps use public registries/theme types; generator uses theme-api plus public evaluation capability types. Minimal actual-consumer ESM/type checks pass. Root is a rendering entry with peers; consumers needing pure evaluation can use `/evaluation`. No consumer migration or export narrowing is needed in this pin-only diff.
- Root, generator and host registries are unchanged. The original generated-custom-element test proves override isolation, capability, animation, transition and SSR consumption through the real package. PublicRoot resource containment, recursion rejection, declared aliases and captured-root behavior pass unchanged tests. Generators continue to target host source and reject output inside installed packages; no normal generated sources were written during this review.
- The imported candidate retains the unreferenced **0.0.8 tarball**. This matches its report but leaves deletion/cleanup outstanding with the adopter. Do not interpret this review as delivery cleanup complete.

One-screen file list/product hunks: **`viewing-approval.txt`**. Full literal scoped diff: `consumer.diff`. Raw graph: `consumer-imports.txt`, `package-import-graph.json`; readiness/lock results: `review-checks.json`.

## Exact bounded commands and results

Commands ran with the variables below expanded to absolute paths. `sparse/conftest.py` loads the exact pinned runtime and generator modules; their unchanged Python dependencies come from the parent worktree via PYTHONPATH. Original test files/assertions are unmodified. `-c /dev/null` isolates collection from unrelated repository conftest hooks; the integration mark emits a registration warning but all selected tests run.

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-public10-agent-composition-review
S=$O/sparse
P=/home/user/work/venv-agent/bin/python
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=/home/user/work/wt/vw-m3-public10-agent-composition-review
export ASTRID_NODE_EXECUTABLE=/opt/node20/bin/node
$P -m pytest -q -c /dev/null -o cache_dir=$O/pytest-cache --basetemp=$O/pytest-tmp $S/tests/packs/rendering/test_composition_package.py
# 6 passed, 1 mark-registration warning, 0.77s (pytest-package.log).
$P -m pytest -q -c /dev/null -o cache_dir=$O/pytest-cache --basetemp=$O/pytest-alias-tmp2 $S/tests/packs/rendering/test_remotion_v3_aliases.py
# 5 passed, 1 mark-registration warning, 0.48s (pytest-alias.log).
$P $O/review_checks.py
# exit 0: real8/real10 readiness, lock equivalence, peers and all built JS graph.
cd $S/remotion
/opt/node20/bin/node review-smoke.mjs
# exit 0: plain Node ESM, SSR, public behavior, scoped capability/override, peer identity.
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --strict --skipLibCheck --module NodeNext --moduleResolution NodeNext --target ES2022 consumer.ts
# exit 0 (types.log).
/opt/node20/bin/node actual-consumer.mjs
# exit 0: Root runtime names + all eight public entry resolutions (actual-consumer.log).
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --strict --skipLibCheck --module NodeNext --moduleResolution NodeNext --target ES2022 actual-consumer.ts
# exit 0 (actual-types.log): exact host/generator public type imports.
python3 $O/check_immutability.py
# exit 0: 77 files / 10 original archives / 113 pinned inputs / clean parent HEAD.
```

Initial alias attempt: **3 failed / 2 passed** because the sparse snapshot omitted declared element directories (`pytest-alias-incomplete-sparse.log`). Imported 45 exact pinned element manifests, then reran the unchanged test file successfully. Initial postmanifest comparison differed only in Path-versus-string sorting of `fade`/`fade-up`; standardized string ordering, and all 77 file bytes/sizes match. No product fix, assertion change, skipped test or xfail.

`review-smoke.mjs` and `consumer.ts` reuse public assertions from the Composition package smoke script; only its installer/npm-ls/cleanup wrapper is omitted. Source hash and extraction provenance: `reused-smoke-source.json`. Fresh extracted package and read-only peer symlinks replace installation. Scratch test/build outputs were removed after recording results; pinned sparse inputs and reproducible review harness remain.

## Limits and next steps

- **Final candidate SHA still needs owner publication/confirmation.** Do not approve or adopt a running branch based on this snapshot.
- **Runtime official `6be970633cc82ab412428151e6bf42f3e7fc3081` / source client 0.2.2 confirmation remains with owners**; no exact-pair integration claim or official-pin inference from `runtime.lock.json`.
- Node used was `/opt/node20/bin/node` **v20.20.0**, TypeScript from the existing App install. The repository pins Node **20.19.4**; its exact engine admission, npm install/typecheck gate, full host typecheck, normal render/visual/audio parity were **not run**. These bounded public-entry/type/SSR checks do not replace those gates.
- Viewing may approve this **eight-file consumer portion** subject to final owner source SHA and Runtime confirmation. Have adopter remove the unreferenced 8 archive as planned, then qualify actual provisioned runtime and normal consumer/render gates through the central service when authorized. No implementation decision was changed.
