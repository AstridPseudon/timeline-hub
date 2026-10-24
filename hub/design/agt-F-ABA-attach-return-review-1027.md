# F-ABA-attach-return-review-1027

Result: **PREPARED PASS**.

- Revalidated candidate `de5c54e30275aa98579b11d9e5c1a93fb09c5d1c` over support commit `546d86816a3df9e5e1529e80ca81f5c1d397c75c`.
- Candidate row SHA256: `3f3d43e39321467a41e06c405c1419376e5f8ec70c408ef0814465f70be302ba`.
- Actual registry pre-hash: `5ada85961e709386b7d7aa328338fda01af6bfc2c8efea6ddd9170671dbe851f`.
- Expected post-hash: `31cfddf295b376036c62e08d935373a78fdc37f153f1445f4a69f08437c56133`.
- Retained 172 non-target rows byte-identically: `afd6f92fe8208bcc211208ca80e3aca7446dede50f2c64e968bc359ea7e5d9bc`.
- Agent source: `0c2c28da`, tree `4ce9de35`; Runtime: `becfe6db`, tree `7edc08e3`; auth blob `979225ab`.
- Runner/helper physical hashes match the sanctioned support checkout.

Validation:

- Targeted pytest with exact Runtime import and harness `TMPDIR`: **21 passed**.
- Scoped Ruff: passed.
- Python 3.12 mypy: passed.
- Candidate `bash -n`: passed.
- `git diff --check`: passed.
- Embedded candidate preflight: passed.
- Durable JUnit evidence: `evidence/PERMANENT.xml`, 3391 bytes.

The 1014 gap is closed: a concrete one-row candidate, exact install manifest, source/module/profile/auth/oracle/clean-tree/budget guards, argv/plugin/sink invocation, retention states, and child-exit preservation are all present and verified.

No live registry install, original ABA body, managed service run, or production-caller proof was performed. Those remain required later; retained `capture.end` JSONL and the original pytest exit must be verified by the manager after normal installation.

The referenced frozen-doc path was absent; I used the matching orchestrator scratchpad copies of `BOARD-HEADER.md` and `commit-v2.md`.

Commit message and `DONE` marker were created.