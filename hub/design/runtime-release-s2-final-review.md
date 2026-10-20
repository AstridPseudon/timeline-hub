# Final composed Runtime S2 release review

**APPROVE the final composed S2 candidate at `f7081c14efd9a5b834987e7a1e2abf597b66313b`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`. No blocking finding in the composed release diff.** This reviews the complete candidate, not the individual staging releases. The local compose branch, harness commit, handoff, all 45 changed-source blob IDs and all five final service snapshots agree. Parent is `8609333456b9537339ee1a5dfc7ffd9609242de8`. Initial tree `790b87ee2b5c84cf926ccd8198fbb8878e1ba4da` is superseded and is not approved.

This is source and bounded qualification approval of the unpublished consumer target. Publication, consumer pins, activation and qualification of a subsequently merged integration tree remain manager actions. No such action was performed by this reviewer.

## Ranked findings and limits

No new blocking P0/P1/P2 defect was found. Two proven inherited limitations remain explicit:

1. **P2, generation proof limitation:** `generators/generate.py:148–157` still reads the checked-in package TypeScript HTTP implementation as input. Its generation check proves a fixed point, not reconstruction of the whole HTTP implementation from an independent template. The changed DTOs, Python client/root exports, installed schema bundle and TypeScript native export line were independently reconstructed after deleting them in a private archive; all source bytes were recovered. The separate conformance TypeScript client is normally emitted from its generator and byte-matches the final source. This is the already accepted proof boundary, not a new release regression.
2. **Existing behavior gap, outside this release diff:** final targeted evidence retains `tests/test_timeline_text_selection.py::test_clear_removes_the_live_binding` as its original strict xfail: text-binding removal is not projected. The entire file is byte-identical to the base. This review does not claim native text-clear completion or hide that failure. No passing behavior test was rewritten to expect refusal or absence.

Consumer qualification is a remaining handoff dependency, not evidence against this source composition. Agent caller branch resolves to `0cfdddd5b85d5a32e5319365e64cb58293381490`; its actual live SDK/CLI/client-pin pairing is not established by these Runtime results. App's accepted inventory has no production persisted-view invocation; copying its final client and matching pin still belongs to App. Browser views remain denied by the unchanged door policy. Nothing here proves an App browser journey, full Gate 5, frame/audio parity, F3/capture pairing, macOS or owner-film readiness.

## Composition and behavior verification

Read PLAN first; read composer HANDOFF/DetailedReport/source inventories and prior contract/client, connector rejection and repair, union, view rejection and successor, F1/F2 current-gate, producer current-gate and main-refresh reviews. Decisions were preserved. Independent checks compared all **413** candidate blobs with the Git tree and all **3022** files of the actual frozen Agent provider archive with Agent `26ef2bbb31b4892fdd7c15ee5b20700bd40cb933`.

| Boundary | Proven result on the final tree |
| --- | --- |
| Current Runtime safety and main behavior | Removing exactly `create_timeline_view` and its added decorator from both service versions yields identical bytes. `server.py` byte-matches approved `44bf744`; its diff from the base changes only views to `projects:write` and forwards the key. Store, daemon, door, visual seam, commit store/port/producer and original producer-boundary tests are unchanged. Thus F1 occupied-destination refusal, F2 legacy-document/headless refusal, main worker credentials without owner-token alias, advisory render seam, disk estimates and producer normalization retain their current implementation. The new regression lanes cover F1/F2 and producer neighbors on this composition. No old whole-file replacement or dropped guard was found. |
| Approved inputs | Ten authored paths exactly match connector `78d14ec045c9b67f32ac2b340c48d4ae9b715345`, union `438a9cf0beaaa599f31370f231e4307403e204d4` or corrected view `44bf74420c1276aae86928f6b2416190fc97b1c7`, as enumerated in the source inventory. Relative to `438a9cf`, `generate.py` adds only the exact S2 floor entry. Connector implementation and 43-case test file are byte-exact approved input. Public `OperationHandle`, `OperationHost`, retirement error and identity/connection exports survive. |
| Persisted view authority and retry | `service.py:2553–2600`, `server.py:585–587`: explicit key, write authority before service, ordinary durable mutation/replay seam and plain response. Fresh unchanged reviewer probes prove denied readers and malformed/missing keys make no SQL/CAS/staging changes; read-only inspect remains pure; changed-body and foreign-route replay refuse; lost response + head advance + restart returns original artifacts without ingestion; expired replay refuses while verified custody remains. Existing MD/PNG tests compare exact renderer bytes and cross-key deduplication. |
| Both TS clients and Python | Package method at `packages/typescript/src/generated.ts:185` and conformance method at `conformance/typescript/generated.ts:196` require four arguments and forward `Idempotency-Key`. Both original transport probes pass; public API and conformance smoke retain missing-key expected errors. Python's template and generated client require the keyword key and preserve the plain response; its main-suite transport test passes. No receipt envelope was added to views. |
| Parent publication documentation | Final OpenAPI includes the approved eligibility description and all three 409 reasons: `timeline_commit_required`, `stale_head`, `headless_content_not_empty`. Publication code is byte-unchanged; this restores documentation only and revives no writer. The initial missing-description failure is superseded by the final passing parity lane. |
| Schema and DTO preservation | Raw command schema equals actual Agent S2 bytes: `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`, **48 defs / 22 ops**. S2 differs structurally from S1 only by optional `ClipSetElementArgs.schema_source: DocumentPin` and description. All five complete compatibility floors and every fixture's actual Git provenance pass; S1 and old fixtures remain immutable. Installed bundle differs only in its Agent resource. Both Python modules and TS retain all **99** previous DTO names: **98 identical**, one gains only optional `consumed`; **19** names added. Old root exports remain. The same **133 HTTP operation IDs** remain. No F3, parent-birth, native text-clear or unfrozen operation was added. |

## Final release identity

All individual artifact digests were recalculated from actual final-tree bytes; aggregate hashing was independently reproduced, rather than trusting a freshness command alone.

| Item | Verified value |
| --- | --- |
| Client release | `0.2.13` |
| Schema digest | `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4` |
| Artifacts | **75**, including `operation-handle.ts` |
| Artifact version | `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56` |
| Raw artifact manifest SHA256 | `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497` |
| Component manifest SHA256 | `1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |

## Exact-tree evidence

Read each service `summary`, `snap`, `exit`, full log and external-head record where present. Reused these results without resubmission; every snapshot is **7ab412cc4bcbe517efcfa806e092336390312e18**, every exit is **0**.

| Service TestID | Result |
| --- | --- |
| `rt-m2-release-s2-final-compose-targeted-1020110503-8618` | **800 passed, 1 deselected, 1 unchanged text-clear xfailed**, 173.56s |
| `rt-m2-release-s2-final-compose-ts-client-check-1020110503-30973` | Build, strict public API compilation; **61 passed / 0 failed / 0 skipped** |
| `rt-m2-release-s2-final-compose-commit-integration-1020110503-17965` | **9 passed**, 8.92s |
| `rt-m2-release-s2-final-compose-occupancy-integration-1020110503-17107` | **1 passed, 17 deselected**, 1.19s; covers the targeted lane's marked occupancy case |
| `rt-m2-release-s2-final-compose-producer-agent-s2-integration-1020110503-5266` | **5 actual passes with `--runxfail`**, 3.06s |

The last lane uses the verified immutable Agent S2 archive and registers its native commit provider, with `ASTRID_RUNTIME_CHECKOUT=$PWD`. It executes the original numeric Node-forwarding/preview/accept/restart/exact retry/one-shot/undo positive and four immutable-artifact mutation negatives. It is neither a fake-provider positive nor an absent-provider skip. Ordinary commit/occupancy lanes instead record external Agent `6a59522421a8a5c0e93fca080aa2d1fd478952f1`; those runs do not establish an immutable four-repository tuple.

Fresh reviewer checks: **7 socket-free Python cases passed in 5.57s** (four existing main-suite cases and the three unchanged earlier authority/replay probes); **2/2 original TS transport probes passed**; required-key typecheck and independent conformance compile/smoke passed. Normal generator/check/manifest commands passed, six deleted outputs and the TS native export were restored byte-for-byte, and normal conformance emission matched both client outputs, eight fixtures and the component manifest. Exact commands and logs are in [DetailedReport.md](../workers/rt-m2-release-s2-final-review/DetailedReport.md). A private checker initially mapped emitted fixture filenames to the wrong source layout; correcting that checker mapping yielded the passing comparison, with no product change.

No full suite, broad repeat, service request, live socket/browser run, repository edit, publication, pin change or Git mutation occurred. Shared dependencies/caches were read-only. The assigned repository remains clean. Review complete, no blocker.

Manager next: preserve the required semantic-view-before-artifact sequencing, requalify the resulting actual integration tree, pair the final client/pin with Agent's caller port and App's copy, then perform the separately owned publication/consumer checks. If source advances, review its actual diff and updated identities; this verdict is tied to the exact commit/tree above.
