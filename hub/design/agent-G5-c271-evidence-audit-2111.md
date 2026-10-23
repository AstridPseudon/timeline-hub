# G5 c271 evidence audit

**Result: PASS — source-stage only.** No merge or P1 GO is claimed.

- Agent source matched `830fba…`, tree `3bdbdd03…`; Runtime matched `8ea0766f…`, tree `6047ac30…`.
- Evidence archive SHA-256 matched `3040be2f…`; 81 JSON packets: 68 event packets and 13 validation packets.
- Recorded test: 1 passed in 40.92s, exit 0; collect-only showed 1 selected, 0 deselected.
- Canonical restoration independently verified:
  - whole undo exactly restored the pre-restructure document;
  - redo exactly restored the restructure document;
  - records contained bindings, writes, reads, dependencies, effects, and contiguous step partitions.
- Final inverse refused with HTTP 409 `intervening_write` at `parent/clip:bed.volume`; SQL, head, history, and document were byte-for-byte unchanged.
- Body lock independently matched `c2711a2d…`; worktree remained clean. All 131 recorded production module hashes matched the exact Agent tree or Runtime pin. Credential scans found zero issues.
- Authentic fixture archive hash matched `2915bd…`; restore and verification passed.

Original qualification command was not rerun, per instruction. Full/integrated/browser suites remain unverified. The separately named R4 control-doc directory was absent, so I did not substitute other documents.

No source changes were made. Commit message and `DONE` marker were created.