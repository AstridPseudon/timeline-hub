Corrected only the source-identity prefix of the existing App suite row `ap2-P3-gate5-h6-0348` in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf:36`. Retained-object identity/content checks pass. **No actual-service or complete synthetic-snapshot prelude PASS is claimed.** Independent review and the manager-authorized single corrected service execution remain next.

First actual failure and retained evidence:

- Read PLAN §3 P1/P3/A2, C0 §§1–5/7 normative prose, repository CLAUDE.md, and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run` read-only. The runner creates `commit-tree $tree -p HEAD`, adds a detached worktree at that generated commit, links node_modules, then executes the suite there. Comparing this generated HEAD with the source commit cannot pass.
- Original result `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P1-reviewed-compose-0959-ap2-P3-gate5-h6-0348-1023103137-14896` remains fail/exit 1 in 1 second, empty log. Its retained commit is `be75f72121d465d4d4e504723162d8afb045ddc2`, sole parent `1117c15f7e37a087a1175ea0e923958ce8a4132d`, tree `654a66946da8a4da65248576a9eb5e32a9e8d382`. Its commit message names that exact result ID.
- Initial review result `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P3-preflight-review-1029-ap2-P3-gate5-h6-0348-1023103030-20262` remains fail/exit 1 in 1 second, empty log. Its retained commit is `cf189516aacea4e6438c9f29eaf872ceb14efa1e`, sole parent `0cdc76782833d594776452e07706acb406c51553`, same tree. Its commit message names that exact result ID.
- Therefore the first failing primitive is the row's very first `test "$(git rev-parse HEAD)" = 1117c15f7e37a087a1175ea0e923958ce8a4132d`. In result 14896 its left operand is `be75…`, not `1117…`; result 20262 has `cf189…`, not `1117…`. No later guard or body is reached. The 1021/1029 green reports do not establish service-snapshot prelude success.
- Recovered these existing loose commit objects by reading the Git object store without writing it, then authenticated their actual contents with `git cat-file -p`, `git rev-parse <object>^{tree}`, and `git merge-base`. No synthetic object was created.

Decision and exact change:

`APP_HEAD` is the actual checkout identity. `APP_SOURCE_HEAD` is either that identity when it is exactly the qualified reviewed `1117…` or owner `0cdc…`, or the actual commit's **entire parent list** (`git show -s --format=%P "$APP_HEAD"`). The latter must equal exactly one of those two commits, so an unrelated source or multiple parents fails. Both source tree equality and explicit `1117…` source ancestry are checked. `0cdc…` is the owner merge whose parents include `1117…` and whose entire tree is identical; this is an exact additional source pin, not permission to accept any descendant or any equal-tree commit.

Replacement prefix (all original text following the former first primitive is byte-identical):

```sh
APP_HEAD=$(git rev-parse HEAD) && APP_SOURCE_HEAD=$APP_HEAD && { test "$APP_SOURCE_HEAD" = 1117c15f7e37a087a1175ea0e923958ce8a4132d || test "$APP_SOURCE_HEAD" = 0cdc76782833d594776452e07706acb406c51553 || { APP_SOURCE_HEAD=$(git show -s --format=%P "$APP_HEAD") && { test "$APP_SOURCE_HEAD" = 1117c15f7e37a087a1175ea0e923958ce8a4132d || test "$APP_SOURCE_HEAD" = 0cdc76782833d594776452e07706acb406c51553; }; }; } && test "$(git rev-parse "$APP_SOURCE_HEAD^{tree}")" = 654a66946da8a4da65248576a9eb5e32a9e8d382 && test "$(git merge-base 1117c15f7e37a087a1175ea0e923958ce8a4132d "$APP_SOURCE_HEAD")" = 1117c15f7e37a087a1175ea0e923958ce8a4132d
```

The original HEAD-tree check, clean snapshot check, 8770 ancestry check, all 46 file-hash guard occurrences, 34e frozen producer validation, private 819acf artifact, package/origin/export checks, pin checks, Python check, exports and selected original npm/grep command are retained. No P1 change, guard waiver, Git shim, host script, product/test/helper, generated/pin or shared dependency edit.

Byte checks (SHA-256 includes each row's newline):

| Bytes | SHA-256 |
| --- | --- |
| P3 before | bc94ca8a61bf2ad0f9afbebacbfdff802287793e914597c899e68f0a6b33866f |
| P3 corrected | 48499e7d96c570ce32065d5e4981002d416a471c955ad83a17bda65c451668d1 |
| P1 unchanged | 234e7430dd785285ed4faa8ee5ff287555310aedda53b70c0ee5b4e33229418c |
| Every row outside P3, before = after | 4907fc1a7e1cc6d1679e33b4137e0eb42e97af146cee4fa0f4b112dab28215ae |
| Original entire P3 suffix, before = after | 635ab44786aaf19edc37a8d85461fb8a02893a03d1b6a1007ddcc9f0f7d04e53 |

Exact qualification commands and results (cwd `/home/user/work/wt/ap2-P3-snapshot-preflight-sol-1035`):

1. `python /tmp/w-fe0023a933/verify.py` — exit 0. Asserts only the source prefix changed and all other rows/P1 are byte-identical; parses the entire corrected command with `bash -n`; authenticates both retained service commits/parents/tree/result messages; proves old first primitive exits 1 for each actual object and corrected source/tree/ancestry logic exits 0. Direct 1117/0cdc pass; unqualified `23b0901ba1991f9720dd5d2522a76a8b89e45202` rejects with exit 1. All 46 unchanged hash occurrences match current source bytes and Git blobs from **both actual service trees**. The exact corrected prefix through HEAD tree/clean passes in this worker's actual 0cdc source checkout.
2. `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — exit 0, `ok runtime.lock.json (matches pinned producer commit)`.
3. Private graph checks, run read-only with `GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules`: original find-count guard (80), all four original negative path guards, and original `createRequire` export-prefix assertion all exit 0. The probe printed the actual three paths under `GRAPH/@banodoco/timeline-composition/dist/`. The exact read-only command is reproduced below.
4. `timeout 35 bash /tmp/w-fe0023a933/pinned-import-check.sh` — exit 0. This file contains the unchanged original row segment from `AG=...` through the final Python import primitive, excluding the following npm body. Exact Agent/Runtime heads, trees, cleanliness, Python executable/realpath and imports pass. No Python bytecode written (`PYTHONDONTWRITEBYTECODE=1`).
5. `node -e 'const fs=require("node:fs");const p="/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules/@banodoco/timeline-composition/package.json";const v=JSON.parse(fs.readFileSync(p,"utf8")).version;if(v!=="0.0.14")process.exit(1);console.log("private package version="+v)'` — exit 0, version 0.0.14. This checks the actual private file directly; it is not a replay of the row's relative require from a synthetic checkout.
6. `git diff --check` — exit 0; `git status --short` — empty. No tracked App worktree edits.

Private graph check from item 3:

```sh
GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules
test "$(find "$GRAPH/@banodoco/timeline-composition" -type f | wc -l | tr -d ' ')" = 80 && test ! -e "$GRAPH/@banodoco/timeline-composition/effects.generated.js" && test ! -e "$GRAPH/@banodoco/timeline-composition/animations.generated.js" && test ! -e "$GRAPH/@banodoco/timeline-composition/transitions.generated.js" && test ! -e "$GRAPH/@banodoco/timeline-composition/typescript" && env GRAPH="$GRAPH" node -e 'const {createRequire}=require("node:module"); const r=createRequire(process.env.GRAPH + "/__p3_probe__.cjs"); for (const x of ["effects.generated","animations.generated","transitions.generated"]) { const p=r.resolve("@banodoco/timeline-composition/"+x); if (!p.startsWith(process.env.GRAPH+"/@banodoco/timeline-composition/dist/")) process.exit(1); console.log(x+"="+p); }'
```

Qualification boundary / existing route:

Both original `.test-<result-ID>` detached directories are already removed by the service. The allowed retained-metadata route was used: real snapshot object identity, real parent list, exact source/tree/ancestry and actual snapshot Git blobs, all through read-only commands. The verifier supplies each retained object explicitly as a Git operand; it does not replace Git, HEAD, the index or refs. Its object-parameter checks and separate source/private environment checks must not be called an exact detached-layout full-prelude/service pass. The symlink swap and full contiguous prelude in a fresh service snapshot remain unverified here. No actual safety denial occurred.

Next: independent OPS review of this one-prefix change and its digest/evidence. After that review and manager authorization, the existing route for **exactly one** corrected original service execution is:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-P1-reviewed-compose-0959 ap2-P3-gate5-h6-0348 --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test <the returned result ID>
```

These commands are a handoff only and were **not executed**. No browser, HTTP/body, full suite, build, service, request-test, daemon/hub/dispatcher/process action, upstream change, Git write, ref mutation or deletion was performed. No independent reviewer was spawned; the manager owns that next dispatch. The two prior service failures and their metadata remain untouched.
