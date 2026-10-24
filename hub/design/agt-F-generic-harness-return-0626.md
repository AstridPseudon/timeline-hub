Implemented the generic reopen harness fixes in `tools/run-generic-reopen-original-0605.py`.

- Pinned Node `v20.19.4`, approved profile, locks, registry state, and `819acf…` Composition archive.
- Required genuine `node_modules` dependencies.
- Added full RECORD digest/size validation and canonical Agent/Runtime direct URLs.
- Added fixed reviewed test/function/assertion hashes and whole-source cleanliness checks.
- Preserved fail-closed preflight, reviewed SHA gate, durable evidence, selector, 30s timeout, and JUnit output.

Verification:

- `python3 -m py_compile ...` — PASS
- `ruff check ...` — PASS
- `bash -n ...sh` — PASS
- `git diff --check` — PASS

Harness SHA: `3ea291035284d0a057fa2a14c7ab8622b59ea0f6aab7cbe32ace5fd5a68a39c5`  
Test SHA: `b4b99d0bd4336f26d65c7763d87d28f0ca98fc5f92b02a70ba41a43c17453709`

Future independent row:

```text
run-generic-reopen-original-0605.py run-original --child-root <qualified-child> --provision-receipt <receipt> --evidence <private-evidence> --tmpdir <private-tmp> --reviewed-script-sha256 3ea291035284d0a057fa2a14c7ab8622b59ea0f6aab7cbe32ace5fd5a68a39c5
```

No preflight, Node, body, install, full-suite, or browser run was performed.