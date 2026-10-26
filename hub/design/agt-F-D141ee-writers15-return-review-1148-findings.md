# Independent return review: U2/G4/G5/F D141ee writers15

Verdict: `PASS_EVIDENCE`.

Behavior is separate and remains `REG_PENDING` for all 15 cases. No case is a
same-body/assertion current PASS, no case is REG0, and no owner retirement is
approved. The corrected return author is accepted as evidence because it
adjudicates each prior finding, preserves the restored originals, and does not
claim source-only replacement credit.

## Finite findings

1. **F1 — sampler:** The earlier author trace is not credited. This review's
   fresh `disk-trace.txt` is the only credited trace: it samples available bytes
   every five seconds and has the 4,000,000,000-byte stop condition.
2. **F2 — stale restoration:** The return author correctly removes the obsolete
   restore action. Tests were not restored or edited again; `445b9c1` and the
   HOME merge are immutable source coordinates.
3. **F3 — route retirement is not purpose retirement:** All 15 protected
   purposes remain REG-pending. Current commit selectors are proposals only;
   C0/G5 does not retire their assertions.
4. **F4 — force split:** Row 7 retains key/one-call/success/head/authority
   scope and separately requires explicit commit-path force refusal. No force
   adapter or overwrite path is permitted.
5. **F5 — live publish caller:** `_cmd_restructure` still calls `tl.publish`
   (`cli_working.py:470-504`), so the wrapper migration is not complete. The
   actual `_commit_document`, `_commit_restructure`, and `_publish_narration`
   mutations submit/flush through `TimelineSession` to `commitTimeline`; no
   second writer body is proven. Receipt, partial-error details, idempotency,
   no-retry, and both output modes remain pending on the actual caller.
6. **F6 — owner-scope presentation:** Row 8 remains pending for the exact
   three-line human summary and JSON envelope. Rows 12 and 13 remain separate
   editor-head and generic-head actor/presenter cases using C0 reason/head and
   no force option.
7. **F7 — exposed old surface:** `WorkspaceClient.publish_parent_composition`
   and RemoteTimelines dispatch remain exposed. Runtime's old route calls
   `_require_timeline_command` and refuses, but that does not retire the Agent
   surface or prove the protected row 15 behavior. No compatibility writer is
   added.

## Source path conclusion

The production commit path is concrete: `TimelineSession.submit/flush` →
`client.timelines.commit` → `WorkspaceClient.commit_timeline` → Runtime
`server._timeline_commit` → `RuntimeService.commit_timeline` →
`_execute_timeline_commit` and the mounted Agent provider. `RemoteTimelines`
creation and parent-media replacement use the same commit boundary. The old
parent-composition method reaches the Runtime refusal, not a writer, but its
Agent/Remote API surface still needs an owner decision.

The exact 15-case manifest, AST spans, source hashes, Git blob presence, and
machine checks are in `source-manifest.json` and `validation.md`.
