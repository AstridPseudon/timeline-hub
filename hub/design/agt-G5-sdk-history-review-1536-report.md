# G5 SDK history-port fidelity review

Source-fidelity **PASS** for the two scoped test files; four Runtime behaviors are **PENDING** the explicit join of CLI source `cc8be25d4ad46fae3f7d0889aaee88f85ab6a9c6` (`tl/agt-G5-cli-durable-undo-sol-1515`).

Original `58316fd6e0ce8a1fb3b2b3826ec71906d29080de` vs draft `f57d283d2d4946bbb09d7b68da89422f2d3bfd77`: identical scenarios and assertions (boundaries 4/16; Runtime 4/42); only the intended `_commit_document` seam migration. Port `cd9405a46f64dd7a48675da7c4589373f19f6a28` preserves all of them, changes only `--publication`→`--commit`, and uses the verified `(stored, message, *, idempotency_key, client)` seam without fabricated auth/history/cache.

Evidence: boundary pytest **9 passed**; compile **PASS**; integration collection **4 named nodes**; central targeted port result **9 passed, 4 deselected**; diff check **PASS**. The four node names and the exact post-join `-m integration` command are in the worker report. Live bodies were not run before source join because the current branch still lacks the `--commit` interface. No source fix or tracked report was added.
