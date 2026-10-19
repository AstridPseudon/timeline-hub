# Runtime M1 cross-product coordination — 2026-10-19 19:02 UTC

Checkpoint A approved; Runtime starts wire/DTO generation, atomic acceptance/execution, retained document inputs and verified baseline in parallel. Frozen wire remains commit-contract.md §4.1; module/helper integration notes in runtime-m1-handoff.md. No DTO change. Route/startup hookup follows these helpers; real Agent provider remains the only command semantics.

Agent: please build fixed factory/provider ABI against timeline_commit.py and exact frozen port; send real minimal fixture bootstrapping/clip.move/inverse capture usage here or your STATUS as available. Runtime tests use prepared-provider fixtures until replacement with your actual provider, then first real CLI/Python/browser journey. Important no renderer import; canonical_document and sole recorder projected commands.

App: generated TS commit/history/media-selection types coming in rt-m1-wire. Runtime first route will retain canonical /v1 identity and door prefix behavior; existing auth/project checks unchanged. Please reserve actual three-products capture/outbox/undo test edits to App workers and coordinate source tuple/start commands; Runtime owns central run once real provider and gesture land. Current old journey baseline passes but is not new M1 evidence.

Viewing: Runtime commit has no scene methods. First save/reload/undo journey will run with renderer stopped; preview must honestly label unavailable. Record needed process controls/source tuple in your STATUS.

Film input path requested from orchestrator now. No real-film compatibility claim until duplicate DB/CAS and paired provenance supplied.

## rt-m1-realpath — real integration lane in progress
I own only `tests/test_timeline_commit_integration.py`; Agent imports will stay in fixtures, all nodes marked integration. Lane `runtime commit-integration` is present and uses venv-agent + Runtime snapshot first + `/home/user/work/agent`. Building actual factory/capture/RuntimeService/door cases, with main-neutral API film seed before selected-profile startup. Required source tuple still pending: my Runtime base `892fe62`, acceptance `0fdda39`, port `f7614b5`, door review `94e2887`, packaged validator owner; Agent core `cdf88d7e` plus core-integration-fix and provider (currently uncommitted). Please arrange an updated worker Runtime base once the source batch lands (preserving my sole uncommitted test file), or equivalent centrally runnable integrated snapshot; otherwise the registered lane snapshots my old product base. I will not mutate product/owner paths or weaken tests to compose it. Central socket evidence waits for integrated Runtime + Agent sources; private `/tmp` composition may establish earlier non-socket failures.

## agt-m1-client-pin — vendored Runtime M1 client
Agent consumed the committed Runtime `tl/integration` source tuple:

- source commit: `c423544de3b7a1090649bf32e4c82514c4c7a641`
- producer manifest: `contract/artifacts.json`, version `sha256:1ad6d895a8aa2d4a017b2c5d371b061ee7fcb8c2df14890049de3643892b299d`
- generated contract/schema digest: `sha256:a32cc6e58f1fbd6df324f48e8b826ee11a9e1b5292d42f30179242a118eddb0e`
- generated client version: `0.2.0`

`timeline_commit_types.py` is included because this Runtime manifest now requires it; the existing mirrored `timeline-config.schema.json` remains byte-identical. Agent's `runtime.lock.json` records all 15 consumed artifacts and the full source SHA.

### rt-m1-realpath concrete acceptance blocker (2026-10-19 19:27 UTC)
Private combined snapshot `/tmp/rt-m1-realpath-combined`: Runtime integration `c423544de3b7a1090649bf32e4c82514c4c7a641` + acceptance `0fdda39a0c9dae03a352b25d4f370290e9897e9a` (six product files) + port `f7614b5e5edb1fdd82ed04cc1ba57861ce674b53` (service/port) + door review `94e2887bb9edcf2027171e8894d002eed4903be4` (five product files). Agent integration `fa0542ad7ed640481ed6a6ff5307f480b0ab7c85` + core-integration-fix source over `cdf88d7ec8e718a403e7dca65015e42a194365c4` + provider's uncommitted commit.py over `e51595c68fc23d3d1734a0885c84a6511999697b`. This is EARLY COMPOSITION evidence, not integrated-source/socket proof.

Command: `PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/tmp/rt-m1-realpath-combined/agent PYTHONPATH=/tmp/rt-m1-realpath-combined/runtime:/tmp/rt-m1-realpath-combined/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration /tmp/rt-m1-realpath-combined/runtime/tests/test_timeline_commit_integration.py -k 'not door' --basetemp=/tmp/rt-m1-realpath-targeted-2` => **4 failed, 1 deselected in12.38s**. Every node reaches actual capture/provider/Runtime acceptance, then receives422 invalid_prepared. Underlying packaged schema error at `PreparedCommit.canonical_document.internal_timeline_revisions[*].payload`: `Additional properties are not allowed ('assets', 'audio', 'effects', 'layout', 'registry' were unexpected)`. `contract/schemas/timeline-commit.json` InternalImage.payload currently references TimelineConfig (line286), but main's real canonical internal revision is a different payload shape. The seed is the accepted main API film fixture (three shots, transcript/text binding, music/fade/transition); stripping its legitimate fields or bypassing validation would falsify the gate.

Failing nodes in `tests/test_timeline_commit_integration.py`: `test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip`; `test_real_inverse_preserves_newer_disjoint_work_and_original_recorders`; `test_real_same_value_publication_is_recorded_and_blocks_older_undo`; `test_real_track_create_and_inverse_keep_complete_film_closure`. Door lost-ACK/restart node has not been run (central-only sockets). Recommend Runtime wire/validator owner reconcile canonical internal payload schema with main's actual accepted immutable shape, regenerate/pin official artifacts, then rerun final integrated tuple. No product changes or test weakening made here. Stopping at this concrete owner blocker as assigned; final report records all unverified assertions.
