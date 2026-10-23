# F-D22 process-cause independent review — 1532

## Verdict

**Review PASS with correction; the 1525 author report is FAIL as written.**
Its detailed body correctly kept the historical seven nodes unconfirmed, but
its result summary incorrectly says “all seven nodes and parameterizations”
passed and attributes all seven to the child environment. The corrected state
is:

- The terminal full service remains **FAIL**, unchanged:
  `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679`, exit 1,
  `185 failed, 16,733 passed, 4 skipped, 19 errors`, raw terminal SHA-256
  `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.
- The exact seven historical D22 failures remain **UNCONFIRMED**, not proven
  product or environment causes. The two retained source-mode representatives
  reproduce a child import failure; the other five historical failures do not
  have retained per-node stderr/argv/PID/lifecycle evidence proving the same
  cause.
- The installed `8c355a` Agent + `9ce424` Runtime control is a separate,
  current-control result: **9 passed in 29.94s**. It is not a re-run of the
  historical `8c355a` + `3b926e` full result and does not promote the five
  remaining historical failures.

## Exact historical node inventory

The content-hashed census
`agent-F-D22-census-return-1500-final-a6684b789b129c65f70a9e53493be1abbc9c04bbb697a03159683a9dbb50c671.json`
contains exactly seven `custody-process-assertion` nodes from
`test_generic_host_actions_v3.py`:

1. Managed review: `[True-False]`
2. Managed review: `[True-True]`
3. CPU release: `[False-False]`
4. CPU release: `[False-True]`
5. CPU release: `[True-False]`
6. CPU release: `[True-True]`
7. CPU uncertain cleanup: `[observation]`

The two source-mode representatives actually run by 1525 were managed review
`[True-False]` and CPU release `[False-False]`. Their retained result was
**2 failed in 8.59s**, with saved output SHA-256
`e173d829c283479d7ee8a4ccf48e20df7de3a951231678f733849c28ccadc313` and
`ModuleNotFoundError: runtime_protocol` during child startup. This establishes
only those two representative reproductions.

## Why “seven selected” yielded nine passes

The control command selected three unparameterized test families:

```text
test_managed_review_cancel_retires_only_observed_owner_and_preserves_drift
test_cpu_shutdown_waits_for_real_original_attempt_release
test_cpu_shutdown_cannot_close_unproved_real_attempt
```

Their decorators collect 4 + 4 + 1 = **9** cases:

- managed review: all four `(keep_attempt, drift)` combinations;
- CPU release: all four `(shared_accounting, keep_attempt)` combinations;
- uncertain cleanup: one `observation` case.

The historical full result failed only two of the four managed-review cases;
the other two managed-review cases are the two extra control passes. Thus the
installed command passed **7 historical IDs + 2 additional current-control
IDs = 9 collected cases**. It did not select seven exact parameterized IDs,
despite the 1525 summary wording.

## Identity and guard checks

The historical full recipe is Agent `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`
(tree `c4d72b065d6e68c92e4335120cc016cadf53b06a`), Runtime
`3b926efab2eed122d374540baee297d4cdcec62a`, parent Python
`/home/user/work/venv-agent/bin/python`, and Runtime source root
`/home/user/work/wt/rt-pin-3b926efa`. The retained child stderr is the
`runtime_protocol` import failure before the intended child body/lifecycle
work. The retained managed and CPU trace slices are respectively
`7f3d7936db47d4e3b9a210f9b07e684f7c1c647cc4fc9cc7c9eb62099dad0144` and
`c99e15d6f4a7d8d883bfbd7e3f3bb399c61910fbd1dd6cecb1cb35321a18c312`.

For the installed current control, the existing 1512 evidence records Agent
`8c355a...`, Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2`, child Python
`/home/user/work/venv-agent-child-d22-8c3b926e/bin/python`, and Runtime
protocol SHA-256 `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`.
No test body, installed/runtime/profile byte, PID/custody rule, lifecycle
guard, timeout, cleanup, or shutdown assertion was changed.

The seven historical IDs all belong to one test file. Its body hash is
`32e8958cce8bbcae19f1771f131e043171d0ac5f62732bfdefe8a1dbcd54708d` at both
old `8c355a` and current `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`.
The three parameterized function-body hashes also match at both identities:

```text
managed review: c70d50ac34cd357a8d5e8fd91e9d6c9f274dd14df7cb93af0258f8abca64360b
CPU release:    454ec01105e535ac5f9740ccc66d1b3897315d54767997eb96db66e460a804af
uncertain CPU:  1d189847157925ed574313536667cd318fce272606b7f51092960d182f9a2260
```

The relevant implementation files likewise match old `8c355a` and current
`58316fd6`: `generic_host.py`
`fc020cc2f6256642203fc4d36a9bb661265fa9a9589d386a46963528d11791d3`, and
`process_group.py`
`bce716c4c544f3247f189100c6fc74ab1decb2e7f9191196e92386959d5861b3`.
The source retains the managed child argv shape, CPU capability-worker argv,
real-entry marker checks, process ownership/returncode checks, PID birth
identity and `verify_tree_absent`/uncertain-cleanup guards. The old full
stderr/trace evidence and these unchanged source identities support the
qualification boundary; they do not prove a common cause for all seven.

## Commands and results

Read-only checks performed:

- Parsed the content-hashed census JSON and recomputed the seven historical
  IDs versus the nine decorator-expanded control cases: **PASS**, 7 and 9
  respectively, with 2 extra control cases.
- Compared `git show 8c355a:<file>` and `git show 58316fd6:<file>` plus current
  SHA-256s for the test, `generic_host.py`, and `process_group.py`: **PASS**;
  all relevant hashes match and `git diff --quiet` returned 0.
- Read the retained raw terminal log at lines 12988–13332 and the child
  startup traceback around lines 1486–1969: **PASS** for the documented
  assertion/trace facts; raw log SHA-256 matches the inventory.
- Attempted one collect-only command for the three families, but the second
  and third arguments omitted the test-file path; pytest correctly returned
  exit 4, “file or directory not found,” and collected no tests. No test body
  ran. The 9-case count above is therefore derived from the retained command,
  source decorators, and the 29.94s control result, not this malformed probe.

No full suite, historical 3b rebuild, environment reprovision, targeted test,
browser/live service, or body duplicate was run. No product/Git/source/test,
schema/client/pin/archive/lock/dependency, or shared-environment change was
made.

## Correct handback

Keep the full10679 `8c355a + 3b926e` result as terminal **FAIL**. Keep all
seven historical nodes **UNCONFIRMED**; credit only the two representative
child-import reproductions as causal evidence. Keep the `8c355a + 9ce424`
9-pass result scoped to the existing current control. No environment
reprovision, old-3b rebuild, or additional approval is needed to retain this
qualification boundary. The next owner, if further proof is desired, is an
orchestrator-assigned exact historical-pair qualification owner—not the
terminal `childenv1454` handoff.
