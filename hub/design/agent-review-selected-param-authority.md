# Independent selected PARAM authority review

**Verdict: APPROVE_PRIVATE for the bounded resolver, with HOLD on fully compatible integration/release.** The forward authority path passed the requested independent reruns. There is a concrete inherited same-batch strict-inverse gap (F1), the newly xfailed legacy-alias positive remains a compatibility gap (C1), Runtime port ACK is pending, and App authenticated capture/browser gates remain unqualified. This is not full compatibility approval.

## Exact reviewed sources

- Candidate Agent: `654da69321b73d7d23fb4b9e689c1c1dcb2334cf` (`tl/agt-m2-selected-param-authority-provider`), tree `d35d0a36e4bc1f0a33f278a1bd798e4e857ec557`.
- Base Agent: `ce363f6d6d60e504dbd4d79803c2d6299f648ade`, tree `78af007de1d7c5a59f86fffacd9823de355cd260`.
- All native runs: immutable Runtime `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`, tree `1711b198be7f693f11ee4640eb0922ec0d0da952`, with ordinary vendored client `0.2.13`. No moving integration checkout supplied runtime code.
- Agent public S2 SHA256: `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`. Schema, generated client and `runtime.lock.json` have zero candidate/base diff.
- Product diff: helper 163 added lines; provider 27 added / 4 removed; command callback 1 added. Total 191 added / 4 removed, net +187. No new endpoint, DTO, persistence, authority cache or Runtime port.

Read PLAN.md first, then the absolute design/selected-param-original-pin-rule.md, design/agent-selected-param-authority-provider.md and implementing worker report. Reviewed the six-file candidate diff and existing history, source, recorder, rebase, inverse, materialization and native Runtime-port code. Repo source and Git remained unchanged. Tests ran from private git archives under this review worker directory; archive/realm temporaries were removed after qualification. Logs and independent probe scripts remain under this report's notes directory.

## F1 — same-batch reselection bypasses strict inverse intervening-write protection

**Concrete native reproduction; inherited on base, not introduced by this diff.** See `notes/test_review_native.py::test_same_batch_inverse_observes_prior_noop_selection`, `native-adversarial.log`, and `native-adversarial-base.log`.

1. Genuinely admit P1 and explicitly select it. Admit P2 containing the same exact E/O.
2. Accept publication T: explicit set-element P1, unchanged authored element JSON.
3. Submit one normal Runtime commit containing `[set-element P2, inverse(T)]` for the same raw clip. These are normal typed commands; no history/SQL/Prepared data is fabricated.
4. Expected under strict guarded inverse: refuse the overlapping staged write atomically. Actual on both candidate and base: accepted; head advances.
5. A following PARAM against P1 succeeds and records P1, despite the staged P2 selection. Captured native diagnostic: `unexpected_acceptance='accepted', head_changed=True, staged_selection_version=3, following_param_version=2` (these version numbers label this fixture's exact distinct pins).

The independent negative assertion fails with `DID NOT RAISE RuntimeErrorBase` on both sources. This is not a forward PARAM pin-switch loophole: an explicit selection and inverse are involved. It is a real hole in the claimed **strict inverse** guarantee when commands share a batch.

Cause: candidate `astrid/sdk/timeline/commands.py:196` still calls `apply_inverse(ctx, inverse_records, intervening_records)` without earlier command records from the current batch. `inverse.py:355` therefore checks accepted intervening records, but misses the already staged unchanged element write. New helper `_selected_param_authority.py:104-118` correctly follows the inverse target's before-publication P1, which makes the missing guard observable as selection authority as well as ordinary inverse behavior. Separate-publication selection ABA is still refused by the passing existing tests.

Recommended minimal follow-up: feed prior staged records into the existing inverse intervening-write check; add this native negative plus a disjoint staged positive and retain the passing inverse-before-selection positive. Do not add a new authority/history framework. The independent `test_inverse_then_explicit_selection_and_param_use_stage_pin` passes on candidate, proving the legitimate `[inverse, explicit selection, PARAM]` order remains useful. This inherited gap is a specific HOLD on claiming strict inverse coverage, not grounds to attribute a newly introduced regression to the resolver.

## C1 — original legacy-alias inverse positive is still held

`test_inverse_of_older_param_record_uses_only_selected_identity` passes on base. On candidate, `--runxfail` fails at the **new PARAM setup** with `selected PARAM authority is unavailable`, before its original inverse and exact-object assertions execute. The candidate only adds the strict xfail marker to this test; its original row/alias and inverse/object assertions remain intact. The wider fixture changes preserve original inverse/opaque expectations and select sources with actual set-element commands.

A current set-element is not a replacement setup for this positive: it deletes the ignored `element_ref` alias by design. Do not call this test obsolete or count its xfail as compatible green.

Recommended repair: genuinely accept the alias-bearing PARAM with a compatible historical provider that natively emitted the old no-params.snapshot shape, preserve that accepted history, then switch to this provider and run all original alias/inverse/selected-object assertions. The pre-`45c3f328` provider (`3565462c05f9d7bf55f169dd925dba28c7ad97f2`) is a source candidate for investigating that fixture after checking its Runtime contract compatibility; it was not qualified here. Another proven alias-preserving explicit selection is acceptable if available. Do not manufacture accepted SQL/Prepared proof, erase the alias, or remove assertions.

A separate independent **real old acceptance / restart / new provider** probe passed: base accepted a first PARAM on a born clip without explicit selection; a fresh candidate process loaded that actual persisted Runtime realm and accepted the next PARAM with its historical source pin. This proves complete historical PARAM triples can supply P before enforcement, rather than relying on a caller cache. It does **not** close C1: that native historical record includes params.snapshot and does not exercise the old alias/no-snapshot combination.

## Bounded authority assessment

No additional introduced forward-authority correctness defect was found in the examined paths:

- `_history` proves the previous-pair chain to the exact HeadPin and checks page heads/cursors/duplicate publications; `_records` checks command ordinals/envelope shape. Native RequestCommitPort restricts ancestry/project/timeline, and Runtime's store authenticates accepted records against its ledger/event digest. `_load` verifies exact revision/project/timeline scope. These existing ports, rather than a caller-supplied bundle cache, are the proof boundary.
- Direct proof requires one consistent command/schema/snapshot/element association and scalar target/owner bindings. Winning P/E/O is compared to the current stage target and native VerifiedDocument/admission/object validation. Most recent relevant unproven effects clear authority; scans do not resurrect an older P. Earlier bootstrap history does not prevent a later genuine explicit selection.
- Raw parent/occurrence identity and the verified State.matches materialization link control ownership. Sibling equality, display suffixes and copied JSON do not establish source authority. Copied targets refuse until explicit selection. Automatic duplicate inheritance is not implemented or claimed by this bounded unit.
- New PARAM cannot bootstrap P, including unchanged or clear-only edits. Explicit reselection can change P with unchanged element JSON. Prior staged records feed PARAM resolution, and base/head resolution retains original guards/schema pins on rebase: disjoint peers pass; relevant P/E changes refuse; ordinary equal-selection ABA still passes. F1 is the precise exception to the broader strict-inverse claim.
- Inverse walks authenticated targets to their exact before-publication boundary, including inverse-of-inverse and inverse-of-restore, rather than treating consumed inverse schema dependencies as restored P. Revision-only restore succeeds even when equal-revision earlier publications disagree on P; later PARAM then refuses until explicit selection. No new restore selector is introduced.
- Independent extra probes passed for duplicate snapshot/element/target bindings, wrong target binding, conflicting source triple, recovery via later explicit selection, and parent copy/suffix refusal. These mutate only detached negative-test history, never native accepted SQL or Prepared envelopes.

**Documentation correction only:** public S2's anyOf requires a nonempty values or clear write. Empty PARAM is invalid before acceptance. The original-pin rule's introductory clarification is correct; remove residual “/empty writes” in its PARAM table and the implementation report's suggestion that a later schema decision is needed merely to accommodate artificial accepted-empty records. No schema widening or accepted-empty capability is warranted by this work.

## Independent commands and results

All pytest invocations used `/home/user/work/venv-agent/bin/python`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=$PWD`, and `-q -o addopts= -p no:cacheprovider`. Native commands also used `ASTRID_RUNTIME_CHECKOUT=../runtime-source`. These in-process RuntimeService tests open no sockets or browsers. No full/full* suite was requested. Shared dependencies/caches were not written.

Absolute working directories:

```bash
REVIEW=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-selected-param-authority
# Candidate CWD: $REVIEW/agent-source (git archive 654da693...)
# Base CWD: $REVIEW/agent-base (git archive ce363f6d...)
# Runtime: $REVIEW/runtime-source (git archive b748ae72...)
```

Candidate CWD, exact commands (log redirections included):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_selected_param_authority.py tests/sdk/test_timeline_commit_provider_scalar.py tests/editing_conformance/test_recipe_scalar_commands.py > ../notes/targeted.log 2>&1
# exit 0: 150 passed, 1 strict xfailed, 80.35s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=../runtime-source /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/sdk/test_timeline_selected_schema_runtime.py > ../notes/native-runtime.log 2>&1
# exit 0: 26 passed, 67.67s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py ../notes/test_review_history.py > ../notes/schema-history.log 2>&1
# exit 0: 35 passed (29 schema + 6 independent history/copy cases), 98.59s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=../runtime-source /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider ../notes/test_review_native.py > ../notes/native-adversarial.log 2>&1
# exit 1: F1 negative fails, inverse-then-selection positive passes; 5.32s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --runxfail tests/sdk/test_timeline_selected_schema.py::test_inverse_of_older_param_record_uses_only_selected_identity > ../notes/legacy-alias-runxfail.log 2>&1
# exit 1: C1 fails in setup, 2.19s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=../runtime-source /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider ../notes/test_review_old_reload.py > ../notes/old-reload.log 2>&1
# exit 0: 1 passed against the genuine base-accepted persisted realm, 1.54s

/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/_selected_param_authority.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py tests/sdk/test_timeline_selected_param_authority.py tests/sdk/test_timeline_selected_schema.py tests/sdk/test_timeline_selected_schema_runtime.py
# exit 0: All checks passed
```

Base CWD:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_selected_schema.py::test_inverse_of_older_param_record_uses_only_selected_identity > ../notes/legacy-alias-base.log 2>&1
# exit 0: 1 passed, 1.94s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=../runtime-source /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider ../notes/test_review_native.py::test_same_batch_inverse_observes_prior_noop_selection > ../notes/native-adversarial-base.log 2>&1
# exit 1: identical F1 bypass, 3.41s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=../runtime-source /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -o tmp_path_retention_policy=all --basetemp=../private-history ../notes/test_review_old_acceptance.py > ../notes/old-acceptance.log 2>&1
# exit 0: 1 genuine old-provider acceptance passed, 2.06s; run before candidate old_reload
```

`git diff --check ce363f6d 654da693` passed from the assigned Git worktree; `git status --porcelain=v1` remained empty. External native probe modules run outside the repository pytest config emitted one unknown integration-mark warning; no test was skipped or weakened. Earlier diagnostic reruns were used to add source-outcome logging and retain P1 genuinely before readmission in the base comparison; the final saved probe/logs above cover the same valid native setup on both sources.

## Handoff

Review task complete; not blocked. Keep this source private pending orchestrator disposition of F1 and restoration of C1's positive, then obtain Runtime port ACK and App authenticated same-client history/source forwarding plus browser refusal/draft/outbox/restart evidence. No App/browser, hosted/live custody, full suite, or integration/release approval is supplied by this report. Do not substitute the implementing worker's 446-pass/1-xfail historical run for the explicitly listed independent results here.
