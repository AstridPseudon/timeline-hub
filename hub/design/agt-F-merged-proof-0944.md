# F merged proof handoff

PASS: integrated Agent tree `543d133c85de16ab800c4df0e9ff504ca077fcbf` / `f6cda3a2956ca702721ad3c1ba79c20932e1506a` passed the exact scoped ten-node proof. Runtime was the actual authenticated `1365e4b17b31c4a7093d5943674637067fd2bab4` / `6c69c3dc47822fffbaf27cd63815d2895155ffaa` origin.

The central targeted run `agt-F-merged-proof-0944-targeted-1023094543-29043` reported **10 passed in 12.90s**: the six checkout nodes and all four parameters of `tests/editing_conformance/test_recipe_m2_video_unplace.py::test_provider_round_trip_preserves_opaque_registry_and_order`. The reviewed `f0af12f67` and `fad05679a` production blobs match HEAD exactly; R1 `d46210398`, R2 `f7fcb7282`, and P4 single/ten/rerun (`ca1f2228c`/`f816d71d9`/`de046064f`) are retained. Normal Ruff/vendor/artifact/diff and the one actual mypy comparator attempt all passed at the stated ceilings (`2149`, `1912`).

No source/test/pin/report file was added to the Agent repository. The seven remaining original provider nodes, P4 HTTP, full suites, and heavy/native/browser cases were not rerun.
