# D124/D54a b742 host14 result custody review

Decision: **PASS for the bounded pristine upstream host14 proof**, with one explicit receipt metadata failure noted below.

## Scope and source custody

- Composition controller base: `tl/integration`, `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.
- Agent: `b742893426a46a99a2f30583a54faeebe2bd98b7`, tree `ccb2f286eae9419b95a3f54b11208f68c57b27cf`.
- Runtime: `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`, tree `1d3e06f4d59ed6d459646d24ab185c36eb5be075`.
- The b742 Agent checkout, its authenticated 08e6 counterpart, and d4f496 Runtime checkout are clean.
- The target source file is byte-identical between b742 and 08e6. Both targeted function-body AST hashes match the authenticated D54a REG14 map; no source-purpose change or semantic retirement is present for these 14 nodes.

## Exact result

- Central request: `runtime-d118-upstream23-targeted-1025130322-26621`.
- Central result: **PASS**, exit `0`, `14 passed, 0 failed`, `2.29s`.
- Durable JUnit: 14 unique exact REG14 testcases; zero failures, errors, or skips.
- Four process-origin records resolve Agent imports only under b742 and Runtime imports only under d4f496; `PYTHONNOUSERSITE=1`, `-n 3`, `--timeout=45`, and the original test budget are retained.
- JSON, XML, artifact hashes, in-memory Python compile, `bash -n`, and `git diff --check` validations passed without rerunning test bodies.

## Receipt caveat / explicit FAIL

The central summary is authentic for the registered service result and reports the required 14-pass exit, but its rendered command still prints `ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-08e6b905` and integration Runtime tree `de2954a0…`. That does not match the b742/d4f496 custody tuple. Therefore:

- **PASS:** central service status/exit/count receipt.
- **FAIL:** central receipt rendered-source-path congruence as a standalone b742 identity proof.
- **PASS:** actual process-origin custody, durable XML, selector/member map, and clean checkout evidence establish the bounded b742/d4f496 proof independently of that stale receipt rendering.

The earlier request `runtime-d118-upstream23-targeted-1025130238-26899` is retained as a separate **FAIL / infrastructure-only zero-body** result: `NotADirectoryError` caused by the worker `tmpdir` metadata file shape. It is not a test outcome and is not blended into the 14-pass result.

## Limits

This review does not close current integration REG14 status, qualify a full/core/browser/P4/stage/render suite, credit absent neighbors, or assert current semantic behavior. It preserves the author worker’s evidence and adds only this independent review bundle.
