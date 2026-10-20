# Commands and results

All commands ran from `/home/user/work/wt/vw-m3-runtime013-current-server-compatibility`.

```sh
git rev-parse HEAD HEAD^{tree}
```

Result: `8f105c26e3b62f9c2683f717a9773a12bc775a8e`, tree
`b7f456d5135cba6049980ebc43a91c7a72ab8f7e`.

```sh
git merge-base --is-ancestor 81f8c7e0b22c34804015c054762af3d737e4698a HEAD
```

Result: exit 0. The reviewed compatible server patch is an ancestor.

```sh
git diff --quiet 2c4ac180..HEAD -- \
  contract/openapi/workspace-v1.yaml contract/manifest.json \
  contract/artifacts.json contract/component-manifest.json \
  packages/python packages/typescript runtime_protocol/contract_metadata.py \
  runtime_protocol/schemas/timeline-commit-bundle.json
```

Result: exit 0; no public wire/generated surface diff.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/rt-vw-m3-runtime013-current-server-compatibility-pytest \
  tests/test_client_parity.py tests/test_contract_fixtures.py \
  tests/test_artifact_manifest.py tests/test_command_schema_compatibility.py \
  tests/test_generated_client.py::test_generator_is_reproducible \
  tests/test_generated_client.py::test_python_client_source_is_tracked_and_generated_check_is_not_self_referential
```

Result: **143 passed in 36.30s**, exit 0.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B generators/generate.py --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B scripts/artifact_manifest.py --check
git diff --check
```

Result: all exit 0; artifact check printed `contract/artifacts.json is current`.

No full suite or socket/localhost suite was run, per the task boundary.
