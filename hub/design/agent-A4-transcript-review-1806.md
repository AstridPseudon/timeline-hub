# A4 transcript witness review

## Verdict

**FAIL for the review gate; behavioral witness PASS.** The seven new tests pass
against the specified Runtime checkout and the test-only scope is correct. The
required parent-to-HEAD `git diff --check` fails because the new test has two
newline bytes at EOF (`tests/editing_conformance/test_a4_transcript_doc_patch_witness.py:406`).
This review made no source or test edits because the brief is read-only.

The diff failure is mechanical, not evidence of a behavioral defect. Remove the
extra blank line and rerun the scoped checks before accepting the witness.

## Reviewed sources and provenance

- Target: `tl/agt-A4-transcript-witness-1758`, `8eab05261e5c441b24b214ea79a66af05bcb011d`.
- Target has exactly one added file, the seven-test witness; blob SHA-1:
  `3784be40e08802d3aa2a864d08cf7eafc30e3bd7`.
- Agent source was loaded from this worktree.
- Runtime source was loaded from `/home/user/work/runtime`, exact pin
  `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` (`tl/integration`).
- App reference was read at `b85e9fb613c00df57b79a374bedbf5fa791d5a37`:
  `project-transcript-host.ts` blob
  `1b4910f27000dd50f7d354f4b95b38dda621743c`,
  `importTranscriptHandoff.ts` blob
  `be6fbfc6d04ebd1ebddfbf2a8ee2ab99c6f76506`, and the old association fixture
  blob `5c39a293009df59f796fe476e107a0a9900244d7`.

## Exact covered map

The line references below are in the target witness file.

| Area | Concrete assertions |
| --- | --- |
| Nested App-shaped planes and preservation | `152-194`: `parent.config.bundle.transcriptReferences`, `itemsBySchemaRef` including unrelated schema data, opaque bundle bytes, canonical document dependency manifest, retained source, accepted status, and receipt canonical result. |
| Null versus absence and raw opaque JSON | `196-210`: explicit `ABSENT` → `None`, `remove` → `ABSENT`, preserved opaque values, and corresponding before/after writes. |
| Current and prior authenticated source pins | `213-237`: exact private `source_fixture("transcript")`, a version-2 prior pin, dependency manifest, recorded dependency versions, and both retained source captures. |
| C0 request metadata, dry run, and accepted metadata | `240-320`: exact request fields for API/project/timeline/base pair/commands/dry-run/source/rationale/label/steps/merge/reads/group id; preview null receipt/status/would-status; step patch/read/dependency; unchanged head; accepted receipt fields and canonical result linkage. |
| Previous-value refusal, identity collision, atomic no-write | `321-364`: structured previous-value mismatch fields (`reason`, `code`, `path`, `current`, `hint`, `suggested_command`), unchanged document/accepted count, and `identity_collision` with unchanged document. |
| Declared reads, fields rebase, atomic scope | `240-320` and `366-386`: nested declared read, request/record read linkage, fields rebase retaining an intervening value, and atomic refusal with the intervening value retained. |
| Source-pin mismatch before nested writes | `389-405`: malformed bytes behind the existing exact pin, refusal before the attempted nested write, unchanged document, and zero accepted commits. |

The witness does not patch reads to empty/missing, alter the fixture pin to make
the malformed source green, or use a self-authored capture as source authority.
The provider's real `_hydrate` boundary verifies pin, document identity,
project, version, content digest, transcript kind/schema/media/source identity
before `execute` is called.

## Exact C0 credit and limits

The witness gives concrete partial credit for request metadata, preview, accepted
canonical-document linkage, records, writes, reads, bindings, dependencies,
steps, and `undo_steps is None` on an ordinary accepted commit. It does **not**
establish all of C0:

- It checks selected record fields and `derived_writes == []`, not a complete
  effects/records schema or every receipt field.
- It checks a stored entry's records, not the history-listing API, complete
  authoritative attribution, or history pagination.
- The fields-rebase assertion expects the provider's `status == "rebased"`; it
  is not an explicit canonical `merged` reply/receipt proof.
- It does not exercise whole/per-step undo, non-null undo metadata, or a merged
  commit's inverse.
- Structured details are complete for the previous-value refusal only; the
  collision and source mismatch assertions intentionally check narrower reasons
  and atomicity.
- The accepted canonical document is checked at the relevant nested planes and
  receipt linkage, not as a whole-document exact equality assertion.

## Deliberately uncovered behavior

- No `transcript.associate` operation, reconciliation, caption ownership or
  generated caption identity, word-anchor behavior, relational timing, or open
  JSON referential integrity. The generic Agent provider has no such semantics.
- No exact App association-fixture identity parity. The witness uses the
  authenticated Agent fixture's `picture` asset, `whisper` source, media digest
  `sha256:` followed by 64 `1` characters, and `line-1` item. The old App
  fixture uses `asset-a`, `source-1`, media digest `sha256:` followed by 64 `a`
  characters, and legacy/canonical segment IDs. The witness remains internally
  consistent with its real Agent pin, but this is not App semantic parity.
- No mounted App invocation, outbox, browser, HTTP, or detached-realm proof.
  `source.surface == "localSaveSession"` is request metadata only. App b85's
  host boundary uses `commitData(..., {save: true, semantic: true})` followed by
  `flushPendingSave`; its tests mock that boundary. The witness does not claim
  to prove it. The dormant `commitSession` path is not treated as production.

## Commands and outcomes

- `timeout 25s env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_a4_transcript_doc_patch_witness.py`
  → **7 passed in 2.17s**.
- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_a4_transcript_doc_patch_witness.py`
  → **All checks passed**.
- `env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m mypy tests/editing_conformance/test_a4_transcript_doc_patch_witness.py`
  → **Success: no issues found in 1 source file**.
- `git diff --check 079580ca46af77e0292d49dc34386b25c8391f99..HEAD`
  → **FAIL**, `tests/editing_conformance/test_a4_transcript_doc_patch_witness.py:406: new blank line at EOF`.
- Diff scope/protected-path scan → one added regular file, mode `100644`, 17,477 bytes; no vendor, archive, node_modules, private artifact, or outside-worktree path.
- Credential scan with `api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY|credential` → no matches.

No full, browser, HTTP, live-socket, daemon, seed, native, SDK-wide, or App
suite was run, per the brief.

