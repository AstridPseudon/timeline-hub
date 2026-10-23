# Handoff: ap2-P4 physical oracle review

Status: PASS for the bounded oracle correction; execution readiness remains BLOCKED on the Agent-owned internal-reader repair.

Candidate: b8163c059a633af4b15836ab974188f6ed2fd398
Candidate tree: 9484211955a9ab31db509772f19311e40cb3140d
Independent baseline: 3696239c48f9705568af30f2704855cc6a9175e5
Baseline tree: 94f7f4ff4d60a798d9cd664638a2b182234ad82c
Candidate test blob: cdb186d001fe8bd7476c2a059ee65e9a312dbec5

Review decision:
- The only candidate test change is the allowed initial physical/shared identity oracle.
- Distinct WORKING occurrence aliases map through authenticated source_mapping to one physical chapter-shot/shot-1 and one chapter-1/internal-1.
- Complete canonical fixture equality, occurrence order/timing/source offsets/tracks/speed/opaque fields, closure edges, one media pin, payload digests, and sorted manifest checks passed offline.
- Prefix and suffix of the original P4 test are byte-identical outside the inserted oracle block.
- No fixture/helper/product/schema/client/generated/pin/lock/suite/launcher changes.

Exact requested collection:
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q tests/editing_conformance/test_p4_ten_note_v2_runtime.py
Result: exit 0, but 1 integration test deselected by existing addopts. With addopts neutralized, exactly 1 test collected.

Other checks:
- Ruff target: PASS.
- Private mypy on target plus commit.py, commit_session.py, emitter.py, sync.py: PASS, no issues in 5 files.
- git diff --check on candidate diff: PASS.
- Offline real bundle_from_document/source_mapping witness: PASS.

Limits:
- No HTTP/socket/service/test body/full/browser/build run.
- No live accepted/merged/conflict/invalid/re-run/inverse evidence claimed.
- Production seam confirmed at astrid/sdk/_remote_timeline.py:86: internal-1 is requested under parent timeline film, but authenticated ownership is chapter-1.
- No production caller or source edge was changed. Do not grant execution readiness until Agent repairs this reader owner bug and a later current-source run qualifies the live body.

