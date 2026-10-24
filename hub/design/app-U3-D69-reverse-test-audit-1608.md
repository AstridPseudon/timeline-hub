# D69 reverse test audit

Completed read-only audit; no product, test, config, generated, pin, or worktree files changed.

Identity:

- Current: `HEAD 6d74fdd88abe2aacb5c605a443e473aaab99ad64`, tree `da2043257a6bce08b2ca37a98c49e53e530026a7`
- Upstream: `3881e9440688f774878e18806da2dc5c993a9b00`, tree `210e5739b838ef7655f87238c711704301d12846`
- Upstream is an ancestor of current.

Inventory:

- Upstream test paths: 1,343
- Current test paths: 1,483
- Common paths: 1,341; blob-exact: 1,284; changed: 57
- Upstream-only paths:
  - `src/tools/video-editor/components/AgentChat/NewChatMenu.test.tsx` — 49 cases
  - `src/tools/video-editor/components/AgentChat/TourChatPanel.test.tsx` — 13 cases

Parsed reverse scope: 1,474 upstream cases.

| Result | Cases |
|---|---:|
| Cleared | 1,403 |
| Cited intentional/D52 deletion | 67 |
| Restore-needed | 4 |

Restore-needed findings:

1. `src/shared/lib/placement/__tests__/placementService.test.ts:181`  
   Upstream stale-head retry case removed. Restore the exact positive assertions that a placement publishes once, retains the sibling, and preserves the placed generation.

2. `src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts:121`  
   Upstream “re-reads the head and re-applies the placement once” case changed to refusal. Restore assertions for sibling retention, created clip presence, and one publication.

3. `src/tools/video-editor/runtime/PanelFullscreenFrame.test.tsx:74`  
   Upstream shell-root/Escape assertions removed: portal parent must be `shell`, class must contain `absolute`, chat Escape must not exit, shell Escape must exit once.

4. `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx:880`  
   Upstream voice-off assertions replaced by positive recording behavior. This conflicts with existing `565d7a90ef` decision and current `CHAT_VOICE_ENABLED = false`; restore the gated negative/positive voice matrix.

Cited intentional cases:

- The 49 `NewChatMenu` cases are covered by the settled U3b decision to retire that split-menu path in favor of `AgentChatMenu` (`app-U3b-freeze-plan-0647.md:41`, `app-U3b-live-first-return-sol-2022.md:17`).
- The 13 `TourChatPanel` cases are intentionally not restored because the upstream test targets the removed tour switch; existing integration coverage is the replacement (`app-U3b-live-first-return-sol-2022.md:20`).
- Five deleted timeline command-runner cases are authorized by the `APP-A4-D37-EXECUTOR` D52 ledger row (`app-A4-current-ledger-1233.md`).

Prior exact evidence reused: six retained region hashes from `app-P2-P3-current-pure-proof-1322.md` (parent, transition single/bulk, element, register, placement), plus the prior D50/D53 and U3-final/D68 preservation records.

Checks:

- `node --check` passed for all scratch parser/comparator/control scripts.
- Scratch parser controls passed for preserved, dropped, and loosened-membership shapes.
- `git diff --check` passed.
- Worktree clean.
- Scratch evidence size: 9.7 MB.
- No Vitest, browser, native, HTTP, service, or full-suite run, per task scope.

Handoff markers and D69 commit message were written.