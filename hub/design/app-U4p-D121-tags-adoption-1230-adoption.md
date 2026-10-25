# U4p D121 adoption

Adopted qualified Runtime history-tags release `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` (tree `de2954a0ceadb4455903d9abdfec3b773318a50f`) through the existing sync and installer-manifest scripts.

The App remains pinned to Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`, the existing producer version, and unchanged generated client/schema/mapping bytes. Only `runtime.lock.json` and `public/install-manifest.json` changed.

Checks passed: Node `v20.20.0`; vendor lock; installer manifest tests; Runtime schema guard; targeted Vitest (17 tests); Runtime generator/artifact checks and `tests/test_artifact_manifest.py` (3 passed); ESLint; JSON parsing; `git diff --check`; 14 mapped SHA comparisons; protected scope check.

No browser, collector, body, service, full-suite, or future P2 proof was run.
