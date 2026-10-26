# Validation

- Full touched file, pinned Node 20/Vitest, private `--no-cache`: PASS, exit 0, 13/13 tests passed.
- The additive control retained two accepted-read identities and heads `timeline-rev-2`, `timeline-rev-3`; the same checker passed the retained artifact and rejected the stale artifact with exit 1.
- Scoped ESLint over the six source/checker paths: PASS, exit 0.
- Locked App TypeScript check (`tsconfig.app.json`): PASS, exit 0.
- Locked Node TypeScript check (`tsconfig.node.json`): PASS, exit 0.
- `git diff --check`: PASS, exit 0.
- The filtered control invocation itself reported the selected test passed but exited 1 because the repository wrapper reports 12 undeclared filtered skips; it was not used as acceptance evidence.

No native service, browser journey, diagnostic body, package installation,
full suite, or test-service request was run. Existing React `act(...)` warnings
remain in the touched test file; assertions were not weakened or skipped.
