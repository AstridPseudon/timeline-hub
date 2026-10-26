# D141k independent review validation

## Commands and results

- `python - <<'PY' ... PY` using only `json`, `hashlib`, `pathlib`, `xml.etree.ElementTree`, `collections`, `shlex`, and `subprocess`: PASS. Reparsed actual XML; checked 9,388 concrete IDs/statuses, 173 unnamed aggregate PASS accounting, pristine table counts, duplicate IDs, exact multiset membership, classifications, root membership, tuple, settings, source-clean witnesses, refusal exclusion, and source-manifest hashes.
- `ulimit -v 4194304; python -u - <<'PY' ... PY`: PASS. Foreground continuous trace ran 5 seconds with five samples; minimum free bytes `4662452224`, never below `4000000000`.
- `git status --short --branch`: PASS; assigned composition worktree remained clean.

## Reconciled facts

- Actual XML SHA-256: `7adf18d3a9cd20c2198d4cd4ccd7e0be59497e6111a73284c4977fe31b92b25d`.
- Pristine table SHA-256: `7535b9a70b0da2f36e2c9e2f0115cf70ef429d3b8152496a7f44a723033ae6a5`.
- Classification logic independently reproduced with zero errors: `8988 CUT_PASS_NOT_REG`, `17 REG_CANDIDATE`, `4 FAILS_BOTH`, `376 UNKNOWN`, `3 N_A`, `173 AGGREGATE_UNNAMED_PASS`.
- Root membership independently reproduced: 22 requested, 17 upstream-present, 5 project-only absent.
- Source-before equals source-after; after-errors is empty; argv contains `env -i`, `-m pytest`, `-q`, `-n3`, disabled cache, and `--timeout=45` over all 22 roots.
- Refused 24049 is `fail`, exit `78`, with a refusal log and no XML.

The only revalidation limitation is the mutable Agent INBOX changing after the join manifest was published; this is recorded as `D141K-LIMIT-001` and does not alter the result.

Tests are `NOTRUN by design` per scope: no pytest, collection, product execution/import, typecheck, or lint.
