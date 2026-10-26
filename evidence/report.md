# F-final launcher whole-path continuation

Status: finite independent READONLY continuation complete. No source, tuple,
registry, installer, builder, service, or product file was changed.

The actual `0495919f...` registry still has the pre-fix launcher: its final and
dry-run rows execute the hash-checked caller without adding the caller parent to
`sys.path`. The unchanged caller imports `delivery_lifecycle` at line 23, so
both delivery rows retain the known ordinary startup failure before lifecycle,
D68, or builder entry.

The current source11 successor at
`rt-F-D141jj-base-fix-next/evidence/candidate` repairs the prior dry-run argv
shape but also drops the required import setup from both delivery rows. The
earlier 1719 private successor had the import setup, but its dry-run row lost
`--wrapper-sha`, `--builder`, `--builder-sha`, and `--receipt`, and pointed
`--wrapper` at `delivery-v2-receipt.json`. Those are the complete intrinsic
row defects found in this continuation.

The actual immutable installer CLI has an additional source-candidate defect:
it pins registry SHA `7b1ffdd7...`, while the actual read-only registry is
`0495919f...`. The exact no-install CLI therefore fails at predecessor
preimage validation. If that preimage were corrected, the same CLI would next
reach `install()` and refuse because the candidate already materializes its own
`final-source-tuple.json` and `final-gate-tuple.json`; the private CAS control
avoids that by monkeypatching those paths and is not production CLI evidence.

No builder, dry-run, clone, service, collection, or repeated lifecycle control
was run. No production-readiness or final semantic-review claim is made.
