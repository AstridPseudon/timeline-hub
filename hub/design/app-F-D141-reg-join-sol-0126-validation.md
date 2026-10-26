# Validation: PASS documentary packet; FAIL zero-REG qualification

No tests, imports, typecheck, lint, browser, preflight, service request or install were executed. No repository/Git metadata changes were made. Only the six requested evidence artifacts and required harness completion files are written. No `report.md` is written manually; the final message is the harness report.

## Existing execution receipts, read in place

Both original service registrations ran `npm test -- --maxWorkers=3`, which expands to `npm run test:app && npm run test:node --maxWorkers=3`. The flag therefore belongs to the Node script in that expansion, not directly to the Vitest command. Vitest command: `vitest run --config config/testing/vitest.config.ts`, after package quality checks. Neither Node phase started because Vitest exited 1.

| Receipt | Status/exit | Vitest file counts | Vitest test counts | Node |
| --- | --- | --- | --- | --- |
| `app-full-1026004326-12174` | fail / 1 | 5 fail + 1356 pass = 1361 | 33 fail + 19734 pass = 19767 | NOTRUN |
| `app-D141-pristine-receiver-0007-full-1026010029-23581` | fail / 1 | 3 fail + 1276 pass = 1279 | 18 fail + 17856 pass = 17874 | NOTRUN |

Normal failed-ID files: four; separate collection-error file: one. Normal shot-group file: six tests, one failure, 3 versus required 2 loads. Pristine shot-group file: six tests, all pass. Pristine affected renderer files: 12 + 12 + 3 = 27 tests, with 5 + 11 + 2 = 18 failures.

## Read-only source commands and findings

Commands used the App object database with exact refs; no checkout:

```text
git -C /home/user/work/app diff 7ca61bb3280beca21d98a854af266a382f7ce5df 867cb2737af1b46dc608c7cd37c349e920fe9422 -- src/tools/video-editor/lib/shot-group-pack-commands.test.ts src/tools/video-editor/lib/shot-group-pack-commands.ts
git -C /home/user/work/app show -s --format='%H %T %P' 867cb2737af1b46dc608c7cd37c349e920fe9422 7ca61bb3280beca21d98a854af266a382f7ce5df
git -C /home/user/work/app cat-file -p 4bb696aceae83a3843df47ff1ff99c9717a3e0aa
git -C /home/user/work/wt/app-F-D141-reg-join-sol-0126 diff --name-only
```

Results: production duplicate caller blob unchanged; mock assembly adds then subtracts one load; source trace identifies cut's second unconditional basis load. Exact source trees/parents match `join.json` and `shot-group-verdict.json`; normal merge has two parents. Hosting checkout diff is empty. `git show REF:PATH | nl -ba | sed -n ...` supplied the cited line ranges. `git cat-file -e` returned expected missing-path failures for pristine A3, runtime-elements and genericPatch files. Those are membership findings, not failed execution or test PASS evidence. Pristine hook source contains older titles and lacks generated prepared-video/Undo families.

`cat`, `sed`, `rg`, `awk`, `jq`, `ls`, `stat`, `realpath`, `sha256sum` read original evidence, runner/registration scripts, package metadata and raw logs. `ls`/`stat` returned expected ENOENT for receiver node_modules and shared theme. `realpath` on a nonexistent leaf alone was not accepted as existence evidence. Shared composition is 0.0.10 versus pristine linked vendor 0.0.2; shared theme is absent versus pristine linked vendor 0.1.0. Shared and pristine-locked Vitest both say 4.1.5; there is no claimed Vitest-version mismatch. No install or product import was used to qualify these bytes.

## Static JSON reconciliation

`jq --rawfile log <normal log> ... <0120 join.json>` checked every exact `FAIL  FILE > TITLE` line: unmatched/duplicate IDs `[]` for all 33. The analogous command against pristine log and 0120 `pristine-environment.json` returned `[]` for all 18. These are text/JSON checks, not test executions.

`jq -n --slurpfile old <0120 join> --slurpfile new <corrected join> ...` returned true for all 33 ID/file/title/presence/pristine-outcome identities, all 32 ours-only predicate descriptions, and unchanged collection semantics apart from the added receipt location.

`jq -n --slurpfile j <join.json> --slurpfile v <shot-group-verdict.json> --slurpfile p <pristine-targeted-recipe.json> ...` parsed all three JSON files and returned true for 33 distinct normal IDs, 32 ours-only, one productREG, zero nonREG-both, separate collection error, matching shot verdict, 18 distinct pristine IDs, exactly three affected files, no submission and no new execution. No semantic input/assertion was rewritten.

## Immutable input hashes

Before and after evidence authoring, `sha256sum` returned these identical values (paths below are relative to ORCH):

| Input | SHA-256 |
| --- | --- |
| `workers/app-F-D141-reg-join-return-0120/evidence/join.json` | `22252b1b23d677d745aff4c4b7b29ece8bfb6f89643048be8628ac80358d18f7` |
| same packet `pristine-environment.json` | `0a76040e30ee699b407501bd62c9187f558e43a4478167be9530299df1590a01` |
| same packet `source-custody.json` | `bc4b83f25fb00802f3e0dfe91a2dd25e89a924459962996f8ab928210678b5a0` |
| `tests/app-full-1026004326-12174/log.txt` | `fcc5e73b9fa41f7ff7afc8f91813a126495d52358f5d32d1505874b546349fd6` |
| same result `snap` | `b6a6d758652411b1efd1bd00e1f5aa1e214900308fec5346cfa302be17a225a7` |
| `tests/app-D141-pristine-receiver-0007-full-1026010029-23581/log.txt` | `636457440c919df79760fe2a9e5e5c008491e283b97ca2b10c475f2b1ffa9ba6` |
| same result `snap` | `a0571d732f06fa0859e4358c77046925859d10ddcb6461998992528c46e5270d` |

Source package/lock hashes were read using `git show REF:PATH | sha256sum`:

| File | Cut | Pristine |
| --- | --- | --- |
| `package.json` | `0f66d33d1fdbcf4ff2fe4c3bde81e6d5125831971d3fe492798116bc0f3b5d77` | `ec14f4ba4ec7efd7496a6335e044e63cb0d8e3281da959896b12c9010addf4b6` |
| `package-lock.json` | `59cd66da9a223eb1ff3cf60fd06dfa5b4b376533786366bd94b74ae3d95140ba` | `89a3094c58bab686ca620fd239228627659ed19fdc9853b2a86ba42388216000` |
| `runtime.lock.json` | `7b630bea187a47350726234a4534a2db7354a29708665b14d8d3c42c4dfaa3a9` | `34afa8e41aad26c710944193797e96f1aea10accb868554969cedc2bacdd90e6` |

No raw KEEP copying, deletion or mutation occurred. New evidence is small and documentary. Pending execution evidence: exact three-file targeted pristine receipt under its lock-derived install and recorded actual settings; separate authorized Node phase after journeys. These do not erase the finite shot-group productREG proof or justify REG0.
