## Report

Implemented the scoped P3 registry refresh in:

- [caller-publication.py](/home/user/work/wt/app-P3-solo-registry-refresh-1018/caller-publication.py)
- [caller-custody.json](/home/user/work/wt/app-P3-solo-registry-refresh-1018/caller-custody.json)

Changes:

- Recorded live registry snapshot: 249 lines, SHA-256 `2ed2444c…`.
- Preserved 248 non-P3 rows byte-exactly; hash `ead5526f…`.
- Preserved P2 row; hash `1fe55269…`.
- Verified only removed prior key: `agent venv-agent-child-app-p3-079-2a9-2147-full`.
- Added concurrent registry-change and installation snapshot guards.
- Did not restore the retired row or alter suites, product code, or specs.

Tests passed:

```text
python3 -m py_compile caller-publication.py
python3 -m json.tool caller-custody.json
bash -n generated P3 scripts
decoded source/body/target/stage/export/custody guard matrix
missing/wrong-source/target refusal checks
bash -c positional-argument proof
retained-row and registry negative checks
git diff --check
```

Candidate P3 row SHA-256: `23226c27…`

No service, browser, backend, provisioning, build, installation, or full suite was run. Integrated P3 execution and daemon identity remain unverified as required.

Commit message written and `DONE` marker created.