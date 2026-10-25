# F-D86 actual Agent home receipt

Status: `SOURCEQUALIFIED / BEHAVIOR PENDING`.

## Actual integrated home

The current clean Agent home is:

- commit `d6294843286c18e57af3c1874cf1996be42212d2`
- tree `6aeae30f0892a424104a4348bca6fd74ba1315d6`
- parents `5554fe792bba5ed17c90e0a1ccf46f4d5df19601` and
  `38c419a54672020f9f9b0bfa0903cab4d9185c3e`
- subject `Merge tl/agt-U4a-D102c-adopt-0625`

The captured base is `5554fe792bba5ed17c90e0a1ccf46f4d5df19601` (tree
`d68a366224e28ee58045805008be092a5a560944`). The actual home diff is exactly
one path: `runtime.lock.json`. The worktree is clean.

## Normal adoption

`runtime.lock.json` now pins Runtime source commit
`1daca2a33f6d7b10053e07c539a54843e3984e19`. Its immutable producer receipt is
`queue/done/checkout-runtime-1daca2a33f6d7b10053e07c539a54843e3984e19`,
pointing to clean detached checkout `/home/user/work/wt/rt-pin-1daca2a3`:

- producer commit: `1daca2a33f6d7b10053e07c539a54843e3984e19`
- producer tree: `a522511414947e48e317a5e5c2103483b121a750`
- reviewed tree: `ab7ebb4244a40d27ccf9faf56a7916f72fa8765f`
- producer version: `sha256:084f3f2510edff28c18d33aac4a459f8aa6df3cb4fd71cba4fb292274ea8ade5`

All 15 lock entries match both their current Agent consumer and the exact
producer artifact. The canonical schema, runtime config, generated client,
commit types, provider, commit session, and v2 validation test are unchanged
from the captured base. The reviewed source mirror is commit
`5e9acf59d266d45d74e5ae844bf62fddb64267f3`, tree
`d68a366224e28ee58045805008be092a5a560944`; protected review
`agt-F-word-mirror-review-0620` is `PASS_SOURCE`.

## Finalized branches

The actual finalized branches, distinguished from their older candidate
handoffs, are:

| branch | commit | tree | parent | lock source |
| --- | --- | --- | --- | --- |
| D100 rebind | `dd2fc40d94e35f93b3428210b58e8d58b3156a4a` | `757e848ddb62c06a800588167448ee324dd9cd1d` | `8d43cc7c6c2c339656bb494ee45791d13f9a1104` | `1daca2a33f6d7b10053e07c539a54843e3984e19` |
| R2/word rebind | `44cfb2884e9ee918ba3ea19e354aeba31dfd2347` | `5d6d1b0f128cc355c5ffa6b85efa3732c4dd6243` | `ea57362992e03919651b2f28936b245d9596d279` | `1daca2a33f6d7b10053e07c539a54843e3984e19` |

Both finalized lock files have SHA-256
`cc204fa670f8895f4c1f57d99b35c596e4d0b9e64c4de81d8f19d43cf03b19db`.
Reviewed product/test hashes were preserved: D100’s four files are
`_command_state.py`, `capture.py`, `test_capture_move_exact_time.py`, and
`test_sequential_shared_item_provenance.py`; R2/word’s four are `_step_undo.py`,
`test_timeline_restore_effect_order_runtime.py`, `native_word_anchor.py`, and
`_commit_timing_validation.py`. Exact hashes are in the JSON receipt and the
evidence file.

The older D100 and R2/word handoffs remain metadata-limited historical records:
both say `HELD_SOURCE_ONLY`; D100 points to precommit `8d43cc…`, while R2/word
points to precommit `ea5736…` and explicitly says `working_tree_only=true`.
Those labels do not describe the finalized branch commits above.

## Caller and contract scope

Static trace remains `TimelineSession.commit` → registered timeline client
`commit_timeline` → generated `commitTimeline` route →
`create_runtime_commit_service`. The strict production caller is unchanged.
The C0 request/reply shapes and all original inputs, topology, opaque values,
assertions, refusal/retry, inverse, ABA, and no-write guards are unchanged by
the lock-only home diff. No policy or authority changed.

## Checks and limitations

Rerun read-only checks:

```text
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-1daca2a3
PASS: ok runtime.lock.json (matches producer manifest)

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
PASS: artifacts.json is current

git diff --check
PASS

python3 -m json.tool handoff-agt-U4a-D102c-home-0647.json
PASS
```

The prior author report exists at
`workers/agt-U4a-D102c-adopt-0625/report.md`; its requested JSON output and
its own evidence directory are absent. This receipt states that absence
truthfully. No pytest, collection, helper/fixture/function execution, probe,
service, browser, render, install, refresh/update mutation, or full suite was
run. Behavioral proof remains unverified.

Detailed lock rows and branch hashes are in
`handoff-agt-U4a-D102c-home-0647.json`; read-only command evidence is in
`workers/agt-U4a-D102c-home-receipt-0647/evidence/F-D86-home-receipt-verification.md`.
