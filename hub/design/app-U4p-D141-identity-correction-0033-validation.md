Read-only commands used by this derivative:

- `git rev-parse <commit>^{commit}` and `git rev-parse <commit>^{tree}` in the immutable App, Agent, and Runtime repositories.
- `git show -s --format=%P <App candidate>` and `git diff-tree --no-commit-id --name-only -r <App base> <App candidate>`.
- `git show <commit>:<path> | jq empty` for all four candidate JSON blobs.
- `git cat-file blob/size`, `git ls-tree`, and `sha256sum` for the 160 App vendor blobs, 159 Agent direct-source blobs, and all 14 Runtime mappings.
- `git status --porcelain`, `git symbolic-ref`, and HEAD/tree reads before and after for normal `/home/user/work/{agent,runtime,app}` checkouts.
- `jq` mechanical comparisons for identity lengths, exact pins, manifest-key conservation, mapping hashes/bytes/modes, and allowed paths.

No tests, lint, typecheck, browser/live-socket suite, Node/Python imports, product/schema execution, generator rerun, Git write, ref write, or permission workaround was performed.

Results: App candidate 9ada0d906a2efc5cf98b18b112d2d4e9d0657098 / tree 2b44a46ca51d880c6a00da4c19aa8629b55eb7dd; Agent 28e56cacb42d3da85b02e5b3543895b44f3d0f70 / tree 2ebe2ddf5a61f013953ab1e21d51ebaab746e58a; Runtime 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d / tree ac5b862744bece65b2e30565db1777bacd60da28. Vendor set 160, direct source hashes 159, Runtime mappings 14, allowed App delta 2. All candidate JSON parsed; all corrected IDs are 40 hex and SHA-256 fields are 64 hex; all listed hash, byte, and mode comparisons passed. Normal checkout guards were unchanged and clean for Agent/Runtime; normal App remained clean at its base as expected.
