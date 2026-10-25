# F-D86 D106 opaque6 source handback

Disposition: **SOURCE-QUALIFIED / BEHAVIOR-PENDING**. This is an authorized source publication only; it is not a functional PASS, full-core result, retirement, normal merge, or proof from the D106 source0537 body run.

## Exact source and receipt

- Source candidate: `3c742a9cfa1509234ca70048612e7302e4e2298c`, parent `6aefd11766c019f8deff0ca5a1bfe18e9e730822`, tree `f41fe5094b2ea419117a7023ffcae0be3198cfca`.
- Listed source path: `tests/editing_conformance/test_commit_runtime_opaque_items.py`.
- Source blob: `339bf63752f509c1c0cb6b1fce30cda385dd2065`; SHA-256 `3a5558085a78f3d8558219921da81029b3cb648e876b84eaefaf713d1e6e722a`.
- Independent review: `rt-D86-opaque6-protected-0517-report.md`, 1941 bytes, SHA-256 `7980b50aba9454fa929e438b16137f00876cae22c2a5707b49c03ab312dfa8d3`, **PASS_SOURCE**.
- Normal receipt: `fd3cbf2b1a9adf772296f54c23649673c054e9b6` (`normalfd3c`), the normal publication pair for this source.
- D106 source body: `rt-D86-new-source-body-0537-report.md`, 1364 bytes, SHA-256 `c5ca88d0db6866f502b01ddac116912c01acbe704a1f851dc3d928591b664cce`; its 60-case body was bounded NO-GO (3 failed, 57 errors), so it grants no behavior credit.

## Conservation and boundary

The protected review records all six parametrized cases (two tests × `item_id`, `id`, `both`) and all 29 original assertions. It explicitly preserves unknown opaque values, IDs, metadata, physical closure, revision pins/digests, timing, graph and branch topology, retry/restart, inverse, refusal, ABA, and no-write guards. The authored setup lane copies the exact ordered `doc.patch.args.changes` into `steps[0].patch`; it does not filter fields, mutate `created`, or alter request/step `reads`. The production route remains the registered `commitTimeline` provider.

This handback keeps the D72 source-qualified / behavior-pending boundary. Historical failures remain failures; no new functional PASS, `fullcore`, retirement, D103 duplicate, D100 fixture-valid claim, or normal-merge claim is made. No source acquisition, stage product merge, or `/home/user/timeline-hub` write was attempted.
