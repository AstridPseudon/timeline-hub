# D124 host14 fallback map — candidateNOTAPPLIED

## Result

No safe product fallback hunk is established. The only qualified upstream-behaviour fallback is an exact environment/source tuple, not a change to this Agent worktree:

- Agent: `b742893426a46a99a2f30583a54faeebe2bd98b7`, tree `ccb2f286eae9419b95a3f54b11208f68c57b27cf`.
- Runtime: `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`, tree `1d3e06f4d59ed6d459646d24ab185c36eb5be075`.
- Pristine comparison: Agent `08e6b905114a3ee2b05c3e7980421f26b4abf15c`, tree `2694ae8d2709526b40fa037bda8b159cf412769d`; its host source and b742 host source are byte-identical.
- Central proof: `runtime-d118-upstream23-targeted-1025130322-26621`; 14 passed, 0 failed, exit 0, 2.29s.
- This is not proof that current normal `5caa12bda353cc46143d3125bce60f8019cf839d` works with its current Runtime boundary.

## Exact source map

Current normal host source is `astrid/sdk/host_bootstrap.py`, SHA-256 `c05d1566ab1932e0018e387426dca0962059e335b85b7eded4b89f15f40e4b78`. Pristine b742/08e6 host source is SHA-256 `5064b2d6fb4d256c8e7be9355fd4f80560ecdbe83cceddb054d9d36bdf97732c`. The four delta groups are:

| Current hunk | Current behaviour | Disposition | Reason |
| --- | --- | --- | --- |
| `_provision_render_runtime_env`, current lines 463–498 | Resolves the selected Agent's canonical timeline schema through `verified_schema_path`; checks source path, symlinks, owner/mode, Runtime lock pin/digest and canonical reader boundary. b742 uses the older Remotion `node_modules/@banodoco/timeline-schema/python` path. | RETAIN | Removing it drops source/hash/symlink/owner/refusal controls and changes the selected schema authority. No C0 exception permits that. |
| `_installed_execution_origins`, current lines 710–769 | Uses non-importing `PathFinder` resolution for eight origins: host, child, action, client, sdk, `runtime_protocol`, `runtime_protocol.platform`, and `astrid_runtime`; rejects foreign origins, symlinked parents/packages and Runtime aliases. | RETAIN | This is the strict installed source-origin guard. D40 requires captured source/custody checks; the original source-identity attacks must continue to refuse before foreign code executes. |
| `_prepare_render_validation`, current lines 796–843 | Carries the selected installed source root and closure digest into Runtime validation and worker probe environments. | RETAIN | This binds validation to the selected source closure and preserves Runtime-owned authority/custody. Reverting would re-open the live/foreign source boundary. |
| Call sites in `_ParkedPackHostPreparer.prepare` and `ensure_pack_host`, current lines 928–930 and 1651–1653 | Pass the authenticated closure digest into validation. | RETAIN | These are the call-site bindings for the preceding custody guard, not incidental host14 behavior. |

The current normal source does **not** contain the held D122 candidate's extra `_dependency_pythonpath` Runtime-root insertion (`9ea` lines 453–462), nor its `PYTHONNOUSERSITE` removal. Those held changes are not part of this fallback. The current normal source retains `PYTHONNOUSERSITE=1` at the child boundary as required by the farm recipe.

## Original14 identity and environment boundary

The untouched original test file in this worktree is SHA-256 `08dfa8dcafeb80c347923630864a29d58dea97e257428e204fc316567795161b`; it must remain byte-exact. The b742/08e6 historical test blob is a different whole-file hash (`8143c3741b1024612c6cb8017d17ee83bd69d5fb64db31fff2d25b3bf0b05362`), although the two requested original14 test-body hashes were conserved in the authenticated map:

- `test_bootstrap_stops_on_correlated_terminal_registration_failure`: `caa9ecdf6ce41fbb524aa2b4d45053b79f6986c62f3eb039bcadc00ef076e800`.
- `test_startup_budget_polling_preserves_identity_and_original_cleanup`: `186173e6c8d37445d2f575c9016861f1347e0b96155117f9ba2099ee0eff85e3`.

The known D122 REG14 cause was child registry discovery failing with `ModuleNotFoundError: runtime_protocol` at `astrid/core/rendering/remotion_runtime.py:26`; the terminal `RemotionValidationError` is only the wrapper. The upstream b742 proof passed because its authentic runtime boundary was the independently captured d4f496 Runtime pair. That is an environment/runtime boundary, not evidence that a product hunk may delete current source guards.

## Production path census

The production caller is `astrid/sdk/autobootstrap.py:497–500` → `ensure_pack_host`. `ensure_pack_host` invokes `_host_render_environment`, then `_prepare_render_validation`, then launches `astrid.core.execution.generic_host` with source checkout digest, source-closure digest, inventory identity, boot-manifest path/hash, credential file and Runtime endpoint. The parked path invokes the same environment/schema/validation helpers before its activation handoff. Child registry discovery then uses `build_child_subprocess_env`; installed mode explicitly removes `PYTHONPATH`, while source mode supplies the selected checkout plus approved dependency roots. `remotion_runtime.py` refuses unsupported Python startup variables, foreign installed origins and invalid schema paths before registry execution.

No caller writes timeline data here. The host path does not alter the C0 commit route, its request fields, or its reply envelope.

## Decision citations

- C0 `contract/commit-v2.md:60–274` requires the existing `commitTimeline` request, idempotency, CAS/rebase, semantic/doc.patch command envelope, labels/steps/reads/merge/dry-run and exact retry behavior.
- C0 `contract/commit-v2.md:276–595` requires verified closure-root identity, source/physical bindings, previous-value guards, managed-field refusal and authenticated allocation/restoration; a host fallback is not permission to bypass those checks.
- C0 `contract/commit-v2.md:595–702` requires ancestry, field/collection/atomic conflict guards and conservative scope dependencies.
- C0 `contract/commit-v2.md:703–1562` requires accepted/merged/conflict/invalid/preview reply semantics and guarded dry-run behavior.
- C0 `contract/commit-v2.md:1563–4543` requires authenticated whole/per-step undo, later-history scans and refusal on intervening writes or surviving dependents.
- C0 `contract/commit-v2.md:4544–4608` requires verbatim `meta` preservation and limits; `4609–` requires authoritative history/attribution and no parallel evidence ledger.
- D40 security review `runtime-D40-security-review-0240.md:4–9` says the Agent consumer must consume captured bytes or revalidate before execution, Runtime owner grants remain private/in-process, and the joined route fails closed before discovery. These are the exact security reasons the source/custody hunk groups above remain retained.


## Fallback acceptance

Use the b742/d4f496 tuple only if the manager's existing D124 condition requires action and only at the existing Farm venue. Accept only a fresh, authentic 14-node result with exact source origins, exact selector/member map, `PYTHONNOUSERSITE=1`, `-n 3`, timeout 45, unchanged budgets and original inputs, zero failures/errors/skips, and no poisoned/foreign import. Do not alter assertions, the original test, profile, installer, acquisition, source pin, or Runtime guards. A PASS from b742 does not authorize applying a product revert to current normal.

