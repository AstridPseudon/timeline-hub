# Runtime ordered observer serialization repair — diagnosis report

Date: 2026-10-21 UTC

## Result

The test-only observer was corrected and the one authorized central diagnostic
run completed. The original proof still fails at the unchanged inverse guard;
the observer no longer masks the function or assumes that return values are
JSON serializable.

Central result:

- Result ID: `rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618`
- Suite: `private017-agent6c-integration`
- Selector: `tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo`
- Command: `env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo`
- Result: **1 failed in 1.83s**, at the original inverse call with `RuntimeErrorBase: media inverse records differ from accepted history`.

The earlier `18808` result remains failed and is retained as a diagnostic setup
failure only: its observer attempted to serialize the original empty-call
return `set()` and Runtime wrapped that observer error. It never reached the
real inverse and is not evidence for Runtime or Agent product behavior.

The full exact JSON call capture, including entry snapshots, compared lists,
origins, hashes, and outcome metadata, is in
`runtime-ordered-inverse-operands-diagnosis-1105.md`.

## Captured boundary

There were three calls. Calls 0 and 1 were ordinary pre-inverse calls with
empty records and returned the original `set()` unchanged. Call 2 reached the
real inverse after restart and raised the original `CommandError` unchanged.

First difference between the exact compared command lists:

```json
{
  "kind": "presence",
  "path": "$[0][\"writes\"][1][\"before\"][\"value\"][\"gone\"]",
  "left": "present",
  "right": "absent"
}
```

At that path, the accepted-record operand contains
`{"state":"present","value":{"gone":null}}`; the accepted-history
operand contains `{"state":"present","value":{}}`. Both values are
objects; this is a member-presence difference, not a type or list-order
difference. The exact `insertion_order` list is equal on both sides:
`["a-before", "com.example.compiler-canary", "z-after"]`.

Call-2 source hashes:

- records argument list: `sha256:5da5f1a12f1ee1a31569868e900957dc261b6372738026fe2d85ca30a37c4336`
- entries snapshot: `sha256:29df32a87a1d0f84a9674172d5d6c3ae55d1d7945f15fea2eab3de685097e80e`

## Ownership and smallest correction

This is evidence for a Runtime history-carrier/persistence correction: the
accepted `records` reconstruction retains the removed namespace member, while
the exact accepted-history entry loaded after restart has already lost it.
The Agent guard correctly refuses unequal operands. Runtime should preserve
the complete recorded `before.value` object when carrying the accepted history
entry across serialization/reload, including the `gone: null` member. No
guard exemption, normalization, assertion change, Agent edit, artifact, lock,
or product behavior change is justified by this run.

## Controls and preflight

- Direct observer controls passed: empty input returned the same `set()`;
  deliberately mismatched real `AcceptedRecords` raised the same
  `CommandError` and retained both operands; JSON output parsed; call numbers
  were `0,1`.
- Runtime source: `36736b0636ad9944a58e8fb58de99b71c6b9a70f`, tree
  `30ba5d0ac57f84c80d956938231f08f1b0f6cded`.
- Agent source: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`, clean.
- Runtime artifact manifest: 76 entries, version
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Agent lock: 15 entries; all consumer bytes matched the Runtime manifest;
  source commit remained `42a7203f49bb89f299ec854cfbf2b1444e815a7c`.
- Imports resolved to this Runtime worktree and Agent6c; Astrid provider
  loaded successfully. One selector collected; setup plan resolved the
  expected `tmp_path`, `film`, `monkeypatch`, `astrid_importable`, and
  `agent` fixtures. Private temp and disk checks passed with 10,910,684 KiB
  available.
- No full, RT03, old44/186, HTTP, socket, browser, render, materialization,
  generation, pin, or second diagnostic run was performed.

