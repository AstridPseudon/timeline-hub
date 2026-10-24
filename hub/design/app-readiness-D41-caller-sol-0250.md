**READY — both existing P2/P3 caller rows now qualify on the authentic D41 backport.** Atomic replacement preserved all 248 outside rows byte-for-byte. App worktree remains clean; commit message and `DONE` written.

Qualified identities:

- App: `804134d74782d40855146aa568ff289200b79142`, tree `8437e47666853b62e03a58af3716235346316fba`.
- Agent: `079580ca46af77e0292d49dc34386b25c8391f99`.
- Runtime: `37eb6c7bdb79dcae2523883e66b5cea5be721ffd`, tree `be4114705127f9ee9e86b26cd6de3f467e771c01`.
- Client identity: `18f0ef33b9b9b981a43b3e4de907df9d62178335e6709da52dfc124ef4f6382f`.
- Child key: `5464e85332660e8d6d133653d0600709f2aac5a6c9a0ff0e0bc1fb18312d7f2f`.
- Child registration: `venv-agent-child-app-ready-079-37eb-0256`.
- Remotion reuse: `agent-remotion-app-ready-079-37eb-0258`; unchanged tree `b01dca9b3b24f54093c20b7c5657316f997725db`.

All four isolated imports resolve inside the new immutable child. Installed backend bytes match the backport. Node `20.19.4`, npm `10.8.2`, receipts, and all 80 graph files verified.

With `T=/tmp/w-02466b7c0d`, final validation commands passed:

```bash
python "$T/check-d41.py" venv-agent-child-app-ready-079-37eb-0256 agent-remotion-app-ready-079-37eb-0258
TMPDIR="$T/qualify-d41" python "$T/qualify-d41/qualify.py" # 24 passed
TMPDIR="$T/stages-d41" python "$T/stages-d41/stages.py"   # 28 passed
TMPDIR="$T/extra-d41" python "$T/extra-d41/extra.py"      # 4 passed
python "$T/install-d41.py"
git diff --check
```

Controls cover actual argc2, decoded Bash syntax, authentic source and real-Git snapshot positives, strict refusals, exports, ordering, consistent ports, and failure closure. Initial scratch recovery runs had overlapping/rebound-file failures; the final isolated runs passed.

Final SHA256 values, including row newlines:

| Bytes | SHA256 |
|---|---|
| P2 | `17fa3a1252db65c15463e97f97df9eac11434976933a066c16aa3e8b04ca7197` |
| P3 | `0a36ea3419a1ff589f094d712678045476ec68d9a4f938af43185a7e41ad2ca1` |
| Outside rows | `b33d30918d6e2ae039dfa296bc75b1e0b2674828b53f07a16ee029933d5ad734` |

A new child was necessary under the installed backend-key and source guards; the unchanged Remotion graph reused normally. Bodies, native21 assertions, history, readiness, 5000ms wait, 90s owner wait, and final tails remain intact.

Independent review reports 145 passes on Agent4151. The separate Agent079 result remains **144 passed, one baseline-reproduced failure**. Actual native/browser journeys remain unverified; historical hang cause remains **UNKNOWN**. No provisioning or test-service requests were submitted here.

App/Proof may now submit the authorized pair:

```bash
"$O/bin/request-test" app-readiness-D41-caller-sol-0250 full-e2e-three-products --no-cache
"$O/bin/request-test" app-readiness-D41-caller-sol-0250 ap2-P3-gate5-h6-0348 --no-cache
```

Use the supplied ORCH path for `$O`, then follow each returned `wait-test` command.