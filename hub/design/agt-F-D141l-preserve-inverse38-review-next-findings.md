# D141ee inverse38 independent review

Verdict: `FAIL_REGRESSION_RESTORATION_REQUIRED`.

The 38 assigned IDs are exact pristine-only rows from `tests/timeline/test_inverses.py` at pristine
blob `941bcfb803b94f9765ac7b71dc88163010cc86cd`. Independent AST comparison found no current test function
with the same body/assertions and no exact old ID in either terminal XML. The
current ref has neither the old test file nor `astrid/core/timeline/inverses.py`.

Under MAIN D141ee (`/home/user/timeline-hub/hub/inbox/agent.md:7546-7551`), generic G5/D52 language, the D05
ledger row, and deletion commits are not treated as owner approval. No genuine
owner-approved retirement was found for these IDs. Therefore all 38 are
`DROPPED_BY_OUR_PATCHES_REGRESSION`, not silently retired and not credited to
the semantically different command-record inverse tests.

## Required restoration

One Agent manager-owned author must restore the exact pristine blobs for
`astrid/core/timeline/inverses.py` (`5d2514841e6cbb3e8cd7172b59dbd315f5bf8bd1`) and `tests/timeline/test_inverses.py` (`941bcfb803b94f9765ac7b71dc88163010cc86cd`),
preserve every original ID/input/assertion, and run:

```text
python -m pytest -q tests/timeline/test_inverses.py
```

No assertion adaptation, xfail, skip, deletion or semantic substitution is
authorized by this review. The review itself made no product/test changes.

## Visible pair context

Cut service `24814` / XML `6710f7fe1b4b1a0b4d43614f0fe58d437b0b6fff76990e4a717022cef773fcd5` has 397 bad
outcomes (`201 FAIL + 196 ERROR`); 19 are `FAILS_BOTH`. Pristine service
`25513` / XML `9d36fcecf662cc9138cd30cb6ad674a57db30209b18593f29da08ed961792bba` is retained. These
numbers remain visible context and are not deducted or converted into REG0.
