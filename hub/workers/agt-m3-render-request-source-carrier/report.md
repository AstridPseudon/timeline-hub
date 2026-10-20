## Report

- Restored the lost private `RenderRequest.verified_source` carrier in `astrid/core/rendering/contracts.py:754`.
- Preserved reserved-key rejection, wire omission, caller-replacement guards, and RenderService authority validation (`service.py:353–358`).
- Existing carrier confirmed: `PreparedTimelineInputs.timeline_source`; no new DTO/factory or Viewing logic touched.
- Reactivated the four unchanged positive capture tests and added direct request/service tests.

Tests:

- `pytest ... test_verified_source.py test_contracts.py test_capture_source_runtime.py` — **134 passed**, 27 integration deselected.
- Real claim/materialization control with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime` — **4 passed**.
- `git diff --check` — passed.
- No full suite run.

Source SHA256: `astrid/core/rendering/contracts.py` = `a8b7403f1247b30c00c14dda0d388ed264adb205151b91b3b5a0646ca64c0211`

Commit message written and `DONE` marker created.