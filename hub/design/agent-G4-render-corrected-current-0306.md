# Agent G4 corrected-current render publication forward

Merged requester base `d4b212572482c56d974c28ac564e97f0287a7fe6` with dispatcher parent `ecea7d8563c93059283ef9475ecb41a37e628a38` (merge base `2410c3bbbb14f4ca2b177dc894f5eea0246826ee`) by file-only resolution; the dispatcher will record the true two-parent commit. Resolved the three actual content conflicts in `timeline_document.py`, `emitter.py`, and `sync.py` to current G3 parent behavior. Other rejects were already parent-identical. Kept requester render publication sources and the original positive publication test; the six approved V4 live-scenes paths remain absent.

Requester publication controls **13 passed**; render/assembly neighbors **221 passed**; open-commit guards **25 passed**; v2/error/meta neighbors **48 passed**; original integration producer **1 passed**; composition/catalog **10 passed, 1 deselected**; vendor/artifact tests **37 passed**. Scoped Ruff and private mypy passed. Vendor lock and artifact manifest passed. Normal ratchets are Ruff **2149/2149** and mypy **1915/1915**. `git diff --check` and conflict-marker scan are clean.

Current Runtime 780 lock-mapped artifacts are retained byte-for-byte. The known malformed partial-receipt/preview-missing-field adoption issue remains Runtime-peer-owned and was not changed here. No full/browser/farm/render-heavy suite was run.
