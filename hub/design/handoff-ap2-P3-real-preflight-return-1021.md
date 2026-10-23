# Handoff: P3 real preflight return

The P3 row in `tests/suites.conf` was minimally corrected. The existing Node probe asserted resolved exports started with `GRAPH/dist/`, but the qualified package is nested at `GRAPH/@banodoco/timeline-composition/dist/`. The exact prelude was red before the change at that probe and green after the change, with all prior guards and the pinned private graph checks passing.

P3 row SHA-256: `bc94ca8a61bf2ad0f9afbebacbfdff802287793e914597c899e68f0a6b33866f`.

P1 remains byte-identical at `234e7430dd785285ed4faa8ee5ff287555310aedda53b70c0ee5b4e33229418c`; outside-row digest remains `4907fc1a7e1cc6d1679e33b4137e0eb42e97af146cee4fa0f4b112dab28215ae`. No App product/test/helper files changed. No browser/body/service rerun was performed.

