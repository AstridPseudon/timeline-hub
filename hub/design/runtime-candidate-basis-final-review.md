# Runtime candidate-basis final review

**APPROVE the bounded repair `082a90506cb0d2a64dfc939f7a87ae377c6664ce`, tree `7b0b8098ba2fb3e085c247fded013eac438f87fd`, relative to `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` (including held `c10bad52ca524e779c54876489d2c12f857f2e13`).** No blocking finding remains in the assigned candidate-base unit. Integrate it **only paired with the Agent-owned approved method/host source** `92427b3af0bfaba2ff604791cf3e5165125b6d54`, tree `525bdabe863a42bc177f5ff331560133f77ce634`, or a separately reviewed and qualified descendant. This review does **not** authorize Agent verifier deletion, a standalone Runtime merge, or completion of Gates 1/7.

Reviewer: `rt-m3-candidate-basis-final-review`, 2026-10-20. Read PLAN, COMMON, current Runtime/Agent STATUS, repair DetailedReport, prior `runtime-capture-authority-review.md` B1, and `agent-review-capture-current.md`. The Agent owner review independently approves this exact bounded source; STATUS still treats capture as a held pair with the verifier retained. My worktree remained at `a5a4f6b11a92ac8f01fbc7941db8a1470337ba9d`; candidate review used exact private read-only archives. No product/test files in a repository were changed.

## Source and evidence provenance

The source audit reconstructed both commits with `git archive`, then compared every archived blob against `git ls-tree -rz` identities: **405 Runtime blobs and 3,008 Agent blobs match**. The fixed Agent archive used by the original central lane also matches all **3,008** blobs, with no extra files. Repeated the audit after private probes; sources remained exact. Both central `snap` files identify Runtime tree `7b0b8098…`, exactly the candidate commit's tree. The central paired command explicitly uses that fixed Agent archive, not the drifting live integration checkout printed in `ext`.

The paired command has no private provider plugin. The fixture loads the installed `astrid` provider class and verifies its module path/type (`tests/test_capture_candidate_actual.py:67`); the actual production optional method is present at `astrid/sdk/timeline/commit.py:636`. Missing-method tests delete a real method. Certified positives, full saved projection comparisons and host consumption pass with that capable source. Missing-method refusal cannot explain these green negatives.

The diagnostic RED plugin substitutes only `_candidate_document` from exact rejected `c10bad52` source. Its archived file is byte-equal to `git show c10bad52:runtime_protocol/capture_validation.py`. The saved negative-control log contains **28 failures, all 28 reaching the projector assertion trap**. It does not patch the Agent provider. I audited this log and plugin; I did not repeat the 28-case run or central lanes.

## Verified behavior and code locations

All Runtime locations below are in `082a905`; Agent locations are in `92427b3a`.

| Claim/scenario | Implementation and verification |
| --- | --- |
| Exact scope, parent/base, candidate/publication hashes and binding | `runtime_protocol/capture_validation.py:26–39,49–50,78–79` compares canonical JSON, including the complete pure-derived publication. Original publication/base cases retain their assertions. |
| Every base placement, including invented/removed entries | `capture_validation.py:52–53` compares the entire saved map. Extra rows and dropped rows cannot hide outside an intersection. |
| Every placement-source row, including unused/deleted/alias/new occurrences | `capture_validation.py:54–62` checks every value against a complete retained row; still-authored saved identities additionally require their own exact source. Authoring aliases can reuse a genuinely retained value. |
| Every shot-source claim, including unused/deleted/renamed/cloned entries | `capture_validation.py:67–71` indexes complete serialized retained source rows, including `item_id_map`, immutable IDs and digests. No source-identity parsing from authoring key spelling. |
| Both child bases under renamed/cloned identities | `capture_validation.py:72–77` resolves by complete retained source value, then compares both `base_payload` and `base_internal_timeline`. Source-less created children allow only empty/absent bases; the existing compiler validates recorded creation and authored structure. |
| Embedded Runtime document, document pins and revision closure | `capture_validation.py:63–64,80–95` preserves exact embedded closure and retained document pins; merges only derived publication images into a detached local document and validates it. `timeline_commit_store.py:248–279,281–295,397` reads/verifies immutable identities/dependencies. No saved revision is rewritten. |
| Refusal before writes and before surviving Agent verification | `store.py:2454–2476` gathers/preflights snapshots and validates captures before its admission transaction and publication writes. `test_capture_candidate_binding.py:52,190` installs the projector assertion trap after genuine snapshot production, refreshes candidate/publication/snapshot/ref hashes and compares **all SQL tables, all CAS bytes/directories and all staging paths** via `test_snapshot_authority_refusal.py:150–170`. Both inline/ref branches are covered. Ref ingest is setup before the baseline. |
| Legitimate new/clone/rename/delete/drop drafts | `test_capture_candidate_binding.py:247` has 16 certified structural positives, including real recorded `occurrence.duplicate`, new shot/occurrence, clone, rename, deleted occurrence/shot and pruned deleted sources. Private probes additionally preserve exact unused retained aliases, renamed occurrence source aliases and independently dropped deleted source maps. |
| Opaque authored content and input detachment | Existing parent opaque edit, source-derived publication equality, `test_capture_candidate_binding.py:330,353` mutating-provider and parent/child host cases; private positives add opaque nested parent/occurrence/shot/item/internal/clip fields and distinguish booleans, integers and floats canonically. Caller objects, frozen preview and saved canonical tables/closure stay unchanged. |
| Optional method absence and native/candidate-less behavior | `capture_validation.py:40–47,111–125` fails candidate certification closed; saved captures do not need the candidate hook. `test_capture_candidate_binding.py:128,136,528` keeps explicit CAS/candidate-less claims UNCERTIFIED and saved certification working. |
| One pure construction seam and existing projector | Agent `commit.py:636–642` deep-copies inputs/results and calls existing `bundle_from_document` and `preview_authoring_candidate`; no new compiler/projector/IO/save path. Runtime product growth is **42 added/2 removed lines** from `6023cfb`, confined to comparisons and exception translation, plus the provider argument at the call site. `project_capture` still uses `project_runtime_parent_composition` (`commit.py:738`). |
| Full saved projection and verified host handoff | `test_capture_candidate_binding.py:464,500` compares the whole saved expansion, including graph/outputs, and tests saved/native inline/ref host behavior. `:353` tests parent/child working-copy inline/ref source bindings. Agent `generic_host.py:6505,6733,6742,7000` and `rendering/verified_source.py:80` distinguish canonical source from CAS and mint attempt-bound prepared source handles. No actual renderer is invoked. |

The **original 22** cases and their helpers/decorators/assertions are AST-identical to held `c10bad52`. The final dedicated file contains those 22, the adapted 31-case independent verifier corpus, **28 new source/base counterexamples**, 16 structural positives, four Node-number cases, four fresh bool/float base negatives, one provider-mutation check, four working-copy host positives, four saved/native host positives, two saved-without-hook positives and 12 fresh semantic negatives: **128 nodes**. The marked central lane adds 13 original neighboring nodes: **141** total, no skips/xfails.

Numeric policy remains the existing exact canonical JSON recipe. Fresh `False`/`0.0` substitutions for retained integer `0` refuse before projection/writes. Authored opaque `[False,0,0.0,1,1.0,0.25,null]` survives the real in-process prepare/admit/claim/host path. Existing Node `JSON.stringify` cases show fractional values survive while `1.0` normalizes to `1`, invalidating frozen hashes and correctly refusing. This is a serialization compatibility limit, not a new ban on authored floats or a reason to redesign hashes.

## Exact commands and results

Abbreviations:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W=$ORCH/workers/rt-m3-candidate-basis-final-review
A=$ORCH/workers/rt-m3-candidate-source-basis-fix/agent-source
cd "$W"
```

Independent source/probe evidence:

```bash
# Original archive preparation used the same git archive/extract operations preserved here:
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python prepare_sources.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python verify_sources.py
# PASS: every source blob, both central trees/exits, exact rejected source,
# all 28 RED assertion traps, and inherited AST equality.

env ASTRID_CHECKOUT=$PWD/agent-source \
  PYTHONPATH=$PWD/runtime-source:$PWD/runtime-source/tests:$PWD/agent-source \
  PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest \
  -q -p no:cacheprovider --confcutdir=. --basetemp=$PWD/probe-tmp test_final_review.py
# 18 passed, 5 unknown-integration-marker warnings, 12.68s; exit 0.
# Eight fresh-hash inline/ref negatives: forged item map, missing live source,
# dropped base row, renamed internal base independently of shot base.
# Ten certified inline/ref preservation/host positives, described above.

/home/user/work/venv-agent/bin/ruff check --no-cache \
  runtime-source/runtime_protocol/capture_validation.py \
  runtime-source/tests/test_capture_candidate_binding.py
# All checks passed; exit 0.

git -C /home/user/work/wt/rt-m3-candidate-basis-final-review diff 6023cfb 082a905 --check
git -C /home/user/work/wt/rt-m3-candidate-basis-final-review status --short
# PASS; clean worktree.
```

Private probes import the real production provider, with no private provider implementation. The real SDK `prepare_filmstrip` uses the existing in-process Runtime read adapter; requests explicitly forward the complete preview as plain task input. These are not SDK invocation/transport tests. The five warnings arise because the private test root intentionally does not load repository lane registration; all 18 nodes executed, with no skips, xfails or disabled assertions.

Reused central evidence (inspected `snap`, `request`, `summary`, `exit`, full logs, paired command and source archive):

1. `rt-m3-candidate-source-basis-fix-capture-agent92427b3a-integration-1020100640-26445`, executed from the service's exact Runtime snapshot:

   ```bash
   env ASTRID_CHECKOUT="$A" PYTHONPATH="$PWD:$A" PYTHONDONTWRITEBYTECODE=1 \
     /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration \
     tests/test_capture_candidate_binding.py \
     tests/test_capture_candidate_actual.py::test_original_working_copy_forgeries_refuse_before_writes \
     tests/test_capture_candidate_actual.py::test_working_copy_without_candidate_is_admitted_uncertified \
     tests/test_capture_candidate_actual.py::test_forged_working_copy_certificate_refuses_before_writes \
     tests/test_capture_candidate_actual.py::test_explicit_cas_candidate_is_native_without_binding
   # 141 passed in 60.01s; exit 0 (service 62s).
   ```

2. `rt-m3-candidate-source-basis-fix-targeted-1020100612-11033`:

   ```bash
   /home/user/work/venv-runtime/bin/python -m pytest -q \
     tests/test_snapshot_authority_refusal.py tests/test_snapshot_preflight.py \
     tests/test_capture_candidate_actual.py
   # 41 passed, 17 deselected in 19.58s; exit 0.
   ```

   This is frozen-provider Runtime seam evidence. The 17 marked nodes are deselections, not passing current-provider tests. Actual saved/candidate/native provider/host evidence comes from the pinned marked lane above.

3. Audited RED control, previously executed by the repair worker:

   ```bash
   # From its original Runtime worktree; WFIX is the repair worker artifact directory.
   WFIX=$ORCH/workers/rt-m3-candidate-source-basis-fix
   git show c10bad52ca524e779c54876489d2c12f857f2e13:runtime_protocol/capture_validation.py > "$WFIX/rejected_capture_validation.py"
   env ASTRID_CHECKOUT="$A" PYTHONPATH="$PWD:$WFIX:$A" PYTHONDONTWRITEBYTECODE=1 \
     /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
     -p rejected_control -m integration \
     tests/test_capture_candidate_binding.py::test_every_advertised_base_and_source_is_retained
   # 28 failed in 52.30s; exit 1, expected. Every failure reaches the projector trap.
   ```

No central requests or broad/full tests were submitted by this reviewer. Source verification and probe scripts/logs remain in the reviewer artifact directory; private source exports and pytest temporary realms are removed after audit. The existing repair worker's pinned archive is left untouched for paired reproduction.

## Limits and next step

This approval closes prior **B1** for the assigned candidate-basis repair and actual provider/host branch pair. The earlier claim-alias **A1/F3** fix is a separately owned unit; historical admission upgrade, all alias/context permutations and mixed-carrier claim certification are not newly qualified here. No newer-head saved test, actual SDK enqueue/CLI transport, RenderRequest propagation, renderer execution, Composition/pixel/audio parity, full suites or delivery artifact was run by this review.

The original **four RenderRequest** propagation requirements remain external to this pair. The original **three SDK invocation early-guard** requirements also remain outside this frozen source; STATUS records separate successor work, which this review does not qualify. Ordinary full-suite and current release/client pin gates remain open. No main suite expectation was weakened, removed, skipped or changed to refusal.

**Recommended next step:** the orchestrator may integrate this Runtime unit only with the Agent owner's approved source, retaining legitimate immutable pins and all existing Agent verification. Review and qualify verifier removal separately against complete supported surfaces; this partial unit evidence is not deletion authorization. Complete F3/legacy, SDK/renderer consumers and the coordinated current release/Gates 1 and 7 independently. No settled plan decision needed changing. Review completion is unblocked; there is no BLOCKED marker.
