# M2 selected schema: bounded counterexample

There is a real invalid new edit on base `e929efef`. With the exact admitted
`elementRef` fixed at the immutable `reveal` revision declaring numeric `seed`
with `maximum: 10`, a freshly captured `clip.set-params` of `seed: 16` succeeds
through capture, execute, authoring compilation and the native commit provider.
The independent validator of the resolved exact descriptor rejects 16. Seed 8
passes the same pipeline, reload, exact undo and redo; existing and newly set
opaque parameters survive. This is a declared-property validity defect. It does
not require changing the policy for unknown data.

## Executable proof

Only repository addition:
`/home/user/work/wt/agt-m2-selected-schema-proof/tests/sdk/test_timeline_selected_schema.py`.

- Line 42 reuses the existing actual `admit_project_pack` fixture and calls
  `resolve_admitted_element` for its max-10 revision. Both old and new immutable
  admissions are retained by the original fixture. No schema is monkeypatched.
- Line 52 creates a valid generated hold effect via native track/clip commands,
  starting with seed 4. The admitted reference is present from creation. There
  is no intervening edit, reference replacement, restore, stale base or ABA.
- Line 62 is the passing seed-8/opaque-data test, including compiler, provider,
  JSON reload, inverse and redo, and re-resolution of the identical schema.
- Line 85 preserves the required refusal with three `xfail(strict=True)` cases:
  capture; capture/execute/compile; capture/execute/compile/provider. Each expects
  an error mentioning seed or the bound and unchanged head/history/documents.
  Current execution reaches `DID NOT RAISE` in all three cases.

The existing admission fixture uses its in-memory Documents client and test
build verifier. The native provider runs unmodified with the existing detached
Runtime port and ABI fixture, using the admission's same realm/project. This
proves provider acceptance in that harness, not a live Runtime HTTP journey or
Remotion build. No fake selected schema, fabricated project-snapshot authority,
renderer, network, sockets or new port behavior was introduced.

## Exact source and decision

All Agent paths below are rooted in the assigned worktree.

| Absolute path:line | Finding |
| --- | --- |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/sdk/timeline/_scalar_commands.py:55` | Reads and guards both exact-reference spellings; the prior guard fix remains valid. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/sdk/timeline/_scalar_commands.py:67` | Chooses a type label for schema lookup, despite having read the exact reference. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/sdk/timeline/_scalar_commands.py:72` | Checks changed values only against `element_schema(type).properties`; ignores the admitted owner/revision declaration. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/sdk/timeline_address.py:285` | Scans sealed pack files by directory name. This lookup cannot select a project admission's exact owner/revision. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/core/element/project_packs.py:64` | Existing admission-document reader validates authenticated realm, document kind/schema, owner and admission fields. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/core/element/project_packs.py:356` | Existing resolver selects the exact owner/id/kind/revision from project admissions and verifies immutable snapshot integrity and build identity. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/core/element/project_packs.py:337` | Reconstructs the descriptor from the admitted immutable definition and checks its revision. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/core/element/catalog.py:146` | Descriptor already carries the full declaration as `schema`. No second schema representation is needed. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/sdk/timeline/commit.py:527` | Provider executes through the same helper. |
| `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/sdk/timeline/commit.py:546` | Materializes the canonical document and reaches acceptance at line 557 without resolving this selected schema. |

Recommendation for the orchestrator: use the exact resolver result's
`record['descriptor']['schema']['properties']` as the smallest declaration
source for changed declared values when an admitted reference is present.
Retain the existing property-value validation, raw JSON, unknown-key policy,
clears, narrow identity guards and immutable-reference semantics. This bounded
proof does not establish a need to validate unrelated opaque fields or apply
whole-object defaults/required/additionalProperties rules during a leaf edit.

For the provider, reuse the existing pack resolver's admission/snapshot logic
with a Runtime-verified project-pack document input, rather than opening a
launcher client inside save or trusting schemas supplied by the caller/bundle.
Factor the existing resolver to consume that verified document and immutable
snapshot as needed. Keep full owner/id/kind/revision selection; caching by bare
`clipType` would reproduce this defect. Admission additions must not imply that
an unchanged exact revision acquired a different schema.

The existing verified-document seam is useful but does **not** support this
document kind unchanged:

- `/home/user/work/runtime/runtime_protocol/timeline_commit_types.py:70` defines
  `VerifiedDocument` as the existing pin/document pair.
- `/home/user/work/runtime/runtime_protocol/timeline_commit.py:38` exposes it via
  `config_source`.
- `/home/user/work/runtime/runtime_protocol/timeline_commit_port.py:289` requires
  a declared/reachable input pin; line 306 restricts config reads to `.config`.
- `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/sdk/timeline/commit.py:279`
  verifies exact scoped document pins; line 299 also restricts `.config` kinds.
- The real pack kind is `astrid.project-pack`, schema `astrid.project-pack/v1`,
  source binding `project-packs`, declared at
  `/home/user/work/wt/agt-m2-selected-schema-proof/astrid/core/element/project_packs.py:30`.

Therefore a follow-up needs narrow explicit authorization/capture of that
existing stable pack document and its pin, with existing retention/CAS checks,
then injection of the resolved declaration into execution/capture. The exact
pin discovery/transport is an orchestrator/Runtime contract decision, not
implemented or pretended available here. Do not relabel the pack as `.config`,
fabricate a verified snapshot in an authoring bundle, or duplicate the schema
into a new command/manifest format merely to make the probe pass.

## Verification

From `/home/user/work/wt/agt-m2-selected-schema-proof`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_selected_schema.py tests/editing_conformance/test_recipe_scalar_commands.py tests/sdk/test_timeline_commit_provider_scalar.py tests/core/test_project_packs.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/sdk/test_timeline_clip_add_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_commit_provider.py
```

Exit 0: **392 passed, 7 xfailed in 29.54s**. Four xfails are the original
clear-only cases, untouched; three are the new exact-declaration refusal cases.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q --runxfail tests/sdk/test_timeline_selected_schema.py
```

Expected exit 1: **3 failed, 1 passed in 2.76s**. All three failures are
`DID NOT RAISE` at line 95; admission, exact schema validation and native
creation succeeded first. No setup/import failure is counted as a defect.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-force-exclude tests/sdk/test_timeline_selected_schema.py
git diff --check
```

Both exit 0; Ruff reports all checks passed. No full suite, make check, central
suite, install, renderer/live journey or cross-repository product edit was run.
The task remains tests-only on its M2 branch; Candidate 1 label-only scope and
the existing M2 integration hold are unaffected.
