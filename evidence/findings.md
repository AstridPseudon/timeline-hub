# D139 Store disposition — PASS_ASSESSMENT / UNAPPLIED_HOLD

This is one independent Luna read-only disposition review of the exact
`c84d1dcd3e7d6c77a17a97bdb4771ba1114ca68b` candidate. `PASS_ASSESSMENT` means
the author disposition is complete and accurately separates qualified source
fixes from open safety guards. It does not qualify the source for installation
or real cleanup: the source remains `FAIL_SOURCE/NOTREADY`.

## Findings, all reported together

1. **D139-F1 — critical — UNAPPLIED, confirmed.** `activity.json` remains the
   only worker/queue/service/KEEP/ACTIVE reference source and its hash is only
   self-consistency. In a private fixture, a reference was refused, then a
   same-inode valid self-hash rewrite erasing it allowed retirement. No
   authoritative Store-owned registry binding was added. Repeated scans and
   self-hashed activity are not authority.

2. **D139-F2 — critical — UNAPPLIED, confirmed.** Process scans are
   observations, not exclusive admission. An independent private hook started
   a process with the quarantined directory as cwd after scan 3; retirement
   returned `retired` while the process remained alive. The source does not
   establish a supported exclusion through quarantine, deletion, and recovery.

3. **D139-F3 — critical — UNAPPLIED, confirmed.** Late lifecycle state is not
   covered through destructive completion. Independent private hooks added a
   worker activity reference after `_retirement_audit` and a `KEEP` marker at
   the deletion validation boundary; both still returned `retired`. Ordinary
   marker/reference checks remain required, but no late-state admission
   protocol is present.

4. **D139-F4 — high — FIXED_ORDINARY_CROSS_ASSOCIATION, qualified.** The
   receipt now carries the exact pre-retirement source snapshot, and `_load()`
   recomputes the receipt from that source. The unchanged/new focused tests
   reject wrong node, path, sequence, lock, owner, registration, suite, and
   missing-source mutations; recovery also rejects a source/receipt mismatch.
   This is structural consistency under the existing Store ownership model,
   not authentication against coordinated same-UID rewriting of all records.

5. **D139-F5 — high — FIXED_CURRENT_TREE_CUSTODY, qualified.** The candidate
   manifest records the exact current `bench_store.py` bytes and mode. Its
   SHA-256 is `d1cdb35cec0ba7a9a27ee97652e185d06169fffdb11b3e0ee4b4a64d71e3391b`,
   matching the reviewed candidate. The earlier return-manifest mismatch is
   preserved as historical evidence, not silently repaired.

6. **D139-S1 — high — FIXED, qualified.** Nested private payload retirement
   passes on the exact candidate; the recursive call now matches the actual
   `delete_children` signature and does not pass the nonexistent `strict`
   keyword.

## Historical applicability

Historical child `3e16336b6a5a2d8293a95a99c3665cbafbefb234b4b421fab53e17edde29af30`
is separately `SOURCEONLY/NOTREADYforcleanup`. The exact `123bb` source and
qualified Agent 2202/2205/2210 packets show that the old owner/entry/
registration shape lacks the candidate's persisted lifecycle fields. No old
field was synthesized, no historical state was adopted, and no disk fix is
claimed. Age alone, repeated scans, or self-hashed activity cannot create
authority.

## Disposition

Keep the candidate unapplied. An owner decision is required for a separately
scoped lifecycle admission/exclusion contract covering real queue, worker,
service, marker, consumer, retirement, and recovery participants. Do not
implement that protocol, mutate real Store metadata, install the candidate,
or perform cleanup in this review.
