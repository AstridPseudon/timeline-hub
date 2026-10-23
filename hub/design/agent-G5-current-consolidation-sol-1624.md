# G5 current consolidation — agt-G5-current-consolidation-sol-1624

**G5 DRAFT ONLY. Source consolidation complete; joined qualification BLOCKED (183 PASS / 1 fixture setup ERROR). P1 remains NO-GO. No integration merge or merge request.**

## Work and scope

Read ORCH/PLAN.md first. Own assigned worktree remained on `98ef2f9c95fd43d88cca2909d8d1518302e3050c`, which exactly matched tl/integration at initial inspection. Imported 44 exact reviewed Python file blobs via read-only `git show` and workingtree writes; deleted only the named `astrid/sdk/timeline/document_diff.py` using `apply_patch Delete File`. No ancestry, checkout, commit, merge, fetch, rebase, push, ref mutation, daemon, dependency provisioning, or shared-install writes.

- Publisher donor: `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a`, containing reviewed retirement `f57d283d2`, durable CLI `cc8be25d4`, normal frontdoor `23cac8b72` + `4b248adc5`, and idempotency fixture repair `d0fc9848a`. Author/reviewer facts read from ORCH/design/agent-G5-publish-final-review-1617.md and agent-G3-frontdoor-final-review-1612.md, plus the earlier f57d report read with git show.
- Ordinary SDK publisher/helper `74b92b2a9` is already incorporated. `tests/sdk/test_timeline_helper_capture.py` matches that source byte-for-byte; no duplicate implementation.
- Four native retained test blobs: `6fff510a8d851a6bd798bb11a34d6476ca0fc6a3`, reviewed by native1602 after fixture1552 repair.
- Two SDK history test blobs: `e8a29acc0c896b2c3c0b78fd6c258b6f809ae721`. Original four integration bodies retained but not executed, per the authentic legacy bootstrap blocker.
- Excluded the private R1 six-file delta `67ba416bc`, including `_commit_patch.py`, `_commit_preview.py`, `commit.py` and all three private sequential-capture test additions. Protected inverse.py / _step_undo.py / _root_inverse.py also remain byte-identical to own starting integration. No new R2/G4 fork or invented fixture.
- Current F–D22 audio/docs/geometry/inventory/custody, normal transport, generated clients/schema, runtime pins/locks, archives and dependencies are untouched. The complete changed-path allowlist was audited against own HEAD.

**Concurrent integration movement:** at final inspection tl/integration was `bac094180aef38a77b86ab165962e6159f873c60`. Its delta from own initial base is solely the separately merged private R1 six-file change (merge bac094180). This worker deliberately did not import or alter those prohibited files. Apply/review this worker's G5 diff on that newer base while preserving its R1 bytes; this report does not claim tests on the newer integration head. No Git write was attempted to move own base.

## Production path and C0 preservation

Normal CLI `_cmd_commit -> cli_native.commit_document -> authenticated TimelineSession.open -> G2 Timeline.commit -> G3 emitter`. SDK compatibility `Checkout.publish -> _commit_document -> session.submit/flush`; restructure uses the registered ordinary semantic command via the same session. Local draft saving reuses the guarded patch application primitive, with no alternate film writer. Production grep finds no imports/callers of retired document_diff, publish_bundle, three_way, _cmd_publish, commands-file or old publication undo. Retained `show --native` is the reviewed read/export projection; the document recipe's compatibility publish alias dispatches the same existing commit function.

Preserved the current durable transport/provider files exactly, including full C0 request fields (api_version, project/timeline, exact revision/publication base, commands/label, step id/label/intent/tags/ordinals/patch/reads, merge, declared reads, key, dry_run, source/rationale/group_id) and complete accepted/merged canonical data/receipt, records/bindings/effects/dependencies/history/undo_steps, preview would_status, structured code/path/head/hint/suggested command. The retained 76 publisher cases cover bounded request/reply behavior; no live HTTP/restart claim.

## One joined targeted run

Executed exactly once, with eight distinct file selectors and no -k, skip, xfail, deselect, assertion/body edit or rerun:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-41c417b40c ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=.:/home/user/work/runtime timeout 300 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 --basetemp=/tmp/w-41c417b40c/joined tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_cli_status_publish.py tests/packs/timeline/test_cli_document_commit.py tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_commit_trim.py tests/packs/timeline/test_cli_native_sheet.py tests/packs/timeline/test_verbs_working_copy.py tests/sdk/test_timeline_checkout_history_boundaries.py > /tmp/w-41c417b40c/joined.log 2>&1
```

**Exit 1: 183 passed, 1 error in 46.72s.** Inventory is publisher76 + wrapper12 + native87 + SDK-boundaries9 = 184 unique cases. Publisher76, wrapper12 and SDK9 passed; native86 passed and one native test errored before its body. Runtime source path HEAD at report time: `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` (shared checkout can advance; not represented as immutable pin).

Failure: `tests/packs/timeline/test_verbs_working_copy.py::test_normal_commit_conflict_keeps_head_and_has_no_force_overwrite`. Setup reaches `tests/sdk/test_timeline_restructure.py:359`, where `runtime_protocol.__file__` is absent. Exact traceback is in [joined.log](/tmp/w-41c417b40c/joined.log).

**Causal ownership:** imported normal-frontdoor test file `test_cli_document_commit.py:12` registers `tests.sdk.test_timeline_commit_provider` as a global pytest plugin; that module's autouse `runtime_abi` fixture installs a synthetic runtime_protocol module with no __file__. The retained native test's authentic `restructure_runtime` fixture requires the real Runtime tree and therefore refuses setup. This is a joined fixture-scope collision, not evidence of a production defect or a permission refusal. Owner: G3 normal-frontdoor wrapper fixture / native joined qualification. No fixture workaround, guard waiver, body change, or second joined run was made. The requested all-green joined proof remains blocked.

`pytest --help` was inspected: this repo exposes --timeout but no --net flag. Used the reviewed authors' timeout style; no unsupported flag or network/sockets/live suite was invoked.

## Static identity comparison and normal ratchets

All remaining diagnostic identities were compared by (repository-relative path, code, exact message), as multisets; line shifts do not create false additions. Full raw outputs and comparison JSON remain outside the product tree:

- [mypy-before.txt](/tmp/w-41c417b40c/mypy-before.txt), [mypy-after.txt](/tmp/w-41c417b40c/mypy-after.txt), [identity comparison](/tmp/w-41c417b40c/mypy-identity-comparison.json): **1912 -> 1911, zero added identities**. Sole removed identity: `astrid/packs/timeline/cli.py`, attr-defined, `"object" has no attribute "data"`.
- [ruff-before.json](/tmp/w-41c417b40c/ruff-before.json), [ruff-after.json](/tmp/w-41c417b40c/ruff-after.json), [identity comparison](/tmp/w-41c417b40c/ruff-identity-comparison.json): **2149 -> 2148, zero added identities**. Sole removed identity: store.py E731 lambda in deleted merger.

Baseline snapshot was made with `mkdir -p /tmp/w-41c417b40c/baseline && git archive HEAD | tar -x -C /tmp/w-41c417b40c/baseline`; no shared dependency files were copied or modified. Raw identity commands:

```sh
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-41c417b40c/mypy-baseline /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --hide-error-context --no-color-output --no-pretty --show-error-codes /tmp/w-41c417b40c/baseline/astrid /tmp/w-41c417b40c/baseline/scripts/reshape > /tmp/w-41c417b40c/mypy-before.txt 2>&1
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-41c417b40c/mypy-current /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes > /tmp/w-41c417b40c/mypy-after.txt 2>&1
# cwd /tmp/w-41c417b40c/baseline:
RUFF_CACHE_DIR=/tmp/w-41c417b40c/ruff-before /home/user/work/venv-agent/bin/python -m ruff check . --output-format json > /tmp/w-41c417b40c/ruff-before.json
# cwd assigned worktree:
RUFF_CACHE_DIR=/tmp/w-41c417b40c/ruff-after /home/user/work/venv-agent/bin/python -m ruff check . --output-format json > /tmp/w-41c417b40c/ruff-after.json
```

Both raw tools exit 1 because they report existing debt. Initial Ruff gate reported an improvement (exit 1); initial attempt to use the typecheck-only interpreter for Ruff reported `No module named ruff` (gate exit 2). Corrected by using the existing dependency interpreter already owning Ruff, without installation or environment mutation.

Normal generated-baseline write route, preserving strict exact-count comparison and raising no budget:

```sh
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-41c417b40c/mypy-current /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline --write-baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-41c417b40c/mypy-current /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-41c417b40c/ruff /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline --write-baseline
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-41c417b40c/ruff /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
```

Mypy ratchet/gate: **PASS**, 1911 exact findings, exit 0. Both normal writer invocations exited 0; both final gates exited 0. Ruff ratchet/gate: **PASS**, 2148 exact findings. Ruff was tightened as required by the repo's shrink-only baseline convention when deleting its merger finding. No generated baseline was hand-edited.

## Other checks and limits

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
python3 /tmp/w-41c417b40c/audit.py
git diff --check
```

**PASS** vendor official producer manifest, artifact currentness, 44 changed Python files compiled in memory with compile(), exact donor-byte match, AST test body custody, protected source custody, path allowlist and whitespace. No full/make-check/40/281/58/original P1–P4/native14/V4/browser/live HTTP/SDK-original-four/c271 or central full request. All behavioral bodies are exact reviewed donor blobs; no skip/xfail was introduced.

## Per-file provenance and hashes

[Full source mapping](/tmp/w-41c417b40c/provenance.json). [Every retained test function AST hash](/tmp/w-41c417b40c/test-body-hashes.json). The table's AST column hashes the sorted function-name-to-AST-SHA256 mapping for each test file; full individual function hashes are in that JSON. Every source and test file matches its donor exactly.

| Path | Donor commit | Git blob | Source SHA256 | Test AST mapping SHA256 |
| --- | --- | --- | --- | --- |
| `astrid/packs/rendering/docs/scripts/timeline_document.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `0984594f6998b321b2e9e35ac5b485199158ddfa` | `5ec4a3f2b2ef1585e6707c029dc271acb6a4bd7f11f010def18f086d51f28e33` | `—` |
| `astrid/packs/timeline/cli.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `257ba096cc064dc6d3ef1a4cfc19e0371270f7f4` | `42701c5ba396786869f229ea1654440eea9461e6056a50a5f71ffa472a720062` | `—` |
| `astrid/packs/timeline/cli_common.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `81fc580285b74e06b67c7d40a9b87b5c98fbb058` | `d0ec52825b1254c032f625ce3696da8b59dee4d087c675c4b381ea9fe2fcbac6` | `—` |
| `astrid/packs/timeline/cli_native.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `eb8a814825cc6e880da7d4ea512a96e40e17e065` | `78ff95edcdf57441190c56ddbb7f058d5f6e2be2f31563173f58c12e081a6cba` | `—` |
| `astrid/packs/timeline/cli_parser.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `d7141b574830eb8d645b2ccf82a202b290e6ca07` | `8e6d163b965d1a93f42f46757188db5a844bb9eddc4cb5e01df6a15f5c2c9a64` | `—` |
| `astrid/sdk/timeline/_command_state.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `803ce9d6f412358b9a1d568fed547bd746c83b09` | `5584a8d08edecf480aa223c3dcf73a5e3064cee14758ebbeef19836043db0384` | `—` |
| `astrid/sdk/timeline/_doc_patch.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `df2388d3a69e7fb9603cca9c540e474a1a570df7` | `66cbc90869fb6d54e70315ecd2ea4993db4cb1dcd4d88f20ba7f6cdc46d36e6c` | `—` |
| `astrid/sdk/timeline/checkout.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `3889da9852a55b1d5e2cfc199ccc9a5a515ef56a` | `9fe76c2eb4e3fee884a59fc28b05e591c4f97795b15852b22b70385886d66c20` | `—` |
| `astrid/sdk/timeline/commands.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `b6375c78f7e5f75edf7eadd24c6c093e8141baba` | `4225ffe4aad63884192305ff687bf0715c80817542da233f55a4d97f1fa9b3a6` | `—` |
| `astrid/sdk/timeline/journal.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `ee774a4da3ebbb99000cf5d941c8e2079b390472` | `f59a74dd3c477a3f8d86b06a61363986d2b33a8a9f63baf7e86edd37f4cef1ad` | `—` |
| `astrid/sdk/timeline/native_restructure.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `1c012335947e81b10614ddf58b4e9ecfdd2a9c36` | `800247535bbe034777fe84beb0612d96ea11992f8d77ad52ba7503dff56afb43` | `—` |
| `astrid/sdk/timeline/publish.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `b697af3d638f31850ae97add8c3c4c92745249c6` | `f8cd74076fce10d35a7a97778b6628aa3f41e8909389f93780ab49d1cc731f2c` | `—` |
| `astrid/sdk/timeline/store.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `cbb122ae9e84aa7fa37f1f4c88e43cc7840f9f26` | `3eedf2c651f91bf0e74b3fc9aba08a6e610a463796c450446c1364792dbe4e3f` | `—` |
| `astrid/sdk/timeline_checkout.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `2370df9e488fdc67b3b678e306430a5e4a0d4de1` | `df26607e2b9973333f01c6a384bc7b493bb43c6ceb49ea23f2d5260172ab1de8` | `—` |
| `tests/editing_conformance/test_native_sheet_current_runtime.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `0a23991cb98ce270da7c6bb7bdd9ec73e2ff402e` | `2dd71d0be3d2f455427de6f96f8926a9d0095d2dd244a5426e9367a598e697c4` | `a839094f86431537c1a9e15f706500ffef73dce3eb7171568d3a7e7dbf64dbc4` |
| `tests/packs/timeline/test_cli_document_commit.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `65e250b1f27bdd3546f811060223291f0d57c905` | `2e6073f52404dafdd3d76f5e385335fc876ecba22e995b8e2c4a747a5875e513` | `ab0b3ca5c625ebc71599f3cc1b7dbee9513b005fa82c51f06565c00f3f370e7b` |
| `tests/packs/timeline/test_cli_parity.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `fdd41177fce354b59f9dbd7967877410c7f6c2ea` | `c0748f89014ca8a6def028c5f0e3d7779ab8ebe251b414c3de3cf2b22837b17e` | `145dc730388efddfc606f1cce29ac350d171468a6af914e4dc03879d8ed6980d` |
| `tests/packs/timeline/test_cli_status_publish.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `2dcc7528436d2472b6f3088796e4c8dad2b4eacf` | `c413da73cdfdc136b4d9b1f6740e1d6ebf8258d261099819f3073c3b61b632b1` | `7e1c727d9530c58bc7e7d77c39ff9fb8ba12fb4cc8b91314056588eb42628429` |
| `tests/packs/timeline/test_parent_clips.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `d138415ae84d9481b4a468a41310e625a5767d6b` | `d79daa161c4fc61b40d56cf3a99384b82cb71b9b9bb96493cd8986496388c247` | `127e212ac8792561369b80c0581180c89d795e93908be5418681146931b9e475` |
| `tests/sdk/test_intent_app_astrid.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `f4340808ab449502159a5345bb25ed7b1eb49f7e` | `58fded34c8a4cc18886f59ce4e3c7f2ebee494f028a325bdc649fefd496a3037` | `fb785f264b8017d48005dee2d271dbd288b232f3ab46fc5d8a2bcfb5cfde9e60` |
| `tests/sdk/test_media_transcript.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `74f704e4d1d03f136aa3805e12bc07d9f85d5fec` | `3335c3393ad276c74ab78725b2a188b572d4580227dfa3a1e6d5480afa509a0f` | `565992a404ffc30d1c669aba155b03d5468fda9d3a0350adf969d46473438c34` |
| `tests/sdk/test_p4_cli_sheet_v2.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `93ed82ee1f7302d88bd30ad864a29ad62f187f8e` | `9b330b5021c28a44bad32e05a588d0fe3c6add42a7b016513af9ead575cf7fa4` | `b4cc57376e7625091dca38aeb4493b2e56a9d062276e29402ecd5837fa717fae` |
| `tests/sdk/test_scene_save_core.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `175a693bdd9200e60c119406250cb3ae39a84026` | `001191544b7921be1595fec6efa43d714083e46fb5e802cb5911d83389b348d4` | `3ea097f8ed05dfe2a3ba3249e0f914201d7d698c1296bc14e55123bca598fa69` |
| `tests/sdk/test_timeline_checkout.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `75a9fae98485d8b0e71261039664c4bdcaf9f7a5` | `0ac675aceddb4706bbada3d115cf58665d46c30cde0ada879589d08738f96b27` | `db45a86ba6fc814dd5dd9168b78f7273f6400ad90af0a6e9d495bf6bfa3c0c68` |
| `tests/sdk/test_timeline_checkout_facade.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `eb50a950fb7152d078bd3c97820479d5f074fe85` | `c61003247ab3c83f8cb4c7ebd6cc1e64de97073bdd335ae92bc39a5e255ffe01` | `025dd374968bc7f31e3cb02b4043a6a3d82fae4d92c5fcddf0623b3b9ae58c3a` |
| `tests/sdk/test_timeline_checkout_history_boundaries.py` | `e8a29acc0` | `d2ee3d0e928896fb8b127b2f3dd556c3d5ebe078` | `b7478f50b80fa73ce8546f7017c3fb0b52f4c722c8e2f74088e8fc8c4cc6446b` | `a36702048360b361e80d0bc370a3f58cea4a2d071e6249e9730ce9b3358675f7` |
| `tests/sdk/test_timeline_helper_capture.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `818154a89e09e5bc82b78c8ffa79a9e2d3b036f5` | `2e4925262bbc605ab199ab0d4dea92e9cc5724eb4fc5865e2030b0307fe890e2` | `32c36525c2357d5dadf79e40e8649500f635d3c5ee5ceaf3b82fdb51e0d51153` |
| `tests/sdk/test_timeline_journal.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `7e99ec1b90742513d69a221b85778d99bfaacb9b` | `e012401808bc2a94abc1310706cc40e30c1d77502d5fd38c1ba438b0acf63c4a` | `9982171124bc2a2b3c6cb6e97e4d480edee552890966880a03538a75009dff56` |
| `tests/sdk/test_timeline_normal_publish.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `23659d463c24becfcbafe85929caa1da5b23eb28` | `df643aef3c7e125de45b2b759de3402fc38f82e1ba4439a16e1612ade10a938c` | `40e8c9b6bcfab7e00cb888432b9a946b37dd9b9e925f9ff1bd805a5344ec59ff` |
| `tests/sdk/test_timeline_owned_move_publish.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `9f046d62c19ecae2891418b7d9ee57d9cc179dc2` | `5e40d0e64f6e5ffb446549e92c6bf22575c526bde322c59d3442bdddd4484999` | `5336af522cb9d37d52b458fca1ccc2af2a9b089b04879e631f08c298f5e04b46` |
| `tests/sdk/test_timeline_persistence.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `89757724d65327a1f023ada441cd483093a99e33` | `2cec94f78293ba6258d04f32c2a17fc87df33b4b8b95e091aa357e211603871b` | `4269387368b534561216ac81203c20a3d47713c25e367d0b159322d5838ad277` |
| `tests/sdk/test_timeline_publish_connection.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `2d3dae36184e1f70f5771ba11e123658d17258d5` | `fcad1e8704933088fb80e1b5b0f0c70a9dee82ffcd1b41f35b8bbf3b31b5edc8` | `d5d98b89d93d34e07ca9f474d69394baee19e0fa2330c50eb27314ad4a471544` |
| `tests/sdk/test_timeline_restructure.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `57bc82e541d25966ebbc568b909ceff1772c99b8` | `8a3a22dafcd3e84d9f79f680bed0176ad15edad21a30b416ca074ff549b9a8f4` | `da2d8e12e55c6cffef527d391975706bd3ff42d83d3089ead588ccf08aeb0d93` |
| `tests/sdk/test_timeline_restructure_guarded_runtime.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `9accc758deb59fc69c614f2e433c8f8cd00cfc27` | `d7dc8942c49b4c464535280b8849520adfba4b67d4dc0560a5b68203abf7983b` | `d3fdabf5617ff96f0587d54ab17d8d5625047a2d4939ea7f4dc3254adca13a3a` |
| `tests/sdk/test_timeline_store_fixes.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `dfd1de6876a44f580350120199066aa2a0be799d` | `a6bb482b38231c5032d02d804f98bca7b959309a65cd2a846f6aed7294800b24` | `e5719ad279b8fff3bed658e724ff9f5bd63be17028a462f258d9c6d7d06d16a1` |
| `tests/sdk/test_timeline_sync.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `e3338599238c2632f78ae5d7996f107150f1ffea` | `0bef08d0fb59f521c1d00f1126d339341e673da75d6b2ecae1bb720c5e327c47` | `c8f04dc5aa4a833e880aacd67227bd6de103e41ec7c1524fecb338918244cae8` |
| `tests/sdk/test_timeline_transaction.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `f0965b3ccbefe6692804ae4dfba86131d0ae080b` | `4ede47251c198b8352453c941b9638334fb61b7280b84bfa36ce7311e3c229e9` | `b1884183b01530db4def24f348c5185d3d49b41dc4c3d6a27e141380e90b3e2c` |
| `tests/timeline/test_authoring_feedback.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `20ae6067b1c92ec4dd2eb40a3346dbfb0167e6cc` | `37ce863249b1cd375064b2297756c4ed0577a9dcd4d74606ae59098a0d95f2e5` | `57f8c4804df90d75e6df2f26200fe24814f7cafd9e06889eda21552078f586cd` |
| `tests/v10/test_domain_cli_projects_timelines.py` | `d0fc9848a0a7acfd0548cf60b9777634b4a1e98a` | `d665cf807da012293f83e6499e1bc1643604eb35` | `c48021a98f9c0ad43270eca3378bf3fe5cf3ca1b912ce5c11769737327fb06ac` | `aa6a941e39881d9da85c1a7b8eb06746e213678049a49c6fec42051c9399644b` |
| `tests/packs/timeline/test_cli_commit_move.py` | `6fff510a8` | `48d56160d77c8bc737a9d3ee0198135d272e61bc` | `da4024e0c999bb33861b72e78a4d48185d7f981a0299b4de6dee5932fada8fa1` | `5d4b3884690ea1792a06a9e79b700c23c4be3a65c1bc4910b114a0c97f6d70d6` |
| `tests/packs/timeline/test_cli_commit_trim.py` | `6fff510a8` | `966227db8797d7421d592f04d8f508eab517d8b5` | `137787402ff3fe7de40042ce2a8a44eb71240f1c3d3bee9190b050b848a1e157` | `39076f8dea1c8e61a1a3abd75a39f9e3a2bb169b965145d96652b4e295daaec3` |
| `tests/packs/timeline/test_cli_native_sheet.py` | `6fff510a8` | `6602ef1abe4dd658507069acf6f39128b6d32613` | `8f552ed4f528efbaa60343fe1798982a4ae8d5bdd0bc315f08023693dd33a9cd` | `33107747f5e39896325a1a1bbdc0fc3656d9a2f8d0d6a919b5d690af7d486375` |
| `tests/packs/timeline/test_verbs_working_copy.py` | `6fff510a8` | `6fd04fa7445cf75a9ee0f9aec794918f673ea2e2` | `abf2d6b6e831d3708da9b028a216a24c33097cd8c9a6b731ee8b20a35bc73afe` | `d643c5de4e57f4b23935c571488f734767b9a369f2f3c74747433113f594b60d` |
| `tests/sdk/test_timeline_checkout_history_runtime.py` | `e8a29acc0` | `73092f1a333e10be6d7966213ccc0a82a7ec7106` | `2575cb71554a104a48eba75bc5edb0998901e1014dca865a42088844a966db2a` | `a866d05df1cd382fe6e0f9e46ea71215688bbe80115dbca6cbd9dc93bd4138f6` |

Protected current-base SHA256 (unchanged):

- `astrid/sdk/timeline/inverse.py`: `fdae9b17f000a6968009222233327a0662748d0289d090a03c36f0e213121ee7`
- `astrid/sdk/timeline/_step_undo.py`: `27fd6a86b215ac99ea163222aa286cabf0ca319af15086cbc567323340991fb7`
- `astrid/sdk/timeline/_root_inverse.py`: `44cb4aa3481a11b1b13bd6f3995905bfdda41edf411ff484311ebc5ca1fc80cd`
- `astrid/sdk/timeline/_commit_patch.py`: `c41946a5efe138039cac06d58e5e46fb253390000cf2fc5655a7b10333954c1a`
- `astrid/sdk/timeline/_commit_preview.py`: `924dc930b624f6a9a85c38745b1070a0e35f35c8d905287d23eadf5cc51e4924`
- `astrid/sdk/timeline/commit.py`: `d51f1a2957fb869a6d8221e569343429030e4c9895b195d366bb481fd4832394`

## Decisions / blockers / next step

Only selected reviewed blobs, authorized deletion and shrink-only baseline generation were applied. No product design decision was changed. Exact reviewed test bodies were preserved even though their combined fixture scopes conflict. Joined PASS is blocked pending a separately owned repair of global fixture registration; the manager should review the concrete source diff, request that bounded fixture repair, and qualify the same 184 cases on the then-current integration base. Do not merge this deletion draft before P1GO. Harness owns the final task commit; this worker creates no merge request.

Generated ratchet source SHA256:

- `scripts/reshape/baselines/mypy_astrid.json`: `6f9f20c21ba495a3e6fd42657ccb152ab94b15d45e9ca7cbea604cc19886c50b`; generated only with normal --write-baseline tool.
- `scripts/reshape/baselines/ruff_astrid.json`: `3825d8b5cc935020c879f57bb841e01403ef1e75690e31ad4363e824a2460e7a`; generated only with normal --write-baseline tool.

Deleted source provenance: `astrid/sdk/timeline/document_diff.py`, starting blob `e61de49fc6ccbcf66ab47fb41f254c47ab8110ba`, SHA256 `9a156686486811cc8017bed44d461dd81b7281cbfa24caa91e7cd9f69f9f107f`. Only whole-file deletion; no replacement executor.
