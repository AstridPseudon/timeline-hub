# Runtime private 613 closed-intent generator fix

## Scope

Private successor of Runtime `a6a11a806a51262192447fdeccc726b01ffd78fb`.
The source schema remains the reviewed Agent357 freeze: 55 definitions, 29
operation clauses, 12 v2-capable operations, and SHA-256
`613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`. Release
metadata remains `0.2.14`; frozen historical floors, receipt aliases, and
Runtime protections are unchanged.

## Finding and fix

Operation-level closed empty objects may omit `properties: {}` while still
declaring `type: object` and `additionalProperties: false`. The generator
previously only recognized objects containing `properties`, so these schemas
fell through to open Python maps and TypeScript `unknown` index signatures.

`generators/timeline_commit_types.py` now treats a false
`additionalProperties` value as a closed object in its nested-definition,
expression, and Python `TypedDict` emission paths. Truly open authored JSON
objects continue through the existing map/index-signature path.

Normal generation emits named closed empty types. For `clip.delete` this is:

```text
Python:     EditCommandVariant1Intent = TypedDict('EditCommandVariant1Intent', {})
TypeScript: export type EditCommandVariant1Intent = { [key: string]: never };
```

The TypeScript representation is checked by a positive/negative consumer
fixture: `{}` is accepted and an own `reason` key is rejected. The focused
Python generator test asserts that the generated intent is an empty
`TypedDict` with no required or optional keys.

## Generated evidence

Normal generation and artifact-manifest regeneration completed in the private
successor. Artifact manifest version is
`sha256:b397e5fdb9fc25502bbda9ad5011e82dd2d63330d5af373834d31e6761276e20`.
Changed generated artifact digests are:

- `runtime_protocol/timeline_commit_types.py`: `sha256:0b816f625014aa2297ef428c3c548588acef7808eea99db1d0b5b0d1158e74c9`
- `packages/python/astrid_runtime_client/timeline_commit_types.py`: `sha256:0b816f625014aa2297ef428c3c548588acef7808eea99db1d0b5b0d1158e74c9`
- `packages/typescript/src/timeline-commit-types.ts`: `sha256:9c8911453c6b28453112e407a82716c9b73f8c432d839c6ec9a4bf112430c98e`

The resulting worktree tree ID before the harness commit is
`d438d3e28a29ad80fa6b7c19c55e1b7a4485eae2`; the harness will assign the
successor commit SHA. No frozen/public artifact was edited.

## Verification

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_type_generator.py tests/test_typescript_generator.py tests/test_artifact_manifest.py tests/test_command_schema_compatibility.py
147 passed in 108.02s (0:01:48)

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python generators/generate.py --check
0

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
0 (`contract/artifacts.json is current`)

git diff --check
0
```

No full suite, native pair, installed-dependency change, or consumer-probe
worker files were touched.
