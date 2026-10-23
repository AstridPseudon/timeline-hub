# P2 automatic-placement integrity return

Ready for independent review on base `7fe66ead924a7902e6509ac3d4252e32c7599e2b`; final spec blob `fea6ba47e59c2a302a70c4162699af2ae4b339d6`. Only `tests/e2e/local/auto-real-proxy.spec.ts` changed.

- Accepted revision must equal the canonical parent revision.
- Official Runtime digest is independently recomputed from retained raw reply text. This preserves Python number spellings that JS serialization loses; raw/parsed envelope correspondence is checked. Existing Python interpreter and Runtime source are reused, with bytecode writes disabled and 30-second timeout.
- Exact parent/inner key sets reject unrelated additions while preserving existing value checks.

Permitted checks pass: one original listed test, scoped ESLint, App/Node types, all 75 prior matcher probes plus 34 new probes (109 total), read-only private819acf Composition 0.0.14/80-file graph, diff/EOF/outside-file identity. All 137 original assertion statements remain verbatim/in order. Baseline audit independently reproduces all three gaps; 24 new negatives fail on the old source and pass after repair.

Supplemental e2e types retain four known errors versus seven earlier baseline, zero introduced. **No browser journey body, HTTP, full suite, build, service or native14 run.** R5 authentic-seed migration remains a separate HOLD; no fixture conversion or duplicate seeding.

Exact commands, decisions, probe provenance and limitations: [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P2-auto-oracle-sol-return-1108/report.md).

Next: independent review, separately owned seed migration, then centrally authorized real journey qualification. No plan decision changed or repair blocker.
