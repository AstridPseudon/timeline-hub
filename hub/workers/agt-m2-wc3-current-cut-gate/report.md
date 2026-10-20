Implemented WC3 in `/home/user/work/wt/agt-m2-wc3-current-cut-gate`.

Changes:

- Removed the 226-line legacy `replace_parent_media` writer.
- Routed replacement through `TimelineSession`/outbox.
- Preserved exact media pins, opaque/order/mirror fields, retry guards, and native undo/reload behavior.
- Added donor `593c2fd3` direct and real-HTTP coverage.
- No P1/F1/init/pin/schema/generated-client files changed.

Tests:

- WC3 + sync: **83 passed**
- Parent/occurrence/native neighbors: **91 passed**
- Focused Ruff: **passed**
- Central Runtime 7d HTTP lane: **24 passed, 1 deselected, 2 unrelated publication-chain failures**. WC3 image/video lost-ACK, restart, exact replay, reload, undo/redo cases passed.
- `git diff --check`: **passed**

Remaining consumer: CLI `replace-parent-media` calls the retained public SDK method; no legacy replacement writer remains.

Commit message written to `commit-msg`; `DONE` marker created. Harness should commit this unit. WC3 integration adoption still requires the App same-cohort qualification and owner normal014 release; not claimed complete.