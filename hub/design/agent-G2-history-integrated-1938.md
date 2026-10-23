# G2 retained-history integrated proof — PASS

Worker: `agt-G2-history-integrated-1938`  
Repo/worktree: Agent, `/home/user/work/wt/agt-G2-history-integrated-1938`  
Date: 2026-10-23

## Exact integrated identity

- Actual HEAD: `07e6d83df69146c7dddea207f32330dc8b58dbc5`
- Actual tree: `43f7379006acec4a7c62ec54dc0fa86e27581305`
- HEAD is the normal merge of `1e1211c7fea5d08a6eb260371b3101e28d323de7` onto `92d0413ae9565f151560faf7814be84e079d3110`.
- The integrated diff from `92d0413a` contains exactly these three paths:
  - `astrid/sdk/timeline/checkout.py`
  - `astrid/sdk/timeline_sheet.py`
  - `tests/sdk/test_g5_retained_sheet_basis.py`
- Source commit `1e1211c7f` blobs are exactly:
  - `checkout.py`: `b8df805d0d1595e64c2ab323d8daa63d53449a92`
  - `timeline_sheet.py`: `a3939ba93fd946dbfb5108f6ba1fd88d41e1afce`
  - `test_g5_retained_sheet_basis.py`: `c40403e0eccbe62dceafe977a40e2595c3336e15`
- Reviewed product patch `697c8fd3b51562fb18e45dedecc56723984db2eb` versus `89c38c9355f5d4bcc68597ec74e4729435a7a07a` has the same three paths, same stat (`100 insertions, 3 deletions`), and the same stable patch-id as `92d0413a..1e1211c7f`: `48d1de94da48789b41ca51dec448d0e5cfceeeb5`.
- `697c8fd3b` is not an ancestor of the integrated HEAD. No G5 retirement commit is in the `92d0413a..07e6d83d` ancestry; the ancestry is only the normal merge and `1e1211c7f` source commit.
- Agent worktree status is clean. Runtime pin worktree status is clean.

## Exact focused run

Command run once, with `-o addopts=` and cache provider disabled:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f ASTRID_AUTHENTIC_LEGACY_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_g5_retained_sheet_basis.py tests/sdk/test_timeline_checkout_history.py tests/sdk/test_timeline_checkout_history_boundaries.py tests/editing_conformance/test_current_pair_reader.py
```

Result: `35 passed in 6.80s`. Collection independently recorded exactly `35` tests. This covered the required current-pair marker/tests; no failure or retry occurred.

## Runtime/source identity evidence

The exact runtime checkout used by the test process was `/home/user/work/wt/rt-pin-2a9e347f`:

- Runtime commit: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`
- Runtime tree: `f79a2355cfb39d9ada7721978bd20d5702105778`
- In-process `runtime_protocol`: `/home/user/work/wt/rt-pin-2a9e347f/runtime_protocol/__init__.py`, SHA-256 `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`
- In-process `runtime_protocol.service`: `/home/user/work/wt/rt-pin-2a9e347f/runtime_protocol/service.py`, SHA-256 `267bec1aee551e7ea1f92f987adb24268be11c6dd165ee56f24aa68ff2b6a692`
- In-process Agent checkout module: `/home/user/work/wt/agt-G2-history-integrated-1938/astrid/sdk/timeline/checkout.py`, SHA-256 `87eb2398942cd0bbfb94addec791703ee55dd9babc0d919a01c607a9b9b70e3d`
- In-process Agent sheet module: `/home/user/work/wt/agt-G2-history-integrated-1938/astrid/sdk/timeline_sheet.py`, SHA-256 `a82366e97ab38809c4b5533f5ac996b61434814f221ba422a6b7bdf5e8ccc9c4`

The checked-in runtime lock/configuration was not used as runtime identity proof; the direct checkout environment above was used. The authenticated archive exists, SHA-256 `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, 16 entries; the simple credential scan returned `0`.

## Scope and limits

- Tree-level outside-path check proves all paths outside the three source blobs remain exactly at `92d0413a`.
- The requested full-v2 request/receipt/history/undo/preview surfaces and preserved `92d` core paths were not changed by this integration; this worker did not rerun their full suites.
- No full suite, browser, HTTP, benchmark, four-way ratchet, or unrelated gate was run.
- Prior evidence supplied for context is not re-run here: independent history-1929 `FINAL 127 + 16 PASS / 2148 / 1911`; current-port-1929 `FINAL 19 + 16 PASS`, scoped with no new identity.
- G5/P1 remain DRAFT/NO-GO; this proof gives no gate-body credit and does not retire G5.

Decision: PASS for the actual integrated retained-history proof only. No source, test, schema, pin, Runtime, benchmark, environment, or Git changes were made.
