## Result

Completed read-only F-D52 custody comparison. No production, test, fixture, schema, generated, pin, registry, or source files changed.

### Five retained Runtime nodes

| Node | Author XML membership | Baseline | Final | Identity |
|---|---:|---:|---:|---|
| `test_captured_config_root_mirror::test_captured_config_root_rejects_tampering_without_mutation[native-order]` | absent | Runtime PASS | Runtime PASS | source `526c2cf21141c6d08b2f643c13c9b630f8617147043bc959e321e674dffe559f`; body `859e238a024d4653fb6f1f1769882923fc3f88a6da83f89d393723a000f07007` |
| `test_nested_config_root_history::test_root_config_history_rejects_tampering_without_mutation[native-order]` | absent | Runtime PASS | Runtime PASS | source `bfb72c87898955afa1402cd255e9aa25f9388671dad5a0928e0dce3c5c976374`; body `49cc7062a3332aace9410273b416052562f9e03abdcf1707d7ef7ac448b604a1` |
| `test_occurrence_fork_source_baseline::test_retained_app_fork_reload_undo_restores_exact_closure` | absent | Runtime PASS | Runtime PASS | source `cd921e3ff19d694c16bae2d7b647d2df10fbbcab1fa7ddc9ade473003f3c9ad0`; body `cc16d7a6edc960d06a92b0ca99c56afe2bdb4ba214f54105b2ccec32c07af085` |
| `test_timeline_inverse_fork_guard::test_fork_output_guard_allows_independent_parent_edit_and_preview_redo` | present | FAIL | PASS | source `8302871093213098be70496272b51fba529296e78bb6bc1e53cc608e868a93c6`; body `43d9a97c074b5b209150ff2dcbde8fd808abd720a6bfd138e7000ee118988180` |
| `test_timeline_inverse_fork_guard::test_valid_fork_history_distinguishes_output_consumers_from_retained_sibling[retained-sibling]` | present | FAIL | PASS | same source; body `ad8f28a05f0feafc375827dbc82721c4462d92f7a97c16a5041a85c486853f51` |

The two retained-fork failures both had the real outcome `CommitRejected: inverse stage image differs from authenticated effects`; no failure was relabeled or suppressed.

### Author XML comparison

- Same 334 testcase keys in both XMLs.
- Baseline: `327 passed, 7 failed`.
- Final: `334 passed, 0 failed`.
- Exact red-to-green set: the mixed-list ancestor case, both fork-guard cases, and whole/step redo for ancestor and retained-fork.
- Lost passes: none.
- Strict controls: all 17 pass in both XMLs:
  - ancestor partition: `config`, `descendant`, `source`, `native-range`, `effect-range`;
  - retained-fork partition: `missing-pin`, `owners`, `pin`, `source`, `native-range`, `effect-range`, `stage-owner`, `parent-edge`;
  - retained destination pin: `revision_id`, `content_digest`, `payload`, `missing`.

### Source and custody boundaries

- Qualified author source/result: Agent commit `4e7f822ec607b163535acc2c4e478907c55f12d2`, tree `f6e66298c4c2a15fc9f8aa5acc3a9847978ba497`, parent `d7efe3c49021daf33ae740e3a8bb4d6f02a5f3b1`.
- Current integration remains baseline: `_commit_patch.py` hash `506def3b...` and `_step_undo.py` hash `f94ef32c...`; 4e7, 1234, and 1238 are not ancestors.
- Agent1234 commit `ba0f6b458fc98e077e272cf897453e0f13249258`, tree `2a4b15e0ef290b70fbf6d76fb3d92a67c7251ac0`, and its `336 passed` result are separate author evidence, not an independent security PASS.
- Agent1238 commit `77c131fadb03f7d3a6899ddde4f0d231c203ac5f` is the unique cumulative join owner; it does not establish current-home, installed, HTTP, gate, or final-tuple qualification.
- Production route remains source evidence only: Runtime commit door/coordinator → Agent `RuntimeCommitService.commit()` → `commands.execute(..., commit_request=request)` → materialization and accepted-history handling.

### Artifact hashes

```text
final XML       afb530a0750a0c9400041cee57c96275a6010dec3b7f3b03f3a54c7fc5141b1b
final log       3a901ca06e450d46a8e269c992edad0d0da186098706c3e3de3ff4922b97f8f8
baseline XML    882049c8217cce76aa6bdad2404342f6327c76bf7776419834c8b78bc7461397
comparison JSON d90a58a2f9571efc80a5305d5b29dae36013176d1da16d241b0ab96631391d47
source blobs    a582286110a3af2967630f7ee768406643d1635eff2c12bc03abdbed09a91b5a
commands        05458475112aadff7eaafed79b72926a6a2b28451b07bd136bd5c7c42c761b06
```

### Verification

- Published targeted qualification: baseline `327 passed / 7 failed`; final `334 passed`; nearby inverse cohort `189 passed`.
- Published scoped Ruff, mypy, vendor lock, artifact manifest, and `git diff --check`: passed.
- This worker independently verified all six hashes, XML membership/outcomes, 17 strict controls, command environment/import custody, current source hashes, `git diff --check`, and clean status.
- No original body, full suite, gate, HTTP, browser, installed-package, or security run performed.
- No task blocker. Those broader behaviors remain explicitly unverified.

Completion marker and conventional commit message were written; worktree is clean.