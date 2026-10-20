# Decision needed: incompatible implicit preview/export defaults

Source-backed followup to0554 frame triage. Full flat report design/handoff-vw-m3-default-theme-owner-proposal-REPORT.md; production/test examples UNAPPLIED beside it.

Existing Agent exported-film default is navy #050814/Arial/cyan, while App and public Composition absent-theme default is black/Georgia/white. Same ID banodoco-default, different full styles (size, weights, lineheight, fadeMs too). Both existed before this migration. Frame fixture has no theme override and actual normal export uses Agent builtin; Player ground is independently hardcoded black. Existing App test positively requires its default. No single implicit result preserves both conflicting outputs.

Do NOT accept the worker's literal compatibility-copy adapter or it.fails marker as a qualified fix: candidate ordinary existing App test is RED (53PASS/1FAIL), and copying another theme authority is undesirable. Agent targeted15PASS and frozen-host3PASS establish the exported default is real, not a guessed theme. Custom runtime-pinned theme transport and nested merge-policy differences are additional unqualified cases; no new DTO proposed.

Recommended policy for owner/orchestrator: preserve existing final-export style as the default shared host theme; explicitly approve/document the corresponding change to implicit App preview. Then implement the smallest common-source adapter under owners' review (avoid long-term copied literal), update the original ordinary test to that explicitly approved behavior, and include default-theme differences in owner-local film viewing guidance. An alternative must name which existing output remains authoritative. No film rewrite or hidden fixture theme override.

Meanwhile the capture fix/frozen candidate are ready; no broad render retry on a known default mismatch. Mouth/scanner/current public10 review continue. Gate6 stays OPEN.
