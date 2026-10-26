# U4a D141 independent normal receiving review

## Verdict

**PASS_SOURCE_TOOLS.** The Agent candidate is a provenance-only adoption of the qualified
normal Runtime producer. Independent checks found no product, client, schema, config,
test, fixture, generated-payload, caller, or pin conflict.

## Findings

- **D141-RECEIVING-001 — PASS:** runtime.lock.json changes only source_commit,
  from 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d to
  95d98f038320d5d46bd679ac000ab3e15825c935. It retains 15 entries and the
  remaining lock structure is byte-equivalent to the 8585 baseline.
- **D141-RECEIVING-002 — PASS:** All 15 consumer payloads are byte-identical to
  the 8585 baseline, the Runtime 95d source files, and the independent 0513
  corrected mapping.
- **D141-RECEIVING-003 — PASS:** Runtime tl/integration is
  95d98f038320d5d46bd679ac000ab3e15825c935 / tree
  78df31d62c5b9ba4c84dee4ea346e43a767718c1. The checkout was clean before and
  after review; its committed contract/artifacts.json bytes and version
  match the lock, and the manifest is unchanged from Runtime 6a to 95d.
- **D141-RECEIVING-004 — PASS:** Existing generated
  astrid_runtime_client/generated.py::WorkspaceClient.commit_timeline
  and Agent wrapper astrid/sdk/workspace_client.py::WorkspaceClient.commit_timeline
  remain unchanged and continue to use the commitTimeline route.
- **D141-CLEANUP-001 — PASS:** Authorized cleanup only: deleted
  evidence/receiving.json and evidence/handoff.md; restored
  evidence/source-manifest.json and evidence/validation.md exactly from
  baseline 8585 Git blobs. Final diff versus 8585 is only runtime.lock.json.
- **D141-MODE-001 — PASS / correction disclosed:** Mode comparison uses
  permission bits, so worktree 0644 correctly equals Git tree mode
  100644; producer source modes are 100644. Raw string comparison was
  not used.

## Environment note

The first direct pytest attempt could not create the harness-provided
tmpdir because that path is a regular harness metadata file, and collection
without Runtime on PYTHONPATH failed with ModuleNotFoundError. The corrected
private /tmp/w-rt-U4a-D141-host-receiving-review-0549 run passed 24 tests.
This is an environment/setup note, not a product finding.

## Limits

No full suite, browser/live service, TypeScript, release, ZIP, product-proof,
or readiness claim is made. No source correction or manual lock/hash edit was
needed.

