# Validation

## Result

The read-only stdlib validator passed the authentic-result checks and found one custody defect. It used `json`, `xml.etree.ElementTree`, `shlex`, `hashlib`, `ast`, `os`, and read-only `git` subprocess calls; it did not import product code, run pytest, collect tests, or open a live socket.

Checks passed:

- Central request, status, exit, summary, snapshot, external-version record, actual command, runmanifest, JUnit, body log, and preflight/body exits all exist at the recorded paths and hash consistently.
- Service `...10086` is distinct from preserved `...1347`; the latter remains exit 1 before pytest with zero selectors and no JUnit.
- Agent/Runtime/App/Composition actual HEADs and trees are exactly `28e56cac/2ebe2ddf...e58a`, `6a011d58/ac5b862...da28`, `867cb273/2b44a46...7dd`, and `635f4de0/5ab5191...148`; all four source checkouts are clean. The service snapshot's `/home/user/work/agent` tree matches the Agent pin.
- Recorded source-before, source-after, and source-final receipts normalize to the same four-way identity. The actual four-way checkout status is clean.
- Launcher, installer, and all three selected test-source byte hashes match the preserved source records. AST parsing found exactly one matching function per selector and no skip/xfail decorator.
- The actual command is a production `run -- -m pytest` command with the later `-m integration`, `-q`, cleared addopts, cache provider disabled, timeout 45, exactly three concrete selectors, and no collection-only/skip/xfail flag.
- JUnit XML reports one suite, three testcases, 0 failures, 0 errors, 0 skipped, and 23.668 seconds. JUnit module names were mapped honestly from dotted module names to the command's slash-path selectors.
- CAS preimage/backup/after hashes, exact candidate `21f407...c2f0b` readback, manifest `67ef...e5b9f` materialization, distinct input/body paths, and outside-row byte equality all pass.
- Source preparation floor was `4,600,000,000` bytes; body dispatch free space was `5,169,483,776` bytes against the recorded `4,700,000,000` body admission floor; recorded post-terminal free space was `5,039,706,112` bytes against the `4,000,000,000` stop floor. No stronger continuous-space claim is made.

## Custody defect

The materialized manifest and runmanifest still name the old `agt-P4-D141-cut-controller-0047/evidence/p4-d141c-normal.xml`. That file is absent. The actual command and actual JUnit are in `agt-P4-D141-operational-return-0055/evidence/body-evidence/p4-d141c.xml`, SHA-256 `afca45b7...3316d`. This is a metadata/discoverability mismatch, not evidence that the body was skipped, collected only, rerun, or run against another source tuple. The stale value remains unchanged in this review.

## Commands and results

- `git -C <each frozen checkout> rev-parse HEAD HEAD^{tree}` and `git status --porcelain --untracked-files=all` — PASS; exact pins and clean status.
- Read-only Python stdlib validation over the central request artifacts, manifest/runmanifest, actual command, JUnit XML, source bytes/ASTs, CAS registry/backup, source receipts, disk receipts, and historical receipts — PASS for all assertions except the explicitly recorded stale `junit_paths` identity.
- `git show tl/agt-P4-D141-operational-review-0101:evidence/review.json` and JSON read of 0106 review — PASS conservation check: 0101 `FAIL`, 0106 `PASS_OPERATIONAL_SOURCE` / `INSTALLATION_NOT_READY`.
- No `pytest`, suite request, body rerun, collection, product import, typecheck, lint, launcher control, registry mutation, or full suite was run by this reviewer.

No source, product, test, launcher, schema, guard, pin, kit, registry, or original evidence file was edited.
