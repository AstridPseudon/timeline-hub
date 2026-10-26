# D141jj independent review findings

- **FAIL F1 — stale source manifest:** `source-manifest.json` records `receiving_controls.py` as `a5d20f98d80c066179e65e7368735c89e09da136a36da0098737431dc2dff08a`; the candidate file observed by review is `fd8c1a24fac14d8690a24e9810e1e20888ea1cd4c5ddc6ae229de69851a54be0`. This is an identity-closure failure even though the diff is only one blank line.
- **FAIL F2 — gate/source root mismatch is accepted:** `run-final-delivery.py:67-145` validates the two tuples independently but never compares their roots, while `delivery_gate_build.py:234-243` stages from gate roots. The positive fixture uses identical roots and no mismatch refusal exists.
- **FAIL F3 — non-App current-upstream binding is incomplete:** `delivery_gate_build.py:213-223` reads current `origin/main` and only checks the recorded object is self-consistent; it does not require current `origin/main` to equal each non-App gate tuple `upstream_base` before applying the delta.
- **FAIL F4 — owner/mode refusal is incomplete:** `run-final-delivery.py:81-99`, `delivery_gate_build.py:187-193`, and `delivery_gate_build.py:390-393` check directory/non-symlink status but not owner or permission mode at source/stage boundaries.
- **NOT QUALIFIED N1 — lifecycle evidence:** the required `candidate/check.sh` run stopped at `caller-parent-death` on the enforced `4,960,000,000`-byte pre-stage guard after available space reached `4,959,588,352`; no bypass or retry under a lower threshold was made.
- **DEFERRED D1:** genuine dispatcher admission, Agent REG0, D141v successor applicability, and final build/install/activation remain explicitly outside this source-only task.

