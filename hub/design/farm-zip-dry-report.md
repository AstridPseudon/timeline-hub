# F-zip-dry report, refreshed 2026-10-23T16:00Z (supersedes the 14:50Z PARTIAL). Verdict: PASS for apply and tree equality on all four repos; fast checks PASS for app, composition and agent (agent mypy red, environment); runtime smoke tests blocked:permission. Nothing pushed.
Per-repo detail: design/farm-zip-dry-agent-3.md, -app-2.md, -runtime-3.md, -composition.md. Escalation for the one open refusal: escalations/farm-20261023T1552-pip-still-refused.md.

| Repo | Integration (tree) | Base | Patch | Fresh apply at base, tree equal | Live upstream tip | Fast checks |
|---|---|---|---|---|---|---|
| agent | d682c5977e0d (7d86b443453d) | 431681a6d | 9,491,748 B, 823 files | PASS | 74f3f7edb, already an ancestor of integration: no drift | ruff, import cycles, structure, doc-refs PASS; mypy gate FAIL (environment: shared venv lacks types-PyYAML and the Runtime package; the base fails the same way); smoke 86 pass, 3 skip, 1 fail (environment: fresh clone has no remotion/node_modules) |
| app | 6294895141 (03714e15a) | 7c17cc9d9 | 8,435,056 B, 517 files | PASS | efe83c77e, 27 commits past base: 510 of 517 files apply, 7 strict conflicts (4 under 3-way) | private 0.0.14 graph: tsc app 0, tsc node 0, lint 0, two quality guards 0, smoke 444 + 2793 pass |
| runtime | 9ce4242bc (92ab1f5f739f) | a98fbc2f9 | 5,209,625 B, 246 files | PASS | aa6c5b0cb, 4 commits past base (tests plus a runtime_protocol/visual_seam.py change); patch applies, drift recorded | py_compile 43 files PASS; no lint or typecheck configured; smoke tests NOT RUN, blocked:permission (pip install refused) |
| composition | 635f4de06fda (5ab5191a2969) | 67b8aa3d0 | 493,374 B, 118 paths | PASS | main is still 67b8aa3d0: no drift | node --check on three .mjs only; npm ci now permitted, not yet run |

Findings:
1. Upstream drift feeds the freeze-time U-tasks: App live efe83c77e (7 conflicts: 4 vitest/package.json/e2e files, groqSdk.ts add/add, tests/e2e/local/support/{app,harness}.ts); Runtime live aa6c5b0cb (overlap in tests/ and runtime_protocol/visual_seam.py).
2. Farm procedure note: a fresh-tree check must use `git add -f` for tracked-but-ignored paths (App's .gitignore has `*.md`, so docs/cutover-inventory.md is dropped by `git add -A`), or compare ls-tree listings.
3. App integration declares @supabase/supabase-js (CLAUDE.md forbids @supabase/*); round 2 checked for src/ imports in design/farm-zip-dry-app-2.md. Owner: App.
4. Agent mypy needs a venv with types-PyYAML and the Runtime package, and its smoke needs remotion/node_modules; a final-build run must provide them.
5. Open refusal: pip install into a tmpdir venv (Runtime smoke). Owner: orchestrator/owner.

Draft ZIP layout (layout only, not built):
```
final.zip
  README.md          base SHAs (agent 431681a6d, app 7c17cc9d9, runtime a98fbc2f9, composition 67b8aa3d0), integration SHAs and trees above, per-repo apply and verify commands
  agent.patch        git diff --binary 431681a6d..<agent integration>
  app.patch          git diff --binary 7c17cc9d9..<app integration>
  runtime.patch      git diff --binary a98fbc2f9..<runtime integration>
  composition.patch  git diff --binary 67b8aa3d0..<composition integration>
  per-repo apply:    git checkout --detach <base>; git apply --check <repo>.patch; git apply <repo>.patch; git add -f for tracked-but-ignored paths; verify `git write-tree` equals the stated tree
```
Heads move; the F-final build recomputes SHAs, trees and sizes at the freeze.
