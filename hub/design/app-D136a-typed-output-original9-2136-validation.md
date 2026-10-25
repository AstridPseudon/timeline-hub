# D136a/D100 typed-output original9 validation

## Receiving and conservation

The receiver started at `e22217705f422436c111b65d40e4f155971864c7`. The exact
final-reviewed blobs from candidate `20dbfdef45f71fa28a63f5382c154f5cca50b83a`
were received byte-for-byte: `validation.py` SHA-256
`e632b2fc36ba78cac330ffe7b59fb4eb002a7cf78f1fc45e8e1ecbc8e21fedae`, the
unchanged evaluator SHA-256 `493fa0a5ee39dfba8a7e878f2a5247fc95fe8590741d0c7232377fd36d7b6268`,
and the D136 test SHA-256
`44bebdc4063bbb97a1e2395daa7aa9a21e5410294c67a286979b432e68b12042`.

Only `astrid/sdk/timeline/validation.py` and
`tests/sdk/test_d136_fps_upstream_compat.py` differ from the receiver. The
held D100 product, boundary test, and projection source remain byte-exact;
the projection census remains 43 predicates, 11 test bodies, and 54 fixture
statements. No fixtures, schemas, pins, or other code were edited.

## Focused checks

- `tests/sdk/test_d136_fps_upstream_compat.py`: **57 passed**.
- Ruff on all three received paths: **All checks passed**.
- mypy on all three received paths: **no issues found in 3 source files**.
- compileall with `PYTHONPYCACHEPREFIX` in scratch: **PASS**.
- `git diff --check`: **PASS**.

## Sole original9

The exact nine retained selectors ran once with the registered provider and
immutable Runtime pin `ab1e4f6141987706132916e2da16477f5a019464` (tree
`7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`). Admission was
5,316,198,400 free bytes before launch and 5,309,915,136 after. The run
exited 1 after 35.996764405 seconds: 9 tests, 9 setup errors, 0 failures,
0 passes, and 0 skips. Every selector reached the same first seam:
`provider intermediate command lacks an authenticated physical observation`.

The XML and log are private mode 0600 artifacts. No retry, adaptation,
selector substitution, fixture migration, alternate Runtime, or false-green
result was used. Original9 qualification therefore remains **FAIL/HELD**.
