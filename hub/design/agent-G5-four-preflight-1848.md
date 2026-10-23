# G5 ORIGINALFOUR fixture preflight

## Verdict

**Fixture/report-all trivial boot: PASS. ORIGINALFOUR qualification: not run.**

P1 integration-merge NO-GO is unchanged. This worker made no Agent product or
test change and did not rerun either ORIGINALFOUR or the c271 restructure body.
The previous 2-pass/2-fail result and lost packet remain historical facts only;
this report makes no recovery or qualification claim.

## Permanent harness

Evidence is permanently under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-four-preflight-1848/evidence/`

- `g5_preflight_observer.py` — SHA-256 `e593c1e43d4ee583c9bf13fe078f4035e733c7492d2c0780710653e965637ec9`.
- `run_original_four.sh` — SHA-256 `458a40e018305c86dad81f568e760794ed7f6b9c4c78bddf6ad7d0716473b366`.
- `report-all.json` — SHA-256 `869c85ea1f2fb9365cf05dd42ddc75da150934740dfcb198350a437e8ec989c0`.
- `observer-boot.json` — SHA-256 `c512fa402cc0bffc5535f84bd3b5cd9ab505c9363777e1b4de70264da0dc7894`.

The observer is external to the product repository. It wraps only the existing
Runtime service/port/store and Agent provider/validation call seams, calls each
original method unchanged, and flushes an initial packet before provider,
port-validation, and store-validation bodies. Packets include actual context,
request, prepared/private state, sequential original/landing capture when
available, source history, native/effect/binding/dependency fields, root-stage
images, document manifest, canonical/reply/receipt/error views, available
guard/base/theirs values, SQL/head/history before and after, no-write flags,
same-process Agent/Runtime module origins and hashes, and idempotency attempt
number. Missing fields are reported as unavailable; no facts are synthesized.

## Immutable identities and locks

- Agent: commit `c59a751774cf74267daab779f6e3dc2604fc3993`, tree
  `051260b73524bf20c5db6cee182c4b0a06d7791c`.
- Runtime used for the preflight: commit
  `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree
  `f79a2355cfb39d9ada7721978bd20d5702105778`.
- Authentic archive SHA-256:
  `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`.
- Runtime schema digest: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.
- Vendored client lock source: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- External artifact identity retained: `819acf6b3815d6eeabe772a9569581fedbe4f9c9`.
- Profile: `astrid`.

Observer-boot module code hashes included Agent `astrid.sdk.timeline.commit`
`f777ad0f307378b69a5aff2266d1e329e4399cce711768a484d231ecda12fc4a` and
`astrid.sdk.timeline.validation`
`dc3305e24bcad677c6573c5bdd8557e2a60d72dd9eedd03c307f8c8a78bf8fbc`, plus
Runtime `runtime_protocol.contract_metadata`
`61ef564dfbc0f0e69a333bdfcd4ae70eedbc3fb2c8147e57aa6c435f2713b57c`,
`runtime_protocol.service`
`267bec1aee551e7ea1f92f987adb24268be11c6dd165ee56f24aa68ff2b6a692`,
`runtime_protocol.timeline_commit_port`
`0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859`, and
`runtime_protocol.timeline_commit_store`
`b1cfdceefc533220ea9a5478f61a971109d1cc2d70fa2c7a76341ffa977f2246`.

All four current test bodies matched their approved AST/source locks:

| body | lines | SHA-256 |
| --- | ---: | --- |
| `test_checkout_reload_undo_cli_redo_uses_retained_history` | 128–160 | `1ea4f8c1a8342c049933e580f70282a9fef87fdc73f9f45366c854664b513056` |
| `test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images` | 163–242 | `0d9c76abdb1304c760cc667273f592c5ba7f987e84170aaa67b7ea2a6722a8d6` |
| `test_retained_restore_does_not_reopen_consumed_draft_steps` | 245–293 | `43a5cab36e8464974c86af04ed37e138ea7ec441c3d1180235587bba4b363b1f` |
| `test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore` | 296–503 | `dcbeca79c3ff4830a6535646edcd76f81646a05e024d17756769e11262140627` |

## Fixture report-all result

Using the existing `/home/user/work/venv-agent` and Runtime checkout, with no
new realm seed or DB injection:

- archive hash matched; standard `verify_backup` PASS; standard
  `restore_backup` PASS;
- schema 31, one project, one timeline;
- exact canonical head pair: revision
  `a3e671256f1c42b8837d3e118c97b21b`, publication
  `txn-11c90075be6c4c8bb9e2627366f0fe4f`;
- canonical closure: 3 shots, 3 internal timelines, 5 media/CAS objects,
  registry present, 9 null values, no opaque top-level keys, and retained
  legacy word value `word:word-1`;
- credential scan: zero findings. No credential value was emitted.

## Commands and results

1. Fixture/report-all trivial boot:

   ```text
   ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_AUTHENTIC_LEGACY_ARCHIVE=/home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz G5_AGENT_ROOT=/home/user/work/wt/agt-G5-four-preflight-1848 G5_EVIDENCE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-four-preflight-1848/evidence PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-G5-four-preflight-1848:/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-four-preflight-1848/evidence/g5_preflight_observer.py
   ```

   Result: `PASS`.

2. Collection-only observer boot (no test body executed):

   ```text
   ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_AUTHENTIC_LEGACY_ARCHIVE=/home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz G5_AGENT_ROOT=/home/user/work/wt/agt-G5-four-preflight-1848 G5_EVIDENCE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-four-preflight-1848/evidence PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-four-preflight-1848/evidence:/home/user/work/wt/agt-G5-four-preflight-1848:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider -p g5_preflight_observer -m integration tests/sdk/test_timeline_checkout_history_runtime.py
   ```

   Result: `4 tests collected in 0.51s`; all four locked nodeids enumerated.

3. Harness checks: `bash -n evidence/run_original_four.sh`, Python AST parse of
   `g5_preflight_observer.py`, and `git diff --check`: PASS. Worktree status is
   clean; no product/test files changed.

## Future launch and limits

`run_original_four.sh` is the one exact bounded recipe: existing venv, Runtime
2a9e source, authentic archive, `-m integration`, observer plugin, and
`timeout -k 15 480` (8 minutes). It is intentionally not executed here.

The observer’s event coverage is prepared but unexercised: no actual
provider/auth/commit body ran in this worker, so there are no per-case request,
prepared, receipt, error, retry, or SQL mutation packets to interpret. A later
meaningful joined R2 candidate may run this exact recipe once; only then can
the observer’s full fidelity and ORIGINALFOUR result be assessed. No route
around farm denial, no browser/live suite, no Runtime build/pin/schema/env
write, no Git mutation, and no test weakening was used.
