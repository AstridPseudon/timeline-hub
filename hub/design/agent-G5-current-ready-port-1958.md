# G5 current-ready port report

Disposition: PASS for the requested mechanical source port; draft-only, P1 NO-GO. No integration merge/request/activation was made.

## Scope and source mapping

- Base: 07e6d83df69146c7dddea207f32330dc8b58dbc5. Reviewed source: f27d524798b14d11bcbe654ce7eee49d47e0b739. Source diff: 51 paths; allowed result: 50 paths (43 modified, 6 added, 1 deleted).
- Excluded exactly: tests/editing_conformance/test_a4_parent_media_raw_witness.py; it remains byte-identical to the base and was not deleted.
- Review-chain mapping: current-final-review 47 paths (9da584010 versus bac094180); docs-review 1 path (003013fa1 versus c59a75177); c271-review 2 paths (70be7e9f versus 89c38c935); restore-oracle-review 1 path (68fbe54e8 versus 697c8fd3b). Their union is exactly these 50 allowed paths; restore overlaps current-final-review only at test_timeline_checkout_history_runtime.py.
- Every resulting allowed blob below equals the source commit blob; deleted document_diff.py is absent. No donor ancestry, reports, Runtime/schema/generated/environment/daemon/Git internals, or pins were imported.

## Exact allowed 50-path manifest and source blobs

| path | status | source blob |
| --- | --- | --- |
| astrid/packs/rendering/docs/SKILL.md | M | 7dee1d8c84afc9a1f8b15150f55db0642d2be142 |
| astrid/packs/rendering/docs/scripts/timeline_document.py | M | 0984594f6998b321b2e9e35ac5b485199158ddfa |
| astrid/packs/timeline/cli.py | M | 257ba096cc064dc6d3ef1a4cfc19e0371270f7f4 |
| astrid/packs/timeline/cli_common.py | M | 81fc580285b74e06b67c7d40a9b87b5c98fbb058 |
| astrid/packs/timeline/cli_native.py | M | eb8a814825cc6e880da7d4ea512a96e40e17e065 |
| astrid/packs/timeline/cli_parser.py | M | d7141b574830eb8d645b2ccf82a202b290e6ca07 |
| astrid/sdk/timeline/_command_state.py | M | 803ce9d6f412358b9a1d568fed547bd746c83b09 |
| astrid/sdk/timeline/_doc_patch.py | M | df2388d3a69e7fb9603cca9c540e474a1a570df7 |
| astrid/sdk/timeline/_step_undo.py | M | 0bdefdb813c9ffcbe94c7a627512784e60da3532 |
| astrid/sdk/timeline/checkout.py | M | 0d7699633bbb5ebbee87bda16ec9eb975de1a5db |
| astrid/sdk/timeline/commands.py | M | b6375c78f7e5f75edf7eadd24c6c093e8141baba |
| astrid/sdk/timeline/document_diff.py | D | DELETED |
| astrid/sdk/timeline/journal.py | M | ee774a4da3ebbb99000cf5d941c8e2079b390472 |
| astrid/sdk/timeline/native_restructure.py | A | 1c012335947e81b10614ddf58b4e9ecfdd2a9c36 |
| astrid/sdk/timeline/publish.py | M | b697af3d638f31850ae97add8c3c4c92745249c6 |
| astrid/sdk/timeline/store.py | M | d7222cf32debe76c5f87af7943b5836de8207dab |
| astrid/sdk/timeline_checkout.py | M | 2370df9e488fdc67b3b678e306430a5e4a0d4de1 |
| scripts/reshape/baselines/mypy_astrid.json | M | 3f257b4f74d85651b33eff2ef2369732de407d26 |
| scripts/reshape/baselines/ruff_astrid.json | M | 97a23dff23eefc42b38a07d0c0f1ca1f7a9b2ba1 |
| tests/editing_conformance/test_captured_config_root_mirror.py | A | 9d3e3330b24dba2e3c2b9d5e14c0e46677c30fa5 |
| tests/editing_conformance/test_native_sheet_current_runtime.py | M | 0a23991cb98ce270da7c6bb7bdd9ec73e2ff402e |
| tests/packs/timeline/test_cli_commit_move.py | M | 48d56160d77c8bc737a9d3ee0198135d272e61bc |
| tests/packs/timeline/test_cli_commit_trim.py | M | 966227db8797d7421d592f04d8f508eab517d8b5 |
| tests/packs/timeline/test_cli_document_commit.py | A | c86712efe1d97ff374104368eaddcfe73269766d |
| tests/packs/timeline/test_cli_native_sheet.py | M | 6602ef1abe4dd658507069acf6f39128b6d32613 |
| tests/packs/timeline/test_cli_parity.py | M | fdd41177fce354b59f9dbd7967877410c7f6c2ea |
| tests/packs/timeline/test_cli_status_publish.py | M | 2dcc7528436d2472b6f3088796e4c8dad2b4eacf |
| tests/packs/timeline/test_parent_clips.py | M | d138415ae84d9481b4a468a41310e625a5767d6b |
| tests/packs/timeline/test_verbs_working_copy.py | M | 6fd04fa7445cf75a9ee0f9aec794918f673ea2e2 |
| tests/sdk/test_intent_app_astrid.py | M | f4340808ab449502159a5345bb25ed7b1eb49f7e |
| tests/sdk/test_media_transcript.py | M | 74f704e4d1d03f136aa3805e12bc07d9f85d5fec |
| tests/sdk/test_p4_cli_sheet_v2.py | M | 93ed82ee1f7302d88bd30ad864a29ad62f187f8e |
| tests/sdk/test_scene_save_core.py | M | 175a693bdd9200e60c119406250cb3ae39a84026 |
| tests/sdk/test_timeline_checkout.py | M | 75a9fae98485d8b0e71261039664c4bdcaf9f7a5 |
| tests/sdk/test_timeline_checkout_facade.py | M | eb50a950fb7152d078bd3c97820479d5f074fe85 |
| tests/sdk/test_timeline_checkout_history_boundaries.py | M | d2ee3d0e928896fb8b127b2f3dd556c3d5ebe078 |
| tests/sdk/test_timeline_checkout_history_runtime.py | M | 79f5d91eba6ae49fafcf6020d7fee7f2a038be6e |
| tests/sdk/test_timeline_helper_capture.py | A | 818154a89e09e5bc82b78c8ffa79a9e2d3b036f5 |
| tests/sdk/test_timeline_journal.py | M | 7e99ec1b90742513d69a221b85778d99bfaacb9b |
| tests/sdk/test_timeline_normal_publish.py | A | 23659d463c24becfcbafe85929caa1da5b23eb28 |
| tests/sdk/test_timeline_owned_move_publish.py | M | 9f046d62c19ecae2891418b7d9ee57d9cc179dc2 |
| tests/sdk/test_timeline_persistence.py | M | 89757724d65327a1f023ada441cd483093a99e33 |
| tests/sdk/test_timeline_publish_connection.py | M | 2d3dae36184e1f70f5771ba11e123658d17258d5 |
| tests/sdk/test_timeline_restructure.py | M | 57bc82e541d25966ebbc568b909ceff1772c99b8 |
| tests/sdk/test_timeline_restructure_guarded_runtime.py | A | 9accc758deb59fc69c614f2e433c8f8cd00cfc27 |
| tests/sdk/test_timeline_store_fixes.py | M | dfd1de6876a44f580350120199066aa2a0be799d |
| tests/sdk/test_timeline_sync.py | M | e3338599238c2632f78ae5d7996f107150f1ffea |
| tests/sdk/test_timeline_transaction.py | M | f0965b3ccbefe6692804ae4dfba86131d0ae080b |
| tests/timeline/test_authoring_feedback.py | M | 20ae6067b1c92ec4dd2eb40a3346dbfb0167e6cc |
| tests/v10/test_domain_cli_projects_timelines.py | M | d665cf807da012293f83e6499e1bc1643604eb35 |

## Preservation and body custody

- Exact worktree audit: 50 changed/untracked paths, zero unexpected, zero missing, zero blob mismatches; excluded witness blob matches base. git diff --check passed.
- Outside allowed set: 0 changed/untracked paths across 3,431 base-tracked paths. Critical identity audit passed for R1 _commit_patch.py, _root_inverse.py, inverse.py, track commands, media transcript, A4 track/transcript/raw witnesses, runtime.lock.json, artifacts.json, edit-command schema, generated client, .env.example, and remotion registry lock.
- Protected values remain: Runtime lock source 34eac0041b0891e9011966b39bcbd26053fde5bc; frozen edit-command schema d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d; client/runtime schema digest sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c; frozen Composition artifact 819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234.
- Current production caller and old-writer grep proof are reused from the exact 47-path review: normal SDK checkout/free-edit/publisher/restore/undo/redo uses the full C0 request and canonical accepted/merged/preview/error reply path; no alternate executor or retired route was reintroduced.
- Behavioral bodies remain at reviewed source blobs, including the c271 captured-config guard and the 68fbe restore-oracle one-function correction. Deferred D14/D23/V4 behavior remains visible and unskipped; no assertion, baseline, guard, or test weakening was authored.

## Checks

Guard command (exact mandated selector):
~~~sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_config_root_mirror.py tests/sdk/test_g5_retained_sheet_basis.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_transient_root_baseline.py tests/editing_conformance/test_a4_parent_media_raw_witness.py
~~~
Result: 71 passed in 23.78s.

- Scoped Ruff over all changed/new Python files: exit 1, 112 inherited diagnostics; no fixes made. Exact source equality reuses the reviewed identity result Ruff 2148 = 2148 with zero added identities.
- Private scoped mypy over 15 changed Agent modules: exit 1, 104 inherited errors in 5 files; no fixes made. Exact source equality reuses the reviewed identity result mypy 1911 = 1911 with zero added identities.
- Vendor lock: ok runtime.lock.json (matches producer manifest) using rt-pin-34eac004. Artifact manifest: artifacts.json is current. Whitespace: pass.
- Runtime origin: /home/user/work/wt/rt-pin-2a9e347f, commit 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d, tree f79a2355cfb39d9ada7721978bd20d5702105778. Agent changed modules resolve from this worktree. High-confidence credential scan over added diff: 0 matches.

## Limits and next steps

No full suite, browser/live socket/daemon run, P1/P4, public redo, c271/original FOUR, or provisioning run was requested or performed. No guard failure occurred in the mandated selector. The draft is ready for orchestrator review at P1 GO, but remains unmergeable until that decision; the orchestrator owns any later integration and qualification.

