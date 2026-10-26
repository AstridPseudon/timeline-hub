> **Superseded (26 Oct, 20:00 UTC).** The current, self-contained version is in `../followups/` (start at `followups/README.md`). This file is kept as a source only.

# Follow-up: App catch-up onto the latest upstream

- **Why:** the ZIP's App targets upstream fc24f849 (owner option B, D141jj). Upstream has moved on (00a014e2 at 13:33Z, 4e667aa5 by 18:48Z).
- **Ready:** catch-up candidate eac97ea5 (onto 00a014e2), built and unmerged. It needs re-basing onto the current tip.
- **Known cost:** the merge touches the paths of all 8 journeys (review 1317), so 7 journey re-proofs plus a full unit pair against pristine.
- **Next step:** App lead re-reads the upstream tip, merges, runs the targeted tests and the full pair, then re-proves the journeys.
