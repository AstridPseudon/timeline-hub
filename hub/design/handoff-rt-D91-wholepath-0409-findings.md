# D91 wholepath static handback

## Scope

- Reviewed exact candidate `39fcc67863d8a0019e527d1c53fcd852847f51ed`.
- Candidate tree: `0c74e4977bfca5b8d6f0b01dc67c9ee9f883ba31`.
- Shared-inverse fixture blob: `19ad54ba92b989590e3f257741e2d6ae3ba7e9e6`.
- Fixture SHA-256: `81c780b575b852f5011cc3a0c5bb910f933293d8cbff77343bddcbb63778ae8e`.
- No product, test, schema, generated, pin, or dependency files were changed.

## Earliest divergence

The first divergence is request step assembly, before Agent creates its prepared
candidate and before the Runtime port accepts it:

1. The D91 fixture now emits the physical occurrence `doc.patch` changes in the
   setup command list (`test_commit_runtime_shared_inverse.py:66-76` and
   `:125-134`). This is the distinct correction after the earlier placement
   omission.
2. The fixture submits that mixed command list through Runtime's integration
   helper (`:137`). The helper creates one `edit` step spanning all command
   ordinals but sets `patch: []` (`runtime/tests/test_timeline_commit_integration.py:126-136`).
3. Agent executes the batch and `normalize_steps()` computes all submitted
   `doc.patch` changes from the command ordinals, then rejects a mixed step when
   any submitted change is absent from the step patch
   (`astrid/sdk/timeline/_commit_patch.py:71-85`).
4. This happens from `commit.py:1331` / `commands.py:229` / `_commit_patch.py:270`
   and therefore precedes prepared construction at `commit.py:1429-1444`.
   Runtime only surfaces the provider rejection.

## Actual proof correlation

The existing central result `rt-D91-corrected-ten-proof-0403-…-17648` records
10 errors, all with `step patch omits doc.patch changes`. Its traceback shows
the actual `original-third` request had a first command containing a guarded
set with prior value `1800`; the request's step was the mixed `edit` step. The
source identifies that first change as:

```text
ref:  parent
path: [occurrences, occurrence_id:occurrence-3, duration_ms]
before: present(1800)
value: 2000
```

Thus the actual missing claim is in step `edit`, command ordinal `0`, for the
`original-third` branch. The `authored-first` branch has its first physical
`doc.patch` after its two native setup commands, at command ordinal `2`; the
existing private records were not expanded here, so no additional path claim
is made from private request data.

## Passing comparison and handoff

- `test_commit_runtime_parent_media.py:33-40` proves the mixed-step pattern:
  aggregate every `doc.patch` change into the step patch while retaining all
  command ordinals.
- `tests/timeline/test_authoring_media.py:672-675,687-691` proves the
  per-command pattern: each `doc.patch` ordinal carries that command's changes,
  and native ordinals carry an empty patch.

Minimal seam/owner: the Sol-owned D91 test file should construct a step shape
matching one of those two existing patterns for the setup batch. No Runtime
validation relaxation or provider change is indicated. The original timing,
physical identity, provenance, and behavioral guards should remain intact.

## Static checks

- Candidate fixture AST parse/compile: PASS.
- `git diff --check 39fcc^ 39fcc -- tests/editing_conformance/test_commit_runtime_shared_inverse.py`: PASS.
- No pytest, collection, fixture/helper execution, service, browser, build, or
  repro was run.
