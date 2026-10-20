# Agent accounted short attempt review

## Verdict: REJECT

Reviewed candidate `973c082e451844aeca399ac4d8a04f3039216cc0`
(`tl/vw-m3-accounted-short-attempt-concrete-patch`) against current root
`78ff61d599b7de467b7caeea3b49588050026aec` (`tl/integration`). Read
`design/runtime-short-browser-scratch-budget.md` and the Runtime answer
`design/peer-runtime-to-viewing-20261020T194312Z-scratch-budget-answer.md`.
The rejected external-`TMPDIR` design was not carried into the short-root
portion of this candidate.

## Blocking executable defect

The exact cumulative diff against current root removes the host-only verified
source custody check:

- `astrid/core/rendering/contracts.py` no longer obtains or retains the
  inherited `VerifiedTimelineSource` in `RenderRequest`.
- `astrid/core/rendering/service.py` no longer compares the request's source
  with the inherited source or calls `source.validate(...)` before rendering.
- `tests/packs/rendering/test_verified_source.py` deletes the strict request
  propagation, reserved-key, and lost-authority refusal tests.
- `tests/sdk/test_capture_source_runtime.py:198-232` changes the real
  saved/candidate source propagation assertion into
  `@pytest.mark.xfail(strict=True, ...)`.

This is a source/receipt-binding regression unrelated to browser scratch. It
does not require a Runtime DTO or public authority field: the existing
host-only environment carrier and `VerifiedTimelineSource` validation can
remain private. As presented, a malformed ambient source is accepted at the
request boundary. Direct probe result:

```text
{'constructed': True, 'has_verified_source': False,
 'to_dict_has_verified_source': False}
```

The probe set `ASTRID_VERIFIED_TIMELINE_SOURCE=not-json` and constructed a
`RenderRequest`; the candidate neither rejected the malformed authority nor
performed the old host-only validation. This violates the requirement to keep
all original strict assertions and leaves source identity unverified at the
render service boundary. Restore the strict validation/tests (without adding
any Runtime/public field) before approval.

## Short-root custody review

The requested short-scratch change itself is directionally correct:

- `root_preparation.py:_accounted_attempt_root` only opts into `.r-*` when
  internal invocation is active, the progress path has the exact marker name,
  the marker ancestry and staging/output ancestry have no symlinks, the
  attempt root is an existing owner-only directory, the staging workspace is
  its direct child, and the output remains under that attempt's `outputs`.
- The browser temp directory is created with `TemporaryDirectory(prefix=".r-",
  dir=attempt_root)`, so normal MP4 browser files remain inside the already
  admitted attempt tree. No external `TMPDIR`, Runtime DTO, public knob,
  codec field, authority field, or quota exemption is introduced by this
  portion.
- Existing `_attempt_tree_bytes`/`_storage_tree_bytes` live/final envelope
  walks therefore include `.r-*` bytes; `.r-` is also classified as a renderer
  workspace for diagnostics.
- `TemporaryDirectory`/`ExitStack` removes the browser child, and the existing
  GenericHost cleanup removes only the ephemeral attempt root or retains it
  when cleanup/process ownership is uncertain. The candidate does not broaden
  cleanup to an external directory.
- Ephemeral allocation retains the `astrid-attempt-` prefix used by
  `storage_ownership` reclaim, while `mkdtemp` supplies uniqueness. Explicit
  `attempt_base` allocation still uses `task_id-attempt_id` and refuses reuse;
  both paths are mode `0700` after allocation. Existing named attempt layouts
  remain discoverable by the established prefix policy.

The path checks are ordinary pathname checks rather than an atomic directory
FD/inode handoff. I did not claim a concurrent same-UID rename/symlink race is
solved; that remains an unverified limit for any stronger local-adversary
interpretation of the custody requirement. The blocking finding above is
independent and directly reproducible from the committed source.

## Evidence run

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_remotion_attempt_temp.py
5 passed in 1.32s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/core/test_generic_host_attempt_isolation.py \
  tests/sdk/test_storage_ownership.py::test_registry_describes_all_reported_persistent_roots \
  tests/sdk/test_storage_ownership.py::test_package_persistent_writers_are_registered \
  tests/core/rendering/test_service.py::test_managed_support_uses_retained_attempt_through_real_transport \
  tests/core/rendering/test_service.py::test_managed_support_keeps_foreign_progress_transport_rejection
12 passed in 2.53s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -c 'import os; from astrid.core.rendering.contracts import RenderRequest; from astrid.core.rendering.verified_source import SOURCE_ENV; os.environ[SOURCE_ENV]="not-json"; request=RenderRequest(schema_version=1,timeline_path="/tmp/timeline.json",assets_registry_path="/tmp/assets.json",output_name="result.mp4"); print({"constructed": True, "has_verified_source": hasattr(request, "verified_source"), "to_dict_has_verified_source": "verified_source" in request.to_dict()})'
{'constructed': True, 'has_verified_source': False, 'to_dict_has_verified_source': False}

git diff --check 78ff61d5..973c082e
pass
```

Not run: browser/MP4 qualification, any test-service run, full suite, root
pytest, or broad unchanged suites. The manager owns actual isolated MP4
qualification as instructed.

## Recommended next step

Drop the verified-source deletions/xfail from the candidate or restore their
host-only equivalent and original strict assertions, then re-run the focused
source-custody tests. Re-review the resulting tree; the short `.r-*` layout can
then be considered on its own custody merits.
