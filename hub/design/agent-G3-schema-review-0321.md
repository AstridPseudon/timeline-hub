# Agent G3/R2 schema review 0321

Source restore **PASS**: `425ab45946b1436d8f1ad02c065be5e2a788d9b5`, tree `11e132061afd45e5d419a5424790c98aef37180e`, parent/base `ecea7d8563c93059283ef9475ecb41a37e628a38`. Exact diff is one file only: `astrid/core/timeline/schema/edit-command.schema.json`. Its SHA-256 is canonical `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`, matching `7d3562028` and home/integration `cedc07280`. `InverseArgs.steps` is present and whole/selected inverse validation passed. All other protected G3/R2/R3/meta/current-V4/client/lock paths are exact base; v2 request/reply fields are preserved.

Full-join readiness is **HOLD**, separate from source restore. The exact tree has the expected four broader schema failures: three current-union fixture equalities omit `InverseArgs.steps`, and composed-schema operation inventory lacks a `doc.patch` fixture (`KeyError`). Corrected test blobs exist in `7d3562028`/`cedc07280`; repair `44ea0257` descends from this tree and owns those test-only assertions. No tests were changed here.

Evidence: published schema floor **1 passed**; parent-media provider reload/undo/redo **1 passed**; current-union **31 passed, 3 failed**; composed schema **4 passed, 1 failed**; Ruff `2150/2150`; private Python 3.11 mypy `1915/1915`; diff check and worktree clean. No full/browser/farm/native14/P4HTTP suite run.
