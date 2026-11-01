# Historical provisional receipt — M-T-07 Agent T-07

**Status:** Historical first candidate; this is not current qualification. No merge was requested. Changed-base requalification is pending. This receipt does not claim a green full T-07 phase.

## Candidate and source identity

- Released Agent source SHA: `2beaa36a3bc9e2c689fea9b3b4dd86742ec6b16b` (`refs/remotes/astrid/int/r1`).
- Source-worker tree: `615bf127ccb9f4db87c36b97779cca5209f7af84`.
- Central targeted-test snapshot tree: `14ee10228fe1bdf5adfbe5bd605dd2f80007637a`.

These are distinct identities: the worker report gives the source-worker tree, while the central test receipt explicitly ran against the central snapshot tree. Do not substitute one for the other.

Main's settled merge-base note is authoritative: merge base `710e9c0aae`, with zero source deletions since that base. The earlier 127-path two-dot inventory and 604-conflict empty-base probe are superseded and are not evidence for this receipt.

## Central targeted run

- Request ID: `M-T-07-agent-partial-targeted-1101052301-23468`.
- Request: `target=M-T-07-agent-partial`, `repo=agent`, `suite=targeted`; selectors are recorded verbatim in the central request file.
- Result: **fail, exit 1**; 1,401 passed, 23 failed, 42 deselected, 39 errors, 2 subtests passed, 5 warnings. Runtime: 632.21 seconds.
- Snapshot tree: `14ee10228fe1bdf5adfbe5bd605dd2f80007637a`.
- Recorded command: `/home/user/work/venv-agent/bin/python -m pytest -q` with the selector list in the central request; the complete environment and invocation are in the central summary.
- This was a targeted run, not a full T-07 qualification. No full suite was run.

## External tuple

The triage report identifies the supplied external Runtime SHA as `95d98f038320d5d46bd679ac000ab3e15825c935`. It identifies the candidate's Runtime pin and loaded checkout as `ecc9f1533234d33bfc082b34e1dc4e18a22e3f3d`, which lacks the timeline commit protocol/provider APIs implicated in failures. The approved source reports do not state the external App or Composition SHAs, so those two tuple members cannot be verified from this receipt's allowed source material. Do not treat the candidate's Runtime pin as the external tuple.

## Failure classification

- **Likely Agent regressions (4 failures):** timeline create emits human output under `--json`; two create selectors lack expected `tracks: []`; and import preparation rejects copied media as competing selected media. Triage assigns these to Agent CLI/config construction and compiler copied-media handling. Confidence: **medium-high** for the first three, **medium** for import pending matched-tuple reproduction.
- **Six visualization fake-client failures, now fixed:** four visualization selectors in `test_timeline_route_integration.py` and two in `test_domain_cli_projects_timelines.py` failed because fakes could not pin the published revision required by visualization. These are fixture/client failures, not evidence of six product regressions. Triage records the fix in commit `66719b2c8b`. Confidence: **high** for the classification and recorded fix; this historical test run predates it.
- **Relocated-skill assertion (1 failure):** `test_video_editing_canonical_doc_route_survives_view_composition` still expected the rendering-skill path after docs moved to the timeline skill. This is an outdated Agent test expectation. Confidence: **high**.
- **Runtime / tuple API gaps (11 failures plus related errors):** tests pass `authoring_profile` to a `RuntimeDaemon` that does not accept it; tests cannot import `runtime_protocol.timeline_commit`; and `RuntimeService` lacks `register_timeline_commit_provider`. Triage ties these to the loaded Runtime `ecc9f153...` rather than external Runtime `95d98f...`. The corresponding errors include test setup importing Runtime from the checkout instead of the temporary archive. Owner confidence: **high** for tuple/setup mismatch; the intended matched tuple still needs requalification.
- **Unresolved concurrency race (1 failure):** `test_concurrent_installs_keep_both_selections` observed a `skills sync` subprocess exit 1 with empty stderr. The receipt cannot determine whether this is product behavior or environment timing. Owner attribution remains **low confidence**; investigate before classifying.

The triage classifies remaining Runtime fixture/setup errors separately from product regressions. The counts above describe failure groups, not additional failures beyond the central run totals.

## Decision and next step

No merge was requested. Changed-base requalification remains pending. Re-run the relevant targeted selectors against the intended matched Runtime/App/Composition tuple; separately investigate the unresolved concurrency race. Preserve the historical distinction between likely Agent regressions, the fixed fake-client cases, the relocated-skill assertion, and Runtime/tuple API/setup gaps.
