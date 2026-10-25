# D89a/D118 Agent core full handoff

Status: terminal FAIL after the one permitted complete body. No product or Composition worktree files were changed.

## Admission and controls

- Corrected only the named `agent-core-full` admission rule in `bin/test-run`: 4,700,000,000 bytes inclusive for this suite; default heavy remains strictly above 5,200,000,000; light remains inclusive at 5,000,000,000. Installed hash/mode: `0be17b74ad1e324bc84e50e61e50e3e07390b262b7abe17a37ad22b9bd10d0fe`, mode 755.
- Exact preimage hash: `5df4145dfb972a0470f20a1959b470f6b17aa68d02c6478da22ed3fadbd922ea`; backup: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/archive-v1/test-run-pre-D89a-1024`.
- Eight offline controls passed before installation, after installation, and after retry: named floor, named below floor, light floor, other-heavy floor/above-floor, invalid `df`, and reciprocal busy cases. No central body was invoked by controls.
- The registered row was updated atomically to the captured test-only tuple. Final row hash: `b4753881a2f4efc6770b78d205a321005f124c46ab5e07cb46ed34e4bf97540c`; `bash -n` passed.
- Positive/poison launcher controls passed: preflight 0; positive body 17 exactly once; poison body 19 with zero body invocation.

## Tuple and run

Captured once through the normal checkout mechanism:

`Agent 120d71202a9ebafa99011aec417cfca6d67fafc2` / tree `9a65a32e4462464825df6cfe4d913408694ad4c5`; Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19`; App `96d4754b4eef0591a208d6b51b60c30fc44b6915`; Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.

Profile/provider remained `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`, Node `v20.19.4`, lock `f4fc0a32...e330be18`, registry `d609b44...adaac96`, schema `867f355...1708b`, composition version `0.0.14`.

The first request (`agent-agent-core-full-1025102221-15065`) was refused during setup with zero body because the manifest source and evidence destination were identical. The same prepared WIP was corrected to use `/tmp/w-e4e38edaae/agent-core-full-input.manifest`; no meaningful body was repeated. The corrected request was submitted with:

```text
bin/request-test integration:agent agent-core-full --no-cache
```

Service ID: `agent-agent-core-full-1025102421-30693`. The exact expanded 22-root command used `-m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45` with no marker filters or reduced scope.

Terminal result: `159 failed, 8823 passed, 86 warnings, 291 errors, 173 subtests passed in 1558.79s (0:25:58)`, exit 1. JUnit XML SHA-256: `483e5c13c3443147488da436acc49d0c0f322f7e4d3f020fbd656a548459139c`; it contains 9,273 testcase elements, 9,446 declared tests, 159 failures, 291 errors, and no skipped tests. All 22 command roots are represented; no absent-case PASS claim is made.

Free space stayed above the 4,000,000,000-byte stop line (lowest recorded monitor value 4,886,441,984 bytes); no disk-stop request was issued.

## Classification and artifacts

Per the settled rule, classification was performed after terminal completion using exact-node matches to the existing D63/upstream924 artifacts. D13_ENV and D23_DEFERRED assignments were preserved; current-only nodes remain unclassified. No independent numeric core or NO-GO verdict is made.

Durable outputs:

- `handoff-agt-F-D118-core-D89a-1024-manifest.json`
- `handoff-agt-F-D118-core-D89a-1024-outcomes.tsv`
- `handoff-agt-F-D118-core-D89a-1024-outcomes.json`
- `workers/agt-F-D118-core-D89a-1024/evidence/agent-core-full-terminal.xml`
- `workers/agt-F-D118-core-D89a-1024/evidence/service-30693.*`

The composition worktree remains clean; no local pytest/full suite was run outside the central test service.
