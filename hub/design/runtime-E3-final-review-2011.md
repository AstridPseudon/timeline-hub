# E3 first-return design review

**PASS** for `design/runtime-E3-audit-revised-2009.md` against `design/runtime-E3-review-2001.md`. This verdict closes the three bounded design corrections, not behavioral qualification, implementation approval, a delivery gate, or authority to merge. The original failed audit and predecessor review remain unchanged.

Reviewed PLAN §3 R1/R2/R2r, D81/E-PLAN, D47, D62, and C0 §§1–7, including the complete §1 request and §4 success/failure/preview examples. Reused the predecessor's 42-file source record; independently checked only the corrected anchors and nine associated fixed-tree hashes. No product imports or test bodies executed.

| Correction | Finding |
| --- | --- |
| Actual mounted App caller | Revised lines 20–35 and 103 correctly identify ordinary saving. At App `f6a21c285267d6475816adbda74233907ac93911`, `src/tools/video-editor/hooks/useTimelineState.ts:620` mounts `useTimelineSave`; `hooks/useTimelineSave.ts:319–323` constructs `createLocalSaveSession` with `send: provider.commitTimeline`. `commands/localSaveSession.ts:179–192` builds the scoped/base-paired v2 outbox request and sends its retained body/key. `src/integrations/runtime/dataProvider.ts:751–767` checks scope/base and rejects a null receipt, `client.ts:735–741` forwards the request/key, and `generated.ts:202–204` sends the commit POST and Idempotency-Key. `commands/commitSession.ts:238–250` separately selects `operation.transmit` for placement continuations. Pinned source search confirms command-session callers are tests, with no ordinary production mount. No App guard removal is proposed. |
| D62 submit-time gap | Revised lines 44, 58 and 113 preserve the limitation explicitly. Runtime `44917baf5976d6a655d582fafc63fde7b6cb242d`, `runtime_protocol/timeline_commit_store.py:1229–1236`, classifies accepted records by physical bindings and explicitly excludes a new submit-time completeness obligation. `tests/test_timeline_recorder_abi_authority.py:145–205`, `test_native_coverage_omissions_at_submit_keep_abi_two`, accepts omission packets, retains ABI 2 and requires exact replay. The revision retains this positive expectation and strict authenticated ABI/use-time behavior; it invents no native attestation seam. Assertion inspection is not a test result. |
| Exactly two finite helpers | Revised lines 73–99 preserve the predecessor's two candidates. Parent blocks at `runtime_protocol/timeline_commit_auth.py:2216–2224` and `2231–2239` total 18 nonblank lines; the helper must keep both calls, execution positions, pin selection, nonempty/unanimous revision/digest check, assignment and distinct messages. Owner blocks at `521–526` and `2451–2458` total 14; retain strict versus defaulted occurrence retrieval, duplicate/order behavior, short-circuit shot handling, direct internal lookup, image construction, nonempty refusal and existing set comparison. No first-owner substitution, inverse-comprehension expansion, hoisting or added authority is allowed. About −9 nonblank production lines / −1 to −5 physical repository lines remains an estimate, including eventual test/formatting additions. |

No blocking overclaim, guard deletion, new wire shape or authority boundary was found. Revised lines 47–71 retain native/ABI/event metadata, physical binding, aliases, reservation provenance, ABA, conflicts, CAS, exact retries, receipt equality and authenticated history. C0 continues to govern scope/base/commands, label, steps/patches/dependencies, merge, declared reads, idempotency and dry-run; accepted/merged retain full canonical data/digest, commands/map/versions/publisher/head pairs and durable receipt with `receipt.result == data`. Publication identity remains `receipt.receipt_id`, not a new result field. Structured conflict/invalid/refused and full preview with null receipt remain unchanged. Historical replay compatibility is not removed by this design.

The separate process-custody discussion at lines 37/59 must be read in its stated process-launch sense: the cited launcher is shipped Runtime source, as the predecessor noted, and its source/PID/role/cleanup controls remain intact. Calling that evidence HARNESS does not make it PRODUCT commit authorization or allow deletion of native process custody. D47 still excludes the deferred memo. No harness success or test provenance substitutes for receipt/history authentication.

The post-ZIP proving gate is coherent but unexecuted. In addition to unchanged authentication/sequential/history/inverse/forward-allocation/ABI/preview and Agent/App local-save controls, implementation review must demonstrate both parent branch messages and exact malformed, empty, multiple, duplicate and ordered owner behavior. The predecessor's named `test_created_child_public_acceptance_and_strict_refusals`, `test_coordinated_capture_record_map_and_digest_forgery`, `test_retained_real_capture_rejects_replay_forgery`, and `test_real_capture_requires_complete_ordered_correspondence` remain targets, not proof of unimplemented equivalence. Add necessary tests rather than weakening behavior, then count all added lines. A nonnegative complete diff earns no E3 reduction claim.

Recommend folding the two candidates into E1 after ZIP only when that migration already provides the implementation and proof. Otherwise retain the source; the tiny estimated saving does not justify forced complexity. D81 remains design-only and non-gating, with no integration merge or final-tuple change.

## Executed checks

Working directory: `/home/user/work/wt/rt-E3-review-return-sol-2011`.

- `git diff --exit-code` — exit 0, no tracked changes.
- `git diff --check` — exit 0, no whitespace errors.
- `git status --short` — exit 0, empty.
- `git rev-parse HEAD` — exit 0, `44917baf5976d6a655d582fafc63fde7b6cb242d`.
- Fixed-tree source/hash check below — exit 0; all nine hashes match the predecessor manifest; duplication inputs are 18 and 14; worktree/C0 design copies equal the pinned source. It reads source only and does not import product code.

Exact source/hash-check command:

```bash
python - <<'PY'
from pathlib import Path
import hashlib,re,subprocess
orch=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
manifest=(orch/'design/runtime-E3-source-checks-2001.md').read_text()
repos={'Runtime':('/home/user/work/runtime','44917baf5976d6a655d582fafc63fde7b6cb242d'),'App':('/home/user/work/app','f6a21c285267d6475816adbda74233907ac93911')}
slices={('App','src/tools/video-editor/hooks/useTimelineSave.ts'):[(319,323)],('App','src/tools/video-editor/commands/commitSession.ts'):[(238,250)],('App','src/integrations/runtime/dataProvider.ts'):[(751,767)],('App','src/integrations/runtime/client.ts'):[(735,741)],('App','src/integrations/runtime/generated.ts'):[(202,204)],('Runtime','runtime_protocol/timeline_commit_store.py'):[(1229,1236)],('Runtime','tests/test_timeline_recorder_abi_authority.py'):[(145,205)],('Runtime','runtime_protocol/timeline_commit_auth.py'):[(521,527),(2216,2239),(2449,2460)],('Runtime','contract/commit-v2.md'):[]}
for (repo,path),ranges in slices.items():
    root,sha=repos[repo]
    data=subprocess.check_output(['git','-C',root,'show',f'{sha}:{path}'])
    digest=hashlib.sha256(data).hexdigest()
    expected=re.search(r'\| '+repo+r' `'+re.escape(path)+r'` \| `([0-9a-f]{64})`',manifest)[1]
    assert digest==expected,(repo,path,digest)
    print(f'HASH MATCH {repo} {sha}:{path} {digest}')
    lines=data.decode().splitlines()
    for start,end in ranges:
        print('\n'.join(f'{i}: {lines[i-1]}' for i in range(start,end+1)))
    if path.endswith('timeline_commit_auth.py'):
        assert sum(bool(x.strip()) for a,b in [(2216,2224),(2231,2239)] for x in lines[a-1:b])==18
        assert sum(bool(x.strip()) for a,b in [(521,526),(2451,2458)] for x in lines[a-1:b])==14
    if path=='contract/commit-v2.md':
        assert data==Path('contract/commit-v2.md').read_bytes()==(orch/'design/commit-v2.md').read_bytes()
for name in ['runtime-E3-audit-revised-2009.md','runtime-E3-review-2001.md','runtime-E3-source-checks-2001.md']:
    data=(orch/'design'/name).read_bytes()
    print('DOCUMENT SHA256',name,hashlib.sha256(data).hexdigest())
print('SOURCE-ONLY CHECK COMPLETE: 9 fixed-tree file hashes; corrected caller, D62, two duplication inputs; C0 copies equal. No product imported or tests executed.')
PY
```

Reviewed document SHA-256: `d29d853194e4f5aa78ef4741f3e8f7e1953f9aab39b7fd6905669cef31e26e7d`. Predecessor: `c67caf688a5cbe690f025468dc5671f692f09c68c3a6e89c4497df31a8b05701`. Source record: `7db9168f155ef42f0dec3293094dc1c483de0e1be1e8f5ec0f0ada849e108a52`.

Additional exact caller checks (all exit 0):

```bash
git -C /home/user/work/app grep -n createTimelineCommandSession f6a21c285267d6475816adbda74233907ac93911 -- src
git -C /home/user/work/app grep -n 'options.send' f6a21c285267d6475816adbda74233907ac93911 -- src/tools/video-editor/commands/localSaveSession.ts
git -C /home/user/work/app grep -n useTimelineSave f6a21c285267d6475816adbda74233907ac93911 -- src/tools/video-editor ':!*test*' ':!*spec*'
git -C /home/user/work/app show f6a21c285267d6475816adbda74233907ac93911:src/tools/video-editor/commands/localSaveSession.ts | sed -n '176,202p'
```

No tests, browser/native execution, full suite, packages, daemon, acquisition, cleanup, or Git mutations were run. Product/tests/generated/pins/contracts and shared logs were not edited. Only this private review and required completion metadata are written; the harness produces report.md from the final message.

**Size/risk/gate:** bounded review under 1 worker-hour; proposal estimates 2–4 worker-hours for post-ZIP implementation/proof. Read-only review risk is low; eventual security-adjacent sharing risk is medium. Gate: exact post-ZIP guard/message equivalence, unchanged positive and hostile/replay controls, and actually negative total physical LOC. Implementation, behavioral equivalence, performance and actual net LOC remain unverified. Nothing blocked.
