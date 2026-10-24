# Actual P4 profile interpretation

Read-only analysis of the original service capture. No original, gate, native or benchmark rerun. Source labels below are opaque; private request paths, keys and identifiers are omitted.

## Original scope

Test protocol wall 46.804486s; original timeout 45s. Handler cumulative 42.070979s. Calling thread only; cProfile overhead uncalibrated. These are diagnostic instrumented times, not uninstrumented performance or a regression comparison. Historical first-redo and current first-undo checkpoints differ.

| Operation | Handler wall (s) | history entries | verify entries | accept entries | commit entries | Outcome |
|---|---:|---:|---:|---:|---:|---|
| Shared initial ten-note commit | 3.552721 | 5 | 6 | 1 | 1 | Handler returned |
| First note undo | 33.992499 | 49 | 48 | 0 | 1 | Failed |
| Later notes / redo | unobserved | — | — | — | — | No claim |

Total method entries: history 71, verify 64, accept 1, commit 2. These are not durable receipts. The shared initial commit cannot be allocated to individual notes.

## Top ten cumulative (overlapping)

| Frame | Primitive/total calls | Self seconds | Cumulative seconds |
|---|---:|---:|---:|
| server.py:1171 _dispatch | 54/57 | 0.001519 | 42.070979 |
| server.py:408 _route | 54/54 | 0.001445 | 42.048654 |
| timeline_commit_store.py:202 _verify_accepted | 64/64 | 0.069124 | 37.854424 |
| server.py:294 _timeline_commit | 2/2 | 0.000063 | 37.542158 |
| timeline_commit_store.py:442 history_entry | 71/71 | 0.068386 | 37.508154 |
| service.py:2435 commit_timeline | 2/2 | 0.000106 | 37.494423 |
| service.py:2450 _execute_timeline_commit | 2/2 | 0.000313 | 37.483851 |
| timeline_commit_execution.py:69 execute | 2/2 | 0.000771 | 37.459443 |
| commit.py:1160 commit | 2/2 | 0.000704 | 36.381040 |
| timeline_commit_port.py:210 _read | 40/41 | 0.001777 | 33.330365 |

verify 37.854424s and history 37.508154s overlap and must not be added.

## Dominant self and leaf costs

| Frame | Primitive/total calls | Self seconds | Cumulative seconds |
|---|---:|---:|---:|
| validators.py:396 descend | 1672/1350359 | 4.202054 | 27.117427 |
| copy.py:119 deepcopy | 35002/3012267 | 3.765243 | 7.948585 |
| validators.py:339 evolve | 1285903/1285903 | 3.433598 | 7.152291 |
| ~:0 <method 'get' of 'dict' objects> | 9356267/9356267 | 1.830736 | 1.830736 |
| validators.py:282 __attrs_post_init__ | 1285926/1285926 | 1.536641 | 1.774405 |
| _types.py:94 is_type | 1640564/1640564 | 1.480605 | 2.623101 |
| copy.py:218 _deepcopy_dict | 16380/457522 | 1.379265 | 7.774054 |
| _keywords.py:282 type | 632056/632056 | 1.318481 | 5.026694 |
| timeline_commit_producer.py:60 value_equal | 32470/768266 | 1.097505 | 2.150176 |
| ~:0 <built-in method builtins.getattr> | 5983040/5983040 | 1.074030 | 1.074030 |
| timeline_commit_validation.py:17 finite_json | 1714/1714 | 0.955649 | 1.700091 |
| ~:0 <built-in method builtins.isinstance> | 4807854/4807860 | 0.949042 | 1.126819 |
| decoder.py:351 raw_decode | 2094/2094 | 0.816542 | 0.817916 |
| validators.py:452 is_type | 1640564/1640564 | 0.754938 | 3.378170 |
| _core.py:165 create_resource | 871721/871721 | 0.721412 | 1.330361 |

The dictionary get leaf alone costs 1.830736s (9,356,267 calls). The actual source seam is `validate_commit_value`: 1,609 calls / 28.368863s, nested under fresh sequential-capture/history authentication. jsonschema descend costs 4.202054s self; evolve 3.433598s self / 7.152291s cumulative across 1,285,903 calls; post-init 1.536641s self. Deepcopy costs 3.765243s self / 7.948585s cumulative and overlaps other callers.

The candidate narrow seam is reuse of immutable installed schema traversal setup, never accepted/history/result/authority state or validation results. Every value must still traverse every applicable schema constraint, finite-JSON and fresh authority check. Do not reduce history or verification entries through a memo. Implementation is conditional on a strict finite measured comparison.

## Capture integrity

Verified 54 ordered begin/end pairs, 54 readable individual profiles; merging their stats exactly reproduces merged `handlers.prof` (including caller maps).

- summary.json: `209c5bbbd80926207389ef22bf7b5b66dba3f9e4aadd6eabc14a4cb480800be4`
- events.jsonl: `0a8bb4b594573f47fecaec3ab8b6ccc4215769c1511ae6cc59856678f15cfecb`
- handlers.prof: `567614cc5a2d959a02f4028706f436cfd9dd5b6659eb536661255aee7a05a49c`
- originals.xml: `0958d3efb2ffd5bd2ad594184bd98eee241e58d15ccc6cf833a5f8da86a0fe7e`

124 reported module origins: 0 present and hash-exact; 124 unavailable; 0 present but changed. Changed module names: . Unavailable origins are not silently verified.
- Local parent timeline_commit_store.py matches captured module: `a2db29e4dbb5ef781d818690647e888b4eb02550c93a3e3d962df161d610d4cd`
- Local parent timeline_commit_validation.py matches captured module: `c4b2143f151db766738eebd330983a8037a9a9fc8627b93303f26a59bbc53115`
- Local parent timeline_commit_auth.py matches captured module: `75f5141cadebafc9f887f5968f39f0ff030d1b2e6c724c24de0bd10b94cde2f0`

Captured path locations are no longer present. Read-only `git show` on the exact captured Runtime/Agent commits verifies {'runtime': 44, 'agent': 80} module source blobs against the recorded origin SHA-256 values; unverified module names: [].


## Production path and inverse boundary

Captured source S1 is the exact Runtime product commit; S2 is the exact Agent product commit. All 44 Runtime and 80 Agent module origin hashes match read-only Git blobs at those commits. The local parent is `44917baf5976d6a655d582fafc63fde7b6cb242d`; the three allowed product files match S1 exactly before editing.

The original fixture in `test_native_batch_ingress.py` passes request bytes through `MemorySocket` into the actual `RuntimeHandler`, not a substitute store. The route reaches `RuntimeService.commit_timeline` → `_execute_timeline_commit` → `CommitExecutionCoordinator.execute` → the real Agent provider `commit`. `RequestCommitPort._read` authorizes under the store mutex; `history_entry` calls `_ancestor`, which walks exact publication/revision pairs through `TimelineCommitStore.history_entry` and `_verify_accepted`. Source S2's inverse `load_boundary` verifies the previous publication, validates the contiguous history segment, and loads both closure boundaries; `AcceptedRecords` carries that loader into inverse selection, later-step guards and `apply_inverse`. These reads account for repeated authentication. They remain unchanged.

Raw call multiplicity: `history_entry` at the store 71, `_verify_accepted` 64, `_historical_sequential` 36, `validate_sequential_capture` 37, `validate_commit_value` 1,609. Direct schema callers include `_capture_records`, `_historical_sequential`, and `_capture_document_images` (1,460 schema invocations from the latter). These are method entries, never acceptance counts.

The top cumulative frame does not justify a history/authority memo. D47 still holds: no stable sealed validation boundary, nine attacks remain open and the deferred memo stays unmerged. D62 recorder classification, its accepted-event/metadata binding, genuine ABI1 behavior and its known submit-completeness gap remain unchanged. No new trust surface is introduced.

## Different finite control

The existing 1850 whole-restore control reported history 258 / verify 254 and 1 passing case in 6.87s. It used a different source/input/checkpoint and is not a timing baseline or evidence of original-45s causality. It was read only, never rerun here.

## Chosen correction and measured limit

The only product edit reuses constructed validators for immutable installed schema traversal. A bounded 256-entry FIFO holds the parent validator, schema, complete resolver object and child validator. Strong references prevent identity reuse; parent identity includes registry/checker configuration. Hit reads do not mutate the map; insert/evict is protected by a lock. Other `evolve` arguments use the original implementation. Every call still runs finite JSON traversal and every applicable schema keyword with fresh errors; no instance or authority result enters this cache.

The final interleaved comparison in `cost-comparison.py` uses the existing retained two-command capture, identical parent/candidate inputs and schema hashes, 10 alternating-order rounds of three complete verifications, plus one diagnostic profile per variant. Median CPU per three verifications: parent 0.387122085s, candidate 0.329615758s, a 14.8548% reduction. Median wall: 0.393285667s → 0.336657966s. Full keyword/type-check call maps are identical. Each verification still makes 56 schema and finite-JSON calls, 54 document-image checks, four claim checks and one sequential-carrier validation. Constructors fall from 21,240 to 1,942; fewer constructors alone is not the acceptance evidence—the complete validation/check map is equal and unprofiled CPU improves.

An exploratory sequential run was noisy, and a lock-on-every-hit variant showed a 1.47% slowdown; neither is accepted evidence. Their small JSON outputs remain labeled as exploratory. The final source avoids lock/mutation on hits and has the measured reduction above. This is focused-control evidence only: no fresh P4/R2 original, service proof, benchmark gate, full suite or browser run. It does not prove the original meets 45s or attribute the historical failure to the same cause.

Additional raw artifact hashes (verified in place): original service log `e263e35bdb1867122bc20995b56c8db853f6cb0ef03f849f64b43d98be59a40d`; service exit file `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` (exit 1). Originals XML reports one timeout failure and two passes. Private original payloads and log paths are not reproduced here.
