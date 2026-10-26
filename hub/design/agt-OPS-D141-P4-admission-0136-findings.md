# D141c P4 admission findings

Result: `PASS_OPERATIONAL_SOURCE` for the private candidate and offline admission controls.

The candidate is a byte-preserving copy of the canonical `bin/test-run` except for the smallest exact policy branch for `repo=agent`, `suite=p4-current-becfe-http-3legs`. That row is classified as heavy and uses the already recorded 4,700,000,000-byte inclusive exception. It must be heavy, not light: leaving it light would allow it to occupy one of the two light slots while another heavy body runs, defeating the existing one-heavy promise. The finite delta is 500,000,000 bytes between the named 4.7 GB floor and the default heavy 5.2 GB floor.

Unchanged policy:

- `agent-core-full` remains heavy at 4,700,000,000 bytes inclusive.
- Other light suites remain 5,000,000,000 bytes inclusive.
- Other heavy suites remain 5,200,000,000 bytes strict.
- The global hard start guard remains 4,500,000,000 bytes: admission is refused at or below it.
- The 4,000,000,000-byte stop line and one-heavy sequencing remain unchanged.

The source candidate is install-ready only after the required independent review. No canonical kit installation, suite-row installation, service request, production body, live queue mutation, alternate route, or product change was performed.

The existing service `agent-p4-current-becfe-http-3legs-1026012948-19479` was read without requesting it. It remains `queued` with the prior light-floor reason (`available=4885204992`, `floor=5000000000`); no extra request was made.
