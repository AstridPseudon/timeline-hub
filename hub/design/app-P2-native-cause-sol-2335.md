**Diagnosis complete: actual7232 failed because door port `17340` was occupied (`EADDRINUSE`). No repair was justified within scope; no files or suite rows changed.**

The failure occurred in `support/harness.ts:113`, called from `DirectHarness.start()` before TLS creation, realm creation, Runtime startup or native seeding. Hosted build and actual-beforeAll completed; native assertions, selector collection, mandatory leaf and all eight originals did not execute. The new bootstrap/readiness behavior remains untested.

This is a proven environment port collision. Retained evidence does not identify the occupant or establish whether occupancy was transient. It provides no evidence of a product, quoting, stage-order or fixture-authority defect.

Provenance:

- App: `d96e45cab356e66332050aa902558789b4382dbd`, tree `1764a55c7e3255628fb750b1f9d22c189289765c`.
- Harness blob: `793f49af6d039f2d23a75fcc7deaff2f1366c533`.
- Agent: `079580ca46af77e0292d49dc34386b25c8391f99`; Runtime: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
- CN2147 provisioning and RN2049 receipts identify that pair and remained byte-unchanged.
- Exact 893-byte native stderr SHA256: `84c7e34708ca559368ad786d12b771f376fdfc25063bcab51affbcfdbf764835`.
- Unchanged P2 row SHA256: `3763145c84305d061f2f8687c28440a21e32518f49b8e2df9e54172227d3dd4c`.

Validation:

- `python3 /tmp/w-f4e63b86b0/native-cause-check.py` — **25 checks passed**: intercepted actual/current outer callers, argc2/`-c`, inner/outer Bash syntax, failure ordering, all 21 native assertions retained, P3 exposure, and byte-unchanged retained evidence/receipts/suites.
- `git diff --check` — passed.
- `git status --short` — clean.

No build, backend, native seed, list, browser, HTTP or service run was performed.

**Next smallest action:** the central test/environment owner should identify and resolve ownership of `17340` before retrying. P3 Sol2330 uses the identical harness blob and also lacks a row-level port override, so it shares this collision risk. Any port reassignment must remain consistent across hosted build and harness; I made no speculative override.

Commit message and `DONE` written.