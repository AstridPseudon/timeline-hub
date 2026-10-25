# OPS Farm metadata protected review

## Verdicts

- EXACT_NARROW_OWNERSHIP_FIX: **PASS**.
- OBSERVED_ROOT: **NO**. The live Farm/bench-store layout is absent and the retained refusal log contains no installed `RECORD`.
- INFERRED_ROOT: `<distribution>.dist-info/licenses/LICENSE`, inferred from the generated setuptools metadata shape and the verifier's refusal branch. The distribution name is not observed.
- MISSING_INPUT: the failed distribution's `*.dist-info/RECORD`; matching `licenses/LICENSE` bytes plus SHA-256; matching `METADATA` Name/Version; matching `direct_url.json` and `WHEEL` rows only.
- Overall disposition: **SOURCE_ONLY**. No install, retry, registration, child creation, or live-kit mutation was performed.

## Candidate and caller

Candidate is immutable evidence at `../rt-OPS-Farm-metadata-1404/evidence/make-child-venv.candidate`, SHA-256 `d2da4aecd759999fe1d7c929b82403533746df746c50b9928f97d083605b2a3a`.
The current installed kit preimage `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv` matches the retained baseline SHA-256 `ff8dbf0ecb615a665e346b36d9d179526a58127d09749748990ea0fa885cf8f8` (**PREIMAGE_MATCH**).

The candidate changes only the private embedded verifier: `owned_local_metadata()` allows the existing fixed metadata set plus exactly `licenses/LICENSE` when its bytes equal authenticated committed source `LICENSE` bytes. The complete caller remains the production path: it extracts `STORE_VERIFY_BEGIN/END` at lines 223 and 679, then invokes it with `python3 -I -` at lines 382-384 and 680. Existing source, origin, immutable, symlink, distribution, RECORD, client-identity, and store admission guards remain in place.

## Independent bounded controls

The fixed harness `/tmp/w-eae4294d9e/bounded_metadata_review.py` filtered `git archive` to five exact Agent and four exact Runtime declared files; it copied no source tree, wheel cache, venv, or installed root. It exercised the embedded verifier through the production subprocess caller:

```text
PASS oldRED-valid-generated-license: rc=1 unowned local distribution metadata
PASS newGREEN-valid-generated-license: rc=0 authenticated inventory returned
PASS valid generated metadata retained authenticated source/provenance/RECORD hashes
PASS reject-extra-metadata: rc=1 unowned local distribution metadata
PASS reject-altered-license-bytes: rc=1 unowned local distribution metadata
PASS reject-renamed-license: rc=1 unowned local distribution metadata
PASS accept-missing-generated-license: rc=0 authenticated inventory returned
PASS reject-wrong-source-license: rc=1 unowned local distribution metadata
PASS reject-missing-source-license: rc=1 unowned local distribution metadata
PASS reject-record-path-traversal: rc=1 missing astrid RECORD file: ../outside
PASS reject-license-symlink: rc=1 unsafe or writable retained path
PASS production embedded subprocess caller exercised for all ownership/path/symlink cases
```

## Acceptance checks

- Extracted embedded Python compile: PASS.
- `bash -n` candidate: PASS.
- Authored focused ownership/caller control: PASS.
- Ruff: baseline and candidate both retain only the same pre-existing `I001` and `SIM102`; normalized no-new result: PASS.
- Mypy: retained current baseline and candidate each have the same seven pre-existing diagnostics after line/path normalization; no-new result: PASS.
- C0 contract was read and not changed; no wire/product semantics were exercised or modified.

## Cause limits

The refusal log proves only the generic verifier message. It does not publish the failed installed inventory. The exact license row is therefore source-backed inference, not an observed Farm root. Runtime's relevant generated client files changed between `1d9ddba5` and `369ffa7c`, and Agent/Runtimes have parity for the newer generated client bytes; however, the full Runtime commit diff is much broader. Changed generated clients alone do not prove this verifier branch caused the refusal. The candidate's exact local ownership predicate is independently proven; live applicability remains gated on the missing four-item inventory.
