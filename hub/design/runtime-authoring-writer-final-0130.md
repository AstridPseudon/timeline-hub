Completed **F-authoring-publish-writer**. Wrote `commit-msg` and `DONE`; no commits, merges, installs, or shared-dependency changes.

- `commit.py` adds only the import and `verified_media.extend(capture_media_admissions(port, calls))` after command validation, before execution/replay.
- Remote `_Writer` delegates the five required history/immutable/media-selection reads and calls typed `commit_timeline`, preserving failures and serializing the actual receipt.
- Media admission consumption uses a final separate step. Combining it with child patches caused assertion mismatch; an earlier empty step caused Runtime to project future child revisions. All inputs remain captured before execution. No guards were relaxed.
- Added real media acceptance, exact retry/no-second-write, preview, remote-adapter, and stale/foreign/forged/unreferenced/mutated-input refusal checks.

The required command passed **7 tests**, including the prior four cases:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_CHECKOUT=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/timeline/test_authoring_media.py::test_real_runtime_import_and_parent_publication_roundtrip tests/timeline/test_authoring_commit_media.py
```

Results: worker **7 passed in 8.51s**; scratch join onto Agent `521c88802330901281cc37ba25818baf2575f05e` **7 passed in 8.87s**. The join preserved current rendererless/private projection and public timing code verbatim outside `_Writer`.

Validation used these eight product paths:

```bash
FILES=(
  astrid/core/timeline/authoring_bundle.py
  astrid/sdk/authoring_remote.py
  astrid/sdk/timeline/authoring_commit.py
  astrid/sdk/timeline/native_media_admission.py
  astrid/sdk/timeline/commands.py
  astrid/sdk/timeline/_doc_patch.py
  astrid/sdk/timeline/commit.py
  astrid/sdk/remote.py
)
/home/user/work/venv-agent/bin/ruff check --no-cache --output-format=json "${FILES[@]}" tests/timeline/test_authoring_commit_media.py tests/timeline/test_authoring_media.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m mypy --no-incremental --cache-dir=/dev/null --hide-error-context --no-color-output --no-pretty --show-error-codes "${FILES[@]}"
```

Identical invocations ran against parent and candidate:

- Ruff: **119 → 119; zero new normalized identities/multiplicities**. Inherited: I001×6, E701×112, BLE001×1. The eight previously allowed paths pass standalone.
- Mypy: **13 → 12; zero new normalized identities/multiplicities**. Removed `_Writer`/`AuthoringCandidateWriter` incompatibility. Remaining diagnostics are in `remote.py`: assignment×2, `None.get`×5, `None.__iter__`×2, `executor_inputs` redefinition×1, `dict` argument×1, `_typed` argument×1.

These all passed:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m scripts.reshape.check_repo_hygiene
git diff --check
```

Original body locks:

- First roundtrip unchanged from parent; all **nine original assertions** unchanged from `b61cebe8e0`. Body SHA-256: `a07bcf7fa51b7028fc3e629890b6364e4c6cd3321c2efa35bbe57a01675f8cc4`.
- Entire second ABA body unchanged: `7816bf80a3ede0cd774ed337dd466de5e9a781292725ccee195dcb168de33eba`.
- No changes to `_recording.py`, occurrence commands, schemas, clients, or pins.

Source identity:

- Parent: `9881665b37eccaf36fc43d933cc46f54e309b75a`; cumulative base remains `b61cebe8e0d6e062f15da922f3812d7b6718f12e`.
- Candidate tree: `59ce7894170b08636ce8340a2b47f2c5319206c3`.
- Scratch joined tree: `7abc766ef0c7627ab8b0c45ad49548ffc673e10e`.
- Runtime: `db11ea82978fba1f78cd79aec9563ea0e3372574`, tree `a92a576a8837187558365a0696b062818f445368`. Its only change versus `458595850` is `contract/artifacts.json`; authorization files match `abd47e68`.

Runtime imports resolved under `/home/user/work/runtime/runtime_protocol/`; SHA-256:

```text
service.py                  267bec1aee551e7ea1f92f987adb24268be11c6dd165ee56f24aa68ff2b6a692
timeline_commit_port.py     0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859
timeline_commit_execution.py 2b0c256757f1bf0b3ab3124840250d2d8ef5dbec31a259c4b1e924e295619dd6
timeline_commit_store.py    b1cfdceefc533220ea9a5478f61a971109d1cc2d70fa2c7a76341ffa977f2246
timeline_commit_auth.py     ecc0149ed0c9e93bac5365ca7ab97f5a85a80b2fe3acb6a962b7ecc635c08872
```

No worker blocker remains. Scratch usage: **4.4 MiB**. No full suite or second ABA run. The inherited broad mypy YAML/NumPy stub failure was not rerun.

Next: **independent Agent cumulative review and home merge**, porting reviewed hunks only; this old-ancestry branch is not an integration merge packet.