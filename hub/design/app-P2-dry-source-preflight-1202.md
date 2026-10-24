## Completed

- Added `caller-dry-preflight.py`.
- Updated `caller-publication.py` to:
  - derive App/Agent/Runtime identities from approved checkouts;
  - run the actual decoded/wrapped P2 identity guard first;
  - preserve historical Remotion producer `079…` and P3 unchanged;
  - record dry-preflight results and source facts.
- Updated `caller-custody.json` with current hashes and preflight evidence.

Approved identities: App `d6ed…` / tree `542b…`; Agent `333b…` / tree `1094…`; Runtime `37eb…` / tree `be411…`; Remotion tree `b01d…`, producer `079…`.

## Verification

- Preparation: `TMPDIR=/tmp/timeline-app-p2-dry-preflight-1202 python caller-publication.py` — PASS.
- Dry guard: PASS in `9.158s`; result recorded in `/tmp/timeline-app-p2-dry-preflight-1202/prepared.json`.
- Candidate hash: `6a45d0567f7dea7a3c15fbcaf687f9dd62debf4527464529d8a4faf8f8e48fee`.
- Negative identity matrix — all refused: wrong source, body, registry, target, receipt, parent, delta, Remotion producer, component tree.
- Python compile, JSON parse, wrapped/decoded `bash -n`, and `git diff --check` — PASS.
- Full/browser suites were not run.

No blockers. Commit message and `DONE` marker were written as required.