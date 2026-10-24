**PASS — export custody only.** Seven files in `evidence/`, all `0600`, totaling 116,840 bytes:

`aba3783-log.txt`, `aba3783-request`, `aba3783-summary`, `aba3783-exit`, `aba3783-status`, `aba3783-capture.jsonl`, and [aba3783-manifest.json](/home/user/work/wt/agt-F-ABA-capture-export-return-sol-1055/evidence/aba3783-manifest.json).

The manifest records source paths, byte counts, full hashes, modes, and retained printed guards. Copies match the service originals and saved 1040 evidence.

Capture: **22,725 bytes**, SHA-256:
`d78efa41a224585476d025d6200e016420ec93131efc744ce92d04830055fde0`

Verification passed: inline `python3` copy/framing/JSON/parity checks, independent manifest recheck, `sha256sum evidence/aba3783-*`, and `stat -c '%a %n' evidence/aba3783-*`. No product tests or execution performed.

Original test remains **FAIL, exit 1**. Run 3783 stopped inside `undo_session.undo`, line 1088, before predicate 41; 41–59 remain unrun. Prior 20732 failed predicate 42: expected `transport_error`, actual `transport_timeout`; 43–59 remain unrun.

The packet explicitly marks `provider.return`, `close.return`, `lookup.2.return`, and `send_hook.call` absent. Its exact JSONL contains **42 records**, differing from the brief’s 43-event statement; no bytes were altered.

No blockers or product changes. Commit message and `DONE` written. Viewing can review the export; completeness establishes neither completion nor acceptance, and Viewing retains the verdict.