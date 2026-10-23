# Handoff: ap2-P1-raw-trim-review-0212

**Verdict: FAIL.** Reviewed `f88759e3f` against `914afe21`; no repo changes.

The requalification keeps the five trim guards (`hold`, `from`, `to`, removal of `app.astrid.for` with `19`, and removal of `app.astrid.until` with `null`), one outbox intent, original basis/created guards, and no-send assertion. The trim and all targeted tests passed in the central service (3 files, 28 tests).

The oracle change is not equivalent: `authoredPayloadClosure()` compares only payloads, while the old assertion compared the complete canonical document. The separate identity check covers only project/timeline ids and the parent revision id/digest. It omits schema/root metadata, dependency-manifest membership/order/identity/digests (including media/documents), and child/internal revision wrapper identity/order fields. `parentOnly()` does not make that omission safe because manifest media/documents remain, and the helper would remain weak for a non-empty closure.

Recommended minimal correction: clone `after`, bind only its parent revision id and content digest to `before`, then compare `local` to that complete expected document. Do not qualify H3: the production caller is still unmounted and the local-only pass is explicitly not GO. Request/response ABI, conflict/invalid details, and authenticated preview/history remain unqualified.

Local exact Vitest command: 20 passed and 8 sandbox `spawnSync git EPERM` failures; typecheck, lint, and `git diff --check` passed. See the worker `report.md` for full commands.
