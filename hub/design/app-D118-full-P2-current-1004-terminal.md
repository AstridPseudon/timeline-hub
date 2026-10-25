# D118 full P2 terminal

The one authorized normal service reached terminal `FAIL` after 605 seconds. D66 recorded 600.974 seconds from `2026-10-25T10:07:17.640Z` to `2026-10-25T10:17:18.614Z`. Readiness passed 1/1. The original phase was 2 PASS, 2 FAIL, 1 ERROR, and 3 NOTRUN; it exited 1.

Per-gesture first unmet predicates and truthful tail reachability are in `terminal.json`. The two PASS cases were popup ADD and automatic child placement. Element edit failed at the existing dialog-status `applied` assertion; popup SWAP was refused with `history_unavailable`; parent move timed out waiting for the commit response. RegisterAsset and both transition-clear cases were serially NOTRUN after earlier failures.

The exact tuple, source hashes, XML/manifest hashes, and supported profile are recorded in `terminal.json`. The retained Runtime search covered the base phase file, five repeated-start namespaces, all retained stderr/stdout filenames, and the private watchdog stack. Stderr files were empty; no safe D102 reason, class chain, or correlation field was retained. The stack was recorded only as redacted file/line/function facts with one invalid-frame marker. No backend outcome was inferred from client waits.
