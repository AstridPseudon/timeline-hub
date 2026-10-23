# CommitV2-current-D12 — agt-V2-current-D12-join-0541

Implementation complete; targeted evidence PASS. Independent review of this new composition is still required. No blockers remain. Harness commit pending; this worker did not commit or change Git refs.

Base: `900ba8f09cff705b5d2db8d31021e4c2ad3f7786`, including reviewed current fork `1f418aea4`. Exactly five changed paths: `astrid/sdk/timeline/validation.py`, `astrid/sdk/timeline/_commit_timing_validation.py`, and the three new donor tests `test_commit_legacy_text_reference.py`, `test_commit_fps_d12.py`, `test_commit_anchor_d12.py` under `tests/editing_conformance/`.

## Donor map and composition for review

Read PLAN §3, BOARD-HEADER, commit-v2 §§1–5, donor reviews 0521/0524/0533, author anchor report, current fork review 0533, source report/call manifest 0504 and current-port brief 0527. The current fork manifest's ten source hashes match HEAD exactly, source-set `e7c96edb911f6a1d89fb218cc951fea6094ee350f2ab62cbf039f951239e6830`.

- `736cfdd15a83c9d22bfcc1269967d3b319eae9a8`: exact legacy text-reference validation and selected-element parameter hunks, plus byte-identical new test.
- `e50beb3063df13b5faa86896eb5161ba1df8cb54`: exact FPS basis/parity helpers and final validation call, plus byte-identical new test. Kept reference donor's equivalent baseline docstring while retaining the current authenticated-source documentation; avoided overlapping donor docstring replacement.
- `ad4e459a32d9abbbe28794fb13ef45b1b9cd6893`: exact legacy word-anchor basis/exemption hunks, plus byte-identical new test.

Applied narrow worktree patches, never old whole production files. Novel composition is explicit: final validation now executes both donor reference validation and FPS parity while preserving current `source_bundles` interface/conditional forwarding; timing validation executes the anchor donor's exemptions while preserving current immutable `document_from_bundle(..., source_bundles=...)` and recursive fallback forwarding. These two composed caller bodies need review. All other helper ASTs match either current HEAD or their exact assigned donor. All eight other files in the ten-file fork manifest remain byte-identical to current HEAD; authenticated inverse reconstruction/closure/capture production files are untouched. No new policy, parser, numeric equality, guessed binding, or write-invalidity exemption was added.

Exact FPS normalizers and timing arithmetic remain unchanged. Declaration, target, physical-owner, retained schema and later timing guards remain active. No writer/G234/replay-c793/inverse48d/show changes were imported. No schema, generated, pin, artifact manifest, client, baseline or shared dependency edit; no deleted files. All tests retain their assertions, with no skip/xfail edits.

## Mounted caller and v2 preservation

Unchanged production `RuntimeCommitService.commit` at `astrid/sdk/timeline/commit.py:1117` imports `validate_final_candidate`; lines 1119–1125 pass the final plan, actual landing baseline, retained schema captures, realm and authenticated inverse sources before canonical preparation and accept/preview. The donor production tests and unchanged real native neighbor exercise this path.

The change does not alter request/reply transport, recorder, metadata, history, rebase or idempotency code. Full v2 fields remain: api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands/label; steps(id,label,intent,tags,command_ordinals,patch,reads); merge(fields|atomic), reads/dry_run/source/rationale/group_id and stable idempotency. Existing complete {data,receipt}, accepted/merged/authentic historical rebased, canonical document/head/revision/digests/records/effects/steps/dependencies/history/undo_steps, conflict reason/head, invalid code/path/hint/suggested command and preview would_status accepted|merged remain at current source. This bounded task does not independently requalify every historical reply case; no full-suite claim.

## Environment and exact commands/results

Working directory `/home/user/work/wt/agt-V2-current-D12-join-0541`. Scratch locator `workers/agt-V2-current-D12-join-0541/tmpdir` contains `/tmp/w-2ad2000c3b`. Shared installs were read-only. Runtime source is a private `git archive` of exact `495769531de8d79d27a2d8022851d75b92f04ebe`, tree `0651fbfe829b4cebb0cfb0fa7540d44e9d999344`. Verified all **466 tracked files** byte-for-byte before and after tests, with no extra files. This includes merged inverse claims, archival and alias production code; the advanced shared Runtime checkout was only a Git object locator.

Common direct test environment:

```bash
export TMPDIR=/tmp/w-2ad2000c3b
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/tmp/w-2ad2000c3b/runtime-495769531
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
P=/home/user/work/venv-agent/bin/python
```

Required lane, **110 passed in 5.24s** (`required.log`):

```bash
$P -m pytest -q -p no:cacheprovider --basetemp=/tmp/w-2ad2000c3b/required tests/editing_conformance/test_commit_legacy_text_reference.py tests/editing_conformance/test_commit_fps_d12.py tests/editing_conformance/test_commit_anchor_d12.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_timing_validation.py
```

Fork controls, **25 passed in 5.53s** (`fork.log`):

```bash
$P -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-2ad2000c3b/fork tests/editing_conformance/test_provider_occurrence_fork.py tests/editing_conformance/test_recipe_occurrence_fork.py
```

Exact causal controls from review 0533's 188 lane, **98 passed in 28.82s** (`causal.log`):

```bash
$P -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-2ad2000c3b/causal tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py tests/sdk/test_timeline_commit_v2_errors.py tests/timeline/test_meta_validator.py
```

Detached provider tests intentionally use their unchanged `runtime_abi` fixture for ABI exceptions/metadata; actual command execution is Agent production code. The native neighbor below uses real Runtime modules.

Only one original native node selected, **1 passed in 3.21s** (`neighbor-original-seed.log`). It is entirely in-process RuntimeService/store plus its historical seed subprocess; no daemon, localhost, browser or socket suite was run. Exact passing command with explicit production import-origin assertions:

```bash
env -u ASTRID_WORD_ANCHOR_SEED_RUNTIME TMPDIR=/tmp/w-2ad2000c3b PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-2ad2000c3b/runtime-495769531 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -c 'from pathlib import Path; import runtime_protocol, runtime_protocol.service, runtime_protocol.timeline_commit, runtime_protocol.timeline_commit_port, astrid.sdk.timeline.validation, pytest, sys; root=Path("/tmp/w-2ad2000c3b/runtime-495769531"); modules=[runtime_protocol, runtime_protocol.service, runtime_protocol.timeline_commit, runtime_protocol.timeline_commit_port, astrid.sdk.timeline.validation]; [print(m.__name__,m.__file__,flush=True) for m in modules]; assert all(Path(m.__file__).is_relative_to(root) for m in modules[:4]); raise SystemExit(pytest.main(sys.argv[1:]))' -s -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-2ad2000c3b/neighbor-original-seed -m integration tests/editing_conformance/test_native_word_anchor.py::test_native_move_refuses_anchor_basis_until_explicit_clear
```

Initial invocation of this same node mistakenly set `ASTRID_WORD_ANCHOR_SEED_RUNTIME` to current Runtime. It failed **before the body**, in the historical `seed()` subprocess's pre-cut publication API, with Runtime `ConflictError: destination_occupied` (1 setup error in 2.64s, `neighbor.log`). Corrected only the process environment to the original reviewed command's unset seed override; the unchanged fixture then used its exact historical `80973d34ae10e498d7213c30287012c9876f4b1a` seed and current exact Runtime for measured edits. No fixture/guard/client waiver or product fix. Two invocations are transparently reported; one test body ran and passed. No duplicate 54-node lane.

Protected fixture remains byte-identical to `38e806316`, SHA256 `4ebec0fa3d56a51a2fdd59a23f04bf256dc50fbcf45659086217baa9f51b6553`; original native test remains byte-identical to `5292b388a`, SHA256 `ab07f5b9cda3a42d0c9273917b46d9486c39b453b979d2ad5d39df5528d4179f`. An integrity-script attempt initially compared the test against the older 38e status expectations; corrected the comparison to its proper protected 5292 revision, without touching source.

Quality commands (all PASS; logs under scratch):

```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-2ad2000c3b/ruff $P -m ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py tests/editing_conformance/test_commit_legacy_text_reference.py tests/editing_conformance/test_commit_fps_d12.py tests/editing_conformance/test_commit_anchor_d12.py
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-2ad2000c3b/ruff make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-2ad2000c3b/mypy-scoped /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py --follow-imports=skip
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-2ad2000c3b/runtime-495769531 MYPY_CACHE_DIR=/tmp/w-2ad2000c3b/mypy-normal /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 $P scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 $P scripts/artifact_manifest.py --check
git diff --check
```

Scoped Ruff: all checks passed. Normal Ruff: **2150/2150**. Scoped persistent private mypy (0529 interpreter): **no issues in 2 source files**. Normal mypy: **1915/1915**. No baseline/budget increase or edit. Vendor: `ok runtime.lock.json`. Artifact: `artifacts.json is current`. Whitespace PASS.

Import origins, captured in `import-origins.log`: Agent validation/timing/client resolve from this worktree; `jsonschema`/`referencing` from `/home/user/work/venv-agent/lib/python3.13/site-packages`; actual Runtime service/store/timeline_commit/port resolve under `/tmp/w-2ad2000c3b/runtime-495769531/runtime_protocol`. Python `/home/user/work/venv-agent/bin/python` is 3.13.16; persistent typechecker is `/home/user/work/venv-agent-typecheck-v2/bin/python` from 0529, Python 3.11.17. Native passing log independently prints/asserts the production Runtime origins.

## Source identity and next step

Final ten-file source-set (same manifest path inventory; compact sorted JSON of path -> SHA256): `e8ea81e61800a47b1ff528d587d3189378b9c30e1b0915f57348f561020e6743`.

```json
{
  "base": "900ba8f09cff705b5d2db8d31021e4c2ad3f7786",
  "source_set_sha256": "e8ea81e61800a47b1ff528d587d3189378b9c30e1b0915f57348f561020e6743",
  "source_sha256": {
    "astrid/sdk/timeline/_commit_patch.py": "22204638d7317bab588b513e85d2b74da375b81bd47ff4e10dd47170de15228c",
    "astrid/sdk/timeline/_commit_timing_validation.py": "e224316936d2753e94c7c3fe1b15c34a771a3525698f78c0f34ecc492c6ff3bf",
    "astrid/sdk/timeline/_doc_patch.py": "9e6d6c4189735b2bc239c26ed036cfb84ecf2dacccadf1a7e0702a05006e669d",
    "astrid/sdk/timeline/_root_inverse.py": "9711d1a6710d44c51bf8091783224f196aebae466f2c57fba03143d3597c4ced",
    "astrid/sdk/timeline/commands.py": "9bae22056be03bdecdc9a83176b068b1883d71724aa3c83436461ca711eaf35c",
    "astrid/sdk/timeline/commit.py": "065a0acdbb74d0458b13d26841e7e4081c6a6c19eecdd3f79639de3ea9159d7c",
    "astrid/sdk/timeline/inverse.py": "6d2c0bed4c963889c313a94d35d4b7273ab34b3c5e17ba0274e657f71c6f3400",
    "astrid/sdk/timeline/native_occurrence_duplicate.py": "d3bb8b88ef5f315ebba67e375b97f3da6f622112901ce35dc1f97bb584e83156",
    "astrid/sdk/timeline/native_occurrence_fork.py": "bb129592203eb0e8bd6353c804d335ce13dca1441813ad266451016d7c7a0d7d",
    "astrid/sdk/timeline/validation.py": "140f02b03f9521690f791f5149a3c868b68d2c9cc0b12148ba5b8106855b4074"
  },
  "changed_sha256": {
    "astrid/sdk/timeline/validation.py": "140f02b03f9521690f791f5149a3c868b68d2c9cc0b12148ba5b8106855b4074",
    "astrid/sdk/timeline/_commit_timing_validation.py": "e224316936d2753e94c7c3fe1b15c34a771a3525698f78c0f34ecc492c6ff3bf",
    "tests/editing_conformance/test_commit_legacy_text_reference.py": "bdbc7ef550b4b800967c16847679c6722be51d09a00275a79645fc67650ef222",
    "tests/editing_conformance/test_commit_fps_d12.py": "02fe9e779f50db2f5b3a7d2537f62df6cd10db9f7506957cdf44438af2e5963d",
    "tests/editing_conformance/test_commit_anchor_d12.py": "b747ee39b4873e4d8a9079bb6c6836a385bff52e0982ac860b5722bb93db28a2"
  }
}
```

Recommended next step: independent review of the two composed validation callers, then harness/manager integration of this worker's own commit only, named CommitV2-current-D12. Broader history/replay/HTTP, D14 undo positives and full/native14/crash24/browser/heavy/farm suites were not run and are not qualified here. The requested bounded evidence is 234 passing tests; no product failure remains.
