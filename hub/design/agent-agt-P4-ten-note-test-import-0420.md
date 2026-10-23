# Agent handoff — P4 ten-note test import

PASS. Base `38b72402e485d4049eafd50179dcbf570b6f4be5`; imported only
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py` from approved proof
commit `81aad71e853fca551163442fcf3bcec6150357b`. Exact blob:
`5ee8dd5b863c164e0ea5f03257ac61849a425061`; `cmp` and `git hash-object`
match. Source parent is `a568c4ebf804119e3e21a1644b6d6068ed037380`.

Six P4 blobs in the current tree:

```text
85218e8e99a1c7602d2b7ee399f3847fac759186  tests/sdk/test_p4_commit_v2.py
1ed257c4604552793d2eaabfc117babe93c5b445  tests/sdk/test_p4_ten_note_provider.py
80c15e2944b5660a18077aa38f84cf3b3ced09bb  tests/sdk/test_p4_note_rerun.py
fd248182a0e1c120fa6440994da545c4e13219ad  tests/sdk/test_p4_cli_sheet_v2.py
05f7aa2bd862fc608ee17515d373c5f5b47c27eb  tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
5ee8dd5b863c164e0ea5f03257ac61849a425061  tests/editing_conformance/test_p4_ten_note_v2_runtime.py
```

Inherited canonical d106 schema and f252 schema-test blobs are exact; normal
official-34e / 15-mapping state is unchanged. Artifact manifest and vendor
lock checks pass. The real public caller is exercised by the imported source;
the HTTP body remains Proof-owned and was collection-only here.

Checks: one integration node collected; scoped Ruff PASS; private mypy PASS;
normal Ruff 2149/2149; normal mypy 1915/1915; tracked `git diff --check`
PASS. The exact donor's existing extra blank line at EOF is intentionally
preserved; `git diff --no-index --check` reports that line. No
full/browser/native-14 run and no unrelated file changes.
