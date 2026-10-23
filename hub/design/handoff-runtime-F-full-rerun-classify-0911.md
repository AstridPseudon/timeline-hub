# Runtime F full rerun handoff — 2026-10-23

## Disposition

The sole manager-requested full, `runtime-full-1023091021-9458`, completed
with **FAIL**: `1 failed, 6237 passed, 26 skipped, 15 xfailed, 0 errors, 12
warnings`, exit `1`, pytest `430.86s`, service elapsed `432s`. This is not an
all-green result. No second full was requested or run locally.

The service command was:

```text
env ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

Captured identity:

| Item | Value |
|---|---|
| Runtime commit/tree | `a01e9d806e08ee4ff6d35bad18dddafa1f09f862` / `645de16949982723f67db58be204611cf0a5bb95` |
| Snapshot key | `b6cba05f52a5847eef3fa2f126783bd8` |
| Agent | `2e21af300abbefc8afbad217189fa4715cf82616` |
| App | `2d3d14d998be2b59fb017b4c0f2458c3a7340423` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` |

These Runtime and Agent heads still match current heads. Relevant captured
Runtime blobs are unchanged: package root `665d99555e0333008cf0e15906a429c1ba6b5953`,
DTO module `8cfbcc4147f71dbbaaae5749317bafbaac147a7f`, schema
`de301d13e44bad44c84bac35f8d929e24fbf55ff`, and test
`4a10974a86d1b588512926a7311991200e31f1d0`. The same blobs were in the
previous `8246` captured tree, so the existing export-cause report is reusable
for the same frozen bytes/cause. No external-source drift occurred.

## Sole remaining failure

`tests/test_timeline_current_union_contract.py::test_public_python_union_types_and_nested_item_references_resolve`

```text
AttributeError: module 'astrid_runtime_client' has no attribute 'DocPatchArgs'
tests/test_timeline_current_union_contract.py:119
```

Classification: real generated-client public-namespace regression, known
P1/freeze gate. `DocPatchArgs` is present in
`packages/python/astrid_runtime_client/timeline_commit_types.py:61`, but absent
from `packages/python/astrid_runtime_client/__init__.py:37-76` and the matching
`generators/python_client_init_template.py`. Causal v2 wire adoption is
`dba528b2d2`; owner is R0/generated clients. This is not an upstream-4563
baseline and not a new R2r store/provider failure.

The exact permitted targeted probe reproduced the same failure in `1.10s`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_current_union_contract.py::test_public_python_union_types_and_nested_item_references_resolve
```

The old 74 fixture/setup failures are cleared in this run only because their
actual test bodies pass: the service reports zero errors and the corrected
cohort is included in the 6237 passes. The old 8246 failure/error shape was
`31 failed, 6162 passed, 26 skipped, 15 xfailed, 45 errors`; the current run
leaves only the known export gate.

The 26 skips are the expected Linux-service native-Windows locations from the
raw summary (`test_m1_review.py` 225/240/255/280/290;
`test_platform.py:273`; `test_platform_filesystem.py` 49/88/101;
`test_platform_windows.py` 20/27/44/61/81/91/109/126/173; and
`test_dirfd_windows.py` 293/318/343×2/360/378/533/581). The 15 xfails are the
existing RT02/D04 direct-writer/clip-replacement/second-client deferrals listed
in the service summary; none were modified.

Full worker evidence and exact xfail names are in
[`workers/rt-F-full-rerun-classify-0911/report.md`](../workers/rt-F-full-rerun-classify-0911/report.md).
`git diff --check` passed; no repository, service, schema, client, pin, or test
changes were made. Ruff/Pyright are N/A for this read-only classification.

Next action: R0/generated clients repairs the package-root import/`__all__`,
runs the exact node and generator acceptance, then the manager decides whether
to authorize a later full. Do not claim full PASS until an authorized full has
zero non-passing failures/errors.
