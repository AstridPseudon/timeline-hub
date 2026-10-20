# Runtime current private carrier: CAS and catalog text

Status: private, reviewable carrier only. This is not a public pin, release,
activation, merge, or native-pair qualification.

## Composition

The worktree starts from reviewed Runtime carrier `7b8d6d9` (tree
`d20b745c26a33c2ea4e20863f846335c8cf33e1e`) and carries the current Runtime
tree represented by `9f211fc` (tree `d22726d982ac279277c4b0210495170556e3309d`).
The resulting tree is a two-parent resolution prepared without creating or
merging Git refs.

The harness will supply the final commit SHA after exit; this worker does not
invent one. The worker handoff report records the exact pre-commit tree.

Current `9f211fc` content is preserved byte-for-byte outside the established
17-path private-carrier allowlist. The private f802 command schema and its
generated bundle/metadata remain unchanged; the ordinary 0.2.14 55-definition/
29-operation source is separate and was not imported. No public generated
0.2.13 hash was published or staged.

The current catalog-text service and tests are retained exactly from `9f211fc`.
The private materialization store, materialization module, ownership fixtures,
promotion/fence guards, audit/shell guards, and existing private authority
checks remain from the reviewed carrier. The current selected-media CAS-byte
check is added to the private commit port without changing caller `id_map`
authority or rewriting map/version/ID-seed semantics.

## Boundary audit

An independent tracked-blob comparison against `9f211fc` reports zero
mismatches outside the 17-path allowlist. The private schema hashes remain:

- command schema: `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`;
- commit bundle: `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425`.

The current public floor was not changed. No tests were deleted, no assertions
were weakened, and no new skip or xfail was added.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B generators/generate.py` — pass.
- Same environment, `generators/generate.py --check` — pass.
- Same environment, `scripts/artifact_manifest.py --check` — pass.
- Direct current-slot subset of `tests/test_timeline_projection_ownership.py` — **10 passed, 45 deselected**.
- Central socket-capable targeted files (`test_timeline_clip_replacement.py`,
  `test_shot_text_bindings.py`, `test_timeline_shot_authority.py`,
  `test_shot_candidate_promotion.py`, `test_render_native_historical_retry.py`,
  `test_timeline_projection_ownership.py`) — **164 passed, 18 deselected,
  10 existing xfailed**. The xfails are the pre-existing D04 retired direct
  clip-replacement controls; none was added by this carrier.
- `git diff --check` — pass.

No full suite and no duplicate coordinated `3730` native pair was run. The
committed successor and its tree must be sent to Agent for final review of the
CAS/text composition, followed by exactly one coordinated `3730` actual pair.
