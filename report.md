# F-D22 census return

Classification is **FAIL**; exact inventory is **PASS** separately.

- Service: `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679`.
- Result preserved: exit 1; 185 failed, 16,733 passed, 4 skipped, 19 errors,
  86 warnings, 565 passed subtests.
- Raw terminal SHA-256:
  `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.
- Identity preserved: Agent `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`,
  Runtime `3b926efab2eed122d374540baee297d4cdcec62a`, profile archive
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

Updated the orchestration handoff and adjacent JSON. The corrected counts are:
87 `child-import-or-recipe` (86 old environment traces plus the moved
Remotion owning-pack-root import error), 11 `custody-process-assertion`, and
37 `profile-fixture`, with all other groups unchanged; total 204.

The 11 named custody/process nodes now carry exact raw-log ranges, source
functions, allowed files, and bounded acceptance briefs. They remain
unconfirmed and are owned by live `childenv1454` plus owning source owners.
The 37 profile nodes remain unconfirmed causal profile/oracle mismatches:
14 archive 80-vs-77, 9 composition 0.0.14-vs-0.0.13, 11 missing
`chunk-SE4TPVLW.js`, and 3 unmapped scopes. No pre-existing/non-regression,
deferred, or PASS credit was added.

Guardrails retained: four skipped identities unavailable; no xfail/xpass or
deselection identities; D14/D23 not exercised; Base583 remains distinct from
the actual 8c355 snapshot; `u=565` remains passed subtests.

No tests, full suites, provisioning, type checks, lint, or environment
commands were run, per the evidence-only brief.
