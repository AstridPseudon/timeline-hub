## D102c report

Implemented distinct bounded diagnostic reasons for all owned `runtime_unavailable`/`not_ready` emitters:

- Door: `not_accepting`, `not_verified`, `credential_missing`, `auth_rejected`
- Service: `provider_none`
- Server: `timeline_commit_unavailable`
- Catch-alls: `catchall:<safeclass>`

Public 503 responses and existing redaction/bounds remain unchanged. Added focused regression coverage.

Test result:

```text
56 passed in 9.46s
```

Exact targeted command passed; JUnit reports zero failures/errors. In-memory compilation, `git diff --check`, Ruff baseline comparison, and focused Pyright checks passed with zero new diagnostics.

No blockers. No full/browser suites run. Commit message written to the required path and `DONE` marker created. Recommended next step: independent review and normal release integration.