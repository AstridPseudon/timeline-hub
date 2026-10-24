## R2 report — PASS

- Qualified exactly one test on actual integration:

```text
1 passed in 2.08s
```

- Membership: `tests/sdk/test_timeline_commit_provider_runtime.py::test_restore_inverse_redo_and_exact_retry_survive_runtime_restart`
- JUnit: [home.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-root-inverse-home-1632/evidence/home.xml)
- Raw log: [home.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-root-inverse-home-1632/evidence/home.log)

Identities remained clean and exact:

- Agent: `ef0363985e645481952448619f2cbb25e9d51a66`, tree `1be86f3b…`
- Runtime: `bc227de07262accb702eae8a44c4a666b568c08e`, tree `1d410a674d827979caf10d2da2ce3767b68c75da`
- Lock source commit matched Runtime.
- `vendor_lock.py check`: PASS
- `artifact_manifest.py --check`: PASS
- All 15 canonical mappings were identical before/after.
- Original AST/body/parameters matched actual1540 and exact47b.
- Runtime security inputs matched source `760269…`.

No product, test, lock, or integration files were modified. No blockers. Completion marker and R2 commit message were created.