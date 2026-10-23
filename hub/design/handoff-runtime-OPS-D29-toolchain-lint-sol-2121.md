Completed on artifact-only branch `tl/rt-OPS-D29-toolchain-lint-sol-2121`. **Do not merge into Runtime.**

Only the fixture and manifest changed. Removed the unused shebang, split sorted imports, and added two explicit `check=False` arguments. Normalized AST comparison passed; all 27 assertions and 14 cases are unchanged. No suppressions, configuration changes, or weakened tests.

Validation:

```bash
/home/user/work/venv-runtime/bin/python "$TMPDIR/test-node-carrier.py"
env -i PATH="$PATH" TMPDIR="$TMPDIR" /home/user/work/venv-runtime/bin/python "$TMPDIR/test-node-carrier.py"
```

Each invocation ran once and passed: **14 cases = 2 explicit + 3 legacy + 9 invalid; store=0, build=0**. This remains 14 unique cases, with no additional acceptance credit. Independent 2117 evidence is retained.

```bash
patch --batch --fuzz=0 -d "$TMPDIR/patch-one" -p1 < ops-handoff/remotion-toolchain.patch
patch --batch --fuzz=0 -d "$TMPDIR/patch-two" -p1 < ops-handoff/remotion-toolchain.patch
/home/user/work/venv-runtime/bin/python "$TMPDIR/verify-lint-repair.py"
git diff --check
```

PASS: both target `cmp` checks, exact hashes/bytes, both `bash -n` checks, five embedded Python compilations, fixture compilation, canonical manifest, AST comparison, and two-file scope.

Ruff 0.16.8:

- `ruff check --no-cache ops-handoff/test-node-carrier.py`: PASS, 0 findings.
- `ruff check --no-cache --isolated ops-handoff/test-node-carrier.py`: PASS, 0 findings.
- Expanded isolated `--select E,F,I,EXE,PLW1510`: 57 → 52 findings; remaining findings are unchanged E501=31, E701=2, E702=19. All requested new findings cleared.

Exact artifact identities:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Patch, unchanged | 5653 | `01c26c4b0b102c83d9159c166eeb0fa3f851e62132f7fc0dd4c228190763d4dd` |
| Fixture | 8709 | `0159a9d70ae81fecd9c4d836fe8c9e7f4bf91bbeee81b862c6960f77e9d1366a` |
| Manifest | 2956 | `e3240b2f388f8b6a7bc99b6931dcddb2052972218cb528522c46da4ea44fac4b` |
| Reviewed maker, unchanged | 28041 | `873ddcfa636b3ae9e285613a6fb65c643e21ac749e00197d582e0c820dd70149` |
| Reviewed requester, unchanged | 2735 | `471fd470efeae102140b96b4f97db857e0d6d79b0839afa10a1a00e911b33b5f` |

Legitimate child-install observations:

- Maker: 33373 bytes, `c887a1bef4831f2ca5a43372ee28430000b2f20b9d290bffb237f27ffc404ff2`.
- Requester: 13326 bytes, `3b771253b465a6ba06b57ab16d6049273114dc75f491ce81d0132fedb3c8aa33`.

Approved App Node/npm remain absent. Production command was preserved and **not executed**; its live requester remains baseline and requires reviewed-requester installation first. The private fixture used the exact reviewed requester. No live writes, installation, build, network, full suite, browser, or gates ran. C0/v2 request/replies and frozen source were untouched.

No blocker to this repair. Commit message and `DONE` created. Next: independent custody/AST review; no further functional repeat needed while source remains identical.