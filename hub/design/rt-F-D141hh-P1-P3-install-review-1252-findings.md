# D141hh P1/P3 installation review

Verdict: **PASS**.

No blocking findings. The actual terminal installer used the return-1307 candidates and the protected return-review-1310 PASS publication, not the original-1252 candidates. Both canonical delivery files equal the reviewed candidates byte-for-byte and remain regular `0644` files. Required predecessor backups match exactly.

Independent checks passed:

- Fresh readonly checker: `python3 .../return-1307/evidence/check_notes.py` — exit 0; `python3 -m json.tool .../return-1307/evidence/source-manifest.json` — exit 0.
- Current outside inventory: 568 individually recomputed path/hash/size/mode tuples equal both durable before and after maps.
- Installer source/log ordering shows before-map and backup fsync before staging, preimage guard before one guarded `os.replace` loop, directory fsync, readback, and after-map; no silent rewrite.
- Production `delivery-build` calls `render_readme`; function-only controlled four-repository/fallback qualification and SHA `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca` match.

Limitations remain explicit: the installer’s first inventory attempt refused before writes; its initial sampler did not emit a sample. Author and protected-review first-tool/whole-worker sampler gaps remain historical gaps, not monitor PASS claims. No product tests, full suite, build, REG0, final pin, service, or ZIP claim was made.

A fresh checker run reports a different current BOARD-HEADER hash than the installer’s recorded post-CAS checker result, while still passing; this is recorded as temporal control-document drift and does not change the canonical byte/CAS result.
