**D115 remains blocked; the producer fix is held.**

Changed `commit.py` so hydration preserves the sealed input manifest. Existing consumed-source bookkeeping adds verified pins at command output. Added mounted source controls; preserved the original PARAM file byte-for-byte and all inherited input-capture assertions.

Validation:

- Final `producer.xml`: **112 passed, 1 failed**; original accepted16 + staged16 all pass.
- Input/source controls: **17 passed**, including restart authority and database no-write checks.
- Source neighbors: **63 passed, 1 failed** because a fixture lacks Runtime’s required `db_path`, before provider execution.
- All three previously disclosed neighbors now pass.
- Ruff, mypy, compilation, AST preservation audit, and `git diff --check` passed. No full suite ran.

The unchanged mounted regression now authenticates its initial input, then fails at Runtime `timeline_commit_auth.py:2864`. `command_output` retains the predecessor revision when payload digest is unchanged, despite a genuinely consumed source changing the manifest. Runtime is outside ownership; no relaxation or source omission was attempted.

Exact commands/results: [checks.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D115-producer-input-sol-1002/evidence/checks.json). Precise next-owner pairing: [unapplied-pairing.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D115-producer-input-sol-1002/evidence/unapplied-pairing.json).

Identities:

- Base SHA: `ff8d14f0213f9c7ebe50b9be2c8f9a0254ec293e`
- Candidate tree: `019ae9944d5f445776bd19c7d0c441190955c1a3`
- Runtime SHA: `1daca2a33f6d7b10053e07c539a54843e3984e19`
- `producer.xml` SHA256: `0f3e98bcc4667203136478226c8aea37689638a724cb64ab6cd03b31f7499ba7`

D115 commit message and `BLOCKED` written. Next: Runtime projection correction, rerun the unchanged regression, then independent protected review and FULL CORE before adoption. No merge requested.