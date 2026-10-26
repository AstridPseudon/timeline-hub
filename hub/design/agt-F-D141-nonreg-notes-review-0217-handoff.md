# F/D141 review handoff

The completed D141 notes template passes independent documentary review and is ready for the later mechanical join only after actual cut evidence is supplied.

- Use the retained D141c per-ID inventory only for exact node-ID matches; preserve `PASS`, `FAIL`, and `ERROR` exactly.
- Keep the 173 null-ID aggregate records separate from the 3,082 concrete IDs; do not fabricate selectors or matches.
- Keep `y=21`, `n=3`, and `UNKNOWN=346` as documented. Only the three exact frozen-source test-file absences support `n`; no inventory absence is an upstream-absence proof.
- Preserve the four conditional same-kind environment reruns and the fifth timeout as `UNKNOWN`.
- Do not infer a current cut failure from historical D134 statuses. All current cut rows are `PENDING`.
- Later join: `REG` requires actual cut nonpass plus same-kind pristine PASS; `NEW_OURS` requires actual cut nonpass plus proved upstream absence; `FAILS_BOTH` requires actual same-kind nonpass in both; no blanket rerun and no current REG verdict.

No product adoption, behavior credit, App P4 verdict, or Farm/Runtime final REG join is included in this handoff.
