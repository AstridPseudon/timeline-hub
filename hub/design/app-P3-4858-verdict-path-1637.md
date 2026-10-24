# P3 verdict: FAIL

Independent verdicts:

- Identity: FAIL for whole-run stability. Start identity matched the manifest, but the afterAll source-tuple guard correctly failed.
- Behavior: FAIL. The primary App behavior/test-contract assertion failed.
- Do not call GO or waive the guard.

## Target execution

Run: `app-d66-plain-p3-three-products-1024163147-4858`

Command:

```text
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p3
```

- Exit: `1`
- Wall duration: `278s`
- Readiness: `1 passed`, `43.8s`, exit `0`
- Original P3: `1 failed`, JUnit `tests=1 failures=1 errors=0`, suite `106.291018s`, case `75.389s`, exit `1`
- Manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-d66-plain-p3-three-products-1024163147-4858/d66/manifest.json`

Target identity:

```text
App          e76ac72d887eee1634288d0208c27e27ef43e8d7
Agent        9a781a38f747ccf97274c22779b941f52184aa97
Runtime      bc227de07262accb702eae8a44c4a666b568c08e
Composition  635f4de06fda22a85fc2e4cfc764d0153a4c9f40
App tree     c13980c7c35c835b804d32c5bc9e501bdb8c1282
```

Versions: Node `v20.19.4`, npm `10.8.2`, Runtime `AstridRuntime/0.1 Python/3.13.16`, protocol `workspace.v1`, provider `astrid-v1`, compiler `authoring-bundle-1`.

Test SHA-256 values matched exactly:

```text
three-products.spec.ts                    95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c
three-products.mounted-readiness.spec.ts  2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593
schema                                        sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b
```

## Primary failure

At [`three-products.spec.ts:1347`](/home/user/work/wt/app-P3-4858-verdict-path-1637/tests/e2e/local/three-products.spec.ts:1347):

```text
Expected intent: Save local editor changes
Received intent: Move f2-app-clip on V1
label: Edit timeline
tags: []
```

The source cause is concrete and App-local:

- [`timelineLocalSaveHandoff.ts:572-577`](/home/user/work/wt/app-P3-4858-verdict-path-1637/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:572) intentionally emits `Move <clip> on <track>` for a move gesture.
- That behavior came from `f2d6d62c7b2ed...`, “preserve parent move read intent.”
- The P3 helper expectation at line 1347 predates that change and still requires the generic save intent.
- P3 setup at lines 1665-1667 already expects the semantic move intent.

Smallest existing owner: App P3 test/contract ownership should reconcile the stale helper expectation with the established move-intent behavior, or explicitly decide that the production contract should revert. No edits were made.

The path reached:

- build and native seed
- Agent identity and authoritative-history readiness
- Gate5 setup/reset
- first mounted local move
- lost ACK handling
- independent Agent `C` commit at line 1705
- second local move and durable-owner inspection

It failed before:

- `expectV2History` for the mounted A request
- page reload
- Runtime restart
- recovery and exact retry
- merged B commit
- undo, preview, final Agent readback, and completion facts

The source path is consistent with C0: gesture → `capture` → durable `appendDocument` → `localSaveSession` full-v2 request construction → Runtime commit endpoint. No evidence implicates Runtime or Agent in this primary failure.

## Secondary identity failure

The independent afterAll guard at `three-products.spec.ts:194` reported:

```text
astridHead:
  expected 9a781a38f747ccf97274c22779b941f52184aa97
  received ef0363985e645481952448619f2cbb25e9d51a66

astrid vendor source_commit:
  expected 8b32cacea617c6d45241d7db90b34893a06d3026
  received bc227de07262accb702eae8a44c4a666b568c08e
```

App head, Runtime head, schema digest, producer version, and App vendor lock remained unchanged. Therefore:

- The actual in-run drift was Agent checkout plus Agent vendor-lock metadata.
- The current manager merge `4395133afb` / integration `7f3d605d` is separately verified as metadata-only App scope: exactly `public/install-manifest.json` and `runtime.lock.json`.
- The target App snapshot remained `e76ac72…`; it did not become App product-source drift.
- This guard failure is preserved and must not be interpreted as the cause of the primary intent mismatch.

## Comparisons

Prior P3 `app-d66-plain-p3-three-products-1024161326-10033`:

- Exit `1`
- Readiness passed in `46.2s`
- Original JUnit: `1 test`, `errors=1`, `75.616859s`, case `37.178s`
- Failed earlier at `Gate5 precondition authoritative history mismatch`
- It did not reach the mounted lost-ACK/second-gesture path.

Passing P1 `app-d66-plain-p1-three-products-1024161133-26312`:

- Exit `0`
- Readiness `42.216s`
- Two behavior cases passed: `39.927s` and `23.671s`
- Reached accepted split, merged trim after Agent edit, lost ACK, restart, exact retry, and stale-trim refusal/rollback.
- Identity was stable for that run: Agent `9502c321…`, Runtime `8b32cacea…`, App `0e580cf…`.

## P3 history behavior row

| Behavior | Author | Review | Home merge receipt | Actual target |
|---|---|---|---|---|
| Gate5 mounted history classified as recorder ABI 2 | `471dc827b631247179b2295ad7a9151b6ab6fe5d` | `tl/app-P3-history-review-1626` | `9f4ec08f569f48fb859b5375e570c57b9bca2862`, tree `c13980c7…` | App snapshot `e76ac72d…` |

C0 `commit-v2.md` §§1, 4, and 7 require explicit step intent/tags/patch, authoritative `{data,receipt}` closure, and complete authenticated history. D62’s additive `recorder_abi` field belongs to authenticated history only. The target readiness and setup history checks passed; the primary failure occurred later at the stale move-intent expectation.

## Commands/evidence

Read-only checks used:

```text
git rev-parse HEAD
git show e76ac72d887...^{tree}
git diff --name-status e76ac72d887.....HEAD
sha256sum tests/e2e/local/three-products.spec.ts tests/e2e/local/three-products.mounted-readiness.spec.ts
jq ... d66/manifest.json
rg -n ... retained summary/log/XML/context
nl -ba three-products.spec.ts | sed -n '1328,1352p;1428,1470p;1634,1765p'
nl -ba timelineLocalSaveHandoff.ts | sed -n '565,590p'
nl -ba localSaveSession.ts | sed -n '158,194p'
```

No new tests, browsers, HTTP runs, full suites, raw wire/auth/trace/environment exports, or source edits were performed. The worktree is clean. Required `DONE` and commit-message markers were created.