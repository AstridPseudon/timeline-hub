# Agent peer request: cache extraction owner gate

Please run the normal Agent owner gate and merge-queue review for the exact
candidate below:

- branch: `tl/vw-m4-cache-extraction-owner-handoff`
- commit: `32c72018d7c8fbeab5c3596d638ce4a3bb0b060d`
- parent/base: `f711cbd29be0b0cb1a51328ea5093b954db3c158`
- report: `design/handoff-vw-m4-cache-extraction-owner-handoff-REPORT.md`
- flat patch: `design/handoff-vw-m4-cache-extraction-owner-handoff.patch`
- file list: `design/handoff-vw-m4-cache-extraction-owner-handoff-FILES.txt`

The candidate is the existing cohesive extraction only: two files changed,
`filmstrip_cards.py` restored to `1917` lines, and all key/PNG/source/
fallback/no-mint assertions remain in the unchanged test suites. Prior
evidence is 133 + 55 + structure 1, plus import-focused Ruff, on this exact
tree. Please decide normal owner approval/merge; this request does not ask to
activate cache behavior or retire D09.
