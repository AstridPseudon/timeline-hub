# D73 source validation

Private candidate only. Source fixes are complete; receiving status is NOT_READY.

All commands ran in /home/user/work/wt/rt-D73-exact-node-source-sol-2156.

## Canonical checks

### controls: exit 0

```bash
TMPDIR=/tmp/w-60e42c3561 ./ops-d73-exact-nodes/dry-check.sh --controls
```

```text
test_duplicate_malformed_empty_and_bad_tuple_refused_together (__main__.ManifestControls.test_duplicate_malformed_empty_and_bad_tuple_refused_together) ... ok
test_key_value_not_json_preserves_equals_and_final_line (__main__.ManifestControls.test_key_value_not_json_preserves_equals_and_final_line) ... ok
test_missing_many_paths_and_schema_collected_without_running_them (__main__.ManifestControls.test_missing_many_paths_and_schema_collected_without_running_them) ... ok
test_no_manifest_census_lists_every_key_and_receiving_need (__main__.ManifestControls.test_no_manifest_census_lists_every_key_and_receiving_need) ... ok
test_wrong_own_node_tuple_is_never_relabelled (__main__.ManifestControls.test_wrong_own_node_tuple_is_never_relabelled) ... ok
test_real_named_parser_run_positive17_and_poison_zero (__main__.RunControls.test_real_named_parser_run_positive17_and_poison_zero) ... d73-ab1e-selected4-exact-nodes: run positive exit=17 calls=1; poison exit=1 calls=0
d73-ab1e-fork-exact-nodes: run positive exit=17 calls=1; poison exit=1 calls=0
ok
test_request_node_guard_requires_files (__main__.RunControls.test_request_node_guard_requires_files) ... ok

----------------------------------------------------------------------
Ran 7 tests in 1.025s

OK
```

### ruff: exit 0

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache --config /home/user/work/agent/pyproject.toml ops-d73-exact-nodes/check.py ops-d73-exact-nodes/test_recipe.py
```

```text
All checks passed!
```

### format: exit 0

```bash
/home/user/work/venv-agent/bin/ruff format --check --no-cache --config /home/user/work/agent/pyproject.toml ops-d73-exact-nodes/check.py ops-d73-exact-nodes/test_recipe.py
```

```text
2 files already formatted
```

### bash: exit 0

```bash
bash -n ops-d73-exact-nodes/dry-check.sh /home/user/work/wt/agt-pin-2eca9a1d/tools/p4-d73-pinned-launch.sh
```

```text

```

### binding: exit 0

```bash
./ops-d73-exact-nodes/dry-check.sh --bind-check /tmp/w-60e42c3561/selected-ID/d66 /tmp/w-60e42c3561/fork-ID/d66
```

```text
binding: PASS (selected-ID -> selected-ID.xml; fork-ID -> fork-ID.xml)
```

### source-census: exit 1 (expected NOT_READY/all-missing refusal)

```bash
env -u D73_MANIFEST ./ops-d73-exact-nodes/dry-check.sh --source-check
```

```text
{
  "status": "NOT_READY",
  "source_errors": [
    "D73_MANIFEST: receipt-rendered key=value manifest missing",
    "manifest missing format",
    "manifest missing agent_sha",
    "manifest missing agent_tree",
    "manifest missing agent_parents",
    "manifest missing agent_path",
    "manifest missing runtime_sha",
    "manifest missing runtime_tree",
    "manifest missing runtime_path",
    "manifest missing app_sha",
    "manifest missing app_tree",
    "manifest missing app_path",
    "manifest missing composition_sha",
    "manifest missing composition_tree",
    "manifest missing composition_path",
    "manifest missing python",
    "manifest missing node",
    "manifest missing profile",
    "manifest missing schema",
    "manifest missing node_version",
    "manifest missing profile_lock_sha",
    "manifest missing profile_archive_sha",
    "manifest missing profile_registry_sha",
    "manifest missing composition_version",
    "manifest missing original_p4_test_hash",
    "manifest missing service_versions",
    "manifest missing junit_paths",
    "manifest agent_path: must bind own-node receipt /home/user/work/wt/agt-pin-2eca9a1d",
    "manifest agent_sha: must bind own-node receipt 2eca9a1da94eb35bb969540e150192ff920ce326",
    "manifest agent_tree: must bind own-node receipt 888c16e3dbbff2d6827e7ffcfea64208b0e2a5e4",
    "manifest runtime_path: must bind own-node receipt /home/user/work/wt/rt-pin-ab1e4f61",
    "manifest runtime_sha: must bind own-node receipt ab1e4f6141987706132916e2da16477f5a019464",
    "manifest runtime_tree: must bind own-node receipt 7d8e77b2f5a4af79305c9212ce5174d3ea9fd657",
    "app: checkout receipt binding missing without manifest identity",
    "composition: checkout receipt binding missing without manifest identity"
  ],
  "receiving_needs": [
    "central agent d73-ab1e-selected4-exact-nodes: row not installed",
    "central agent d73-ab1e-fork-exact-nodes: row not installed",
    "selected4: fresh central per-ID XML/raw logs/submit and end disk witnesses NOTRUN",
    "fork: fresh central per-ID XML/raw logs/submit and end disk witnesses NOTRUN",
    "manifest interpreter/schema: genuine import/distribution readiness unqualified here; D139 owns dependency recipe, no Main-only schema overlay permitted"
  ],
  "source_ready": false,
  "body": "NOTRUN",
  "preflight": "NOTRUN"
}
```

### diff: exit 0

```bash
git diff --check
```

```text

```

## Additional final checks

`bash -n /home/user/work/wt/agt-pin-2eca9a1d/tools/p4-d73-pinned-launch.sh` — exit 0.

`bash -n ops-d73-exact-nodes/dry-check.sh` — exit 0.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python - <<'PY'
from pathlib import Path
for path in sorted(Path('ops-d73-exact-nodes').glob('*.py')):
    compile(path.read_text(), str(path), 'exec')
    print(f'compile: PASS {path}')
PY
```

Exit 0; both private Python files compiled in memory without bytecode writes.

`git diff --check` — exit 0 after final README update.

The control command uses current central parser source read-only against private rows. Each exact row had one run-mode positive dispatch (exit 17), then a source poison exit 1 with zero preflight/body dispatches. Stub XML proves distinct per-ID output paths only; it is explicitly not a functional XML result.

Read-only old Agent/Runtime receipts, launcher/test hashes, origin, clean source, lock tuple and all 15 file hashes passed inspection; no rendered own-node manifest exists in this packet.

Initial Ruff --include was unsupported and an initial format check requested formatting. Corrected by explicit file arguments and repository-config formatting; final canonical checks above pass.

No central row, product source/test/pin, shared dependency or sealed child was modified. No actual preflight/body/full/core/child/provider/browser/socket/network/install ran.

Independent review is next. Operational owner must supply genuine manifest and dependency inputs, install reviewed rows through normal ownership, then separately receive real per-ID body/disk evidence. D139 schema/distribution recipe ownership is exclusive; Agent 2136 frozen-tuple inputs are not reused as admission.
