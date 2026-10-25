Implemented F-D86 corrected safe metadata packet at [superseding-exact22]( /home/user/work/wt/rt-D86-20-22-exact-return-0358/evidence/fd86-20-22-safe-export-0347/superseding-exact22 ).

- XML-backed exact22: 4 PASS, 18 ERROR; no complement inference.
- Verified producer hashes, selector digest, membership, limits, venue, and actual run ID.
- Preserved all 22 identities and left original exact22/actual20 packets unchanged.
- Recorded A20 service 18575 and Agent peer 033346 request accurately.
- No raw artifacts, commands, credentials, URLs, or stacks exported.
- No product/test changes.

Checks:

- Inline metadata/XML/hash/redaction verifier: PASS.
- `git diff --check`: PASS.
- No full pytest requested; evidence-only task.
- `DONE` and commit message created.

Blocked: none.