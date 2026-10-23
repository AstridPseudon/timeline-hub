## Result: PASS with custody limitation

- No source, test, fixture, helper, generated-file, pin, or Git changes.
- Integrated Agent: `c36ca8c94b695b0e25b7d42c89f194661f187423`, tree `50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92`.
- Runtime: `8ea0766f5e9fb23cea26c7398770a8aaac06b258`, tree `6047ac3033c3594b8f83db3afd8bb2c47cafa6d6`.
- Source integration preserved 47-path G5 scope, sole `document_diff.py` deletion, 3,391 outside paths unchanged, +87 reviewed mirror-guard lines, R1/A4 critical files and `runtime.lock.json` unchanged.
- Retired-writer grep, vendor lock, artifact manifest, diff check, and clean-worktree checks passed.
- Reused exact-source quality evidence: Ruff 112 and mypy 104 diagnostic identities unchanged from 2141.

### Targeted proof

The mandated 16-file command from worker 2148 passed exactly once:

```text
350 passed in 100.57s
```

No test was rerun by this audit worker.

### Live SDK/c271 proof

Separate fresh-process commands from worker 2149 passed:

- SDK-four selectors: `4 collected, 0 deselected`; `4 passed in 34.02s`, exit 0.
- c271 selector: `1 collected, 0 deselected`; `1 passed in 39.24s`, exit 0.
- D21 preflight passed for both processes.
- Runtime origins stayed at `/home/user/work/wt/rt-pin-8ea0766f/runtime_protocol/__init__.py`, hash `4e4064e1…`, before/after each observed case.
- Body locks matched all four SDK tests and `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
- Durable logs record SDK4’s 49 packets and c271’s 81 packets, including guarded no-write/head/history-preservation assertions and zero credential findings.

The 350-suite import probes are not treated as per-case Runtime provenance; that claim comes only from the dedicated 2149 observer runs.

### Custody limitation

The 130 raw integrated observer packets under `/tmp/w-81dac9a766` are absent. They were not reconstructed or claimed durable. The surviving 1.44 MB worker log preserves the commands, exits, source/runtime identities, body locks, packet-count summaries, and observer assertion results.

The prior c271 source-stage archive remains durable and verified:

- SHA-256 `3040be2f…`
- 81 packets
- 1 passed in 40.92s
- It is historical source-stage evidence, not the current integrated packet set.

No full/P1/P4/browser suite was run. Overall final delivery gates remain outside this audit’s scope.