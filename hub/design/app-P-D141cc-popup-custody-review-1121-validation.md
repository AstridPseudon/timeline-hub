# Validation

Read-only validation completed with Python standard-library SHA-256, JSON, XML, and TSV parsing plus Git checks. No product test, service command, browser rerun, typecheck, lint, or pytest/vitest command was run.

- Controller worktree: clean at Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- Recipe `/dispatches/0`: exact hash `d665c4907abd063edc9da0f29c887b56f7b66fb80febbe52f14732ea66e95d0d`; command and row hashes recomputed equal to declared values for both preflight and normal.
- Exact new namespace: one preflight ID and one normal ID; no duplicate normal ID.
- Raw normal result: status `fail`, exit `1`; XML counts `1` test/`1` failure for popup and `1` test/`0` failures for readiness.
- Raw normal collection lists exactly one test in one file; its SHA-256 is `83f635e5f20b9cf48dd8244bd361227f5e9d1d2ffce7fdd7bb849ac2099d4d23`.
- Native trace: 44 samples, minimum `5471948800`, max gap `5.006s`, standing stop not reached.
- Source pins and builder SHA/blob match the accepted source manifest and raw D66 manifest.
- Old `13234`/`20413` remain cancelled; `20413` has no body exit/summary and was not treated as a body verdict.
- The review sampler command was foreground and reaped: `while true; do date -u '+%Y-%m-%dT%H:%M:%SZ'; df -B1 /tmp \"$PWD\"; sleep 5; done >> evidence/disk-trace.txt`; session `10000`, exit `1` after Ctrl-C. Its trace is reviewer-only and not body evidence.
