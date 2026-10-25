# D127c attach recipe and whole-path result

## Supported D66 identity

The supported diagnostic identity is the canonical basename `p2_commit_phase_capture.py`, resolved by the D66 helper guard from the selected Runtime checkout or an explicit absolute helper path. The guard requires a regular non-symlink file and an exact lowercase SHA-256. The candidate helper hash is `a92122c24afc581f71687d25ffc6a4bd8bb7c2e7381e5b47a6be861d23594a1c`; the normal integration Runtime helper remains `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`.

The ordinary D66 control shape is:

```text
D66_OUTPUT_DIR=<private-TMPDIR-child> <runtime-node> --import tsx scripts/testing/d66-plain-stack.mjs p2-element --submit
```

The D66 script validates the helper path/hash before launch, and the Runtime child receives the canonical helper by the D66/sitecustomize mechanism. This is a source recipe only; no production launcher, App pin, or body run was changed or credited.

## Actual mounted call path

The protected App Apply action is `ElementsLibraryPanel.applyElement` and submits `timeline.apply_element` through the mounted element adapter. The element save owner builds the next document, the commit session creates the durable outbox record, and the provider/client sends the Runtime commit route:

```text
POST /v1/projects/{project_id}/timelines/{timeline_id}/commit
```

Runtime `_dispatch` prefetches the body before `_route`, and `_route` reaches `RuntimeHandler._timeline_commit`, which reads the prefetched body and forwards it to `runtime.commit_timeline`. This is the genuine supported Runtime handler seam.

The App commit builder preserves the C0 v2 shape: API version, project/timeline scope, base revision/publication, native command objects, label, steps and patch, merge mode, reads when applicable, dry-run false, source, and the HTTP idempotency key. The Runtime reply remains the existing accepted/merged/conflict/invalid/dry-run contract with canonical document/digest, normalized command and identity/revision/landing data, receipt/records/bindings/effects/dependencies/history/undo data, or conflict/invalid diagnostics. The candidate only observes prefetched bytes and does not mutate request or response authority.

## Why this recipe does not qualify the candidate

The protected first element POST is `doc.patch`, not `clip.set-element`; later params are also `doc.patch`, and Undo is `timeline.inverse`. The candidate therefore does not attach to the intended first POST. Its direct handler exception test can also create a request without `_dispatch` provenance. Finally, the strict App validator rejects the new `cprofile` summary key and the candidate helper hash. Keep the candidate unapplied until the helper selector/provenance and scoped type diagnostic are corrected, then handle the App validator contract in its own authorized change.

