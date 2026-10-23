# Runtime R2r handoff: normal sequential input classification

**Status: PASS for classification / FAIL for qualification / HOLD.**

Runtime 859 correctly refuses the moved-head Agent peer-1335 step-2 request because its original unlanded physical ID is not in the authenticated landing boundary or accepted-history continuation map. The issue is normal sequential-step input authority, distinct from inverse-leaf materialization. The Agent provider candidate is held; no Runtime code, test, contract, wire reference, pin, or generated file was changed.

## Owner disposition

The original sequential authority input is already present in the Agent 1335 flat capture and must be verified. Agent owns the source-bound claim/capture transport. Runtime owns the existing refusal and the future narrow verification seam. There is no evidence for a guard waiver, blind retarget, fabricated continuation, or contract escalation.

## Evidence

- Agent candidate: `851439d95647820815e69b4d7163e179540f28db` (held).
- Runtime: `8592822fd11275540f596562f43c715676f2bc0f`.
- Agent review: `e44b4854ce32db55d922b27352cee20589d48e45`.
- Flat packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R1-sequential-current-runtime859-packet-23d309fb6f841fbb.json`, SHA-256 `23d309fb6f841fbba8560317c336b495ec4fcf2700a7e4c69bb7e1ea5c0f7ca7`.
- Exact qualification: `2 failed, 7 passed in 8.95s`. Fresh head and five strict refusals pass; only the two moved-head positives fail.

## Causal seam

`timeline_commit_store.py` builds landing source, base, and accepted-history continuations. `timeline_commit_auth.validate` validates request reads/step claims against the landing `boundary`; `site` only follows unique authenticated shot/internal continuations. Later `command_inputs` are derived from earlier command outputs, but the submitted step-2 original alias is still normalized at the landing boundary. Therefore the original unlanded Agent-generated ID is refused as `invalid_records: provider alias is outside its authenticated boundary` before write/accept.

Required proof before a future code task: original staged ref/path, original revision/content digest, source step/ordinal, base/evaluated head, owner and complete owners, exact landing/replay ref/digest, authenticated source-to-landing mapping, and complete request/reads/order/dependency/effect custody. Preserve foreign/stale/owner/ABA/no-write refusals. Do not reuse inverse-stage history or invent a continuation.

## Recommendation

Keep 851 unmerged, G5 draft-only, P1 NO-GO. Re-open only when the flat artifact is available in the normal hub and the bounded Runtime verification seam is explicitly authorized.
