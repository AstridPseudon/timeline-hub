# D139 preflight validation

Captured 2026-10-25T22:15:47Z before the one central-service submission.

- Runtime source: `f103bb46866999c961a8865636f2e66d544e0c9b`, tree `5d0cedf2e5134acf895e8d43191cc5fdc09f9883`; worktree clean.
- Required Runtime ancestry: `cf0b82dd47452a7a34fc63eb233e9b1dc0532806` and `0bb3bc45cef22bc317398d79e1617da3eb430df2` both present.
- Agent source: `4c4ee35d5687c4cd40a0e5395efda53aa56f939d`, tree `d50fd98f7d1bc6860de810f38e8a0b3a55ca224e`; `/home/user/work/wt/agt-pin-4c4ee35d` clean and exact checkout receipt present.
- Interpreter: `/home/user/work/venv-runtime/bin/python`, Python 3.13.16. Imports resolved from the Runtime worktree and the pinned Agent checkout; no fallback origin observed.
- All six selected test files parsed successfully with `ast.parse`; their SHA-256 values and byte sizes are recorded in `source-manifest.json`.
- The central registry has exactly one `runtime d139-integration-six-2214` row. It changes only harness configuration; existing suite rows were not edited.
- No Runtime product/test source changes were made. No pytest command was run locally.
