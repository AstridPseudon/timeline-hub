# PASS — P4 physical-boundary oracle review

## Scope and decision

Reviewed candidate b8163c059a633af4b15836ab974188f6ed2fd398 against independently reviewed
3696239c48f9705568af30f2704855cc6a9175e5 and C0c §2/§4/§5. Candidate tree:
9484211955a9ab31db509772f19311e40cb3140d; baseline tree:
94f7f4ff4d60a798d9cd664638a2b182234ad82c.

PASS for the bounded oracle correction. The only candidate product/test change is the
allowed initial identity assertion in
tests/editing_conformance/test_p4_ten_note_v2_runtime.py; report.md is the only other
changed file. No fixture, helper, product, schema, client, generated file, pin, lock, suite,
or launcher changed.

The replacement correctly treats WORKING occurrence aliases as intentionally distinct while
binding both through authenticated source_mapping to exactly one physical
chapter-shot/shot-1 and one chapter-1/internal-1. It retains the shared physical meaning,
the full canonical document shape, occurrence order/timing/source offsets/tracks/speed/opaque
fields, shot/internal edges, one shared media manifest pin, payload digests, and sorted
manifest entries. An offline bundle_from_document witness compared the complete canonical
document to the original shared fixture and passed.

The original test body is unchanged byte-for-byte before and after the inserted oracle block.
The ten-note/one-commit/per-step undo-redo, mirrored note fields, full authored-closure,
show/history, restart, publisher, exact v2 scope/base pair, commands, labels, step patches,
reads, fields merge, dry-run flag, idempotency key, accepted reply, canonical/head/digest/
receipt/effects/bindings/steps/dependencies, and existing downstream coverage remain intact.

This is not an end-to-end acceptance or execution-readiness GO. The genuine Agent-owned
reader seam remains blocked: astrid/sdk/_remote_timeline.py:86 requests the internal
revision using parent timeline film, while the authenticated physical image is owned by
chapter-1. No caller, source edge, or production implementation was changed.

## Checks

All checks were offline and targeted. No HTTP, socket, Runtime service, test body, central
test service, full suite, browser, or build was run.

Exact requested collection command:

~~~sh
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q tests/editing_conformance/test_p4_ten_note_v2_runtime.py
~~~

Result: exit 0, but 1 deselected / no tests collected because the repository's existing
default addopts excludes the integration mark. With only addopts neutralized, the same
file collected exactly 1 test; the existing unknown timeout configuration warning remained.

~~~sh
RUFF_CACHE_DIR=/tmp/ap2-p4-review-0540/ruff-cache /root/.local/bin/ruff check tests/editing_conformance/test_p4_ten_note_v2_runtime.py
~~~

PASS: Ruff.

~~~sh
MYPY_CACHE_DIR=/tmp/ap2-p4-review-0540/mypy-cache /root/.local/bin/mypy --no-incremental tests/editing_conformance/test_p4_ten_note_v2_runtime.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/commit_session.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py
~~~

PASS: no issues in 5 files; two existing unchecked-body notes.

~~~sh
git diff --check 3696239c48f9705568af30f2704855cc6a9175e5..b8163c059a633af4b15836ab974188f6ed2fd398 -- tests/editing_conformance/test_p4_ten_note_v2_runtime.py report.md
~~~

PASS.

Offline witness command:

~~~sh
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python - <<'PY'
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from tests.sdk.test_timeline_commit_provider_document import document_fixture

document = document_fixture(shared=True)
bundle = bundle_from_document(document)
assert bundle["source_mapping"]["_runtime_document"] == document
canonical = bundle["source_mapping"]["_runtime_document"]
assert [(r["occurrence_id"], r["shot_id"], r["shot_revision_id"])
        for r in canonical["parent_revision"]["payload"]["occurrences"]] == [
            ("occ-a", "chapter-shot", "shot-1"),
            ("occ-b", "chapter-shot", "shot-1"),
        ]
assert [(r["shot_id"], r["revision_id"]) for r in canonical["shot_revisions"]] == [("chapter-shot", "shot-1")]
assert [(r["timeline_id"], r["revision_id"])
        for r in canonical["internal_timeline_revisions"]] == [("chapter-1", "internal-1")]
refs = [canonical["parent_revision"]["payload"]["registry"]["assets"]["picture"]["media_id"],
        canonical["shot_revisions"][0]["payload"]["items"][0]["media_id"],
        canonical["internal_timeline_revisions"][0]["payload"]["registry"]["assets"]["picture"]["media_id"]]
assert len(set(refs)) == 1
for row in [canonical["parent_revision"], *canonical["shot_revisions"], *canonical["internal_timeline_revisions"]]:
    assert row["content_digest"] == _digest(row["payload"])
print("PASS physical mapping and full original fixture comparison")
PY
~~~

PASS. The source-mapping alias witness also passed: two distinct
shot-placement-* aliases map to the same authenticated physical shot/internal digests.

## Handoff

The oracle correction is review-ready and has no source delta. Keep execution readiness
blocked until the Agent owner repairs the internal-reader timeline scope and a later current-
source test-only run qualifies the live body. Commit message is supplied separately.
