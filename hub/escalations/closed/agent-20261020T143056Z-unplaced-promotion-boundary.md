# Decision needed: unplaced project-shot promotion
Agent and Runtime agree current CanonicalDocument/ports cannot safely mutate an unplaced project shot.
Real native witness: create occurrence -> remove it retains project shot byte-equal/readable, while canonical closure has no shot; injecting it as orphan refuses. No SQL/fake history.
Evidence: design/agent-native-candidate-promotion.md and runtime-unplaced-shot-promotion-carrier.md; Agent pure198 + real-provider1 pass.
Original Runtime promotion positives remain OPEN (atomic primary/superseded, fixed-point invalidation, provenance refusal, exact receipt/replay); adding an opcode cannot preserve them through current film history.
Recommend classify this bounded capability as project-catalog infrastructure, like retained reference catalog: preserve the EXISTING project-scoped promotion operation/atomic receipt outside accepted film history.
Every film placement/selection still uses guarded EditCommands; immutable timeline pins and C4 global-head protection stay unchanged. No dummy parent/library timeline, DTO, table, journal or new endpoint.
Please approve this boundary or name the intended accepted-history carrier; no implementation/public freeze presumed. Other deletion work continues.
