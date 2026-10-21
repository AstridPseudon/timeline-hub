# Agent transcript Gate 1 current readiness

Date: 2026-10-21

## Result

The Agent transcript association proof is source-complete for the corrected
carrier and has a bounded accepted-history witness against the approved
Runtime successor `3dcae1836a609363135d07ee435ce9beea975504` (tree
`4fa58b2551f716c35cab6005cc8add84e59da8a9`, compatible with Runtime parent
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`). The Agent source under test is
base commit `b39ceb060d87cdb2038a17f610b7f270ef09c29e`, tree
`3c4dcaf409f5cc947f7eb84369b6ca48e6a90cc4`, plus the uncommitted focused
proof in `tests/editing_conformance/test_gate1_transcript_accepted_reload.py`.

The witness uses only the existing persisted App carrier:

```text
parent.config.bundle.transcriptReferences
parent.config.bundle.itemsBySchemaRef["astrid.transcript_segment/v1"]
```

It accepts an initial pin, updates the same transcript to a new exact pin,
reopens from the persisted accepted closure, accepts the replacement, checks
both exact pins in the accepted record and dependency manifest, restarts,
then performs guarded inverse and redo while checking the old/new nested
states. No schema/provider monkeypatch, generation, freeze, pin, activation,
or alternate carrier was introduced.

## Evidence

Passed:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3dcae183 \
PYTHONPATH=.:/home/user/work/wt/rt-pin-3dcae183 \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -m integration \
tests/editing_conformance/test_gate1_transcript_accepted_reload.py
=> 1 passed

PYTHONPATH=.:/home/user/work/wt/rt-pin-3dcae183 \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
tests/editing_conformance/test_recipe_film_transcript_association.py \
tests/editing_conformance/test_recipe_film_transcript_association_spike.py \
tests/sdk/test_timing_compiler.py
=> 59 passed

/home/user/work/venv-agent/bin/ruff check \
astrid/sdk/timeline/native_transcript_association.py \
tests/editing_conformance/test_recipe_film_transcript_association.py \
tests/editing_conformance/test_gate1_transcript_accepted_reload.py
=> All checks passed

git diff --check
=> passed
```

## Smallest remaining gate

**Native qualification remains BLOCKED** because this Agent checkout does not
contain the normally generated App transcript counterpart/fixture needed to
prove the live App serializer and generated caption/review provenance together.
The pure Agent suite does cover the no-asset generated caption, accepted/review
leaves, opaque/order preservation, ownership/fingerprint guards, nested
serialization, and local inverse/redo. The Runtime witness covers persisted
accepted carrier history, but intentionally uses a bounded source fixture and
does not claim App qualification.

The smallest remaining cohort is one normal App-generated transcript
association: serialize the real App nested carrier (including its asset-less
generated caption and accepted/review leaves), submit it through the current
Agent command to Runtime3dca, reload after restart, and prove inverse/redo
with both exact pins. Keep the existing App positive assertions; do not add a
new schema, provider, endpoint, generation, or pin operation.
