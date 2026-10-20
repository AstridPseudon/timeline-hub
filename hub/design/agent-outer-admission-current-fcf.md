# Agent outer admission on current ordinary014 Runtime

## Exact source and tuple

- Agent source tree under test: `1c1403b3e1fd930a449d84dec4141f159cc3cf43`.
- Runtime source: commit `fcf4c3d5e9444bf9e221d05aa8fa8d203fb27bd3`.
- Runtime source tree: `69abf4e2a8340d7d39a955d71d08afbf3a311a35`.
- Runtime contains the approved generic producer admission fix from `0113bc7`.
- Agent client metadata was unchanged: contract `0.2.14`, generated schema
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`,
  lock source `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, producer
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`,
  and raw command schema `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

## Change and selector

`tests/packs/video_editing/test_outer_voiceover_native.py` now locates the
Runtime at the exact `fcf4…` commit. The obsolete strict xfail was removed from
the outer admission node only, with a comment identifying the fixed source.
The provenance carrier xfail and all original assembly/two-child controls are
unchanged.

The central Agent suite `outer-admission-current-fcf-sockets-integration` pins
the exact Runtime commit and tree before selecting only:

`tests/packs/video_editing/test_outer_voiceover_native.py::test_outer_admission_records_exact_spec_and_worker_has_no_commit_authority`

It does not select a default file set or any full suite.

## Result

Central test service result:

```text
agt-m2-outer-admission-current-runtime-retry-outer-admission-current-fcf-sockets-integration-1020205949-8620
1 passed in 13.77s
```

The node preserved the exact outer capability identity, admitted target,
ordered script manifest, and successful pinned admission. It also preserved
the worker credential `401` / `unauthorized` refusal and unchanged bootstrap
history/head assertions. No outer execution, settlement, requester success,
inner WAV pair, or other test node was run.

The direct local invocation reached the node but could not open localhost
sockets in the sandbox (`PermissionError: [Errno 1] Operation not permitted`);
the central socket-capable result above is authoritative.
