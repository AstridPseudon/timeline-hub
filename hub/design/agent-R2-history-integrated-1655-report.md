# Agent R2 integrated readonly qualification — 1655

## Verdict

**PASS.** The actual integrated Agent tree is the normal owner merge
`63baa707b4bce52b36c06dc3345d2fd357b10f66`, with exact tree
`7700a8a4e5befeffb68bf1bf644492f460328d94`. It is the reviewed `257f0a853`
tree byte-for-byte. The required single targeted run passed all **103 tests**.

No product source, test, documentation, pin, generated file, lock,
dependency, Runtime checkout, or Git ref was changed by this qualification.
No merge request was made.

## Integrated identity and scope

- Agent HEAD: `63baa707b4bce52b36c06dc3345d2fd357b10f66`
- Agent tree: `7700a8a4e5befeffb68bf1bf644492f460328d94`
- Merge parents: first `bac094180aef38a77b86ab165962e6159f873c60`, second
  `257f0a853720d431ab9c9d2a9bd2c73842253b8b`
- Review ref `tl/agt-R2-source-history-review-1649` resolves to the same
  `257f0a853` commit and the same tree.
- Runtime checkout: `/home/user/work/wt/rt-pin-d9e2a71e`
- Runtime HEAD: `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`
- Runtime tree: `9b07545cac9a8bbafb16246aaa6f72050ef7cffe`
- Both worktrees were clean before and after the test.

The merge against its first parent has exactly these seven paths and no
others:

```text
M astrid/sdk/timeline/_commit_patch.py
M astrid/sdk/timeline/_root_inverse.py
M astrid/sdk/timeline/_step_undo.py
M astrid/sdk/timeline/commit.py
M astrid/sdk/timeline/inverse.py
A tests/editing_conformance/test_captured_nested_redo.py
A tests/editing_conformance/test_captured_registry_redo.py
```

All seven HEAD blobs equal the reviewed `257f` blobs. Their final file
SHA-256 hashes are:

```text
b971050c92b14304bbc037ed775ddb7ddfa6cf5a233cd2075f92ba68725c3163  astrid/sdk/timeline/_commit_patch.py
0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a  astrid/sdk/timeline/_root_inverse.py
206f13ac5991ed6abecbc0b1fbde24f2526cb3bf2f47f57f9b91c66aa43fa1dc  astrid/sdk/timeline/_step_undo.py
a4d612aeadfd66011258b9003d3b7d9a4f33c4fa387c50b65bf4fa79bafb4e91  astrid/sdk/timeline/commit.py
fb0cb16bab8a4fbd72a24c9dffadd6992e397925b383ce9ec79f6cc6bbb00d5a  astrid/sdk/timeline/inverse.py
d7567b519698bd9ae36b44f1747ad26dd0e394dd7f1cdaaf3b83866ed2b7f8d4  tests/editing_conformance/test_captured_nested_redo.py
8b2b899d3b5c833855b2bb2dbb230e01a5ab363c98bd3d2285a986a424730c57  tests/editing_conformance/test_captured_registry_redo.py
```

The existing R1 private sequential capture and atomic behavior remain in
the integrated tree. The six forgery/new-partition control families and the
private sequential capture cases were exercised by the requested six-file
run; no test was weakened, skipped, or marked xfail.

## Exact test command and result

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_captured_nested_redo.py tests/editing_conformance/test_captured_registry_redo.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_private_sequential_capture_runtime.py
```

Result: `103 passed in 18.31s`.

The test run used no bytecode and no pytest cache. It left the Agent HEAD and
tree unchanged, and left the Runtime checkout unchanged.

## Reused evidence and limits

The independent 1649 final-pass evidence remains applicable because the
reviewed tree identity is exact: Mypy baseline `1912` and Ruff baseline
`2149`, plus the independent vendor/artifact checks, are reused as prior
evidence and are **not claimed as new runs here**. No additional review
barrier was introduced.

This was only the specified offline targeted qualification. No full suite,
browser/live-socket suite, original nine-case duplicate, public nested redo,
c271, P1/P4, native14, or browser-body run was performed. No client
adoption/regeneration, Runtime provisioning, daemon tool, or manual
environment setup was performed. The production C0 request/reply contract
was not changed or newly requalified by this readonly task.
