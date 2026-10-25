# Runtime P2 SWAP tags handback

The `369ffa` Runtime tree now emits one bounded private D102c-style reason tag for intentional `history_unavailable` refusals observed at the coordinator/service boundary. Public response envelopes, status, history/authentication guards, and write behavior are unchanged. Tags cover baseline integrity subtypes, known port refusal messages, and a fixed provider/store guard fallback. Catch-all exception diagnostics remain catch-all and do not get relabeled.

`timeline_commit_store.py` and `timeline_commit_port.py` were not edited because Sol owns those live files. Their direct branch-level labels are listed as a ready handoff in the worker evidence; the current boundary tag is intentionally the minimal safe change until that ownership transfers.

The exact App-15203 native replay is not claimed. The central allow-list exposed only the existing D83 native seed control, which passed 8 tests with 1 deselected. The retained D112 native harness and exact recorded App request sequence are not an allow-listed suite for this worker, and no synthetic request/history or guessed hash was used.

Focused diagnostics passed, protected D102c controls passed, compilation and diff-check passed. No browser, full, original App, or P4 suite was run.
