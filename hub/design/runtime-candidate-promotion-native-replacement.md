# RT02 candidate-promotion native replacement

Status: **RT02BLOCKEDbyAgentsemantic**. Runtime remains bounded; this is not an
all-work blocker.

## Scope and original capabilities

The two original positive tests remain unchanged in their assertions:

- `tests/test_shot_candidate_promotion.py::test_candidate_promotion_is_atomic_fixed_point_and_byte_stable_on_replay`
  (`tests/test_shot_candidate_promotion.py:25`) retains atomic primary/superseded
  status, plate/proxy/timeline-asset fixed-point invalidation, exact receipt,
  byte-stable idempotent replay, and stale refusal assertions (`:45-62`).
- `tests/test_shot_candidate_promotion.py::test_candidate_provenance_is_verified_before_promotion`
  (`:76`) retains foreign-project provenance refusal and zero version change
  assertions (`:85-88`).

Only the strict-xfail reasons were made explicit: the retired endpoint is still
expected to raise `ApiError`, and the restoring requirement is the missing
Agent-native semantic, not endpoint restoration.

## Current Agent sole-commit review

Reviewed current Agent integration (`/home/user/work/agent`, current native
source) at:

- `astrid/sdk/timeline/commands.py:29-72`: 20 registered operations, none for
  candidate promotion or item mutation.
- `astrid/sdk/timeline/_shot_commands.py:12-41`: `shot.set` is restricted to
  `occurrence:<id>/shot` and only writes shot `name`/bounded `settings`.
- `astrid/sdk/timeline/native_occurrence_media_commands.py:101-178`:
  occurrence add/swap edits canonical media clips and registry bindings; it does
  not update project shot-item status or dependent assets.

The smallest missing semantic is one Agent-owned recorded command that can,
within one accepted commit and normal recorded guards:

1. select a candidate and its superseded primary by stable shot-item identity;
2. verify candidate provenance scope and source content digest;
3. atomically write primary/candidate item statuses; and
4. invalidate the transitive dependency closure (plate → proxy → timeline
   asset), preserving exact identities/digests and exposing the result through
   the existing receipt/retry/history path.

The current command set cannot address project shot items at all, so composing
existing media swap, shot settings, or pool commands would not preserve the
original behavior and would be an invented fallback writer. No Runtime DTO,
schema, operation, endpoint, SQL history, fake provider, or retired writer was
added.

## Compact executable bootstrap/gap probe

The private probe is outside the repository at
[`native-gap-probe.py`](../workers/rt-m2-candidate-promotion-native-replacement/native-gap-probe.py).
It uses `RuntimeService`, the installed Agent provider, a normal project and
provider-backed `create_timeline` bootstrap, then enumerates the current native
registry. It does not call retired shot/item writers or mutate shared sources.

Exact command and result:

```text
ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/agent" /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-candidate-promotion-native-replacement/native-gap-probe.py
agent=/home/user/work/agent
bootstrap=bootstrap-55149e02bde0467cbedf1a50a4e48e23
operations=clip.add,clip.delete,clip.move,clip.set,clip.set-element,clip.set-params,clip.split,clip.trim,occurrence.add-media,occurrence.delete,occurrence.duplicate,occurrence.swap-media,placement.create,placement.move,placement.unplace,producer.guard,shot.pool,shot.set,track.create,track.set
candidate-promotion=unexpressible
```

The probe is dependency evidence only; it is not claimed as a promotion
positive.

## Tests

Central targeted Runtime lane, exact files:

```text
request-test rt-m2-candidate-promotion-native-replacement targeted --files "tests/test_shot_candidate_promotion.py tests/test_timeline_shot_authority.py"
```

Result: **131 passed, 2 strict xfailed, exit 0** in 113.49s. The two xfails
are exactly the original promotion test IDs above. The shot-authority neighbors
remain green and the retired route remains refused.

No full suite was requested. No Agent product files, public schema, generated
client, Runtime endpoint, legacy writer, or shared dependency was changed.

## Peer request / remaining dependency

Agent must supply the smallest native recorded-command semantic described above
for these exact original tests:

- `tests/test_shot_candidate_promotion.py::test_candidate_promotion_is_atomic_fixed_point_and_byte_stable_on_replay`
- `tests/test_shot_candidate_promotion.py::test_candidate_provenance_is_verified_before_promotion`

The Runtime follow-up can then port the unchanged assertions through the sole
commit path and qualify them with the real Agent provider. Until that Agent
semantic exists, RT02 candidate-promotion positives remain open; the retired
route stays refused and no endpoint restore is requested.
