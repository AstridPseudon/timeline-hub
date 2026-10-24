# D42 Security Review — FAIL

Reviewed candidate `35320a9e90853ca2e9a863baedccdafe23a4fe38` (tree `a51d298e...`) over parent `42080f33...`.

Finding: `_verify_replay` keys on `auth.validate`, but not its mutable helper dependencies. `auth.validate` calls `validate_claims`; mutating that helper after a warm read was skipped by the memo and returned success. Clearing the memo caused refusal. This violates the complete dynamic-dependency requirement.

Evidence:

- Exact Agent archive `415181d...`, tree `f49cae...`.
- Required lanes: `145 passed`; `159 passed`.
- Combined collection: `304 tests collected`, no exclusions.
- Private dynamic-dependency attack: reproduced bypass.
- Ruff: same 11 inherited findings.
- Pyright: parent/final both 1,449 diagnostics; zero normalized new/removed identities.
- Artifact manifest and `git diff --check`: passed.
- Contract/schema/client protected paths: unchanged.
- No tracked edits, full/browser/HTTP suites, or duplicate benchmarks performed.

Recommended next step: make the memo key include a complete immutable auth/validation dependency version, or ensure every helper change invalidates the memo.