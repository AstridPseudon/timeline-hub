# D100/R1 protected test-purpose review

Result: FAIL exact evidence finding; source/test purpose checks PASS; behavioral test bodies NOTRUN.

## Exact scope

- Final commit/tree: `42040a9c05ae7105cf88459cad5f0b8b9bf56fd1` / `66c0215955332af8ed32ae7d4c17d4f71ccb17d4`.
- Base commit/tree: `9486cbb06e2ab53402086772e6c2bc18bc4849fc` / `0919e511bd28b3d3af76bb18155efda12c3e94f6`.
- `git diff --name-status BASE HEAD`: only `M tests/sdk/test_d100_item_birth_boundary.py`.
- Full tree comparison: every other repository blob and mode exact; product file unchanged.
- Product SHA-256: `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`.
- Test SHA-256: `fcd5f187e185faa2222fb23c69827bd6d8bcbb710fdad131f649973f95e6de37`.

## Purpose/predicate review

AST/source checks passed for all 11 test functions and 25 required predicate fragments. The two new custody cases compare `shots`, `placements`, and `_runtime_document` separately, allow only `_doc_patch_images` as an extra top-level key, and authenticate its owner, physical source IDs/revisions, payload, and internal timeline. Existing item correspondence, canonical payload, internal revision, original-bundle, no-write, wrong-source, digest, duplicate/empty/unique-ID, and previous-value guards remain present. No skip, xfail, `.fails`, arbitrary-key exclusion, or weaker positive was found.

The shared-owner setup uses admitted `source_offset = 0` and recomputes the parent payload digest. No non-default-trim semantic or product change is present. The current passing shared-occurrence comparator and authoring compiler guard were read; the 1858 disposition was treated as setup input, not as an automatic behavioral PASS.

## Commands and results

- `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_d100_item_birth_boundary.py` — exit 0.
- `/home/user/work/venv-agent/bin/mypy --config-file pyproject.toml --cache-dir=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-D100-test-review-1919/tmpdir/mypy-cache tests/sdk/test_d100_item_birth_boundary.py` — exit 0.
- `/usr/bin/python3.11 -c 'from pathlib import Path; p=Path("tests/sdk/test_d100_item_birth_boundary.py"); compile(p.read_text(), str(p), "exec")'` — exit 0.
- `git diff --check` — exit 0.
- Read-only AST/source/tree/hash check — exit 0 for source purpose and scope.

## Exact finding

The supplied `source1914/evidence/source-manifest.json` has both `agent.protected_product.sha256` and `agent.protected_product.required_exact_blob` set to the 63-character value `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a`, omitting the final `3`. The actual file matches the required 64-character value ending `...fa808a3`. This evidence inconsistency blocks `PASS_SOURCE_PURPOSE`; the product hash itself is correct.

Behavioral bodies were intentionally NOTRUN: free space was 4,492,472,320 bytes, below the 4.6 GB source floor and 5 GB behavior floor, and the brief forbids pytest/provider/live suites. Prior App candidate 24/27 and Runtime1858 setup disposition remain inputs, not automatic PASS.
