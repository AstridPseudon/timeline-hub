# G5 fixture-current return report

- Current pre-harness commit: `bac094180aef38a77b86ab165962e6159f873c60`.
- Donor: `a63296af6fd16680cfba59d60f2f30ec658dee84`, applied as the file diff `98ef2f9c95fd43d88cca2909d8d1518302e3050c..a63296af6fd16680cfba59d60f2f30ec658dee84`.
- Real Runtime checkout used: `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`.
- Donor path mapping: all 47 paths from `git diff --name-only 98ef..a632` were applied from `a632:path`; `astrid/sdk/timeline/document_diff.py` is the donor-authorized whole-file deletion. The current changed path set is exactly the same 47 paths (42 tracked changes plus 5 additions).
- Exact source audit: every non-frontdoor path is byte-identical to `a632:path`; the only authorized source mismatch is `tests/packs/timeline/test_cli_document_commit.py`.
- Front-door current SHA256: `e5ffb3e24a6fb13d6b9111d5fceb93ce1d5138eb0b9aaa4bef0b5d70cdef3865`; donor SHA256: `2e6073f52404dafdd3d76f5e385335fc876ecba22e995b8e2c4a747a5875e513`.

## Authorized fixture hunk

Removed the global plugin declaration:

```python
pytest_plugins = (
    "tests.sdk.test_timeline_commit_provider",
    "tests.sdk.test_timeline_public_command",
)
```

Added module-local fixture imports:

```python
from tests.sdk.test_timeline_commit_provider import runtime_abi  # noqa: F401
from tests.sdk.test_timeline_public_command import public_session  # noqa: F401
```

This retains the same fake ABI for the front-door module's 12 controls while preventing the fake `runtime_protocol` module from becoming a global plugin fixture for authentic native Runtime tests. No fake `__file__`, guard waiver, fixture/body weakening, skip, xfail, deselection, or exclusion was added.

## Body/source custody

The eight selected test files' AST body maps all match their donor versions. The audit covered 181 test/helper function bodies in those files; the joined collection was 184 cases.

| File | AST body count | mapping SHA256 |
| --- | ---: | --- |
| `tests/packs/timeline/test_cli_parity.py` | 31 | `8efb2aac518d7b85378df2bec6669763bf7a349a09f5eed0cfe05020fd97fe53` |
| `tests/packs/timeline/test_cli_status_publish.py` | 24 | `e3664700cdd845d632d1490082660a14c8fee7fb978005c33a5b6ad35ce80442` |
| `tests/packs/timeline/test_cli_document_commit.py` | 18 | `419fb32f54843c53c721d8d21d75071fcbaededf4038e4d3d08f611851b96caa` |
| `tests/packs/timeline/test_cli_commit_move.py` | 20 | `dfc5982f9199090c0a68a090eeb461c84c4cd2425d6e24b9442dbe25430d509d` |
| `tests/packs/timeline/test_cli_commit_trim.py` | 10 | `84c5cde6e4e572806debce92ca7d422ac60684c2defdd587c171679618999cc7` |
| `tests/packs/timeline/test_cli_native_sheet.py` | 20 | `c00c89e1d96b907d398fa595790a01163c9d2ea6a88de388596e96614f635345` |
| `tests/packs/timeline/test_verbs_working_copy.py` | 48 | `bdce6131596488f0793edf8a27f8d513b056a026c6f20b9500872c83e8786b48` |
| `tests/sdk/test_timeline_checkout_history_boundaries.py` | 10 | `d52ad97d9ed05ed6416a8bd0ba4aa2f2bb72131fc0dd4c9e2aea46ae2ad333c1` |

Protected current-base files are unchanged from `HEAD`:
- `inverse.py`: `fdae9b17f000a6968009222233327a0662748d0289d090a03c36f0e213121ee7`
- `_step_undo.py`: `27fd6a86b215ac99ea163222aa286cabf0ca319af15086cbc567323340991fb7`
- `_root_inverse.py`: `44cb4aa3481a11b1b13bd6f3995905bfdda41edf411ff484311ebc5ca1fc80cd`
- `_commit_patch.py`: `dff428d155cbb009d36412f973fa090a5d48f2fec2a72f14fd6a6c43f386f481`
- `_commit_preview.py`: `70ad40a78248805bee83fe0261145b7e0c3b470ebb770f5f78526900a42dfce5`
- `commit.py`: `b73586b0254de7c0d7a84c5f10f4f1e0a662e92568adcfcce21967a045aa57fe`

## Verification

PASS — exact joined command, with the eight donor-selected files and no filtering:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/agt-G5-fixture-current-return-1633 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=.:/home/user/work/runtime timeout 300 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -pno:cacheprovider --timeout=30 --basetemp=/tmp/agt-G5-fixture-current-return-1633/joined tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_cli_status_publish.py tests/packs/timeline/test_cli_document_commit.py tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_commit_trim.py tests/packs/timeline/test_cli_native_sheet.py tests/packs/timeline/test_verbs_working_copy.py tests/sdk/test_timeline_checkout_history_boundaries.py
```

Result: `184 passed in 39.22s`.

PASS — `PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/agt-G5-fixture-current-return-1633/mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline`: 1911 current, 1911 baseline, exit 0.

PASS — `PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/agt-G5-fixture-current-return-1633/ruff /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline`: 2148 current, 2148 baseline, exit 0.

PASS — `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`: manifest matches.

PASS — `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`: artifacts current.

PASS — `git diff --check`.

No full suite, P1–P4, original four SDK tests, native14, V4, browser/live HTTP, or independent review was run. The first attempted joined command was not executed because the harness-provided worker `tmpdir` is a regular file; the successful run used the allowed named `/tmp/agt-G5-fixture-current-return-1633` scratch directory. No product/shared dependency files were modified.

