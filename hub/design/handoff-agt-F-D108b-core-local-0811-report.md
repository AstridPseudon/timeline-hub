# F-D108b Agent core-full report

## Result

One meaningful `agent-core-full` body ran through the central service on the
exact pinned tuple. The retry terminal result was `FAIL`, exit `1`, after
`1456s` / `24:11`:

```text
159 failed, 8763 passed, 86 warnings, 347 errors, 173 subtests passed
```

The retained JUnit XML is
`workers/agt-F-D108b-core-local-0811/evidence/agent-core-full.xml`,
SHA-256 `72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a`.
The service body log and stdout/stderr capture are retained at
`workers/agt-F-D108b-core-local-0811/evidence/agent-core-full.body.log`.

## Exact execution

- First request: `agt-F-D108b-core-local-0811-agent-core-full-1025081708-25132`.
  It failed before pytest because the launcher copied a manifest from and to
  the same evidence path. The log records the exact same-file `cp` error;
  this was a zero-body setup failure.
- Retry: `agt-F-D108b-core-local-0811-agent-core-full-1025081835-2016`.
- Request command: `bin/request-test agt-F-D108b-core-local-0811 agent-core-full --no-cache`.
- Published argv used the unfiltered 22-root command with
  `-m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45`, including
  `tests/packs/rendering/test_live_scene_composition.py`.
- Retry preflight exited `0`; body exited `1`. No marker filter, skip, or
  reduced scope was used.

## Controls and custody

- Parsed registered row: `bash -n` exit `0`.
- Positive control: exit `17`, exactly one stub call.
- Poison control: exit `1`, zero stub calls.
- CAS/backup/atomic suite registration passed; outside bytes were preserved.
- Agent source: `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, tree
  `6056414359ae9fce08d999d54cbecf719fda33c3`.
- Runtime source: `1daca2a33f6d7b10053e07c539a54843e3984e19`, tree
  `a522511414947e48e317a5e5c2103483b121a750`.
- App source: `04beedcd18b8abb49502f65cd3facaafbe93db4e`, tree
  `300d186a45d3d0b96ef2ae39582f1e9b4a760e7d`.
- Composition source: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree
  `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- Genuine profile, Node `v20.19.4`, schema digest, registry digest, and
  composition `0.0.14` are recorded in the manifest and provider-origin log.
- `476` original selector source files were hashed; import origins and runtime
  provider paths were recorded before submission.

## Coverage and classification

The XML contains `9269` unique testcase nodes across all 22 selector roots;
all nodes have an explicit outcome and no absent case was marked PASS. The
published outcomes files contain every node, outcome, failure type/location,
failure-text hash, source hash, upstream match, and classification:

- `handoff-agt-F-D108b-core-local-0811-outcomes.tsv`
- `handoff-agt-F-D108b-core-local-0811-outcomes.json`

Existing D63/upstream-924 matching was used without an independent NO-GO or
numeric core-open verdict:

- `2940` exact upstream-924 matches with the same status.
- `15` exact matches with a different current status/cause; these remain
  different-cause/result classifications, not pre-existing or regressions.
- `6311` current nodes have no exact upstream selector and remain explicitly
  `UNCLASSIFIED_NO_UPSTREAM_EXACT_NODE`.
- Existing boundary identities remain `D13_ENV` (1 node) and `D23_DEFERRED`
  (2 nodes); approved dead-scope assignments remain zero.
- Upstream-924 reference remains the existing `294156...4657f` XML with its
  documented runtime-isolation uncertainty.

## Next step

Use the published outcomes and XML for manager/D63 review of the 159 failures
and 347 errors. Do not infer a core-open count or regression closure from this
report alone; the 6311 current-only nodes require the existing classification
workflow.
