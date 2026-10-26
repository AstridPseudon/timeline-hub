# D141jj independent review findings

Verdict: `NOT_READY`. Static source review passes; source qualification is not a positive-path PASS.

- F1 closed: the source manifest includes the final `receiving_controls.py` hash and the candidate hash closure. Independent manifest hash/mode validation passed.
- F2 closed: caller root binding requires source and gate tuple roots to resolve identically before staging. The dedicated mismatch refusal passed.
- F3 closed: non-App recorded bases must equal the source checkout’s current `origin/main`; App remains the explicit `fc24f84994dc36cfae9349112782ab4d91dbc73b` / `faf477adef3ec24c9cc359486ac16866500ab219` exception. The stale non-App refusal passed, and the final sync receipt matches the live tuple.
- F4 closed: source and staging roots enforce effective-user ownership, no group/other write, and private staging mode `0700`. Wrong-owner and wrong-mode refusals passed.

No new static finding was identified. The caller validates pinned core/wrapper/builder bytes, source cleanliness and identity, frozen gate refs, App base, overlap, aggregate 100,000,000-byte staging bound, 4,960,000,000-byte pre-stage floor, 4,860,000,000-byte post-stage floor, and final source identity. The installer validates the complete three-row replacement, old/preserved Runtime rows, candidate/predecessor hashes, poison markers, tuple bindings, and no-install preimage without writing the registry.

Unexecuted and therefore uncredited:

- positive four-repository alternates-backed staging;
- actual caller → D68 wrapper → stub builder path;
- inherited SAME33 lifecycle controls, including real five-second available-byte observations and 4 GB whole-body stop;
- builder output/receipt and source postflight after positive staging;
- canonical activation, real delivery build, installation, ZIP, or service action.

The required floor was not lowered and no source or history mutation was made to accommodate the final tuple.
