## PASS — F-harness integrated static qualification

- Integrated HEAD: `d5665e898ac6e3347c8b8ddfc06b3c678dea04fa`
- Tree: `184ab4f6cf5cade44bafefa8f465bb4ef4fcf06d`
- Integrated delta contains only the four harness files; `suites.conf` unchanged.

Source SHA-256s match independent PASS reviews:

- Discovery runner: `9e64aab7342ad3005bcd8e634c726920e523470e9787799886da6fbd9d92d4b8`
- Discovery wrapper: `fe48a6a55c02b8cad366353be26b5c074acbb92729174ee84832e63ae6274a35`
- Generic runner: `6eb755728488122c905d8111e8e68a93d6961e679d2b10a804240b0b311b837e`
- Generic wrapper: `b1bda1c3771c29588c70a3ad20369ee908e78f1a65bae7da97258055a0cce29a`

Git blobs are identical to reviewed commits `65239cdc1b` and `40d6f6833b`. Staged rows match:

- Discovery row: `38b2cd712193e7ac6cad90a787971a844f8e606b55cb1634590c1e20c4edad33`
- Generic row: `8d5b3fd0aa08bf70a349ca226bb7324e75cbb6ec01446538be6c779d8fac3122`

Checks passed:

- `py_compile`
- Ruff
- mypy: no issues in 2 files
- Both `bash -n` checks
- `git diff --check HEAD^ HEAD`

Independent reviews confirm the normal lease → snapshot → approved carriers → custody/maker/RECORD/client/profile/origin checks, durable `NOTRUN`, and nonzero postcheck handling.

Limits: `bb50/f320` child does not exist; `ba8f` is ineligible. No preflight, Node, install, probe, child-maker, original-body, full-suite, or source-provider execution was run. Full v2 DTO/reply coverage is not claimed by this narrow harness qualification.

Commit message and `DONE` marker recorded.