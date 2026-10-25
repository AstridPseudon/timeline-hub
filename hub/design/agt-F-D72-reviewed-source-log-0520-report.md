Implemented the source-only ledger append.

- Added four separate `SOURCE-QUALIFIED, BEHAVIOR-PENDING` entries for D99 roles, D92 catalog A-B, ordinary sheet, and word46.
- Preserved existing 550/23 dispositions and D95 retirements; no counts or authority changed.
- Added only the narrow D100 cross-reference; D100 final publication and D103 entry remain withheld.
- Ledger CAS evidence: pre-hash `c2cd8e68…`, 168,319-byte prefix preserved; post-hash `814e693a…`, 175,497 bytes.
- Static Markdown/reference parse, prefix comparison, and `git diff --check` passed.
- No product imports, pytest, services, or behavioral tests run, per SOURCEONLY scope.
- Created the required commit message and `DONE` marker.