# F-D22 independent terminal census review

## Decision

**FAIL for the classification handoff; inventory completeness is PASS separately.**

The retained service itself is terminal **FAIL** (exit 1). The 204-node
inventory and the run identity/counts are exact, but the submitted
classification overstates the profile-fixture non-regression conclusion and
has mixed 11 direct process/custody assertion failures into the
`child-import-or-recipe` bucket. No product, test, schema, pin, dependency, or
runner files were changed.

## Run identity and counts

Reviewed:

- branch `tl/agt-F-D22-terminal-classify-1442`, comparison/base commit
  `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`;
- actual service snapshot commit `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`,
  tree `c4d72b065d6e68c92e4335120cc016cadf53b06a`;
- Runtime commit `3b926efab2eed122d374540baee297d4cdcec62a`;
- profile `agent-remotion-v3-819acf-1110`, archive hash beginning
  `819acf6b3815...`, composition version `0.0.14`;
- service `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679`.

The comparison/base `58316...` is not the tested snapshot `8c355...`; no
result is relabelled as a Base583 result.

The retained summary and raw log agree on:

| result | count |
| --- | ---: |
| failed | 185 |
| errors | 19 |
| passed | 16,733 |
| skipped | 4 |
| passed subtests | 565 |
| warnings | 86 |
| xfail/xpass/deselected | 0 / 0 / 0 |
| elapsed | 3712.16 s (1:01:52) |
| exit | 1 |

The JSON inventory has 204 entries, all unique, with 185 `FAILED` and 19
`ERROR` IDs. Every inventory ID is present in the terminal summary after
normalizing one pytest summary line that appends ` - ...` to
`test_no_audio_wire_parity`; the JSON and traceback retain the exact ID. The
marker arithmetic is `16,733 + 185 + 19 + 4 + 565 = 17,506`, so `u` is the
summary's 565 passed subtests, not an unknown or missing outcome.

The raw log SHA-256 is
`e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.
The retained summary/status/exit/request/snap/ext files match the companion
hashes in the submitted JSON inventory.

## Classification audit

I sampled the first, middle, and last node of every group against the full
retained traceback, and checked the group-wide outlier patterns. The bounded
trace evidence supports these observations:

| group | nodes | trace evidence | review |
| --- | ---: | --- | --- |
| `child-probe` | 17 | probe/child launch failures, including `original_wait_exit_code=1` | bounded unconfirmed probe/environment claim supported |
| `child-import-or-recipe` | 97 | 86 show `runtime_protocol` import failure or missing child `sdk/result.json` | 11 are not supported by this source claim; see below |
| `fixture-declared-gap` | 2 | `audio.render_source` is `None`; fixture explicitly describes the prepared-envelope gap | bounded unconfirmed fixture-gap claim supported; not D14/D23 |
| `g5-inverse` | 23 | history unavailable / authenticated physical binding and one ambiguous successor | source-backed failure routing is supported; new-regression status remains unproven |
| `profile-fixture` | 38 | 37 profile/fixture mismatches; one `runtime_protocol` child import | non-regression status is not proven; one node is misbucketed |
| `child-import` | 9 | direct `No module named 'astrid'` from isolated children | bounded unconfirmed child-import claim supported |
| `d13-preflight` | 1 | required D13 environment/binding variables absent | bounded environment claim supported |
| `r1-private` | 7 | authority/capture assertion failures, missing expected rejection, or `inverse_conflict` vs `intervening_write` | source-backed routing supported; no preexisting/upstream credit proven |
| `g5-publisher` | 2 | forbidden archive/history surface and missing `fetch_bundle` helper | source/test contract-mismatch claim supported |
| `g5-schema` | 2 | `timeline.duplicate` and `occurrence.place-shared` differ from asserted union | source/test schema-mismatch claim supported |
| `r3-docs` | 1 | `commit.py` missing from `giant-file-rationale.md` | bounded docs claim supported |
| `d09-probe` | 3 | `RemotionValidationError` with `original_wait_exit_code=1` | bounded unconfirmed probe claim supported |
| `r5-retired-route` | 2 | Runtime raises `RetiredRouteError` for the legacy route | current contract mismatch supported; no upstream claim made |

### Classification defects

These 11 IDs are in `child-import-or-recipe`, but their retained trace is a
direct assertion/process or environment-context mismatch, not an import or
missing-result-file failure. They must remain unconfirmed or be split into a
separate source-backed group until an owner establishes causality:

```text
tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[command]
tests/core/execution/test_custody_broker.py::test_isolated_wrapper_target_restores_network_hook_and_original_environment[engine]
tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-False]
tests/core/execution/test_generic_host_actions_v3.py::test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift[True-True]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-False]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[False-True]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-False]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_waits_for_real_original_attempt_release[True-True]
tests/core/execution/test_generic_host_actions_v3.py::test_cpu_shutdown_cannot_close_unproved_real_attempt[observation]
tests/core/rendering/test_installed_registry_security.py::test_installed_native_readiness_context_must_match_projected_context
tests/core/rendering/test_installed_registry_security.py::test_installed_actual_worker_environment_matches_launch_projection[command]
```

Their observed failures include `denied=False` instead of `True`, no observed
managed process, missing `shutdown-entered`/`uncertain-shutdown-entered`, and
an unexpected `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` in the registry context
(raw log around lines 2027, 13031, 13278, 14824, and 14923).

The 38-node profile group is also not a proven non-regression group. Thirty-
seven nodes do have bounded fixture/profile evidence: 14 assert archive
contents length 77 but observe 80, 9 expect composition `0.0.13` but observe
`0.0.14`, 11 cannot find `chunk-SE4TPVLW.js`, and 3 report unmapped generated
scopes. Those facts prove a mismatch in this run, not that it predates the
tested snapshot or cannot be a product regression. The remaining node,
`tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root`, fails with a
`runtime_protocol` import error and should not be in `profile-fixture`.

## Skips and deferred credit

The four skipped IDs are unavailable. I searched the retained D22 worker,
service, queue, log, xdist, and registry artifacts read-only; only the count
and final summary were retained. No exact skip identity can be recovered
without a new run, so qualification remains missing rather than inferred.

There are no retained xfail/xpass or deselection lines. Exact D14 and D23
nodes do not occur in this log. Neither is credited as passed, deferred, or
cleared. No upstream/preexisting credit is inferred from this run; owner names
in the submitted handoff are routing information only.

## Commands and limitations

No test command, targeted suite, full suite, browser, service, benchmark,
provisioning, or source type/lint command was run by this review. The reviewed
service's retained test invocation was exactly `pytest -q -n 3`, and its result
was the terminal FAIL recorded above. Review work used read-only artifact
inspection and parsing only.

Recommended next step: correct the two classification defects above and
retain per-node skip reporting (for example, a verbose skip report) on the
next authorized qualification run. Do not use this service as evidence for
Base583 behavior or as proof that the 37 profile-mismatch nodes are
pre-existing.
