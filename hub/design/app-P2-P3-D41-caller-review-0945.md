## FAIL — PREPARED-only review

Reviewed `b2f7113cc2` against `1d92503b4c` and `b5fc832b78`. Only `caller-publication.py` and `caller-custody.json` differ. No product edits, installation, service, browser, backend, or original run performed.

Findings:

- `caller-custody.json:37` adds unsupported request field `scope`; C0 names `project_id`/`timeline_id`, not `scope`. Reply inventory also duplicates `steps`, `merge_mode`, and `base`.
- `d41_agent_input()` checks the manifest parent only against itself (`caller-publication.py:243-248`); it does not require exact parent `AGENT` or verify an allowlisted qualified backport delta.
- Receipt validation is substring-based (`caller-publication.py:142-167`). A dispatcher-local design file with matching hash needles was accepted by `immutable_receipt()` as a receipt. This is a reproducible forged-receipt bypass.
- Child-root validation only checks the basename and installed bytes (`caller-publication.py:287-301`); receipt content is not structurally bound to child key/root.

Checks:

- `python3 -m py_compile caller-publication.py` — PASS
- `python3 -m json.tool caller-custody.json >/dev/null` — PASS
- `git diff --check 1d92503b4c..HEAD` — PASS
- Decoded-row rebind control — PASS: 60 P2 / 106 P3 fingerprints; native body and tails exact; both inner/outer `bash -n` passed.
- Actual extracted source guards with inert files — PASS: positive and mutated-source negative controls for both rows.
- Outside-row preservation — PASS: 248 rows, SHA256 `b33d30918d6e2ae039dfa296bc75b1e0b2674828b53f07a16ee029933d5ad734`.
- Missing, malformed, incomplete, and self-PASS manifest controls — correctly refused.

The genuine D41 Agent source, exact receipts, and new child remain absent, so custody correctly remains `PREPARED` / `NOT_GRANTED`; no readiness or execution permission is claimed. I did not write the design file per the explicit read-only review instruction.