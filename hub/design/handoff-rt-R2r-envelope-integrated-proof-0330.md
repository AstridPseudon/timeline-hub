## PASS — R2r integrated proof

- Integration commit: `34eac0041b0891e9011966b39bcbd26053fde5bc`
- Integrated tree: `9853574865f25e08284e82ffb26c0bdecaa16a30`
- Reviewed source: `f8a397d2389f5fd7e102fee142f1ce24b011076b`
- Review base: `780da6d605033ca71dbe2ad48c10ec2870ea4865`
- Reviewed source and integrated trees are exactly equal; `git diff --quiet` passed.

Evidence:

- Service `runtime-targeted-1023032723-4090`: PASS, exit 0, **75 passed in 36.66s**, exact snapshot tree verified.
- `/home/user/work/venv-runtime/bin/python generators/generate.py --check`: PASS
- `/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check`: PASS
- `git diff --check`: PASS
- Reused exact-tree independent evidence: Python **75**, TypeScript **63**, build/conformance/artifact checks, Ruff **75/75**, Pyright **147/147**.
- Public probes: 4 valid cases passed; partial receipts and missing `would_status` refused; historical `rebased` preserved.
- No full/native/browser/heavy suites run.

Producer metadata:

- Contract version: `0.2.14`
- `SCHEMA_DIGEST`: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`
- Artifact producer: `astrid-runtime`
- Artifact producer version: `sha256:d5f98db3213e91d96d4a7f5b184e17bf5268357b37dc06eaa5b568c4b788a572`
- `contract/artifacts.json` SHA-256: `7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d`
- Python generated hash: `9b5686c388347108898956c3475b16960e2434d64adcefcc71a26fc269cdd904`
- TypeScript generated hash: `7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4`
- Canonical Agent `edit-command` retention: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`

No product files were changed. `DONE` created; commit message written and names R2r.