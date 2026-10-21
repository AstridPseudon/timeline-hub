# Agent private15 action advisory preservation

## Result

Preserved successful managed `plan_only` and `unchanged` outcomes while keeping
real changed proposals on the private managed path.

- The action now calls the private
  `_sync_draft_voiceover_proposal` entry, never the public
  `sync_draft_voiceover` publication helper.
- `planned` and `unchanged` results are settled as the existing successful
  advisory report in `report.json` plus the universal `manifest.json`. They do
  not fabricate commands, a receipt, a publication, or an authoring proposal.
- A changed result still requires the existing six-key
  `timeline/authoring-proposal` carrier, verifies the outer producer and
  admitted target, validates the proposal, and writes only
  `authoring-proposal.json` plus its manifest.
- The public helper retains its original preparation, validation, CAS
  publication, receipt, and failure behavior.
- The private helper's authoritative-media boundary is checked only after the
  plan has proved that the result is changed. This preserves advisory
  success while keeping changed proposal production closed until the separate
  media-read worker lands.

## Output convention

The current executor output-port schema has no supported optional-output field,
so no new optional wire field or DTO was added. The pack declares the existing
proposal file and the existing JSON report file; the standard result manifest
contains exactly one concrete primary result for each outcome. The report is
therefore an existing report/result-manifest carrier, not a fake proposal or a
new metadata channel.

| Shared result | Settled file | Action result |
| --- | --- | --- |
| `planned` | `report.json` (`application/json`) | `{"report": result}` |
| `unchanged` | `report.json` (`application/json`) | `{"report": result}` |
| changed proposal | `authoring-proposal.json` (`timeline/authoring-proposal`) | `{"authoring_proposal": proposal}` |

## Qualification boundary

The private changed path still fails closed at the existing
authoritative-media-read boundary. This change does not claim native-success,
Runtime media-selection proof, normal private-pin success, requester outbox
submission, retry, or guarded undo. The separate media-read worker owns that
source and may replace only the pending boundary implementation.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_draft_voiceover.py
45 passed in 6.11s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/execution/test_python_action_context.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_draft_voiceover.py tests/editing_conformance/test_recipe_native_voiceover.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py
183 passed in 16.51s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check astrid/packs/video_editing/actions/sync_draft_voiceover/run.py astrid/packs/video_editing/shared/draft_voiceover.py
All checks passed!

git diff --check
passed
```

No full, live, browser, Runtime, normal-pin, or broad qualification suite was
run.
