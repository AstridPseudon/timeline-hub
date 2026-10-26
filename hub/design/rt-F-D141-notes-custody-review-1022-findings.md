# F D141 notes custody correction review

Verdict: **PASS_CORRECTION_BOUNDED**.

The immutable correction passes for the current canonical content and for its explicitly bounded earlier-to-current aggregate interval. The original installation review remains **FAIL_CUSTODY_LIMIT**; this review does not convert it to a historical-install pass.

## Independent findings

- All seven recovered originals match the base `d77575d45ad8920592b7d5352518e63b6048cfb6` Git bytes. The full SHA-256 values and Git blob IDs are recorded in `source-manifest.json`.
- The mandated command completed read-only with exit `0`: `python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141-final-unit-notes-custody-return-1015/evidence/comparison.py`. The script SHA-256 is `f02c7accbdff821f88a0e008a2139391665a5674c8a9de133dcb3717a6820f27`.
- The actual `README.template.md` target and candidate are SHA-256 `48013c7fbcb8f72a7d4371540b50a4abcc43dd8c6274d90726beec82b8f9fc02`; its backup is `13f2b3409d42313dd2ed02d1d479bc5e27cb74f7ec29151e30199428fe0bc776`.
- The actual `gate-results.md` target and candidate are SHA-256 `506e4461b63e81af490e4b43c5eb7fe2717ebb07825c77d216a59967d863a55d`; its backup is `b29945990c34adc8d8ae0b25f8c6621c4c509f43c84b22adb7dedca141815b47`.
- Both targets, candidates, and backups are independently regular, non-symlink files with mode `0644`; target/candidate bytes and backup/preimage bytes match.
- The current outside-target inventory has `568` items and map SHA-256 `0c11b4b85b75c19657a3a824f4c85176f6bb78e96fc27a9f653e06b015103724`.
- The exact original 0254 inventory serialization was inspected in its retained log: sorted `os.walk(followlinks=False)`, target exclusion, `mode`/`regular`/`symlink`/`sha256` fields, and compact sorted-key JSON hashing. Recomputing it yields `568` and `eea4cb8759a00a1ad7e9a5eab5922e4ebeb36d2a6ec0b0bde22c8f63e3c7fded`, equal to the genuine 0258 retained aggregate.
- The retained function-only `render_readme` result remains the caller evidence at SHA-256 `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`; this review did not rerender or invoke delivery-build.

## Custody boundary retained

The installer’s genuine immediate pre-CAS 568-item map, genuine pre/post conservation, and original installer sampler PID/exit/wait/reap remain **UNKNOWN / NOT_RECOVERABLE**. The retained before map was later populated from current bytes. The earlier aggregate is not an immediate pre-CAS map and does not prove absence of transient changes. The new review sampler’s lifecycle belongs only to this review.

## Prose discrepancy

The retained validation and handoff prose abbreviate hashes with ellipses (for example `48013c...f9fc02`, `506e44...63a55`, and `eea4cb...7fded`). These are not complete hashes; each expands to the exact controlling value recorded above and in the controlling JSON. No conflicting full-hash value was found. The originals were not edited.
