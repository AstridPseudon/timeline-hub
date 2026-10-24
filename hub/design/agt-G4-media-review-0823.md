## Verdict: PASS

Reviewed `publish.py` and the new admission tests against PLAN G4 and contract §§1/2/4/7.

Findings:

- Production `Checkout.publish → _commit_document → TimelineSession.submit` uses the new path.
- Runtime remains authoritative for media bytes, project ownership, catalog selection, and digest validation.
- `media.admit` is appended after existing authored commands with contiguous step ordinals.
- Accepted retries reuse the durable admission command and receipt.
- Foreign media rejection preserves document and history.
- Existing missing/forged/changed-catalog controls remain intact.

Tests:

- New + normal publication targets: `14 passed`.
- Existing authoring/media controls: `32 passed`; one integration-lane test was deselected by lane rules.
- Compile and Ruff: passed.
- Vendor lock: passed against `becfe6db...`.
- Artifact manifest and diff checks: passed.
- Typecheck-v2: `current=1902 baseline=1902`, zero new findings.

No product files were modified. No full/browser suites were run. Commit message and `DONE` marker were created for the harness.