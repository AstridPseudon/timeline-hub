# D141cc handoff

Status: **COMPLETE — independent read-only whole-path investigation**.

Result: preserve the native implementation and treat the popup outcome as cancelled custody, not a functional popup failure. Placement `9168` remains the only bounded PASS. Popup `13234` and `20413` remain cancelled with UNKNOWN body verdict; six selectors remain NOTRUN. No D141j diagnostic exists.

The concrete future path is in `source-map.json`: one production caller/tool session invokes the unchanged builder; the builder derives the exact recipe, registers two rows, persists the artifact, takes the existing artifact file lock, requests preflight, waits, requests one normal ID, then the daemon snapshots/runs the original body and `wait-test` returns the durable receipt. The C0 request/reply shape is unchanged.

The review-next private model cannot be adopted as native proof. R1 is a synthetic retry command/row; R2 permits two normal calls in a preflight/normal interleaving; R3 ignores a same-source wrong command/row instead of refusing. These are candidate-procedure findings only. No new interface, kit, guard, lease, authorization, or product fix is proposed.

Smallest safe future procedure: retain one submit owner/tool session; inspect and adopt exact authoritative existing IDs under the unchanged builder lock; never manually repeat a normal request because an artifact is incomplete; stop finitely on unknown owner, mismatch, ambiguity, missing receipt, or safety refusal. Do not resume `13234`/`20413` or backfill their body.

Inputs read include Main D141cc 10:28–10:29 decision, contract §§1–7, independent 1026 custody packet, review-next originals, genuine builder, registry, queue/request/wait scripts, and retained result artifacts. All output paths are absolute and private to this worker.
