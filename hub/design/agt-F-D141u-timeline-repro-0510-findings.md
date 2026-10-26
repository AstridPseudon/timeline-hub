# Findings

Result: `CONFIRMED_CANDIDATE_FAIL_CUT_PASS_PRISTINE`.

- Cut Agent `8585ed9c0404d0187b2ce70242d25114a32747c2` / tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`, Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`: both selectors failed; both failures report `AttributeError: 'Session' object has no attribute '_capture_bundle'`.
- Pristine Agent `64197afa297f86f1e738238d5e80aff6d33e303a` / tree `6c0488b3efdfa47479b0ad1b7bd20608383be26e`, Runtime `fa9cd5464a8b37b02f971de375e56be846cd69e2`: both selectors passed.
- This is a confirmed candidate under the settled rule (fail cut / pass pristine). No source or test fix was authored.
- The pristine source lacks newer `astrid.sdk.timeline.commit`, `astrid.sdk.timeline.sync`, and `runtime_protocol.timeline_commit` modules; their unavailable origins and import errors are recorded in `source-manifest.json`. The requested test identities and files were present on both sides.
- D141r media metadata behavior was exercised only through the original `test_authoring_media` selector; no fixture or assertion adaptation was made.

Raw private JUnit/XML/stdout/stderr are in `private/`; exact argv and source witnesses are in this evidence directory.
