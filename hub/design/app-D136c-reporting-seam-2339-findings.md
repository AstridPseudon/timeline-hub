# D136c finite seam findings

## Result

The first loss is the pytest JUnit serialization edge, not Runtime production.
Runtime constructs the approved `details.safe_diagnostic` map at the existing
missing-observation guard, `reject` mounts it on `CommitRejected.failure`, and
`public_failure` deep-copies it into `RuntimeErrorBase.details`. The existing
focused test proves that mounted reply and proves the refusal envelope is
unchanged when only `safe_diagnostic` is removed.

The original-nine path then reaches the existing Agent publication fixture and
pytest setup reporting. `_pytest/junitxml.py:217-229` formats an error from
`reprcrash.message` and `str(report.longrepr)`; it does not serialize the
exception's `details` attribute. This is the first edge that fails to serialize
the map.

## Exact actual path

1. `tests/sdk/test_capture_source_runtime.py:216` registers the provider loaded
   by `load_timeline_commit_provider("astrid")`.
2. The retained fixture calls
   `publish_authoring_candidate` at
   `tests/sdk/test_timeline_capture_projection.py:430`; its writer at lines
   270-276 calls `service.commit_timeline` directly. This is an in-process
   Runtime call, not an HTTP or RemoteTimelines route.
3. Runtime `service.py:2556-2559` invokes the registered Agent
   `RuntimeCommitService`; Agent `commit.py:1437-1444` calls `port.accept`.
4. Runtime `timeline_commit_port.py:688-694` enters store acceptance;
   `timeline_commit_store.py:1532-1539` invokes the private sequential
   validator; `timeline_commit_port.py:702-712` enters auth validation.
5. `timeline_commit_auth.py:2982-2987` calls `command_output`; at
   `2272-2279`, `require` calls `_safe_observation_diagnostic` and forwards the
   map. `timeline_commit_store.py:36-50` mounts it on the refusal.
6. Runtime `service.py:2566-2579` converts the refusal with
   `public_failure`; `timeline_commit_port.py:99-103` preserves the full
   details mapping on `RuntimeErrorBase`.
7. Pytest receives the setup exception. Its JUnit reporter writes only the
   rendered long representation. The map values are absent from the retained
   XML; source text mentioning `safe_diagnostic` is not a retained map.

The Agent `RuntimeCommitService` is therefore the intermediate provider
caller, but there is no Agent `ErrorObject` conversion on this exact original9
route. The direct fixture writer raises the Runtime public exception into
pytest. Any Remote SDK normalization is outside this actual path.

## Retained artifact facts

The mode-0600 retained XML parses to 9 test cases, all setup errors, with the
common first-seam message. It contains 9 occurrences of the literal
`safe_diagnostic` only in traceback source context and zero occurrences of all
approved value keys. Retained stdout has the same zero approved-value-key
result; stderr is empty. No raw artifact was copied or published.

The safe map's actual values are therefore `UNKNOWN`, not absent by source
inference. The source establishes production construction and transient public
exception custody; the retained result cannot establish the per-boundary
booleans, enums, ordinals, or digest presence/hash.

## Scope and decision

The reviewed allowlist remains exactly 13 keys: fixed enums, booleans, bounded
ordinals, `UNKNOWN`, and one-way digest hash. No raw XML, traceback, IDs,
references, paths, payloads, images, keys, URLs, user content, or private paths
are proposed for publication. The guard predicate, status/code/message, CAS,
and no-write behavior remain unchanged.

The C0v2 request and reply shape is unchanged: `api_version`, `project_id`,
`timeline_id`, `base_revision_id`, `base_publication_id`,
`commands[{schema_version,op,version,select,args,created}]`,
`label`, `steps[{id,label,intent,tags,command_ordinals,patch,optionalreads}]`,
`merge`, `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, and
`group_id` remain as authored; accepted/merged `{data,receipt}` (including
canonical closure/digest/commands/idmap/base/landing/merge/records/bindings/
effects/dependencies/history/undo_steps), conflict reason/head, invalid
code/path/hint/suggested command, and preview would-status/null-receipt remain
the existing shapes. `safe_diagnostic` is only the reviewed additive field on
this refused Runtime detail map.

No implementation or test body was added. No additional original-nine run is
needed for this reporting seam; the existing original-nine is spent and remains
`FAIL_ACTUAL_ORIGINAL9` / `NO_GO` / `UNKNOWN`. D130 SWAP/WAL/recovery and
related qualification remain held.
