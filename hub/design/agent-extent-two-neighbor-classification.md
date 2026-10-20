# Agent extent two-neighbor classification

Classification recorded 2026-10-20 (UTC, from `date -u`). This is a
classification only. No product source, test, artifact override, fake
history, or assertion was changed.

## Source identities and environment

- Base: `1cea89a17e116600e8c205784235a7d07a2cbc3a`
  (`tl/agt-m2-voiceover-native-command-builder`).
- Candidate: `11724a7dc1c2f15cf4e0e7c543c9a68b056d77cc`.
- Python: `/home/user/work/venv-agent/bin/python`, Python 3.13.16.
- Each tree was made with `git archive` into a separate temporary directory,
  then made read-only with `chmod -R a-w`. Both runs used the same virtualenv,
  `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH` pointing only at that archive, and
  `-p no:cacheprovider`.

The imported modules were `tests.editing_conformance.test_recipe_occurrence_delete`,
`tests.editing_conformance.fixture_loader`, `astrid.sdk.timeline.commands`,
`astrid.sdk.timeline.native_occurrence_delete`, and
`astrid.sdk.timeline.commit`. The relevant source hashes were:

| Source | Base SHA-256 | Candidate SHA-256 |
| --- | --- | --- |
| `tests/editing_conformance/test_recipe_occurrence_delete.py` | `12fe687cf755680eda483b75267c29785c33729ff43d18580669ae0b3e38cdd3` | same |
| `tests/editing_conformance/fixtures/recipe_m2_occurrence_delete.json` | `9a52d55130a4c857e3cb4d8962ea63155c2d3c3b2a6ed035d8babf38666d1e96` | same |
| `astrid/sdk/timeline/native_occurrence_delete.py` | `fea3a2352d66dae9156f5daaa526c1185f26130ccad31732066fa4b76a7f5886` | same |
| `astrid/core/timeline/authoring_bundle.py` | `e7867e768761ad6f485b45086bd144e0bb904b703b327836030b6d997aa0b2bb` | same |
| `astrid/sdk/timeline/commands.py` | `2061025241f2e0fa9270a898966bf4b474c9c8822f46ddd6aaba57755c50e3dc` | `d6172dd2511aed829ed95d4702e431a325503acd488a3ec72bedea5862eee10f` |

The commands diff contains only the `occurrence.resize` import and registry
entry. The candidate-only extent files were the schema, the resize handler,
its resize witness, and the materialization schema-union control. None is on
either failing delete path.

## Exact reproduction

The predecessor record named these exact nodes:

```text
tests/editing_conformance/test_recipe_occurrence_delete.py::test_legacy_group_refuses_with_migration_needed_and_no_mutation
tests/editing_conformance/test_recipe_occurrence_delete.py::test_closed_schema_and_portable_native_capture_golden
```

Archives were prepared with:

```bash
WORK=$(mktemp -d /tmp/agt-m2-extent-two-neighbor-classification.XXXXXX)
mkdir -p "$WORK/base" "$WORK/candidate"
git archive 1cea89a17e116600e8c205784235a7d07a2cbc3a | tar -xf - -C "$WORK/base"
git archive 11724a7dc1c2f15cf4e0e7c543c9a68b056d77cc | tar -xf - -C "$WORK/candidate"
chmod -R a-w "$WORK/base" "$WORK/candidate"
```

Base command:

```bash
cd "$WORK/base"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WORK/base" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --tb=short \
  tests/editing_conformance/test_recipe_occurrence_delete.py::test_legacy_group_refuses_with_migration_needed_and_no_mutation \
  tests/editing_conformance/test_recipe_occurrence_delete.py::test_closed_schema_and_portable_native_capture_golden
```

Result: `FF`, `2 failed in 0.95s`, exit code 1.

Candidate command:

```bash
cd "$WORK/candidate"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WORK/candidate" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --tb=short \
  tests/editing_conformance/test_recipe_occurrence_delete.py::test_legacy_group_refuses_with_migration_needed_and_no_mutation \
  tests/editing_conformance/test_recipe_occurrence_delete.py::test_closed_schema_and_portable_native_capture_golden
```

Result: `FF`, `2 failed in 1.00s`, exit code 1. The traces are identical:

```text
assert error.value.kind == 'migration_needed'
AssertionError: assert 'unsupported_dependency' == 'migration_needed'

assert portable_golden() == fixture
Differing items include 'bundle' and 'after_bundle'
```

## Causes and classification

### Legacy-group admission classification — baseline

`execute()` checks `parent.config.pinnedShotGroups` before dispatching the
operation. At `astrid/sdk/timeline/commands.py:242-249`, the global guard
raises `CommandError(..., kind='unsupported_dependency')` unless the sole
command is the migration command or an authenticated inverse. Therefore the
occurrence-delete handler's own `migration_needed` branch is unreachable for
this setup. The handler source and the test source are byte-identical between
base and candidate, and the same exception kind and message were observed in
both runs.

Classification: **baseline failure; not a candidate regression**. The defect,
if repaired later, is the legacy-group admission error-class precedence (or
the test's expected contract), not the new extent carrier.

### Portable capture golden classification — baseline

The diagnostic import probe built `portable_golden()` in both archives and
reported:

```text
source_mapping_keys ['_runtime_document', '_source_closure', 'placements', 'shots']
fixture_source_mapping_keys ['_runtime_document', 'placements', 'shots']
extra_source_mapping_keys ['_source_closure']
```

`astrid/core/timeline/authoring_bundle.py:478-481` adds
`source_mapping._source_closure` when `capture_sources` is true. That source is
byte-identical between base and candidate, while the delete fixture is also
byte-identical. The candidate does not introduce this key and does not alter
the delete capture path; both exact runs fail for the same extra-key mismatch.

Classification: **baseline failure; not a candidate regression**. The defect,
if repaired later, is the stale portable golden versus the existing captured
source-closure contract.

## Conclusion

Both occurrence-delete neighbors are same-cause baseline failures. There is no
new candidate defect to report and no extent-source freeze decision is changed
by this classification. The extent proposal remains private and unactivated.
