# A4 parent raw witness report

## Delivered

Added only `tests/editing_conformance/test_a4_parent_media_raw_witness.py`.
No Agent product/API/schema/pin/Runtime files or existing tests were changed.
The test-only witness reuses `test_recipe_m2_parent_media.parent_inputs/args`,
uses the reviewed old App parent rows read from
`parentAfterAnchorCapture.test.ts`, and runs both the direct Agent executor and
the real Agent provider's preview/commit boundary.

Cases and observed current outcomes:

- literal ordinary parent birth: accepted; exact unknown/opaque/null fields and
  absent `at_ms`/`transition` survive;
- missing/null hold for raw video, raw image, and ordinary birth: refused as
  `invalid_edit_command` before write. The old after-anchor video rows were
  accepted by the old capture, so this is recorded as old accepted -> current
  refused rather than treated as parity;
- duplicate source clip identity in both parent mirrors: refused as
  `identity_conflict` before write;
- explicit null `track`/`asset`: refused as `invalid_edit_command`; explicit
  null `effectId`/`effect_id` is accepted and preserved in the positive row;
- source `at_ms`: refused as `unsupported_timing`, retained in the submitted
  input and not normalized/dropped;
- positive `.01s` subminimum: refused as `invalid_document` at final timing
  quantization because the interval collapses at the fixture FPS; zero: refused
  as `invalid_edit_command`. Neither is silently floored;
- incoming transition: refused as `unsupported_timing`, retained in the
  submitted input and not dropped.

Accepted evidence asserts preview receipt/status and no mutation, accepted
receipt/result, C0 label/merge/step/source/rationale/group metadata, exact
row/mirror preservation, authoritative reads, previous-value `ABSENT` writes,
created asset/clip identities, media owner/track bindings, and source
immutability. Refused evidence asserts structured status/reason/path/hint/
suggested-command and unchanged head/history/documents/accepted state.

## Source identity and scope

- Agent base before/after: `9a095a95178e0bb89ef3b2024d6502d47b35ac25`.
- Runtime authority used by tests: `/home/user/work/wt/rt-pin-2a9e347f`,
  before/after `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
- Reviewed App donor: `7f7e2daffad39a6d9aa3917a9fc526ba91caf2e6` (commit); exact
  `parentAfterAnchorCapture.test.ts` blob
  `346ae62eac5936e946266924f5e79e27df8dab54`.
- Current App source checked read-only: `2107e1870e51c650d59315f4cc1ab6af338f198c`.
- New test SHA-1 blob: `5aafdc44f52008625a66797ac6aaa928e6bf7f9c`.
- New test SHA-256: `59365260cd8ca828b6b1298c610a775a73611e92b96e914372da4c851f615c29`.
- `git status --short` showed only the new test path; `git diff --check`
  passed. Credential scan of the new file: 0 matches.

## Verification

All commands were run with the pinned Runtime path where applicable:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_a4_parent_media_raw_witness.py
13 passed in 1.77s

PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_a4_parent_media_raw_witness.py tests/editing_conformance/test_recipe_m2_parent_media.py::test_exact_capture_replay_scoped_birth_and_inverse[video] tests/editing_conformance/test_recipe_m2_parent_media.py::test_provider_exact_reload_inverse_redo_and_retired_ids[False]
15 passed in 1.96s

/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_a4_parent_media_raw_witness.py
All checks passed!

/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy tests/editing_conformance/test_a4_parent_media_raw_witness.py --hide-error-context --no-pretty
Success: no issues found in 1 source file
```

No full/browser/HTTP/gate suite was run or requested. No inverse, obsolete
capture-envelope, track.reorder, transcript.associate, source/catalog pin
negative, or retained original-14 matrix was duplicated. Uncovered by design:
mounted App execution/HTTP transport, Runtime service outside the Agent
provider boundary, and old after-anchor ripple/normalization parity beyond the
raw guard mappings above.
