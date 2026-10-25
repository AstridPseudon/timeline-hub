# D118c host14 core review

**SOURCEPASS — adoption held pending authentic proof.**

Reviewed `bae5ab76f0acbf08b2d92d9f770fcf3dbe95f2fd` against `942855e56e774d83b3930bbfd87df22dbcd94ad1`.

Findings:

- Diff is exactly the two authorized files.
- `PYTHONNOUSERSITE` is genuinely rejected by strict `probe_context`.
- Sanitization reaches both validation and actual `popen_owned_group` launch.
- Caller environment, Runtime/Agent/Remotion provenance, and strict `NODE_OPTIONS`/`PYTHONHOME` refusals remain intact.
- Protected source-identity test is byte-identical; original 14 purposes remain unchanged.
- No guard or catch-all bypass found.

Checks:

- Additive pytest: **3 passed**
- Ruff: **PASS**
- Mypy: **PASS**
- Pycompile: **PASS**
- Diff check: **PASS**
- Protected 14-node selector: **NOT RUN**

The authentic 14-node service proof remains owed. The available profile is marked `079580ca`, a disallowed near-match, so it was not used.

Required selector:

```bash
pytest -q -p no:cacheprovider \
  tests/sdk/test_host_bootstrap_source_identity.py \
  -k 'bootstrap_stops_on_correlated_terminal_registration_failure or startup_budget_polling_preserves_identity_and_original_cleanup'
```

Run it only with an existing receipt-backed Remotion profile, Node executable, approved Runtime checkout, matching Agent source commit, and preserved `PYTHONNOUSERSITE=1` environment. Do not claim 14-node GREEN until all 14 unchanged nodes pass.

Evidence: `evidence/review.json` and `evidence/ledger-paragraph.md`.