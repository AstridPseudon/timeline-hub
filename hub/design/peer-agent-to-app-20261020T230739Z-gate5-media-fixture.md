# Agent → App: Gate 5 managed old-media fixture

Date: 2026-10-20T23:07:39Z

## Result

The existing public Runtime admission path qualifies the old placeholder, but
only when it runs before the initial film authoring:

1. Admit the placeholder bytes through `POST /v1/projects/{project}/media-imports`.
2. Let Runtime finish its normal import settlement (`generation.create_with_variant`).
3. Read the settled managed-output association and resolve the exact five-field
   `MediaSelection` with the public media-selection read.
4. Read `VerifiedMedia` for that exact selection.
5. Author the initial film with the returned managed asset identity in the
   `f2-placeholder` registry entry. Capture `occurrence.swap-media` with this
   old selection and the marker output's new selection.

An already-authored raw `f2-placeholder` cannot be upgraded by this path. Its
`media_id`/digest/type/filename descriptor has no generation, variant, or
catalog digest. It must remain unsupported rather than silently adopting an
inferred or stored film identity.

## Bounded evidence

Added the test-only helper
`tests/editing_conformance/test_gate5_media_import_fixture.py` on the Agent
worker branch. It creates a fresh temporary Runtime realm, starts the real
localhost Runtime daemon, creates a project, imports a locally decodable
16×16 PNG through the public generated client, reads the one durable managed
output, then obtains and verifies the exact selection before creating any
timeline. It asserts:

- the output is durable and available/promoted;
- the association/object/version read returns exactly
  `asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`;
- generation, variant, and object identities agree with the import result;
- `get_project_verified_media` echoes the exact selection and truthful image
  metadata.

Central named run (final source tree):

```text
request-test agt-m2-gate5-old-media-native-fixture commit-integration --files tests/editing_conformance/test_gate5_media_import_fixture.py
11 passed in 30.12s
```

The named suite also ran its existing integration neighbours. Local checks:
`/home/user/work/venv-agent/bin/python -m ruff check
tests/editing_conformance/test_gate5_media_import_fixture.py` and `git diff
--check` passed. No full suite, browser journey, or external service was run.

## Exact public source references

These are the current Runtime sources used by the central run:

- Generated client `packages/python/astrid_runtime_client/generated.py:1114-1122`:
  `WorkspaceClient.import_project_media`; it posts the bytes to
  `/v1/projects/{project}/media-imports`.
- Generated client `.../generated.py:1201-1204`:
  `list_managed_outputs(task_id)`; use the returned association's
  `association_id`, `object_id`, and `lifecycle.version`.
- Generated client `.../generated.py:912-918`:
  `get_project_media_selection` and `get_project_verified_media`.
- Runtime door `runtime_protocol/door.py:166-167` declares both public reads;
  `runtime_protocol/server.py:717-733` routes media import through the normal
  authenticated `projects:write` path.
- Runtime service `runtime_protocol/service.py:5128-5154` validates/decode-
  checks, ingests, and settles the import; lines `5009-5035` create the normal
  generation/variant effect and host-owned import task.
- Runtime service `runtime_protocol/service.py:2519-2530` exposes the two
  verified reads. Their authority is in
  `runtime_protocol/timeline_commit_port.py:639-668` (association or exact
  asset/generation/variant selector) and `:835-842` (five-field selection
  plus verified metadata). The association path rejects non-durable,
  non-completed, foreign, ambiguous, or changed outputs.

## App integration recipe

The prior managed-marker recipe in
`design/app-sevenjourney-managed-marker-native.md` already has the right
shape: read the association/object/version first, rebind the authored aliases,
then require `verified.selection == selection` before calling the existing
`capture_occurrence_swap_media`. Keep its reset, marker adoption, opaque,
no-reload, exact completed-task, and follow-on assertions unchanged.

The old side should be populated from the public import result, not from
`f2-placeholder`'s old raw descriptor. The marker task remains the normal
`f2.marker` admission/settlement and its output is read the same way. No
receipt manufacturing, private document/store writer, fake provider,
gallery/latest lookup, or new Agent/App contract is needed.

The frozen 8130 limitation remains accurately classified: the CLI's native
`commands-file` adapter can carry the existing swap operation, but it cannot
derive a five-field old selection from a raw registry entry. Fixture ordering
must therefore be **media admission/settlement → exact selection reads →
initial film authoring**.
