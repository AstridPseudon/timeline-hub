# Runtime PUBLIC018 generation and qualification handoff

Status: **prepared, held**. This is one bounded command set for the next
generation worker. It does not generate, pin, publish, activate, or change a
caller. PUBLIC018 is the owner-authorized ordinary transition `SET` plus the
approved derived `Document.content_digest` successor. Private017 is outside
the elapsed inclusion window.

## Inputs and hard prerequisites

Use a fresh Runtime worktree based exactly on Runtime commit
`b92d3e7a05eec65c142294ef4873edd059e9b31d` (tree
`6abc2f117391de8e7e35c0283f575a002199894d`). The following values must be
filled from the final Agent freeze before any command below is run; they are
not defaults:

```sh
RUNTIME_ROOT=/absolute/path/to/this-runtime-candidate
AGENT_SOURCE_DIR=/absolute/path/to/the-frozen-agent-source
AGENT_SOURCE_COMMIT=<future-exact-agent-commit>
AGENT_SOURCE_TREE=<future-exact-agent-tree>
AGENT_SCHEMA_SHA256=<future-exact-raw-edit-command-schema-sha256>
DIGEST_SOURCE_COMMIT=4e1133fb77784a494124e9a73c7c277b6a0cc51e
DIGEST_SOURCE_TREE=5302fe1423356c20be739df4789ce63218462328
```

The freeze must name the committed Agent source, tree, raw schema digest,
55-definition/29-clause inventory, and independent repair verdict. The
reported repair candidate `5b3e41941b1263011f52f9f1291cbbc854563dbb` /
`705fc969ffcc2281d3b3e808e68e8a02467066bc` is review evidence, not a silent
input: use it only if the final freeze explicitly names it. Never substitute
ordinary47 `47b716d0`, complete/private `fcf8`, or any Private017 source.

The Agent collection must be exactly these semantic files (plus the frozen
schema and the two named tests):

```text
astrid/core/timeline/schema/edit-command.schema.json
astrid/sdk/timeline/_clip_scalar_commands.py
astrid/sdk/timeline/_collections.py
astrid/sdk/timeline/_recording.py
astrid/sdk/timeline/_selected_param_authority.py
astrid/sdk/timeline/commit.py
tests/sdk/test_timeline_current_union_schema.py
tests/sdk/test_timeline_transition_schema.py
```

The Runtime delta must be exactly the approved digest source
`4e1133fb77784a494124e9a73c7c277b6a0cc51e` / tree
`5302fe1423356c20be739df4789ce63218462328`, limited to:

```text
contract/schemas/document.json
runtime_protocol/service.py
tests/test_transcript_documents.py
```

It adds only the optional, derived digest. Confirm the digest source’s
independent review and the Agent freeze before materializing either input.

Preserve the immutable published floor while preparing the successor:

```text
published Runtime producer: 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3
published Runtime tree:     d3a290b407fa61e6ab2d476f50c068073f70df00
published package:          0.2.14 / workspace.v1
published artifacts:        76/76
artifact version:           sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac
artifact-manifest digest:   sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d
published Runtime schema:   sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816
ordinary raw Agent floor:   sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
ordinary bundle floor:      sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3
```

Do not rewrite the published floor, old fixtures, or old lock bytes. Start
only with at least 5 GiB free (`df -Pk`); the current Runtime status reports
about 11 GiB free. Do not install dependencies or mutate shared
`/home/user/work/venv-runtime` or `/home/user/work/app/node_modules`.
Use the installed Runtime Python (`/home/user/work/venv-runtime/bin/python`,
Python 3.13.16), Node (`/opt/node22/bin/node`, v22.22.0), and `sha256sum`.

## One normal generation sequence

Run from `RUNTIME_ROOT`, after the source freeze and exact delta collection
are available. The identity checks are deliberately explicit so an unfrozen
source cannot be selected by path or current checkout state.

```sh
set -eu
cd "$RUNTIME_ROOT"
PY=/home/user/work/venv-runtime/bin/python
NODE=/opt/node22/bin/node

test "$(git rev-parse HEAD)" = b92d3e7a05eec65c142294ef4873edd059e9b31d
test "$(git rev-parse HEAD^{tree})" = 6abc2f117391de8e7e35c0283f575a002199894d
test "$(git -C "$AGENT_SOURCE_DIR" rev-parse HEAD)" = "$AGENT_SOURCE_COMMIT"
test "$(git -C "$AGENT_SOURCE_DIR" rev-parse HEAD^{tree})" = "$AGENT_SOURCE_TREE"
test "$(sha256sum "$AGENT_SOURCE_DIR/astrid/core/timeline/schema/edit-command.schema.json" | cut -d' ' -f1)" = "$AGENT_SCHEMA_SHA256"
test "$(git rev-parse "$DIGEST_SOURCE_COMMIT^{tree}")" = "$DIGEST_SOURCE_TREE"

# Materialize the already-approved three-file digest delta from its exact
# committed source. Do not broaden this allowlist.
for path in contract/schemas/document.json runtime_protocol/service.py tests/test_transcript_documents.py; do
  git show "$DIGEST_SOURCE_COMMIT:$path" > "$path"
done

# Stage the frozen Agent schema at Runtime's existing canonical input path,
# then prove byte identity. This is the normal source collection step.
cp "$AGENT_SOURCE_DIR/astrid/core/timeline/schema/edit-command.schema.json" \
   contract/schemas/edit-command.json
test "$(sha256sum contract/schemas/edit-command.json | cut -d' ' -f1)" = "$AGENT_SCHEMA_SHA256"

# Confirm only the approved digest paths are added to the b92 candidate.
test "$(git diff --name-only b92d3e7a05eec65c142294ef4873edd059e9b31d -- \
  contract/schemas/document.json runtime_protocol/service.py tests/test_transcript_documents.py | sort)" = \
  $'contract/schemas/document.json\nruntime_protocol/service.py\ntests/test_transcript_documents.py'

# Version owner: generators/release.json. Set its contract_version to 0.2.18
# in this candidate before running the normal generator.
test "$("$PY" -c 'import json; print(json.load(open("generators/release.json"))["contract_version"])')" = 0.2.18
$PY generators/generate.py
$NODE tools/generate_typescript_conformance.mjs \
  --contract contract/openapi/workspace-v1.yaml \
  --schema-manifest contract/manifest.json \
  --component-manifest contract/component-manifest.json \
  --fixture-root conformance/fixtures
$PY scripts/artifact_manifest.py

$PY generators/generate.py --check
$NODE tools/generate_typescript_conformance.mjs \
  --contract contract/openapi/workspace-v1.yaml \
  --schema-manifest contract/manifest.json \
  --component-manifest contract/component-manifest.json \
  --fixture-root conformance/fixtures --check
$PY scripts/artifact_manifest.py --check
git diff --check
```

The version must agree in `generators/release.json`,
`packages/python/pyproject.toml`, `packages/typescript/package.json`,
`packages/typescript/package-lock.json` (both version fields), generated
`packages/python/astrid_runtime_client/contract_metadata.py`, generated
`runtime_protocol/contract_metadata.py`, and generated
`packages/typescript/src/contract-metadata.ts`. Python package root exports
are `packages/python/astrid_runtime_client/__init__.py`; TypeScript root
exports are `packages/typescript/src/index.ts`. Verify `CONTRACT_VERSION` and
the new `SCHEMA_DIGEST` through those roots, not an unrelated installed
client.

## Smallest qualification set

Run with the frozen Agent source selected as the real provider, not a fake
provider and not a neutral Runtime:

```sh
export ASTRID_CHECKOUT="$AGENT_SOURCE_DIR"
export PYTHONPATH="$RUNTIME_ROOT:$RUNTIME_ROOT/packages/python:$AGENT_SOURCE_DIR"
$PY -m pytest -q \
  tests/test_client_release.py \
  tests/test_client_parity.py \
  tests/test_timeline_commit_contract.py \
  tests/test_timeline_current_union_contract.py \
  tests/test_timeline_commit_provider.py \
  tests/test_timeline_ordinary_http.py::test_ordinary_http_empty_bootstrap_must_be_reachable \
  tests/test_timeline_fresh_bootstrap_scope.py::test_real_provider_fresh_create_uses_normal_bootstrap \
  tests/test_transcript_documents.py \
  tests/test_timeline_document_object_contract.py
```

The real-provider selector is `authoring_profile="astrid"`, which resolves
exactly `astrid.sdk.timeline.commit.create_runtime_commit_service` through
`runtime_protocol.timeline_commit_provider.load_timeline_commit_provider` and
checks provider id `astrid-v1`, interface `1`, and the generated schema digest.
The ordinary door test asserts that the daemon actually installed that Agent
provider. The Agent-side transition selector, when the frozen source’s
semantic lane is checked separately, is the existing command (no new suite):

```sh
cd "$AGENT_SOURCE_DIR"
PYTHONPATH="$AGENT_SOURCE_DIR:$RUNTIME_ROOT" \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_clip_scalar_fields.py -k transition \
  tests/sdk/test_timeline_transition_schema.py \
  tests/sdk/test_timeline_selected_param_authority.py
```

No full, HTTP/browser/renderer, install, pin, or repeated proof is part of
this handoff. The test list above is the minimum contract/client/door/
Document set; report exact collection and results.

## Compatibility boundary

The digest is derived from canonical finite JSON `content` only. The schema
property is optional: old resources remain valid without it and JSON `null`
remains invalid. `_command_replay` is ledger-first, so old accepted results
and exact replays remain byte-for-byte unchanged and may omit
`content_digest`, including after newer writes or restart; only newly
accepted document results carry the field. No live callers changed (**NONE**).

Current blocker: the Agent selected-presence repair has review evidence, but
Runtime’s latest freeze frontier still says the exact committed source,
independent delta verdict, and explicit source freeze are pending. Stop at
that prerequisite; do not silently use 47b, fcf8, or Private017.
