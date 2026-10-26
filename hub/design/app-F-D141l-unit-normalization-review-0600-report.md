# D141l independent DATA/PROVENANCE review: PASS

The supplied `tl/app-F-D141l-unit-witness-return-0549` evidence passes this independent review. No product bytes, Composition bytes, validator, kit, service, receipt attachment, or live job were changed or created.

## Controlling facts

- Retained same-controller admission: `5433016320` bytes at `2026-10-26T00:42:39.754967+00:00`, from the authentic JSON `available_bytes` field at source byte range `[104, 135)`.
- Authentic normal run: `app-full-1026004326-12174`; in-body minimum `4839120896` bytes at `2026-10-26T00:48:37Z`, from the retained `df -B1` row at source byte range `[1157219, 1157291)`.
- `X = 5433016320 - 4839120896 = 593895424` bytes.
- `floor = max(4600000000, 4000000000 + 593895424 + 200000000) = 4793895424` bytes.
- This is a bounded admission-to-in-body-minimum bracket, not a continuous peak. Gaps remain unobserved: 44 seconds from normal body start to the first timestamped normal sample, intervals between normal samples and after the normal minimum, 10m35s from pristine body start to its first timestamped comparator sample, and intervals between/after pristine comparator samples.
- The pristine comparator `app-D141-pristine-receiver-0007-full-1026010029-23581` contributes a justified timestamped delta of `11431936` bytes; it does not exceed the normal `593895424`-byte bracket. The retained untimestamped pristine first row is not used to enlarge the bound. No convenient lower bracket or continuous-peak claim was substituted.

## Findings

1. Raw source ownership, hashes, original bytes, offsets, run IDs, source heads/trees, timing, and comparator custody agree with the supplied immutable evidence. PASS.
2. The numeric extraction and arithmetic are exact. PASS.
3. `normalized-start.df` and `normalized-stop.df` are exactly `Avail\n<decimal>\n`, but the companion metadata correctly labels them `DERIVED_DATA_PROJECTION_NOT_ORIGINAL_STDOUT`; they are not claimed as historic stdout or new observations. PASS.
4. The existing installed D89d validator accepted the canonical projected inputs in an isolated fixture with trusted manager-root ownership and returned exit `0` / floor `4793895424`. PASS.
5. The production caller path is preserved: `test-run` obtains the registered `app/full` command `npm test -- --maxWorkers=3`, and invokes the installed validator with the receipt, trusted manager root, job/repo/suite, worktree, HEAD, computed tree, and registered command before admission. PASS.
6. Composition remains clean and byte-exact at HEAD `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`; `git diff --check` passes. PASS.

No FAIL finding was identified. No tests, typecheck, lint, full suite, browser, Node suite, `request-test`, `run/submit`, or live socket were run; unchanged code makes those lanes not applicable to this data/provenance review.

The C0 request/reply surface was not edited: request `api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands[schema_version,op,version,select,args,created]/label/steps[id,label,intent,tags,command_ordinals,patch,reads]/merge fields|atomic/reads/Idempotency-Key/dry_run/source/rationale/group_id` is preserved, as are accepted/merged `data/receipt/canonical_document/document_digest/provider_version/compiler_version/normalized commands/id_map/base/previous/accepted revision/publication pairs/rebased_onto/merge_mode/complete steps/records/bindings/effects/dependencies/history/undo_steps/publisher/annotations`, conflict `reason/head`, invalid `code/path/hint/suggested_command`, and preview `would_status/nullreceipt` fields. This source-only review did not exercise or alter that API.

No production receipt is attached and no body is admitted by this review. A later manager/controller may attach only a real generated job receipt after the normal gates and current head/source binding are independently satisfied.
