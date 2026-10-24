Completed the one-node D40 closure: **201+1=202 closed; 66−1=65 open; total 267**. All other 266 node records, prior proofs, historical 172/95 and 179/88 counts, and 59 mapping members remain unchanged. Mapping now has **60 members**; active families sum to 65, owners to **59+2+4=65**.

Updated only these five artifacts:

- [Corrected JSON](/home/user/work/wt/agt-F-count-D40-delta-sol-0558/evidence/agent-D32-current-node-reconciliation-H30-corrected.json)
- [External SHA](/home/user/work/wt/agt-F-count-D40-delta-sol-0558/evidence/agent-D32-current-node-reconciliation-H30-corrected.sha256)
- [Delta CSV](/home/user/work/wt/agt-F-count-D40-delta-sol-0558/evidence/agent-D32-current-node-reconciliation-H30-delta.csv)
- [Mapping JSON](/home/user/work/wt/agt-F-count-D40-delta-sol-0558/evidence/agent-D32-current-node-reconciliation-H30-delta-mapping.json)
- [Limits](/home/user/work/wt/agt-F-count-D40-delta-sol-0558/evidence/agent-D32-current-node-reconciliation-H30-limits.md)

Final JSON SHA-256:
`3cce6b4c4e36e4fe7e65f99d9943706d2c84b2e84026e456d4d5ff7a68fb56fb`

Checks passed:

- `python3 "$TMPDIR/verify_d40_count.py"` — exact delta, counts, CSV/JSON, hashes, scope, retained origins, 32 custody hashes, and three assertions.
- `git diff --check` — exit 0.
- From `evidence/`: `sha256sum --check agent-D32-current-node-reconciliation-H30-corrected.sha256` — OK.

Retained 0551/0552 qualification supports this one original only. Older installed markers and 0520/0612 limits remain explicit; no whole-current-HEAD installed or second generic_host credit. No behavioral tests or probes ran.

Commit message and `DONE` written. No blockers. Next: independent package review.