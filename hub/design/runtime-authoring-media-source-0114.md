Implemented the available files; **original media-roundtrip acceptance is blocked on the reserved capture hook**. Wrote `commit-msg` and `BLOCKED`; no `DONE`.

- `publish_authoring_candidate` now uses authenticated history/immutable reads and v2 `commit_timeline`, with guarded patches and atomic merge.
- Added registered `media.admit`: exact Runtime raw/catalog captures, recorded dependencies, and rejection of unreferenced or mismatched inputs. Imported receipts provide no authority.
- Migrated `TargetBoundAuthoringBundle.publish` and the first test’s authorised fixture plumbing.
- Preserved all nine original first-test assertions and scenario operations after fixture normalisation. Second test unchanged: SHA-256 `7816bf80a3ede0cd774ed337dd466de5e9a781292725ccee195dcb168de33eba`.
- Left `commit.py`, `sdk/remote.py`, occurrence translation guards, schemas, clients and pins untouched.

Required `commit.py:961–988` handoff, after command validation and before execution/replay:

```python
from astrid.sdk.timeline.native_media_admission import capture_media_admissions

verified_media.extend(capture_media_admissions(port, calls))
```

The function returns only actual port captures; raw pins use `raw_media_info`, and five-field selections use `selected_media`.

For the reserved `sdk/remote.py` `_Writer`, replace its retired publisher method with:

```python
def __getattr__(self, name):
    return getattr(self.owner._client, name)

def commit_timeline(self, project_id, timeline_id, body, *, idempotency_key):
    self.result = self.owner._typed(
        "commit_timeline", project_id, timeline_id, body,
        key=idempotency_key, idempotency_key=idempotency_key,
    )
    if not self.result.ok:
        raise RuntimeError(self.result.error.message)
    return {"data": self.result.data, "receipt": self.result.receipt}
```

Validation:

```bash
PYTHONPATH=$PWD:/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_CHECKOUT=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/timeline/test_authoring_commit_media.py
```

**4 passed.** Covers production retry/no second history write; stale, modified-key, forged-base and foreign-candidate refusal; real-port raw/image/audio capture; foreign/undeclared pins, catalog digest mismatch, unreferenced inputs and forged receipt arguments. Media capture plus command execution is verified; complete media acceptance awaits the hook. The original roundtrip was deliberately not rerun.

```bash
/home/user/work/venv-agent/bin/ruff check astrid/core/timeline/authoring_bundle.py astrid/sdk/authoring_remote.py astrid/sdk/timeline/authoring_commit.py astrid/sdk/timeline/native_media_admission.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/_doc_patch.py tests/timeline/test_authoring_commit_media.py tests/timeline/test_authoring_media.py
/home/user/work/venv-agent/bin/python -m mypy --cache-dir /tmp/w-ce96520eed/mypy-current astrid/core/timeline/authoring_bundle.py astrid/sdk/authoring_remote.py astrid/sdk/timeline/authoring_commit.py astrid/sdk/timeline/native_media_admission.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/_doc_patch.py
```

Both passed. Matching four-existing-path mypy invocation: parent **2 diagnostics**, current **0**. Repository baseline command, `PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-ce96520eed/mypy-baseline-check /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_mypy_baseline`, failed on missing YAML stubs and NumPy stub syntax; dependencies unchanged.

These passed:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m scripts.reshape.check_repo_hygiene
git diff --check
```

Source parent: `b61cebe8e0d6e062f15da922f3812d7b6718f12e`; prospective tree: `56a50852194f8f19c636bf194ab43da8699d9dc6`. Eight changed paths are listed in the lint command.

Runtime verified as `458595850c354f4403dabc58a72b98bebbc2c3a3`, origin `banodoco/banodoco-workspace-runtime`; service, port, coordinator and store bytes match qualified `abd47e68…`. Frozen refs remain Agent `11caf1d9de29`, Runtime `31c7ac3a00f7`, App `8f0c2484463e`, Composition `c82eb7c459d0`. Scratch: 19 MiB. No full suites.

Next: owners join the two reserved hunks, then run the original first roundtrip and focused regression together before independent Agent review/home merge.