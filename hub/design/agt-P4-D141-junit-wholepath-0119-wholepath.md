# P4 D141c whole-path assessment

Verdict: the actual D141c body is independently bound as `3 passed / 0 failed / 0 errors / 0 skipped`, but final custody remains `FAIL`.

The path is coherent through execution:

1. The normal-manifest recipe is `tests/suites.conf.candidate.request.md:84-116` (Git blob `fbde96168dca681a76cff1526c23b8d0b74001eb`). The retained input manifest is SHA-256 `67ef4348b4b77eb02b74abe20ad6fefdb075f980dc8ca563c0a3c79d1f0e5b9f`.
2. The strict launcher is `tools/p4-d73-pinned-launch.sh` (Git blob `f1bde17ea107a8b669cb6924fbdbd2f3979da988`, file SHA-256 `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`). It checks exact absolute checkout paths, SHA/tree/parent/clean state, the combined original-test hash, lock/import/schema/client/profile/composition identities, then returned preflight `0`.
3. Materialization copied the input to the distinct body destination byte-for-byte: both manifests hash `67ef4348b4b77eb02b74abe20ad6fefdb075f980dc8ca563c0a3c79d1f0e5b9f`; `samefile=false`.
4. The runmanifest is SHA-256 `86595e66a6739d9d6c9cdaa5fe583c4b7eff50a5f2ba5aec4e620df91104dc71` and repeats the tuple, but preserves the old `0047` `junit_paths`.
5. The actual shell argv is SHA-256 `ad2168fde0f0c928a975e2f2898a824031ce434ec1ecd47db97f16932f32f352`. It contains `run -- -m pytest`, `-m integration`, three concrete selectors, and explicitly writes JUnit to `0055/evidence/body-evidence/p4-d141c.xml`.
6. That XML is SHA-256 `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`, 724 bytes, with 3 tests, 0 failures/errors/skips, and 23.668 seconds.
7. Central service `agent-p4-current-becfe-http-3legs-1026011042-10086` has request SHA `20d18d526ebe3bc848eb82659025636c41bf810b48dc5de2d4c590b9baf58b97`, summary SHA `9376311d8eb310841c1c11ea68c5db328a8460029cc53b54a12a2bd244ac9aa1`, status `pass`, exit `0`, and summary `3 passed in 23.68s`.

## Finite gaps

`P4-D141c-W001` — the manifest and runmanifest say `0047/evidence/p4-d141c-normal.xml`; that file is absent. The actual XML is under `0055/evidence/body-evidence/p4-d141c.xml`. This is a discoverability/custody mismatch, not a body or source mismatch.

`P4-D141c-W002` — the selector manifest has an identical 0055 copy, but the manifest still references the 0047 path. The actual XML, logs, command, central summary, snapshot, ext, and exits are private files in worker/service directories. The retained review explicitly says raw originals were not copied into the review. The App receiver has no recorded receiver-owned copy or retention fact, so artifact lifetime after worker recycling is unverified.

`P4-D141c-W003` — source origin is matched, not defective: the pinned Agent/Runtime/App/Composition checkouts and central Agent snapshot agree on the frozen tuple and are clean before/after. The bounded missing fact is direct body-process import-origin telemetry; the body log contains only pytest output. The launcher preflight and exact source/hash comparisons are the evidence actually available.

`P4-D141c-W004` — the App source-binding publication is source-only/no body. The 0119 handoff leaves cumulative P4 verdict ownership with App and records the custody hold, but does not provide a receiver-owned machine-readable final P4/JUnit binding. App can preserve the separate actual PASS and custody FAIL only by consuming that handoff and private paths.

## D97 comparison

The retained D97 design path is comparison context only. It records one original ten-note PASS at 28.101 seconds and launcher controls, but its independent design report and GO review disclose that the App pointer advanced after execution and that the ambient Agent tree differed from the captured fixed tree; the launcher-selected captured tuple was the binding. No D97 body was rerun here. D141 is stronger on the source tuple because its central snapshot, pinned launcher path, source receipts, and four clean checkouts all agree on Agent tree `2ebe2ddf...e58a`. D97 does not repair or substitute for the D141 JUnit custody defect.

Historical 1347 remains a separate pre-body failure (`exit 1`, zero selectors, no JUnit); 0101 remains `FAIL`; 0106 remains `PASS_OPERATIONAL_SOURCE / INSTALLATION_NOT_READY`. None is converted into the actual 10086 body PASS.

No product, launcher, guard, schema, test, registry, C0 contract, or environment defect is inferred. No body, pytest, import, collection, or full suite was run by this worker.
