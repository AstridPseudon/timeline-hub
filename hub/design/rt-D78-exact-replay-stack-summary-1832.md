# D78 exact retained request: blocked on original state

No daemon, browser, provider execution, HTTP request, signal, or debugger attachment ran. No blocked frame or hang cause is established. No early refusal was produced or counted as a resolved hang. No product, test, kit, generated artifact, pin, shared dependency, or Git reference changed. No unapplied causal hunk is justified.

The retained packet is available and verified. Its raw UTF-8 body is 4,459 bytes with SHA-256 `e58a09dcafa9fc499448d216d48a1e17f6ee326123e0a3281c169b20ab92b992`. The private packet file SHA-256 is `2ed85677c85e2d6ab389e9c2a60d3ada737d3c4b2425e3154dd8fa552a6e2d5b`. Parsed body equality and header/key equality pass. This verifies the supplied packet, not an emitted replay or independent comparison against the absent original trace files. Raw packet, body, URL, key, header values, credentials, and private scope identities are not copied into this evidence directory.

All four sanctioned checkout receipts, full SHAs, tree hashes, and clean working trees match the packet. Runtime remains captured `327da207ed30880fe2ae0cd0b116722bb2c6f7a6`; newer Runtime source was not substituted. Full identities and seven caller/source file SHA-256 values are in `audit.json`.

## Precise missing original state

Owner: App lane / Timeline Child 1, original producer `app-P2-22847-phase-producer-1753`, original run `app-pin-587316e3-d73-p2-current-1747-1024175319-22847`.

Required: an authentic original realm or supported consistent snapshot retaining `realm/realm.sqlite3`, its CAS objects and revision/publication closure for the packet's existing project, timeline, and base pair, plus its authoritative history/idempotency state. Also required is the original support/credential custody needed to start that realm and authenticate the product through its normal Runtime door: support discovery/configuration, original hosted-origin binding, and product credential file (or a genuine supported newly provisioned credential for that same authentic realm). New session credentials would be explicitly distinguished from absent original auth bytes. No original realm directory or snapshot path is supplied by the packet.

The packet's referenced original run directory and manifest are absent locally. Its original trace ZIP, diagnostic file, and extracted network/body files are also absent at their recorded paths; the newly supplied packet itself remains usable. There are zero top-level `/tmp/astrid-direct-*` directories in this worker environment. This does not prove no archive exists elsewhere; no accessible archive is identified by the handoff.

Captured App harness source creates a private `astrid-direct-*` temporary directory (`tests/e2e/local/support/harness.ts:599`), places its realm/support/product credential underneath it (`:560`), provisions the credential through Runtime (`:783`), and removes that directory in normal teardown (`:1390`). This is source evidence about lifecycle, not an observed deletion from the original run.

Original Authorization/Cookie headers and cookies are explicitly absent from the retained packet. Browser auth headers are not replaced or invented: captured Runtime door uses its own provisioned product credential (`runtime_protocol/door.py:586-608`) and rejects browser Authorization/Cookie headers (`:539`). The original credential file is separate state that this packet does not retain.

The retained nine headers also lack `Origin`. Captured door admission requires the configured Origin at `runtime_protocol/door.py:532-533` and explicitly does not accept Referer instead (`:526-528`). Sending exactly those retained headers would therefore fail door admission on an otherwise valid matching listener. That conditional source result is not an observed replay response, and absent retention does not prove the browser omitted Origin on the wire. An invented Origin or direct authenticated transport would change the replay and cannot establish the original hang cause.

## Caller and stack facts

The normal captured App launcher starts `runtime_protocol.cli start` with realm/support paths, door origin/port/credential, and `--authoring-profile astrid` (`tests/e2e/local/support/harness.ts:687-706`). Its authoring restart uses the existing Agent interpreter (`:675-684`). The trusted provider factory is `astrid.sdk.timeline.commit.create_runtime_commit_service` (`runtime_protocol/timeline_commit_provider.py:19`). Importing that factory under the captured Runtime/Agent PYTHONPATH succeeds in the existing Agent venv and yields the synchronous `RuntimeCommitService` from the captured Agent source.

The production path is door admission/dispatch (`runtime_protocol/door.py:510-556`) → `commit_timeline` (`runtime_protocol/service.py:2435`) → `_execute_timeline_commit` (`:2450`) → coordinator (`:2499`) → synchronous `provider.commit` (`runtime_protocol/timeline_commit_execution.py:87`). Provider execution is in-process by this source path. There is no observed daemon process shape or provider request thread because the missing original state prevented launch/replay. These locations are not blocked-stack attribution.

No >10-second pending owned request exists. No faulthandler registration or signal was attempted. Installed-tool discovery found no `py-spy` and found `gdb`; neither was invoked. No unowned/original PID was targeted. Stack file/line/wait/call and request startup/admission/provider/response durations are unavailable, rather than zero. Audit-only timings: packet verification 0.626 ms; checkout verification 479.798 ms; total audit 704.558 ms.

## Verification and disposition

Exact audit command (exit 0):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-pin-327da207:/home/user/work/wt/agt-pin-f4d6c72c /home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D78-exact-replay-sol-1832/evidence/audit.py
```

Output was retained in `audit.log`; exit 0 means the read-only audit passed, not that replay passed. `git diff --check` exited 0; `git status --porcelain=v1` was empty. No test suite was run because source/tests are unchanged and authentic replay prerequisites are missing. No safety or permission refusal occurred.

Next: original App state owner identifies an authentic pre-request realm/snapshot and normal credential/origin custody, and resolves the unretained Origin from genuine evidence. Resume on the same captured tuple; retain the exact body/key, record any credential/origin changes separately, and capture all threads only if an owned replay genuinely remains pending. A new seed or a new realm would not preserve this packet's base/history state and is not a substitute.
