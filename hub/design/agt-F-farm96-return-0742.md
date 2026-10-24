Implemented the corrected evidence packet in only:

- `farm96-causes.json`
- `farm96-causes.csv`
- `farm96-causes-source-and-limits.md`

Changes preserve all 96 members, raw offsets, hashes, source limits, 88+8 cohorts, and 80/1/15 classification. Replaced Farm failure excerpts with scoped prior-proof references; recorded 96 qualified references, zero missing, no duplicate credit, and distinguished old Runtime45c from current authenticated f320. Added exactly one current giant-file challenge.

Validation:

- `python3 -m json.tool farm96-causes.json` — passed
- Standalone JSON/CSV preservation validator — passed
- `git diff --check` — passed
- No product, test, probe, browser, full-suite, or new-source execution performed.

Unverified: independent docs repair and production v2 caller qualification remain outside this packet.

Commit message and `DONE` marker are ready.