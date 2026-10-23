# Runtime R2r native occurrence-order review

## Verdict

**PASS — narrow Runtime producer correction only.** The candidate correctly
authenticates the physical `parent/occurrences` collection, then removes only
the managed `shot_revision_id` from each authenticated physical row before
comparing it with the native authored row. It preserves list membership,
order, ownership, `shot_id`, and every other row field. This is not acceptance
of G5, public redo, or the overall inverse journey.

Reviewed candidate:

- Runtime commit `e3159e353c6184e146dde4e759db24f2e9ffc66b`, parent
  `cfa0af0d476e6954df041c08d7ef378fd6782932`.
- Runtime tree `92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`.
- Changed paths are exactly `runtime_protocol/timeline_commit_auth.py`, the
  retained native-order fixture, and its focused test additions.
- Candidate Runtime auth file SHA-256:
  `27ff45721dcd2af70908b0e1afc582543e1a8f2988cd89ca9c9395a3b493e38c`.

## Review findings

The retained evidence fixes the orientation: accepted event117 is parent
`caa332...` with three occurrences/config `e6d3e227...`; predecessor event129
is parent `a58d...` with one occurrence/config `32613189...`. The first three
native writes authenticate; the fourth `parent/occurrences` write is the
physical/native representation seam. Native rows intentionally omit
`shot_revision_id`; the candidate does not add that pin to Agent output.

`_inverse_stage_occurrence_collection` is appropriately narrow. For every
physical row it requires a unique occurrence, unique existing shot revision,
matching authenticated `shot_id`, a string internal revision, an existing
internal root whose payload repeats that revision, and `_physical_owner`
agreement for both shot and internal roots. It then strips only
`shot_revision_id`. There is no broad revision-key stripping, equal-payload
root mapping, provider-supplied history authority, or shot-id alias
normalization. Existing source/history, effect, owner, digest, stage/step,
range, sequential image, ABA/later-history, and final-equality guards remain
in force.

Independent scratch probes accepted the exact positive packet with the input
objects unchanged. They refused all of the following as `invalid_records`:
missing, foreign, and ambiguous physical pins; shot-id aliasing; wrong native
pin and native row; coordinated effect, binding, history, owner, and payload
tampering; membership and order; publication, step, ordinal, range, and digest
tampering; and final-closure tampering. The retained packet's ABA control is
also recorded refused. No Agent/public inverse body was retried or changed.

The original Agent body provenance was independently checked at exact Agent
commit `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`; the supplied function-body
hash (including its terminating newline) is
`c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
That later Agent/public-body result remains a separate acceptance question.

## Packet custody

Manifest and round-trip checks passed for all retained packets:

- actual packet: 1,931,658 bytes,
  `a94e094388a4c3159b25d2f1b2a088a15729142e54113ad01f40f0b0f3ca96c0`;
- cfa offline packet: 557,388 bytes,
  `a141c3702335878e9b964900ec2f3aed9ca5b733ddb9b44bda23389ddc4c0b7c`;
- Runtime859 offline packet: 557,388 bytes,
  `d57677670e1a22466dbd93f4e02e9d566b1333b4982e993a75e4d9b38db60e1b`.

Each matched `agent-G5-inverse-1416.manifest.json`, parsed and JSON-roundtripped
identically, and had the manifest credential scan clean. The candidate fixture
has the cfa offline packet hash exactly and retains source packet hash
`01ccdec35f2a8f3e72e99541092f99ec20bda2de036adc6fe77d7f773157aaeb`.

## Commands and results

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_source_duplicate_authority.py
193 passed in 57.69s

/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
All checks passed!

/root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py
0 errors, 0 warnings, 0 informations

git diff --check
exit 0
```

The worktree was clean after review. No product, schema, client, pin,
contract, or configuration edit was made by this reviewer.
