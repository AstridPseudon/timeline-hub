# U3/D141 handoff

## Return required

Do not normal-merge or freeze this candidate as source-qualified. The App source owner must restore the upstream tour gate in `src/tools/video-editor/components/AgentChat/AgentChat.tsx`, preserving the current-parent availability door and unified AgentChatMenu behavior. The required behavior is:

1. import `TourChatPanel` and `useEditorTourRunning`;
2. evaluate the tour-running predicate in `AgentChatPanel`;
3. return `<TourChatPanel isExpanded={isExpanded} />` before live session hooks mount;
4. retain the current `isTimelineAgentSessionsAvailable` door for non-tour renders;
5. rerun the affected 15-file targeted suite and scoped checks.

This is an owner-return source REG, not permission to weaken or xfail the protected TourChatPanel tests. The reviewer did not apply the fix.

## Generated dependencies still deferred

After source repair and review, the manager still needs qualified final Agent/Runtime inputs, then the existing manifest updater and vendor refresh/verifier. The observed Runtime head does not match `runtime.lock.json`; historical vendor reproduction does not qualify the two known merged vendor mismatches. No guess pins are acceptable.

## Evidence boundary

The candidate has both required parents, no conflict markers, and clean static/lint/type/installer checks. Central targeted evidence is 14/15 files and 484/497 tests passing, with the 13-test TourChatPanel failure explained by the missing gate. No full suite, browser journey, build, ZIP, or merge was run.
