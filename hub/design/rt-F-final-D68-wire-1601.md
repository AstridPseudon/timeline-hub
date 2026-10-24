## Completed

- Added private D68 delivery caller, guarded installer, and candidate service rows under `evidence/candidate/`.
- Preserved the existing 83-test + TypeScript core row unchanged.
- Delivery rows now call the reviewed wrapper (`bae840…`) and f25d builder (`f25df…`), forwarding owner extras unchanged.
- Receipts record source identity, synthetic applied identity, and actual overlap paths.
- Durable artifact hashes:
  - Installer: `9b9f42db…`
  - Caller: `db872fa2…`
  - Rows: `d742a754…`

## Validation

- Python compile — PASS
- Ruff — PASS
- Mypy — PASS
- Shell syntax for all rows — PASS
- Candidate installer/preimage and outside-byte guards — PASS
- Synthetic external-cwd f25d dry-run through D68 wrapper — PASS
- Conflict fixture retained staging — PASS
- Wrong tuple/wrapper/builder refusals — PASS
- No live install, real build/ZIP, full suite, network, or product execution performed.

Final tuple data remains pending. Commit message written; `DONE` created.