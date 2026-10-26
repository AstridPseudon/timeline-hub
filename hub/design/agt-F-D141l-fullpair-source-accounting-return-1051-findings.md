# D141l corrected full-pair source-accounting findings

Verdict: `PASS_EVIDENCE` for the bounded source/accounting return; product acceptance remains incomplete.

- Cut XML `6710f7fe1b4b1a0b4d43614f0fe58d437b0b6fff76990e4a717022cef773fcd5`: 9561 declared, 9388 concrete, 173 null-identity aggregate PASS members; 201 failures and 196 errors.
- Pristine XML `9d36fcecf662cc9138cd30cb6ad674a57db30209b18593f29da08ed961792bba`: 3255 declared, 3082 concrete, 173 null-identity aggregate PASS members.
- Exact concrete membership remains 3018 matched, 6370 cut-only, and 64 pristine-only.
- The five named cut-only failures are exact source-backed N/A: their current files exist, but their exact target functions are absent at pristine Agent `64197afa`; no renamed body match was accepted as a fuzzy equivalent.
- The corrected classification is `N_A=378, UNKNOWN=0` for cut non-PASS rows; their actual cut failures remain failures/NEW_OURS known gaps, not PASS, REG, or deducted outcomes.
- Every pristine-only ID is mapped in `pristine-only-map.json`. Three CLI parity IDs have exact current function/body identity; the other rows are source-present, source-absent, or no exact counterpart, but all behavioral results remain unproven because no current result is present in this pair.
- The existing 19 FAILS_BOTH remain actual failures with their existing limits. No environment-sensitive claim was added beyond the settled source/cause evidence.
