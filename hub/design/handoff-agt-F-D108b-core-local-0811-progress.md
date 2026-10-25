# F-D108b local Agent core progress

Submitted one named heavy `agent-core-full` request through the existing test
service at `2026-10-25T08:17:08Z`.

- Service ID: `agt-F-D108b-core-local-0811-agent-core-full-1025081708-25132`
- Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-F-D108b-core-local-0811-agent-core-full-1025081708-25132`
- Request: `bin/request-test agt-F-D108b-core-local-0811 agent-core-full --no-cache`
- Suite admission: named `agent-core-full` is recognized as heavy by the existing runner.
- Tuple: Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` / tree `6056414359ae9fce08d999d54cbecf719fda33c3`; Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19` / tree `a522511414947e48e317a5e5c2103483b121a750`; App `04beedcd18b8abb49502f65cd3facaafbe93db4e` / tree `300d186a45d3d0b96ef2ae39582f1e9b4a760e7d`; Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- Controls before submission: parsed-row `bash -n=0`; genuine positive launcher control exit `17` with exactly one stub call; poison control exit `1` with zero stub calls.
- Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D108b-core-local-0811/evidence/`

Terminal outcome and D63/upstream-924 classification will be appended after
short-polling the existing service. No product or test source files were
changed.

The zero-body setup fix was installed via the existing CAS/backup/atomic
mechanism and parsed-row `bash -n` passed again. The retained evidence
manifest is byte-identical to the private input manifest at
`/tmp/w-f749cb78cc/agent-core-full-input.manifest`; only the launcher input
path changed.

Retry service ID: `agt-F-D108b-core-local-0811-agent-core-full-1025081835-2016`

Retry result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-F-D108b-core-local-0811-agent-core-full-1025081835-2016`

While the admitted body is running, available space reached
`5,183,291,392` bytes at `2026-10-25T08:20Z`, below the 5,200,000,000-byte
heavy admission floor. The run is left untouched; no shared bytes were
recycled or modified.

## Setup retry

The first request terminated before pytest with exit 1 because the launcher
attempted to copy `agent-core-full.manifest` from and to the same evidence
path. The log records the exact `cp: ... are the same file` diagnostic; no
pytest body was started. The same manifest bytes are retained in evidence,
and the registered command is being corrected to use a private input path
outside the evidence directory before the single allowed zero-body retry.

At `2026-10-25T08:21Z`, available space was `5,042,421,760` bytes while the
retry body continued and its log was growing. This is the latest exact
below-floor figure reported to the manager; no recycling, cache deletion, or
interruption was performed.

## Terminal

Retry terminal status is `fail`, exit `1`, after `1456s` / `24:11`:

```text
159 failed, 8763 passed, 86 warnings, 347 errors, 173 subtests passed
```

The JUnit XML, body log, manifest, complete outcomes TSV/JSON, and terminal
report are retained under the worker evidence/design paths. XML SHA-256 is
`72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a`.
Coverage is 9269 unique nodes over all 22 roots, with explicit outcomes and
no absent-case PASS. Existing D63/upstream-924 matching produced 2940 same
status, 15 different status/cause, and 6311 current-only unclassified nodes;
D13_ENV and D23_DEFERRED boundaries remain preserved, and no numeric core-open
or independent NO-GO verdict was issued.
