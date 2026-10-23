# Runtime D17 authority handoff

Runtime source: `tl/rt-D17-source-authority-0842` at base `eb13b2051`
(`tl/integration`), working tree changes uncommitted for harness commit.

## Stable interface

The existing semantic command args carry one exact `source_ref` object:

```json
{
  "project_id": "destination-project",
  "timeline_id": "other-active-timeline",
  "revision_id": "accepted-source-revision",
  "publication_id": "accepted-publication-for-that-revision",
  "content_digest": "sha256:<source-parent-payload-digest>"
}
```

Agent calls `RequestCommitPort.revision_closure(source_ref)` (or the explicit
`source_revision_closure` alias). Runtime authenticates the existing caller,
requires same-project/different-active-timeline scope, verifies the exact
publication/revision pair and parent digest, returns the immutable full source
closure, and repeats all source checks at acceptance. Source media and
documents remain existing `raw_media_info`, `config_source`, and
`transcript_source` reads; no caller/provider grant, schema, client, pin, or
new Runtime semantic executor was added.

## Evidence

Focused real-port/store suite:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_source_duplicate_authority.py
8 passed in 2.56s
```

Required neighboring suites:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_source_duplicate_authority.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py
93 passed in 14.73s
```

Negative inventory covered by the focused suite: forged media, foreign
project/source, outside source timeline, archived/stale source, publication /
revision mismatch, source digest mismatch, revoked caller source access, and
changed source capture. The positive control accepts an exact historical source
pair after the source head advances, proving no silent source-head refresh.
Existing destination CAS, receipt/idempotency, manifest, archive, and provider
guards remain exercised by the neighboring authentication/read-basis tests.

Static checks: `ruff check --no-cache tests/test_timeline_source_duplicate_authority.py`
passes; `PYTHONDONTWRITEBYTECODE=1 python -m py_compile` on both changed
production modules passes; `git diff --check` passes. Scoped Ruff reports only
pre-existing diagnostics in the two touched production modules. Scoped Pyright
reports the same existing Runtime nullable diagnostics plus two dynamic test
fixture attributes; no new production diagnostic occurs in the D17 additions.

## Agent-owned remainder

Agent must implement and qualify the one semantic source-copy command using the
existing carrier: fresh IDs, repeated-shot sharing, source occurrence order,
semantic records, inverse/undo, stable idempotency, and archive-cleanup
behavior. Agent must explicitly consume each copied source media/document pin
through the Runtime port and preserve normal destination manifests/records.
The original positive semantic assertions remain intact until that work is
qualified; this Runtime change does not claim Agent semantic completion.
