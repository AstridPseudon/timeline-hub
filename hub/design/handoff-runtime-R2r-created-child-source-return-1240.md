# R2r captured source authority return

Implementation and candidate review complete; **landing remains blocked on harness commit, merge and integrated proof**. No DONE file is created. Base is exact `3b926efab2eed122d374540baee297d4cdcec62a`; the only worktree changes are the four allowed Python files. No Git write, commit, merge, checkout, push, dependency/host-daemon/config/client/schema change or file deletion was performed.

## Change

Ported the exact cumulative TWOFILE diff from `9345cb58fe8c54f114d666929e167bbeb5899c6c` (tree `1675bb7084786f55a4343b366782bc209ad9a1c4`) using read-only Git reads, directly onto the fresh base. Failed ancestors are not landing parents. The previous 1204 allocation, physical identity, ownership, before-image, digest, ambiguity, ordering and inverse-stage guards remain.

Sequential document manifests now consume the frozen `source` and `transcript` kinds rather than a non-wire `document` kind. The request port checks every recorded source/transcript/media assertion against exact captured authority and candidate-manifest membership. Source/transcript kinds must match the actual captured document kind. Revalidation of ownership, live/retained versions, bytes, selected media lifecycle and current authorization remains in the existing pre-write acceptance path. A dependency assertion alone grants no authority.

A genuine native transcript capture exposed an existing effect-before parent mismatch: the provider derives the input parent with hydrated document pins while the stored input retains its old parent ID. The smallest normalization derives the exact scoped authoring parent ID using the step input plus only first-command document dependencies, retains digest equality, and excludes inverse-stage boundaries. It does not admit arbitrary equal-byte revisions or later-command authority. The new positive exercises public verified-document capture, native anchor, occurrence birth and child track, with canonical readback, authenticated history and exact retry. Wrong before-pin and late dependency both refuse without writes. Initial malformed test word-ID and development/history-scope failures were corrected as fixture/implementation issues; their logs are diagnostic only.

The original unconsumed dependency acceptance seam is **preexisting on 3b926ef**: port validation was one-way (manifest pins needed records, but extra records were unchecked). The `document` enum mismatch was in the imported cumulative patch. Both are repaired inside the authorized auth/port boundary. No settled plan or contract decision was changed.

## Evidence

Exact new forged-source control copies command 1's schema-valid `source.forged` / foreign-document / version 1 / sha256:111...111 dependency, with no capture or manifest pin. A fresh public flow against exact 9345 accepted it and persisted history as `txn-935ed33c320b44e79cba29f9a0d09531` (`red9345-forged-source-accepted.json`). Current source refuses it and preserves head/history/database. The old module blobs are durably retained and read-only overlay use is solely causal evidence, never fresh acceptance credit.

Exact1204 unchanged forged-candidate hash is `aa811bd4ff1086bb0683d4553d3f03494c7dde844a035076bb726ac70a1b2c1b`: old 7fbb full validate ACCEPTS; current full validate REFUSES; authentic original candidate passes both. This is causal evidence, not reused receipt credit.

Final-module fresh receipts include:

- Three native commands: `txn-2f9e6ede47074e19afaf99ce8d46f6ca`.
- Five commands with earlier parent media: `txn-9e746c8cf8694a19b322b75b224ec109`.
- Native transcript capture / created child: `txn-8c38dd865b844dafb09262bb3d0f73d1`.

`evidence-index.json` identifies 49 durable current-module controls. Public witnesses retain actual full-v2 requests, prepared candidates (effects/bindings/dependencies), authenticated sources, receipts/readback/history, and before/after module origins/hashes. Source/transcript/media controls include authentic capture acceptance and uncaptured, missing, foreign, changed version/digest/owner, manifest omission and wrong-kind refusals. Tests directly assert head/history/full database equality on refusal. All 23 original auth and 44 original port top-level test/helper ASTs are preserved. All 77 frozen client/schema/control files remain unchanged, plus comparison against frozen 34e schema/client/generator bytes; edit-command digest remains d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d.

## Exact commands and results

From the worker worktree (`E` below is this worker's absolute `evidence` folder):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:$E ASTRID_CHECKOUT=/home/user/work/agent TMPDIR=/tmp/w-0c92cfbbb2 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p pytest_source_evidence tests/test_timeline_commit_authentication.py tests/test_timeline_commit_inputs.py tests/test_timeline_commit_port.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_raw_capture.py
```

Final result: **273 passed in 75.94s**, exit 0 (`safe-targeted-final.log`). All marked nodes are included by `-o addopts=`; no separate duplicate marked lane was requested. The final rerun followed the inverse-stage restriction change.

Socket files ran only through the central service:

```bash
$ORCH/bin/request-test rt-R2r-created-child-source-return-1240 reference-fixture-agent-current-integration --files 'tests/test_timeline_commit_read_basis.py tests/test_timeline_source_document_boundary.py'
$ORCH/bin/wait-test rt-R2r-created-child-source-return-1240-reference-fixture-agent-current-integration-1023125725-31318 1
```

Central command: `env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_commit_read_basis.py tests/test_timeline_source_document_boundary.py`. Result **15 passed in 5.85s**, exit 0, snapshot tree `ed9856f43a4e44a058bf2230badea2c4c7080050`. Neither file has integration-marked nodes, so its default marker filter excludes none. Full summary retained as `central-socket-summary.txt`.

Thus all **288 nodes across the requested eight files pass**, with sockets delegated centrally. The exact SINGLE combined eight-file invocation was not completed: an initial direct development invocation was interrupted (exit 130, seven unmarked passes) when the socket-containing scope was noticed; a central request with `-o addopts=` in `--files` was rejected as `bad file arg -o`. No suite ran for that rejected request. An asynchronous question requested a suitable exact-command named suite or direct authorization; no answer was received. The split qualification above respects the socket-service rule and covers every requested node, but does not claim the exact single invocation.

```bash
/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_port.py
/root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_port.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python $E/static_checks.py
R2R_OLD=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python TMPDIR=/tmp/w-0c92cfbbb2 /home/user/work/venv-runtime/bin/python $E/original1204_probe.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python TMPDIR=/tmp/w-0c92cfbbb2 /home/user/work/venv-runtime/bin/python $E/original1204_probe.py
```

Ruff exits 1 with **12 inherited diagnostics**, versus 13 on base, **zero added identities**. Pyright exits 1 with **35 inherited diagnostics**, versus 35 on base, **zero added identities**. They are not clean whole-file checks; inherited code was not reformatted or rewritten. AST/diff/frozen checks pass; normalized before/after diagnostic JSON and identities are retained. Both exact1204 commands exit 0 with the expected opposing causal results.

Fresh public standalone probes (full logs and code retained) used `ASTRID_CHECKOUT=/home/user/work/agent ASTRID_RUNTIME_CHECKOUT=$PWD PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent:.:packages/python TMPDIR=/tmp/w-0c92cfbbb2 /home/user/work/venv-runtime/bin/python $E/public_probe.py` and `$E/public_parent_media_probe.py`; the forged-source run prefixes the latter with `R2R_MUTATION=forged-source`. The red9345 probe sets `ASTRID_RUNTIME_CHECKOUT=/tmp/w-0c92cfbbb2/old9345 PYTHONPATH=/tmp/w-0c92cfbbb2/old9345:.:packages/python` and runs `$E/red9345_public_probe.py`. Final-tree proof credit comes from the indexed 49 witnesses, whose origins/hashes exactly match current code.

## Review, remaining work and next steps

Independent read-only Luna review found no remaining blocker; `independent-review.md` retains its findings and resolution of the media-manifest concern. It ran no tests and changed no files.

No full, prohibited broad/native/original/browser/Agent or P1–P4 suite ran. No shared dependency or tool cache was modified. No merge/integrated proof is claimed: `.git` is read-only, and task instructions forbid this worker committing or merging. `commit-msg` is ready for one harness-created R2r commit. The orchestrator must arrange the requested exact combined invocation if still mandatory, then dispatch the normal merge worker and integrated proof against the resulting integration head. Only after that can the whole task receive DONE. BLOCKED records these external prerequisites; the source implementation and candidate evidence are ready.
