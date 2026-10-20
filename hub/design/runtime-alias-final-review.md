# Runtime F3 final alias review — REJECT

Reviewer: `rt-m3-alias-final-review`, 2026-10-20. Assigned independent review is complete and unblocked. No merge is requested.

Reviewed `tl/rt-m3-alias-legacy-context-fix` at **aa784ab8fc0dc7df082d81b77eda998b46023eeb**, tree **9f569980c3da073c7537770e281ac15940bbeea8**, against original **6023cfb10307b4c0004642b5fa1995d72ba4f6d1**. The branch still resolved to that exact commit at final verification. Capture-validation SHA256: `25962634c8c186ef6fcfcfd6a0ac0ee732470b65b1bd9d33b67cb586d6fc823b`.

**A1's missing outer-context downgrade is repaired. A new same-digest collision prevents approval:** an invalid outer reference causes a genuinely valid nested reference with the same alias and object digest to lose saved/candidate authority. All three aliases reproduce it. The invalid reference itself is downgraded; no forged authority escape or stored-byte loss is claimed from these probes.

## Finding F3-R1: a failed claim poisons a different successful claim for the same bytes

At `aa784ab8:runtime_protocol/capture_validation.py:150`, failures are indexed only by `(alias + "_ref", digest)`. At lines 162–165 the recursive replacement uses that same incomplete identity. Revision, revision digest, source kind, scope and working-copy binding are not part of the match. Inspecting both authority contexts makes this observable even when the preferred nested context is entirely legitimate.

Concrete saved counterexample, reproduced through real pre-validation store admission and public `RuntimeService.claim_next`:

1. Publish the fixture's immutable `parent-1` closure. Register its **capable** `FrozenProjectionProvider`, whose `project_capture` returns the fixture's real frozen projection. Ingest the exact saved snapshot into CAS.
2. Nested `spec.authority_context.filmstrip_snapshot_ref` is a genuine saved reference. Outer `authority_context.filmstrip_snapshot_ref` points to the **same** CAS digest/project/timeline/revision but asserts a false revision digest. Include the genuine nested reference in `inputs.filmstrip_authority` and JSON-list copies in `inputs.argv`.
3. Call the real `validate_capture` separately: the nested reference returns `True`; the outer reference raises a Runtime refusal. This is not an absent-provider negative.
4. Admit the old envelope using `service.store.create_task`, with no capture-validator argument. This is the existing pre-validation store seam: the preferred nested reference passes store scope/revision validation. No new public admission validator is removed, monkeypatched or bypassed inside `RuntimeService.create_task`.
5. Public `claim_next` relabels **both** references to CAS. It also strips the successful nested reference's claims from the filmstrip JSON and list copies because they collide with the failed outer reference's key.

Exact first final-run example from `final-review.log` (the valid nested reference):

```json
{
  "digest": "sha256:6578f18cb83d16818ff4a36fdd49bdcb8df7e6aa81e609044eb5ff6aa46ce5bd",
  "project_id": "a43de964037c49858e991b758493034a",
  "timeline_id": "main",
  "revision_id": "parent-1",
  "revision_digest": "sha256:9e3c93e1cce58dddb37c775b2e1a0ee6c90548edbf3d8485d065472121052369",
  "source_kind": "revision"
}
```

The invalid outer reference differs only in `revision_digest`, which is `sha256:` followed by 64 zeroes. Expected: the valid nested reference above stays exact and only the invalid outer reference becomes CAS. Actual nested reference becomes just `digest`, `project_id`, `timeline_id`, `source_kind: "cas"`. The same failure occurs for `input_snapshot_ref` and `capture_snapshot_ref`.

Three additional counterexamples use **actual Agent df2739f903edac02bd36b4446deeea847524c040** candidate production and its real `RuntimeCommitService.project_capture`, without a prototype method or a replacement verifier. Produce an SDK parent-edit snapshot with its whole authoring preview; the good working-copy reference verifies. In an outer copy of the same reference, replace `working_copy.candidate_digest` and `revision_digest` with the zero digest. The real validator accepts the good claim and refuses the bad one. `claim_capture_view` then downgrades both. Each alias fails independently. These are pure claim-view probes, not host or public candidate-admission qualification.

The six strict preservation assertions fail. For every case the probe also executes the exact original `6023cfb` claim function against the same spec and service: the valid nested reference survives there. Original code leaves the invalid outer reference untouched (the already-known A1 defect); this comparison is not approval of that old behavior. It demonstrates that indiscriminately stripping the valid claim is a regression while repairing A1.

In the three public saved counterexamples, before reaching the failing preservation assertion, all checks for unchanged admitted spec/task-spec rows, canonical history/closure rows, CAS and staging bytes, and same-key original-spec store retry pass. The failure is confined to the worker's claimed view.

Required correction: distinguish complete authority claims when propagating a failed claim's downgrade. Exact duplicates of a failed claim must lose authority in every supported JSON/list copy, while a separately verified claim for the same bytes must remain exact. Preserve the two-context inspection and original A1 regressions. Add permanent same-digest mixed-success cases for revision and candidate bindings, all three aliases, and both JSON/list copies. Do not solve this by letting the invalid outer claim retain authority or refusing legitimate saved/candidate claims generally.

## Context precedence and repaired coverage

Read PLAN, COMMON, current Runtime manager STATUS (header 10:03:46Z), A1 in `design/runtime-capture-authority-review.md`, the source worker's DetailedReport, original reviewer probes, complete diffs and adjacent consumers. No settled decision was changed.

Actual consumer behavior:

- Runtime `snapshot_refs.rewrite_spec_snapshots:194–196` prefers a nested dictionary and otherwise uses the outer dictionary. Restoration follows the same rule at 258–260.
- Runtime `store._validate_spec_snapshot_refs:522–524` prefers a nonempty nested context, falling back to the outer dictionary when it is empty. This empty-dictionary distinction means the consumers are not literally identical.
- Frozen current Agent `df2739f9:astrid/core/execution/generic_host.py:6676–6685` prefers the nested Mapping, otherwise outer, and hydrates all three aliases. At 6692–6704 it checks matching filmstrip JSON refs and hydrates each alias's own object.
- The repair does not replace those selections. It inspects both dictionaries, including outer when nested exists, so the empty-dictionary difference does not leave an outer reference uninspected. It avoids A1's skipped outer claims. Its subsequent digest-only global relabeling fails to preserve the consumers' successfully verified preferred reference, as F3-R1 demonstrates.

Passing independent controls on the exact repair:

- All **10 original reviewer alias probes**, adapted only to load the exact repaired module: inferred/explicit revision kinds, differing digests, mixed results, all aliases, dictionary/list JSON copies; three pure outer negatives and three real store-to-public-claim outer config-forgery negatives.
- **6 additional real outer saved-forgery probes**, all aliases × inline/ref. They use valid CAS identities, retained saved closure and a capable frozen provider. They prove semantic config mismatch downgrade, not a missing-provider refusal.
- **2 real outer multicarrier probes**, inline/ref, with all three aliases together, distinct digests, a genuine saved input carrier and forged filmstrip/capture carriers. Every output/JSON/list reference keeps its own digest; only failed claims lose authority.
- **6 saved/native controls**, all aliases × outer/nested, each checking both genuine saved and explicit CAS refs unchanged, including JSON/list copies. Saved projection here is Runtime **unit-seam evidence only**, not a real-current-Agent saved/host golden.
- **6 actual-Agent candidate controls**, all aliases × outer/nested, with SDK-generated whole previews and real projection equality. Their valid candidate refs and duplicates stay unchanged without a colliding failed claim. No absent method is their passing reason.

The real outer tests compare exact `task_specs` row bytes, stored task specs, timeline history/state, parent/shot/internal revision and dependency rows, CAS file bytes and staging file bytes. Claim lease/attempt/event changes are expected; no claim is made that all SQL remains unchanged during a successful claim. Same-key store retries return the original task/spec. The committed nested 12-case matrix additionally exercises public `create_task` retries.

## Existing central results — finished, not queued

No central request was submitted by this reviewer. All three final request IDs from the source worker have completed; they are cache hits on the **exact reviewed Runtime tree**. The canonical underlying results are:

| Final request suffix | Underlying original request suffix | Result |
| --- | --- | --- |
| `targeted-1020100236-12249` | `targeted-1020095923-5310` | **41 passed**, 23.57s, exit 0 |
| `commit-integration-1020100236-6176` | `commit-integration-1020095920-20018` | **9 passed**, 12.39s, exit 0 |
| `capture-legacy-integration-1020100236-11822` | `capture-legacy-integration-1020095920-25788` | **5 failed, 31 passed**, 20.99s, exit 1 |

All IDs have prefix `rt-m3-alias-legacy-context-fix-`. The 10:02:16/17 intermediate retries are also cache hits, not additional runs. Read each final `status`, `exit`, `summary`, `snap`, `cached_from`, and original logs/external-source records.

Exact recorded commands, run by the central service from its source snapshot:

```bash
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_snapshot_authority_refusal.py tests/test_snapshot_preflight.py

env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py

env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_capture_candidate_actual.py
```

The capture lane's four parent/child inline/ref host positives fail importing `astrid.core.rendering.verified_source`. Its explicit-CAS host positive fails because host returns a dict without `timeline_source`. The 31 passing cases include the preserved 12 nested alias nodes, 6 new outer nodes and mixed-context control. These five failures are outside the alias diff's changed host behavior and reproduce the qualification limitation already recorded in A1's review; they are not waived or counted as passing.

Original capture and commit run `ext` records include Agent moving between `df2739f903edac02bd36b4446deeea847524c040` and `e2ad59584addc892f1a6dd9fd644c75f80a2e28f`. Thus their Runtime tree is fixed but their external Agent is not a frozen whole-product pair. Cache hits do not establish a newer Agent pairing. No full suite or repeat central run is justified or requested here.

## Independent commands and results

Let:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W=$ORCH/workers/rt-m3-alias-final-review
cd "$W"
```

`prepare_sources.py` reconstructs read-only `git archive` sources: complete Runtime `aa784ab8...`, plus Agent `df2739f9...` paths `astrid astrid_runtime_client schemas config runtime.lock.json pyproject.toml`. `baseline_capture_validation.py` was read with:

```bash
git -C /home/user/work/wt/rt-m3-alias-final-review show 6023cfb:runtime_protocol/capture_validation.py
```

Final complete **targeted private review corpus**, with all final immutable-state and original-baseline differential assertions:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD/runtime-copy:$PWD/runtime-copy/tests:$PWD/agent-copy" \
  ASTRID_CHECKOUT="$PWD/agent-copy" \
  /home/user/work/venv-agent/bin/python -m pytest -q -s -p no:cacheprovider \
  --confcutdir=. --basetemp=private-final \
  test_original_alias_probes.py test_final_alias_review.py
```

**6 failed, 30 passed, 3 warnings, 17.99s, exit 1** (`final-review.log`). Exactly the six F3-R1 preservation assertions fail. All original A1 assertions are green. Warnings are imported modules' unregistered `integration` markers in this standalone private harness; no tests are skipped, disabled, xfailed or weakened.

Earlier targeted development runs used the same environment and pytest options with these exact tails (retained logs):

- `--basetemp=private-tmp test_final_alias_review.py`: **6 failed, 18 passed**, 17.21s (`final-probes.log`), before multicarrier controls and baseline differential checks were added.
- `--basetemp=private-controls test_original_alias_probes.py test_final_alias_review.py -k 'not same_digest'` without `-s`: **30 passed, 6 deselected**, 9.23s (`controls.log`).
- `--basetemp=private-counterexamples test_final_alias_review.py -k same_digest`: **6 failed, 20 deselected**, 2.19s (`counterexamples.log`). A preceding preparation command initially used `git show` from the nongit artifact directory and exited 128; the shell then ran the existing probes. No source was changed by that failed preparation. It was corrected with explicit `git -C`.
- `--basetemp=private-differential test_final_alias_review.py -k same_digest`: **6 failed, 20 deselected**, 5.79s (`differential.log`), after baseline differential checks were added. The final complete run supersedes these development runs.

Read-only repository checks:

```bash
git diff --stat 6023cfb aa784ab8
git diff 6023cfb aa784ab8 -- runtime_protocol/capture_validation.py tests/test_capture_candidate_actual.py
git diff --check 6023cfb aa784ab8
git rev-parse tl/rt-m3-alias-legacy-context-fix aa784ab8^{tree}
git show aa784ab8:runtime_protocol/capture_validation.py | sha256sum
git status --porcelain
```

Diff: two files, 237 insertions / 19 deletions. Diff check passes; own worktree status remains empty. Own worktree started at `a5a4f6b`; the reviewed code was executed from its exact private archive, not accidentally from that unrelated checkout.

## Limits, decisions and next step

No product/repo edits, new state/DTO/projector, git mutations, service requests, sockets, renderer/browser use, dependency installs, shared dependency/cache writes, integration edits, merge requests or full suites. Private realm/source copies and temporary pytest trees were removed after evidence collection; reconstruction script, exact probe sources and logs remain in this worker's artifact directory.

A1's outer saved config-forgery proof uses the frozen capable Runtime fixture deliberately and is labelled unit-seam evidence. Actual current Agent full saved/native host certification remains unverified. Actual candidate pure projection and claim controls use pinned df2739f9 and do not qualify a production host or the separately owned candidate-source-basis repair. No claim is made that all broader candidate provenance checks are sound.

Decision: **REJECT this final alias unit until F3-R1 is fixed and the strict valid-claim preservation probes pass alongside A1's repaired negatives.** The settled two-context/one-projector direction needs no change. This report is complete; the product correction and current-pair host qualification are follow-up work for their owners, not external blockers preventing this review's delivery. Keep the original behavior expectations. No merge is requested.
