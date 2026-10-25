# D108 P1 resumed original

- Same retained ID `app-pin-f7201e02-d108-p1-current-0648-1025064944-15075` was waited, not resubmitted; terminal PASS, exit 0, duration 177s.
- Separate readiness: 1/1 passed, failures 0, skipped 0, errors 0. Original P1: 2/2 passed, failures 0, skipped 0, errors 0.
- Coverage is the retained two-case P1 chain: accepted split → merged trim after Agent edit → lost acknowledgement/restart/exact retry; and refused stale trim with rollback/message.
- Tuple: App `f7201e02dc53` / `cdc1809f3ec8`; Agent `d6294843286c` / `6aeae30f089`; Runtime `c91626f5e905` / `16264479ae18`; Composition `635f4de06fda` / `5ab5191a2969`.
- Source hashes, manifest/XML hashes, exact-checkout receipts, and adoption receipt are retained in the JSON evidence packet.
- Independent read-only review `app-D108-P1-independent-GO-review-0655-r2` returned GO. Its immutable Git-object check matched the recorded App service snapshot tree and sole parent; temporary snapshot-directory recycling is disclosed as a limitation.
- P3 may now proceed serially; no P3 body has been submitted here yet.
