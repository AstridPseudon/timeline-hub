# Runtime capture integrated gates

Date: 2026-10-20

## Result

The requested Runtime capture gate `0a04782e9a5c5420b2d506d393cd79d8d5b47418`
was merged into Runtime `tl/integration` as `27ad20bf45f7840c26dfefc69f32d52222abc33a`.
The immutable service snapshot used for all three requested runs was Runtime
tree `129f4abe2be034341afb400e341b611ed3955010`, the tree of that merge.

The approved capture product source is byte-for-byte/hash-for-hash present:

```text
runtime_protocol/capture_validation.py
SHA256 572d4c8ec61e2705ce56aa3d5733b500c64ba06b9e5addca885bd457388f6b75
```

The actual Agent source pair was the persistent archive of Agent
`cf7448ed6c1298b172d004914cfe2bb8c99048e7`, tree
`c8a5e0cb320095129e9a1be125295dfa7adc2793`:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m3-capture-actual-agent-current-pair/agent-source
```

## Service evidence

All requests targeted `integration:runtime` and used the
`capture-agentcf7448-integration` suite, whose source environment loads the
archive above. The exact requested selections passed on the same snapshot:

| Selection | Request | Result |
| --- | --- | --- |
| Candidate | `runtime-capture-agentcf7448-integration-1020115606-12279` | 141 passed |
| Claim/aliases | `runtime-capture-agentcf7448-integration-1020115606-12522` | 25 passed |
| Commit integration | `runtime-commit-integration-1020115606-11082` | 9 passed |

The candidate selection was `tests/test_capture_candidate_binding.py` plus
the four specified candidate cases in `tests/test_capture_candidate_actual.py`.
The claim selection was `tests/test_capture_claim_identity.py` plus the three
specified alias/outer-context cases in that same actual-candidate module.
The commit selection was the named `commit-integration` suite.

## Published-base audit

Compared with published Runtime `2c4ac180`, the complete diff is six paths:

```text
runtime_protocol/capture_validation.py
tests/test_capture_candidate_actual.py
tests/test_capture_candidate_binding.py
tests/test_capture_claim_identity.py
tests/test_timeline_media_completion_fence.py
tests/test_timeline_verified_media.py
```

The last two test paths are the already-merged media-completion-fence parent
unit (`57d0f32`), not this capture gate. Excluding tests, the only changed path
from `2c4ac180` is `runtime_protocol/capture_validation.py`. `contract/`,
`packages/`, all other `runtime_protocol/` files, and the remaining Runtime
product surfaces were byte-identical to published `2c4ac180`.

After the service snapshot was taken, the integration server advanced to
`a51267ec` with an unrelated text-clear custody unit. That later change was
not included in, or silently mixed into, the three gate results; the results
remain pinned to tree `129f4abe` as required.

## Findings and boundaries

No new finding was found in the requested capture gates, so no product fix or
test relabeling was made. The prior actual-Agent report's external caller gaps
remain open and are not relabeled green: four host assertions still encounter
the missing `RenderRequest.verified_source` attribute, and the separate SDK
invocation guard requirement remains open. Those are outside this Runtime
integration gate. No full, broad, renderer, browser, or live-socket suite was
run.
