# F D141y — Main source-only rehearsal

Result: **REFUSED_ALL_REPO_PREFLIGHT** (CLI exit 2). The existing canonical delivery-build CLI ran once on all four exact receipted heads. App was refused because pinned `4de54db1…` is not descended from fresh `origin/main` `fc24f849…`. The CLI stopped before any actual build, patch, bundle, apply verification, staging, ZIP, or publication.

All four actual build counts are **NOT_REACHED**. Prospective Git diff statistics are separately labelled in `results.json`. Source heads stayed exact and clean; script/template/gate hashes stayed unchanged. Tests/typecheck/lint were NOTRUN by design.

Raw command streams and exit are retained privately. The disk trace stayed above the 4 GB stop line and was reaped after evidence finalization.
