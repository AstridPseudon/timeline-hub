# D139 independent final review — FAIL_SOURCE

Reviewed exact `tl/rt-OPS-store-retire-return-2235` at
`2ab240fcdcdae0db60497bb7a355cbfe6e53b5a8` read-only. The prior four attacks
are not all closed by the return source.

Findings, all reported together:

1. **D139-F1 — critical: mutable activity authority.** `activity.json` is the
   sole worker/queue/service/KEEP/ACTIVE source and its hash is only a
   self-consistency check. A valid same-inode rewrite erased each reference
   and allowed retirement. The source has no authoritative registry binding.

2. **D139-F2 — critical: post-final-scan process race.** Private cwd, fd and
   cmdline processes introduced after `_delete_owned`'s third/final scan all
   survived to deletion. Repeated scans do not provide exclusive admission.

3. **D139-F3 — critical: late marker/reference race.** A KEEP marker created
   after the quarantine audit was deleted by retirement; a worker reference
   added after `_retirement_audit` was ignored. The admission guard does not
   cover the state through deletion.

4. **D139-F4 — high: receipt cross-consistency.** Primitive malformed fields
   are refused, but a valid-shaped wrong node, sequence, and registration
   association was accepted by `_load()`.

5. **D139-F5 — high: custody mismatch.** Return source-manifest hash
   `5af33a48e76c7cbd94ef2948d1b7bb6225a318bb0715762e98087b93c970b747`
   does not match the exact candidate source hash
   `5504746d7348611878bb75128e20c1df22a9f237ad1b5a135fa40992c868758b`.

The original age/clock, caller-field schema, malformed primitive receipt,
journal/recovery, inode/no-follow/hardlink, and fixed-two controls passed in
private testing or the candidate suite. Those passes do not cure the five
findings above.
