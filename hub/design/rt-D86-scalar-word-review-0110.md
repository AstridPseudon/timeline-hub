1. `FAIL_SOURCE` — `tl/agt-D86-scalar-return-0107`

Scope: commit `7adb3f16…`, parent `f2def388…`; source SHA matches `3ff8e779…`.

Blocking finding: `_seed_current_app_document` patches a registry containing newly ingested media (`test_commit_runtime_clip_scalar_fields.py:68`), but `_patch` executes without `verified_media` and no `media.admit` command. `_doc_patch.verify_media` therefore rejects the fresh empty-bootstrap manifest before Runtime acceptance.

Static checks passed: compile, Ruff, mypy baseline/candidate, `git diff --check`, hash/tree/blob verification, and AST conservation. No pytest or function execution.

2. `PASS_SOURCE` — `tl/agt-D86-word-return-0107`

Scope: commit `32619f865…`, parent `7d0e6c07…`; production SHA `eec60cd2…`; test SHA unchanged `058d8210…`.

The manifest correction preserves authenticated hydrated transcript pins while retaining inverse removal behavior. Runtime hydration still obtains pins through `transcript_source`; caller-invented pins are not trusted. All measured test bodies are AST-identical to the original migration source.

Static checks passed: compile, Ruff, mypy baseline/candidate, `git diff --check`, exact source identities, and AST conservation. No pytest or functional qualification was run.

No source changes were made. Commit message and `DONE` marker were created.

Recommended next steps: return scalar to the author queue for genuine Runtime media admission; send word to the normal Agent queue for later behavioral proof.