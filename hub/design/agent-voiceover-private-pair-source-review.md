# Agent voiceover private input-pair source review

Date: 2026-10-21 (UTC)

## Decision

**REQUEST CHANGES** for target commit `6e9843662618b7bd3bde336094d7b8de7ce4063b`,
tree `937eb0f1206345a4032e7b399dadbf293a9f1894`, parent
`f738ca1c81b47ebcd5f4193d37b1ba07c7d0c8bf`. The target branch changes only
`astrid/packs/video_editing/shared/voiceover_requester.py` and
`tests/packs/video_editing/test_voiceover_requester.py`.

## Blocking custody finding

`_consume_settled_voiceover_input` makes `target`, `script_pin`, and
`requester_key` optional (`voiceover_requester.py:470-480`).
`_request_identity` compares each claimant field only when the corresponding
optional argument is non-`None` (`:383-388`), and it never requires the
claimant target's `project_id` to equal the consumer's `project`.

Thus a caller that omits those arguments lets the claimant JSON choose the
request identity. A foreign target/script/requester can be placed in the file
and the claimant can recompute `root_idempotency_key`; the H3 envelope and
`input_digest` do not bind those fields, and the verified Runtime task/media
checks can still succeed for the current project. The `consume` rows then no
longer carry the target/script/requester identity, so the mismatch is lost at
the outer seam. This violates the requirement that claimant JSON never be
authority and that requester root identity remain separate from the trusted
outer identity.

Make the expected target, script pin, and requester root key required trusted
arguments (or reject when any is absent), require the target's project to
match `project`, and compare the complete values before using any claimant
identity to recompute/accept a root key. Add negative tests for a foreign
target, script pin, and requester key with otherwise valid Runtime task,
managed-output, selection, verified-WAV, and duration reads.

## Secondary consistency finding

`_request_identity` checks request-level settings only against the first plan
job (`:376-378`). A supplied plan whose later job has different settings can
therefore pass request validation; each entry is checked against that later
job, and the input digest is computed from the later entry. Require one
canonical settings mapping for every ordered job (or compare request settings
to every job) and add a later-job mismatch negative.

## What is sound in this source

- The requester root call is separate from the outer producer identity. The
  requester invokes only `generation.generate_speech` at `:226-234`, sends
  text/settings without duration (`:225`), and imports one immutable carrier.
  The settled consumer has no generation, action dispatch, delegation, grant,
  proposal publication, or commit call.
- The consumer reads the materialized file under the attempt root, rejects
  direct symlinks/path escape, enforces the closed H3 envelope/result shape
  and digests, and refuses changed/duplicate/reordered plan entries.
- Runtime task/spec/result and managed-output identities are cross-checked;
  `_read_authoritative_media_info` remains the authority for the exact
  five-field selection, verified `audio/wav` bytes/hash/size, and intrinsic
  positive duration. No claimant duration is treated as authority.
- The existing managed action read connection requests only
  `worker:execute`, `projects:read`, `tasks:read`, and `objects:read`; no write
  scopes are requested. The current outer action/caller is still unwired, so
  no live requester or native qualification is claimed here.

## Evidence

Focused targeted test:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/packs/video_editing/test_voiceover_requester.py
10 passed in 0.63s
```

`git diff --check` passed. No full, native, renderer, live-socket, or external
model suite was run. No product source was edited by this review.

## Next step

Repair the required trusted-identity arguments and all-job settings check,
then rerun the focused requester tests with explicit foreign-identity
refusals before wiring the current action/caller.
