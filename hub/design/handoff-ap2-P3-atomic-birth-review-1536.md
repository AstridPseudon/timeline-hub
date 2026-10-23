# Runtime owner handoff: atomic native-birth authentication seam

Independent bounded review on exact Agent `58316fd6e0ce8a1fb3b2b3826ec71906d29080de` and Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2` confirms the Sol1527 diagnosis. The unchanged real `created_child_public` fixture has no source occurrences and submits native `occurrence.create -> track.create -> occurrence.add-media`. `fields` accepts in grouped and one-step-per-command forms; `atomic` refuses in both forms.

Verdict: **FAIL for atomic durable seed acceptance.** The original body/full fixture remains RED. No production or test change was made.

## Causal seam

`runtime_protocol/timeline_commit_auth.py:1569` performs the atomic touched-scope scan against `boundary = images(source)` before sequential `command_output()` effects and `boundary = output` advancement. `native_site()` reaches `site()`; `site()` line 156 searches the input parent occurrence list, cannot find the occurrence born earlier in this same request, and raises `provider occurrence alias is outside its boundary`. The exact trace and limits are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-atomic-birth-review-1536/report.md`

## Portable worker-authored bounded reproduction

The following is preserved byte-for-byte from the worker-authored reproduction (Git blob `d9de57f20c2bbcbb1bd3f6f451fff0dead4e4ccc`), without product-repository changes:

```python
"""Bounded owner-seam reproduction using Runtime's existing public fixture."""
import copy

import pytest

from tests.astrid_checkout import astrid_importable
from test_timeline_commit_authentication import created_child_public


@pytest.mark.parametrize("merge", ["fields", "atomic"])
@pytest.mark.parametrize("individual_steps", [False, True])
def test_native_birth_followed_by_child_edit(created_child_public, merge, individual_steps):
    runtime, project, source, submitted, held, document, publish = created_child_public
    submitted = copy.deepcopy(submitted)
    submitted["merge"] = merge
    reads = [{"kind": "scope", "ref": "timeline", "path": []}]
    submitted["reads"] = copy.deepcopy(reads)
    if individual_steps:
        submitted["steps"] = [{**copy.deepcopy(submitted["steps"][0]),
            "id": "seed-" + str(ordinal), "command_ordinals": [ordinal],
            "reads": copy.deepcopy(reads)} for ordinal in range(len(submitted["commands"]))]
    else:
        submitted["steps"][0]["reads"] = copy.deepcopy(reads)
    print("public native commands:", [command["op"] for command in submitted["commands"]])
    print("source occurrence count:", len(source["parent_revision"]["payload"]["occurrences"]))
    result = publish(submitted, "bounded-native-birth")
    assert result["data"]["status"] == "accepted"
    assert result["data"]["canonical_document"] == document()
    assert document()["internal_timeline_revisions"][0]["payload"]["clips"] == [held]
```

Run with the approved child interpreter and exact pins:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-58316fd6 PYTHONPATH=/home/user/work/wt/rt-pin-9ce4242b:/home/user/work/wt/rt-pin-9ce4242b/tests:/home/user/work/wt/agt-pin-58316fd6 /home/user/work/venv-agent-child-ap2-current-583-9ce-1503/bin/python -m pytest -q -s -o addopts='' -p no:cacheprovider test_native_birth_boundary.py --basetemp=/tmp/private-boundary
```

Observed result: exit 1, `2 failed, 2 passed, 7 warnings in 5.56s`; the two failures are the atomic expected-acceptance cases, and both reach the exact guard above.

## Owner next step

Repair atomic touched-scope authentication at proven sequential birth/input boundaries, preserving all source-boundary/owner/no-write/forged/outside/ambiguous guards. Do not switch the original transaction to `fields`, merge fields into the original fixture, strip raw data, add bootstrap publications, or introduce private authority. After an approved Runtime correction, rerun the original bounded normal-harness full-fixture seed qualification.
