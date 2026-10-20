# Runtime raw-media base eligibility — final review

**Decision: APPROVE**

Review date: 2026-10-20T16:41:25Z

## Reviewed identity

- Candidate: `dcac221296ef2c73e02d30534effb2a09d9a91bd`
- Candidate tree: `84cd47d40d4682fffa736c7dedf724f383de6952`
- Candidate parent: `b73139121169b72a2af9371f7808999ee91a1471`
- Review worktree/base: `e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`, tree `94c5ffbc0b636e25475c0f351bfb384dd06ee8ab`
- Approved reader reference: `e220670e40e196fb8f37dd8ce5d558fe0f6adf1c`, tree `6f802e315a7a447fa8d8245bf6f30963da6bb4f2`

## Decision basis

The candidate adds the missing base-scope predicate in `RequestCommitPort.media_info`:

1. validate the exact two-field media pin;
2. require recursive declaration by the detached original request;
3. resolve only `self.__request["base_revision_id"]` through `revision_closure`;
4. require membership in that closure's media manifest; and
5. only then consult the request memo or call `MediaReads.media_info`.

The base closure path verifies the original base publication/revision pair through `_ancestor`; it does not use latest head, candidate state, observed-head state, history traversal supplied by the caller, or caller arguments as a substitute base. A same-project object declared by the request but ingested after the base is therefore refused before memo lookup, descriptor open, CAS read, or metadata return. The exact base-pin positive path remains available.

The candidate preserves the approved descriptor-stable reader: pre-parse and post-parse CAS verification occur on the same open descriptor. It also preserves acceptance-time consumed-media recheck (`validate()` re-runs `reads.media_info` for each memoized raw pin) and ledger-first retry handling (`accept()` looks up the idempotency ledger before candidate validation/provider work).

The candidate delta from e220 is limited to the two-line base-closure guard plus the one permanent same-project/post-base counterexample and base-pin control. No schema, API, table, ABI, or release changes are present.

## Evidence

Recorded target-source test evidence:

```text
PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py
8 passed

PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_port.py tests/test_timeline_commit_contract.py tests/test_timeline_raw_payload_contract.py
122 passed

PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_commit_acceptance.py
59 passed, 1 deselected

git diff --check
passed
```

Those three pytest runs were executed on the exact candidate worktree by the implementation worker and are recorded here as evidence; they were not duplicated in this read-only review. The independent contrast evidence used fresh isolated imports of immutable e220 and b731 archives: e220 refused the same-project declared post-base pin before the reader, while b731 returned verified WAV metadata. The contrast also confirmed identical constructor/service/reader paths and isolated the eligibility difference to `RequestCommitPort.media_info`.

Independent checks in this review:

- `git rev-parse dcac221296ef2c73e02d30534effb2a09d9a91bd^{tree}` matched `84cd47d40d4682fffa736c7dedf724f383de6952`.
- `git diff --check dcac221296ef2c73e02d30534effb2a09d9a91bd^ dcac221296ef2c73e02d30534effb2a09d9a91bd` passed.
- An AST/source-order probe passed for exact-pin validation → declaration check → original request base closure → base-media membership → memo → raw reader, and found no latest-head/current-observed/candidate/caller-publication authority in `media_info`.
- Source inspection confirmed acceptance recheck and ledger-first ordering described above.

## Limits

No full suite, browser/HTTP/live-socket journey, native Agent pair, or duplicate broad run was performed. Shared dependencies were not modified. The review worktree has no source changes.

