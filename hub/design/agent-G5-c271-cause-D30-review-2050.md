# D30 causal re-review

## Verdict

- Causal re-review: **PASS**.
- Original G5 conclusion that this was an **Agent emission defect is RETRACTED**.
- Precise owner: **Runtime inverse-stage projection**.
- Product qualification remains **DRAFT / P1 NO-GO**. No repair or original c271 rerun was performed.

## Evidence integrity

- Agent base: `f120159fae86b5fb1e5379437737b4e0a16627eb`; tree `e56d741e65f94f22122c9dcced134480d08dc03b`; clean.
- Runtime replay: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
- Packet archive SHA-256: `a8dcf1d1fe6c2ce6905749ea11fe96057b421f7497c0e233c13ca1e0182bc3d4`; 14,794,303 bytes; 85 members.
- `060-port-prepared.json` SHA-256: `58051ef4e6e23f717c07fdce2d12e8d2b74caa106eb8422fe6e1c604c34f9d4d`.
- Capture SHA-256: `0202aa4f4507a3e0bdaad61307e2e9fee6f9ed37fe83c597439a9f0cb5ab890e`.
- Comparison SHA-256: `9869b7af089c54dae91821bbbb197b3e8692ddab5d9a456705518a5c35889702`.
- Credential-pattern scan: **0 findings**.

## Exact replay

Command:

```sh
PYTHONDONTWRITEBYTECODE=1 \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f \
PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f \
/home/user/work/venv-agent/bin/python \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-c271-effect-sol-2013/evidence/replay.py
```

Result: **exit 1, expected preserved Runtime RED**.

Confirmed:

- Agent candidate, native writes, and step patches exactly match the captured prepared packet.
- Runtime raises HTTP 422 `validation_error`, reason `invalid_records`:
  `inverse stage native writes do not cover its authenticated effect image`.
- Original packet remains unchanged.
- Native range: `[0, 10]`.
- Effect range: `[0, 9]`.

Write 6 projection trace:

```text
line 1200:
occ-film -> e792...
chapter-shot-837... -> 398...
chapter-shot-3f... -> c5cc...

line 1201:
chapter-shot-837... -> MISSING
occ-film -> MISSING
chapter-shot-3f... -> MISSING
```

Independent recursive comparison found exactly three payload differences:

```text
parent.occurrences[0].shot_revision_id: MISSING -> 398...
parent.occurrences[1].shot_revision_id: MISSING -> e792...
parent.occurrences[2].shot_revision_id: MISSING -> c5cc...
```

All seven physical root keys are present on both sides. All non-parent physical payloads are equal. The only non-payload differences are the expected parent revision/content-digest endpoint changes.

## Causal proof

Runtime authenticates occurrence rows in `_inverse_stage_occurrence_collection` (`timeline_commit_auth.py:817–854`), including each physical `shot_revision_id`, then deliberately removes that field for authored comparison.

The inverse write for `parent / occurrences` is then projected through `project_observation` at lines 1198–1201. That whole authored collection has no revision pins, so Runtime removes the already-authenticated pins from its physical parent image. The final equality check at lines 1373–1375 consequently fails.

Adding materialization bindings would not fix this exact comparison:

- Runtime’s `_align_materialized_images` excludes `parent` images.
- Materialization bindings concern authenticated shot/internal physical turnover, not authored parent occurrence-row projection.
- The accepted source history contains 10 `commit.effect`, 3 `commit.read`, and 3 `commit.atomic` bindings, but no `commit.materialization` bindings.
- The source history explicitly contains `source.via = python`, `timeline.restructure`, and the complete prior publication chain.

Agent attribution is therefore unsupported. Agent `State.get()` returns authored placement rows, and `State.set()` only permits an exact authored-row permutation (`_command_state.py:290–292`, `369–379`). Agent root validation also rejects occurrence roots carrying revision fields. Adding physical pins to Agent-authored captures would violate the existing normalizer contract.

Agent materialization emission intentionally skips an existing occurrence when the native write already writes that occurrence root or `shot_id` (`_commit_patch.py:633–650`). This source writes `occurrence:occ-film`; absence of materialization bindings is not the causal defect.

## History constraints

Verified chain:

```text
txn-aca0c19f9cfc4e77a9c0deb109f70a68
 -> txn-1caf8d8641d74d3aa012388faf0fdd4c
 -> txn-0e37f757d72c4226b04fcf6315980651
```

The request base, captured head, prepared expected head, inverse `previous`, source publication, source revision, and source documents all agree. No source history, native writes, effect images, pins, aliases, or credentials were fabricated.

## Limits and next step

No product edits, tests, Runtime repair, original c271 body, SDK4, full suite, HTTP, browser, P1/P4, or later 2041/2047 boundary was run. The preserved RED is diagnostic evidence only.

Recommended next step: Runtime-owned bounded repair of the parent occurrence-order projection, preserving authenticated pins while retaining strict ownership/membership checks, followed by independent negative controls and only then the manager-owned original qualification.