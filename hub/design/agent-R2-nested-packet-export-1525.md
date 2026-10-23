# R2 nested packet export 1525

Evidence-only publication for the Runtime counterpart. The Agent base `58316fd6e0ce8a1fb3b2b3826ec71906d29080de` was treated as read-only. No product, test, validator, schema, client, pin, archive, lock, dependency, daemon, Git, or shared-environment change was made.

## Published artifacts

- Source-complete packet, copied without transformation: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-staged-redo-1500-3a718d9537faec49.json`
- Packet manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-nested-packet-export-1525-manifest.json`
- Independent review, copied byte-for-byte with its final verdict unchanged: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-nested-contract-review-1515.md`
- Export report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-nested-packet-export-1525.md`

Source packet and published packet are each 4,790,931 bytes with SHA-256 `3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09`; `cmp` passed. The requested digest is SHA-256, as confirmed by the source `packet-manifest.json`; it is not a SHA3-256 digest. The independent source report and durable report are each 832 bytes with SHA-256 `4eced28cb1c8894e89270e86eacc888a52fc2ea76dbb0bf0af15a43bf6f80c8d`; `cmp` passed.

## Independent verdict and ownership seam

The independent diagnosis records diagnostic fidelity **PASS (8/8)**, strict candidate behavioral acceptance **FAIL (1)**, and retained controls **PASS (14)**. The strict positive fails on the unchanged competing-selected-media compiler guard before Runtime acceptance. Normal public `timeline.inverse` targets one `undo-0` with two inherited ordered source stages. The outward two-group candidate fails Runtime's expected-one-stage condition; the compiler strict-positive failure is a separate competing-selected-media failure. Runtime owns private authentication of the nested ranges under one outward public step. No public carrier, schema, or history identity change is proposed or inferred.

The production caller's C0 v2 request shape remains fully in scope: `api_version`, project/timeline scope, exact `base_revision_id` and `base_publication_id`, `commands`, `label`, `steps` (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge` (`fields` or `atomic`), declared reads, idempotency key, `dry_run`, `source`, `rationale`, and `group_id`. Replies remain accepted/merged canonical result plus receipt, records, bindings, effects, dependencies, history, `undo_steps`, preview with required `would_status`, and structured `code`, `path`, `head`, `hint`, and `suggested_command`.

## Exact verification commands and results

```bash
wc -c "$SRC_PACKET" "$DST_PACKET" "$SRC_REPORT" "$DST_REPORT"
# 4790931 source packet; 4790931 published packet; 832 source report; 832 published report

sha256sum "$SRC_PACKET" "$DST_PACKET" "$SRC_REPORT" "$DST_REPORT"
# packet source/published: 3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09
# report source/published: 4eced28cb1c8894e89270e86eacc888a52fc2ea76dbb0bf0af15a43bf6f80c8d

cmp -s "$SRC_PACKET" "$DST_PACKET"
# PASS
cmp -s "$SRC_REPORT" "$DST_REPORT"
# PASS
```

The source packet's embedded manifest was also checked against the supplied packet size and SHA-256. The copied report was not edited, summarized in place, or replaced.

## Limits and test disposition

This is an evidence export only. No product/test/fix/validator body was repeated, and no full, P1–P4, native14, V4, browser, live-socket, daemon, hand-provisioning, or shared-install run was requested. The packet's retained evidence reports Ruff `2149/2149`, mypy `1912/1912`, diagnostic `8 PASS`, strict positive `1 FAIL`, and retained controls `14 PASS`; those results were not rerun here. Runtime should receive these exact facts through the durable hub paths above, not worker-local links.
