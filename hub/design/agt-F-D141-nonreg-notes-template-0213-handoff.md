# F/D141 handoff

This packet is ready for the later mechanical cut/pristine join. It contains 370 retained D134 IDs, conserved exactly once across 52 disjoint roots, with managed105/root-019 and nested media48 explicitly non-additive. CLI22/root-045, fork18/root-008, identity16/root-004 plus separate root-005, selectedPARAM14/root-022 plus neighboring roots 020/021/023, legacyword35/root-048, and all remaining roots are retained.

Every row has `cut_status=PENDING` and `final_classification=PENDING`. Historical D134 classifications are measurement-only. Pristine status is copied only for exact per-ID matches; no-match rows remain UNKNOWN. Upstream-present is `y` only for exact pristine ID matches, `n` only for the three rows whose exact retained test file is explicitly absent in the frozen-source preflight, and `UNKNOWN` otherwise. This avoids treating inventory absence, parameterization, collection, or the 17-root pristine scope as proof of upstream absence.

The pristine inventory remains separately accounted as 3,082 concrete IDs plus 173 null-ID aggregate records = 3,255 outcomes. The four pristine environment-type bad nodes are marked for a same-kind Farm rerun only if the corresponding cut row later fails. The fifth pristine bad node is a timeout and remains UNKNOWN. No Farm cut outcome exists here, so no join, REG/nonREG verdict, behavior closure, or current count closure is issued.

Later join contract:

- `REG` = actual cut nonpass + same-kind pristine PASS.
- `NEW_OURS` eligibility = upstream-absent own ID + actual cut nonpass.
- `FAILS_BOTH` = actual nonpass in both, with required matching environment kind.

Source-only admission is recorded as 4,854,058,016 bytes against the 4,600,000,000-byte floor; no heavy body, acquisition, import, collection, or product execution was performed. Product source and frozen integrations were not modified.
