# AP2-M2 ordinary membership conversion review

**APPROVE** the five-member ordinary assertion conversion. The action uses
`visualClips(snapshot)` without filtering; canonical projection order is the
two parent clips followed by the three `f2-occurrence` child clips, so the
truthful batch is ten commands (move + hold for each member) with selectors:

```text
parent/clip:f2-app-clip
parent/clip:f2-transition-clip
occurrence:f2-occurrence/clip:f2-plate
occurrence:f2-occurrence/clip:f2-agent-clip
occurrence:f2-occurrence/clip:f2-agent-clear-clip
```

Existing canonical owner-qualified identities, source mapping, selection
proof, occurrence intent, static-duration carrier, transition retention, and
opaque preservation support these members. The move-before-hold intervals are
all within the 12-second occurrence; no fixture or intent correction is
warranted. Existing Agent/lost-ACK/restart/retry/undo/zero-legacy assertions
remain real and the generic batch is atomic, not filtered partial success.

Evidence reused: Vitest 1 file/45 tests passed; ESLint passed; `git diff --check`
passed. No old-source rerun, browser/socket/full/Runtime-door/central gate was
run. Native acceptance remains unverified pending the known stale App
`TimelineOps` adapter fix.
