# D122 independent source review

- Reviewed commit `9ea67534f61d3604c9cb136de449803c4cbe51c2` (`ded3451dca1546b971d512cc97f5d83181490d93`), whose direct parent is `21b304678e809874fea3a447434da8b81fe6d08f`.
- The successor diff contains only `astrid/core/rendering/remotion_runtime.py` and `tests/core/rendering/test_source_registry_runtime.py`; `git diff --check` passed.
- Extracted the exact successor fresh-child `source` string from the immutable Git blob and ran real subprocesses with isolated temporary package roots. Symlinked platform, spoofed platform `__file__`, preloaded package, preloaded platform, foreign platform-directory/loader, and symlinked approved package-init attacks all refused before foreign initializer execution. Trusted-parent positive control passed.
- Extracted the exact predecessor source string and reproduced the two actionable attacks: both foreign initializers executed and the predecessor origin guard did not reject them.
- Successor and test blobs compiled successfully with Python 3.13; no assigned worktree files changed.
- Author validation retained from `evidence/validation.md`: 4 RED, 24 focused/source/environment GREEN, 37 installed/security GREEN, Ruff 2143=2143, mypy 1902=1902.
- The advertised immutable `queue/done/checkout-agent-9ea67534f61d3604c9cb136de449803c4cbe51c2` directory was absent in this sandbox, so the repository pytest lanes were not independently rerun from that checkout. No original14, batchcore, full, browser, socket, or central-service run was requested.
