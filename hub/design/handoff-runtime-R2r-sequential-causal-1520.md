# R2r sequential causal recovery — FAIL qualification; Runtime history fix BLOCKED

No product/test/contract/schema/client/pin edits, service writes, body retry, merge, push, or Git mutation. Runtime remains `85b2feeb58bc54174ac7b89fda4805883865d3b2`; Agent source is exactly `67ba416bca813f4931b557f6f2ca2abf935d7d35`.

## Precise causal result

This is a **Runtime-owned accepted-history revalidation defect**, not an Agent duplicate-read defect. The four original positive bodies returned accepted/merged in 1512, but that is not four passing original tests. Original stdout remains `..FF.`; five strict negatives are unqualified.

Both moved cases deterministically reproduce the same failure using the actual retained inputs and production Python functions, without constructing a service or writing a database:

1. `timeline_commit_store.py:255` calls `validate` from `_verify_accepted`. Its request is constructed from `_history_metadata` plus stored commands/base pair. The metadata does **not** include submitted `steps`. It provides neither original `base` nor request-private `sequential` proof.
2. `timeline_commit_auth.py:2193` → `validate_bindings:448` tries to resolve the second command's original intermediate physical ref against the independently reconstructed landed input. That original image was never an accepted-history revision, and the genuine peer history plus already-landed step cannot map it to the landed intermediate.
3. `timeline_commit_auth.py:173` raises `CommitRejected("provider alias is outside its authenticated boundary")` with HTTP 422, code `validation_error`, reason `invalid_records`. `timeline_commit_store.py:296–297` wraps it as `ProtocolError("accepted commit record is corrupt")`, code `protocol_error`.
4. The existing `WorkspaceClient._call_generated` and `RemoteTimelines._typed` turn that exception into a failed `DomainResult`, so the original test's line 109 obtains `history = None`. Executing the **unchanged original AST at lines 109–110** then raises **`TypeError: 'NoneType' object is not subscriptable` at line 110**, `entry = next(row for row in history['items'] ...)`, in both moved cases. The expected value is an iterable history page containing the accepted publication; the actual value is `None`. This fails before the later record/digest assertions, rather than failing one of those assertions.

| Retained capture | Original case | First rejected binding | Original unlanded revision suffix | Landed revision suffix |
|---|---|---|---|---|
| 12 | moved=True, declared=False | command 1, binding 0, `doc.patch:0` | `45745d4892f6f656e1650246ecbac69fcf25c24281c47d429d5de2267edcfb53` | `b53f0a012472c5dbbf4ab1b3cb5d0b5d9b631c459d068db7aab9eeb6bee2677b` |
| 17 | moved=True, declared=True | command 1, binding 0, `commit.read` | `24968c839d1289f983481193058256606226a038b0d4af92e791db141a3b402d` | `0c49b3c179af18d23a8c356fdccafad487dd43b1c767d75d0789dd2089ba20c6` |

All four captured prepared-record sets pass every reconstructed boundary/head/ordinal/step/digest comparison. There are **14 passing binding digest comparisons**, including the three declared-read bindings in each declared case. Each expected input is reconstructed by the real unchanged Agent `execute` from captured `source_closure`, not by trusting a provider snapshot. Current-head captures 03 and 07 pass the exact historical `validate` call. Both moved cases fail that call and the actual `_verify_accepted` method before any uncaptured raw event rows are read.

An earlier exploratory replay used the full submitted request and failed sooner at `validate_step:399`/`:329`. That is **not** the production history path. The final retained reproducer uses `_history_metadata` exactly and records the actual `validate_bindings:448` path above.

## Evidence and limits

[Flat manifest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/r2r-causal-manifest-ded0a0f97c1017841ea8b50d7beaa82c80c2d37c959f192097fc76c4715f2432.json) — SHA256 `ded0a0f97c1017841ea8b50d7beaa82c80c2d37c959f192097fc76c4715f2432`.

The manifest covers **26 immutable flat hash-named JSON files**, each under 1.3 MB: all **20 capture files copied byte-for-byte**, complete 1512 observer/source/log snapshots and prior interrupted log, exact Agent assertion source and adapter source, diagnostic script/output, all original assertion comparisons, inventory, credential scan, and preservation checks. All hashes were verified; zero credential-key/value-pattern findings. Original worker evidence is unchanged. Capture 18/19 are trailing peer observations; they do not establish completed negative assertions. They lack some pre-validation observer fields, faithfully retained without filling them in.

The offline comparison records every one of the **20 assertion source locations** in the positive body, across all four parameter combinations, and marks all four assertion locations for each of the five negatives unverified. **156 available comparisons pass**. Some compare retained candidate/result projections, not original post-acceptance reads; each comparison states its provenance.

The original pytest longrepr is **not recovered**. Exact original raw SQL dump lists, post-preview/post-acceptance document reads, post-acceptance history response/page, final retry reply, and after-retry history page were not captured. The history row/ledger projections used to call `_verify_accepted` are explicitly reconstructed from retained request/prepared/result/receipt with the exact `_publish` and `_history_metadata` code. They are not claimed as recovered raw SQL rows. No current head or event sequence is invented. The accepted candidate and genuine peer history are actual retained values. The two TypeError traces are **new offline reproductions of the original AST tail**, not a historical pytest report or a new public original-nine run.

Reproducer: [rt-R2r-sequential-causal-resume-1534/offline_compare.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-sequential-causal-resume-1534/offline_compare.py). Detailed comparisons and full exception chains: [offline-comparisons.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-sequential-causal-resume-1534/offline-comparisons.json). Log: [offline.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-sequential-causal-resume-1534/offline.log). Run the reproducer command below from the specified Agent checkout to avoid Runtime's `tests` package shadowing Agent's. The test module is additionally loaded by exact importlib file path.

## Commands and results

Executed from `/home/user/work/wt/agt-pin-67ba416b`:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-R2r-sequential-causal-resume-1534 PYTHONPATH=/home/user/work/wt/agt-pin-67ba416b:/home/user/work/wt/rt-R2r-sequential-causal-resume-1534:/home/user/work/wt/rt-R2r-sequential-causal-resume-1534/packages/python /home/user/work/venv-agent/bin/python /tmp/w-24af835d08/offline_compare.py
```

**Exit 0:** 156 available comparisons/14 binding digests pass; two current historical-validation calls pass; both moved historical-validation calls reproduce the expected defect; both actual original AST tails raise the exact TypeError at line 110. These are diagnostic expectations, **not product conformance PASS**.

```sh
python /tmp/w-24af835d08/export_packet.py
python /tmp/w-24af835d08/finalize_packet.py
git diff --check
git status --porcelain
```

Export: 20 lossless captures. Final packet: 26 files, scan PASS, preserved original Agent test byte-equal to commit 67ba. Finalizer initially encountered absent `credential_clean` in trailing peer capture; inventory now records that missing field without fabricating it, and final run exits 0. `git diff --check`: exit 0. `git status --porcelain`: empty. Sources unchanged, so no static diagnostics could have been introduced by this worker.

No new pytest suite was run: there is no meaningful safe product correction. Retained independent 1512 evidence remains **353 Runtime tests passed in 80.78s**, including **44 verifier tests**, Ruff **22**/Pyright **80** baseline diagnostics, **0 added/0 removed identities**. This worker did not rerun or requalify those suites. No full/58/40/281/native14/browser/P1–P5 suite was requested.

## Blocked correction and next owner

The explicit task instruction says **“do NOT touch ... history authority”**. The required correction lies in that exact authority path, `runtime_protocol/timeline_commit_store.py:_verify_accepted` and `runtime_protocol/timeline_commit_auth.py:validate_bindings`. There is no safe one-line fix under the remaining constraints. Passing `base` alone cannot make an original unlanded intermediate resolvable at a landed step; skipping the alias check, projecting submitted refs onto landed refs, trusting self-consistent snapshots, or adding an accepted-history continuation for an unlanded original would weaken the guards explicitly required by the task. None was attempted. No Agent edit or Agent-owner handback is indicated by this evidence.

Recommended next step: assign a **Runtime historical-verification correction** with explicit authority scope. It must reconstruct original command/step inputs from the authenticated base and actual preceding original execution and reconstruct landing inputs from the accepted head/preceding landed execution, while preserving exact submitted refs, unique mapping, native/effect/materialization coverage, owner/read/ordinal/ABA/history/forgery checks, and single-use private capture behavior. Use this packet as the causal regression input. After a meaningful correction, run the scoped 353/static/frozen checks and then the one original-nine with durable per-node pytest longrepr and pre-validation captures. No body retry is justified before that correction.

Report-only source **NEVER MERGE**. Integration merge hold remains in force. No settled PLAN/C0 decision was changed.
