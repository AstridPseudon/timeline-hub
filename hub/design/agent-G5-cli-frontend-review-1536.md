# G5 CLI frontend independent review

2026-10-23 UTC: bounded source review of \`cc8be25d4ad46fae3f7d0889aaee88f85ab6a9c6\`.

**PASS for the bounded frontend scope; not a cumulative G5/P1 PASS.** Normal
CLI \`undo --commit\` and \`redo --commit\` use the existing public
\`TimelineSession.undo\` full-v2 path. Numeric local undo/redo remains local.
The public client shape was checked against \`RemoteTimelines.history(project,
ref, *, cursor=None, limit=50)\` and \`RuntimeRevisions.list\`; immutable
history head/ancestry, exact receipt/base/previous pair, project/timeline
closure, publisher/provider/compiler identity, label/steps/merge metadata,
ordered batch selection, and accepted-undo-only redo checks are covered.
Unknown, forged, cross-scope/ambiguous, mixed draft/numeric, and retired
overwrite selectors are refused before write by source logic/tests where
applicable.

Targeted evidence: 57 parity + 6 neighboring local/status + 1 hint + 4
public-history adapter nodes = 64 distinct passing nodes. Mypy findings 88/88
and Ruff findings 16/16 against an exact archived parent baseline, with zero
added identities. Vendor lock, artifact manifest, and diff check pass.

Limits: tests use the existing in-memory \`DetachedPort\` and derive metadata
from its prepared provider records; they do not prove a real Runtime socket,
authorization boundary, App journey, or full G5/P1/R2 qualification. No full
suite or known-failed R2 body/restructure/redo repeat was run. The target
commit also includes an extra design draft beyond the stated three CLI plus two
test files; this review did not alter it. Worktree remained clean.

