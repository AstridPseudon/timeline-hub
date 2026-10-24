## Report

Status: **PREPARED, not READY**

Created:

- [caller-preparation.py](/home/user/work/wt/app-P2-P3-retained-caller-prep-0600/caller-preparation.py)
- [caller-custody.json](/home/user/work/wt/app-P2-P3-retained-caller-prep-0600/caller-custody.json)

Bound current App source `e42ee6227f`, tree `c0a54b2b…`, parents `79cd94f7e0… 9b5be36fa9…`. Preserved Agent `079`, Runtime `37eb`, child0256, Remotion0258, existing receipts, client/backend/graph fingerprints, and all 248 outside suite rows byte-identically.

Added private per-stage output children:

- P2: `native-history`, `mounted-readiness`, `original-body`
- P3: `native-history`, `mounted-readiness`, `gate5`

Final catalog and P3 source remain explicitly `MISSING`.

Tests/checks passed:

```text
python3 -m py_compile caller-preparation.py
git diff --check
24 controls passed
28 stage controls passed
4 corruption controls passed
2 restricted-export controls passed
2 fail-closed wrong-key controls passed
bash -n on all generated draft shells
```

Tool versions: Node `v22.22.0`, npm `10.9.4`, Playwright `1.60.0`.

Artifact hashes:

```text
caller-preparation.py  d6d6433a14377921c882ee831345e278fdd869d8f6ee0842f1e39eead36b6115
caller-custody.json    d5fd55ac8dba03c19c7aca2464cb36fb36a2bfaf395e20465e706d168de8d6d4
```

No live browser, backend, service, full-suite, or production caller execution was performed. Commit message and `DONE` marker were written.