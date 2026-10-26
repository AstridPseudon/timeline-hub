# Independent validation

- Parsed both retained native JUnit XML files with Python `xml.etree.ElementTree`: PASS.
- Reconciled nested suite declarations: cut `9561 = 9388 concrete + 173 unnamed`; pristine `3255 = 3082 concrete + 173 unnamed`: PASS.
- Recomputed statuses: cut `PASS 8991 / FAIL 201 / ERROR 196`; pristine `PASS 3047 / FAIL 20 / ERROR 15`: PASS.
- Recomputed exact membership: matched `3018`, cut-only `6370`, pristine-only `64`; no duplicates; per-ID records cover the exact XML union `9452`: PASS.
- Recomputed classifications: `CUT_PASS_NOT_REG 8991`, `FAILS_BOTH 19`, `N_A 373`, `UNKNOWN 5`, `PRISTINE_ONLY 64`; exact candidate set empty: PASS.
- Direct `git cat-file -e` / `git rev-parse` readback for all 441 source-map rows at frozen Agent refs: PASS.
- Reconciled all 344 D134 rows and all historical root labels against retained source tables: PASS.
- Verified all 21 retained manifest input hashes and both terminal XML hashes: PASS.

No product tests or full suites were run; this was a protected evidence review only.
