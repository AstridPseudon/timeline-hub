# Agent P4 four-file packet

PASS: imported only `tests/sdk/test_p4_cli_sheet_v2.py` from
`fe781e4d2cf267994d655dc57320448dddd5d708`, exact blob
`fd248182a0e1c120fa6440994da545c4e13219ad`, onto base `b9a640b5d`.

The three existing packet tests remain byte-for-byte identical to donors:
`test_p4_commit_v2.py` (`85218e8e99a1c7602d2b7ee399f3847fac759186`),
`test_p4_ten_note_provider.py` (`1ed257c4604552793d2eaabfc117babe93c5b445`),
and `test_p4_note_rerun.py` (`80c15e2944b5660a18077aa38f84cf3b3ced09bb`).

Evidence: the four-file targeted pytest run passed 15 tests; scoped Ruff,
private mypy over all four files, and `git diff --check` passed. The first
pytest invocation hit only the worker temp-path harness issue (regular file
at the requested tmpdir); the rerun passed. No full/browser/farm/actual-wire
suite was run.
