## Report

Found the shared REG14 boundary: 18455 exports `ASTRID_REMOTION_PROJECT_DIR` and `PYTHONNOUSERSITE=1`; unchanged host code reaches `probe_context()` and rejects `PYTHONNOUSERSITE` before host launch or Runtime execution. This explains all 14 REG14 failures as an environment/launcher issue, not a proved product regression.

Relevant source blobs match exactly between `a4e016b6` and `96df3f5b`. The bounded 1345 PASS lacks a complete environment receipt, so the prior no-Remotion-branch explanation remains explicitly limited.

Evidence:

- [wholepath.json](/home/user/work/wt/agt-F-D134-host14-wholepath-1948/evidence/wholepath.json)
- [per-id.json](/home/user/work/wt/agt-F-D134-host14-wholepath-1948/evidence/per-id.json)
- [findings.md](/home/user/work/wt/agt-F-D134-host14-wholepath-1948/evidence/findings.md)

Validation commands:

- `python3 -m json.tool evidence/*.json` — PASS
- REG14 accounting: 14 IDs + 1 separate host-bootstrap UNKNOWN — PASS
- Relevant Git blob equality check — PASS
- `git diff --check` — PASS

No tests or product commands were run, per task restrictions. Raw XML/runner receipts remain unavailable. Recommended owner: D73/full-measurement environment setup; retain a complete prior-vs-current environment receipt before any rerun.