# D100/R1 independent CORE/SECURITY review

Verdict: **PASS_SOURCE_SECURITY**. Behavioral qualification is **NOTRUN** under
the mandatory disk gate.

## Scope and source identity

- Candidate: `9486cbb06e2ab53402086772e6c2bc18bc4849fc`, base
  `d4ba991638f7d94e6b9f91f5a463cd3587af00eb`.
- Exactly two candidate paths changed: `astrid/sdk/timeline/_command_state.py`
  and `tests/sdk/test_d100_item_birth_boundary.py`.
- The product delta is limited to `State.shot_item_map`, `State._item_ids`, and
  `State.project_shot_items`.
- Runtime is the immutable normal checkout `ab1e4f6141987706132916e2da16477f5a019464`
  with tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`; it was clean.
- The original peer report, author source-manifest, guard-map, red-green, and
  validation evidence were read. The author’s behavior result remains NOTRUN.

## Independent source/security result

The new physical-source branch authenticates the source shot, revision, internal
timeline, and all three content digests against the verified runtime document,
and requires the authenticated `item_id_map` to be exactly empty. The immutable
closure is revalidated by `bundle_from_document`. It admits only unique,
non-empty string item IDs for the physical source image and uses identity
correspondence; it does not derive allocation authority from caller
`source_mapping`. Existing copied/remapped placement checks remain on the strict
mapped-membership path. Existing wrong-pair, revision/digest, duplicate/empty-ID,
previous-value, and no-write guards remain fail-closed before writes.

The registered production path was traced statically as:

`RuntimeService.commit_timeline` → registered Astrid provider →
`commands.execute` → `doc.patch` → `State.set` →
`State.project_shot_items` / `State.shot_item_map`.

No Runtime/C0/private-trust source was changed. No findings.

## Commands and results

- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_command_state.py tests/sdk/test_d100_item_birth_boundary.py`
  — exit 0, all checks passed.
- `/home/user/work/venv-agent/bin/python -m mypy --no-incremental --cache-dir=/tmp/rt-Agent-D100-security-review-1803-mypy-cache astrid/sdk/timeline/_command_state.py tests/sdk/test_d100_item_birth_boundary.py`
  — exit 0, no issues in 2 source files.
- `/usr/bin/python3.11` compiling both exact changed files — exit 0, both
  compiled successfully on Python 3.11.17.
- `git diff d4ba991638 9486cbb06e --check` — exit 0.
- Exact changed-path check — passed; only the two authorized paths differ.
- Candidate file SHA-256, Git blobs, candidate tree, Runtime HEAD/tree, clean
  status, and import origins — all matched the recorded source identity.

## Behavior gate

The requested command was:

`/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d100_item_birth_boundary.py`

It was not started. Free space was `4,926,775,296` bytes, below the required
`5,000,000,000`-byte light floor. ParentRED and candidateGREEN are therefore
NOTRUN, not PASS; no alternate fixture, bypass, waiting-floor run, full suite,
or App own9 run was attempted. Product merge/release remains held pending a
fresh admitted behavioral run and App-owned own9.
