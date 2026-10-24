# F-ABA-attach-return-1019

Result: **PREPARED PASS**. Integrated/live qualification remains intentionally unrun.

Implemented:

- Added offline controls for candidate argv, partial/oversize retention, and child-exit preservation.
- Produced exact one-row candidate: `evidence/suites.conf.candidate`
- Produced installation/retention manifest: `evidence/install-input.txt`
- Support checkout: `546d86816a3df9e5e1529e80ca81f5c1d397c75c`
- Candidate row SHA256: `3f3d43e39321467a41e06c405c1419376e5f8ec70c408ef0814465f70be302ba`
- Registry pre-hash unchanged: `5ada85961e709386b7d7aa328338fda01af6bfc2c8efea6ddd9170671dbe851f`
- Expected post-install hash: `31cfddf295b376036c62e08d935373a78fdc37f153f1445f4a69f08437c56133`
- Outside-row identity: `afd6f92fe8208bcc211208ca80e3aca7446dede50f2c64e968bc359ea7e5d9bc`

Tests:

- Targeted pytest: **21 passed**
- Scoped Ruff: passed
- Mypy Python 3.12 mode: passed
- Candidate `bash -n`: passed
- `git diff --check`: passed

No live registry install, original ABA execution, full/live/browser suite, or production changes were performed. The current live row remains direct pytest until the manager performs the normal checkout/install and central service run.