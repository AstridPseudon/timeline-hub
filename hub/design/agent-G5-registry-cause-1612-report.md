# G5/R2 registry-cause report — agt-G5-registry-cause-1612

## Disposition

**Source classification: PASS. Behavior: FAIL. Capture custody: PASS.**

This is a read-only, offline source-cause report for Agent `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee` plus Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2`. No product, test, schema, client, pin, environment, inverse, public-body, or Git change was made. The existing R2 owner remains the sole inverse owner; no competing author is proposed.

The precise first source boundary is Agent `astrid/sdk/timeline_restructure.py:507-509`, in `split()`:

```python
parent["registry"] = registry
if isinstance(config.get("registry"), Mapping):
    config["registry"] = copy.deepcopy(registry)
```

The fixture's source `config` had no `registry`, so the forward stage intentionally retained absence in `parent.config` while creating `parent.registry`. The native handler then whole-assigns `parent.config` and separately assigns `parent.registry` (`astrid/sdk/timeline/native_restructure.py:64-69`). This is the first omission; it is not a Runtime SQL or historical-503 cause.

## Full causal rows

| Row | Captured fact | Source-backed consequence |
|---|---|---|
| Forward source candidate | `split()` line 507 writes top-level `parent.registry`; line 508-509 mirrors only an already-present `config.registry`. | `parent.registry` becomes present; `parent.config.registry` remains absent. No absence-to-`{}` normalization is justified. |
| Native forward before/after | Packet events 152/153 record `parent.registry: {}` → `{"assets": {Q,R}}`; `parent.config` before/after has no `registry`; `derived_writes` is empty. | The native command's authored effects preserve the asymmetry exactly. |
| Accepted forward canonical closure | Event 154 (`timeline.restructure`, accepted) has top-level `parent.registry` with Q/R and `parent.config` without `registry`. | Forward acceptance and canonical materialization preserve the source asymmetry. |
| Native whole-undo before/after | Events 259/260 record `parent.registry` Q/R → `{}` and `parent.config` from the forward config → the original config, both without `registry`; `derived_writes` is empty. | Whole undo is accepted with the same absent config mirror. |
| Accepted whole-undo canonical closure | Event 261 (accepted), event 264 state snapshot, event 317 post-failure snapshot, and event 320 `before_forward` all show top-level `parent.registry: {}` and `parent.config` without `registry`. | Document/head/history/SQL are stable and the reconstructed redo input is genuinely absent at `parent.config.registry`. |
| Inverse canonical closure | The inverse accepted record carries `parent.registry` after `{}` and `parent.config` after the no-registry config. | The record itself does not claim that the canonical config had a registry. |
| Inverse guard seam | Event 312 expects `parent.config` with `registry: {}`; event 313 throws at `_recording.py:286`, called from `inverse.py:640`, via `commands.py:250` and `commit.py:1072`; `commit.py:1204` translates it to `inverse_conflict`. | The inverse alias/coalescing seam maps the separate top-level `parent.registry` effect into the `parent.config` root guard, creating an expected `{}` at a site whose captured closure is absent. The guard is correctly strict for the supplied expected value; it must not be waived. |
| Runtime/transport | Event 315 is the surfaced HTTP 409 conflict. | Runtime correctly reports the Agent provider refusal; no Runtime production cause is evidenced. |

All non-registry keys at the failing `parent.config` address compare equal. The only difference is expected `registry: {}` versus actual absence. The accepted canonical result, head, history, and SQL are unchanged before/after the failed redo.

## Precise bounded proposal to the manager

Keep the forward source semantics and previous-value guard. Assign the existing sole R2 owner to make inverse alias folding presence-aware at the exact parent-registry/config-mirror seam: when accepted history shows a top-level `parent.registry` write but the authored `parent.config` mirror was absent, preserve that physical authored address and its absence instead of synthesizing a `parent.config.registry` expectation. The repair must retain the strict before/after guard and must not normalize absence to `{}`, waive the guard, or change public request/reply shapes. Leave `_step_undo`, `_root_inverse`, `inverse.py`, and inverse-only `_commit_patch` untouched in this diagnostic; this report only identifies their seam for the already-assigned R2 owner.

The distinct R2 `a29df82beb548306...` shot-id packet and nested `3a718d9537faec49...` packet concern native physical/source correspondence. They are not this G5 parent-registry closure and are not a common cause by assumption or evidence.

## Immutable minimal input facts and hashes

- Agent base: `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`; Runtime: `9ce4242bc01f100bab9efc51032a73985cefb2b2`.
- Original body: 6,798 bytes, SHA-256 `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
- Immutable packet, absolute path `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/evidence/agent-G5-redo-budget-1605-7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15.packet.jsonl`, SHA-256 `7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15`, 320 events, contiguous 1–320.
- Prior immutable report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-redo-budget-1605-report.md`, SHA-256 `6f9ebc37365cc2957bdf3238e9a9920b507b62a9db7e0ea98de9168a12b9b116`.
- Captured source hashes: `_recording.py` `85aefe0328a7c9787a18c2b7e19eb8b3e4220a1c53627d1e16102b42b29c8b43`; `inverse.py` `fdae9b17f000a6968009222233327a0662748d0289d090a03c36f0e213121ee7`; `commit.py` `741e8afcca27577e3a620b60351880a8df60aa2f4b48f15e0961fb63695edabc`; `native_restructure.py` `800247535bbe034777fe84beb0612d96ea11992f8d77ad52ba7503dff56afb43`; `timeline_restructure.py` `842850e1e867eaf2a8c003897b6624bb040a2b7c8f910eecad1d5aa8c9f851ee`; `_command_state.py` `5584a8d08edecf480aa223c3dcf73a5e3064cee14758ebbeef19836043db0384`.
- Relevant packet event hashes: 154 `6449766aac5a77a48b7cf8db71db7e3450158d4fe544dd931420982b0a378031`; 261 `8b107c7cf7eae14429f0afa084c2e32881a95601abde658ad1ab61c84ce452ef`; 313 `2ffe29f6ed255b3dad51c672a48a46723faade69dcbf9ba23107cfd5324baaba`; 315 `aa60fb9545ff94aa977df047aaddec7401de29022b3e22f1ead4dc536d4bb225`; 320 `c896a47e605de931dbdfacd59dc80930a6b0da68dcec3b9bc1219afcb388f057`.

## Checks and limits

Read-only commands run:

```sh
sed -n '1,240p' /tmp/.../scratchpad/orch/PLAN.md
sed -n '1,320p' /tmp/.../scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/report.md
nl -ba astrid/sdk/timeline/_recording.py | sed -n '240,330p'
nl -ba astrid/sdk/timeline/inverse.py | sed -n '609,653p'
nl -ba astrid/sdk/timeline/commit.py | sed -n '1060,1078p;1190,1206p'
nl -ba astrid/sdk/timeline/native_restructure.py | sed -n '64,69p'
nl -ba astrid/sdk/timeline_restructure.py | sed -n '476,510p'
sha256sum <packet> <prior report>
python3 <read-only packet event/count extraction>
git status --short
```

Results: source/packet inspection PASS; packet count and contiguous sequence PASS; current worktree clean; no test suite was run because this task made no product change and explicitly forbids a new public/body attempt. The packet proves the observed stack, closure states, and no-write comparisons. It does not prove a historical 503 cause, and none is inferred.
