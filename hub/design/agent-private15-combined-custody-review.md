# Agent private15 combined custody review

Decision: **APPROVE FOR ONE NATIVE PROOF**.

Reviewed identity:

- commit `6a8dfb2286659dd67c108a230d24f14ba4599344`
- tree `5f5449a2b668c96a9bc816cea1dd73eacc04f7ab`
- parent `8444290337e2f7cb22e39b995834a80cb1cc1ef2`

## Review disposition

The combined executable source closes the two earlier custody findings without
adding a new authority or wire path.

- Media authority uses the two existing concrete `WorkspaceClient` reader
  methods and the existing generated C3d operations. The arbitrary callable
  lookup is gone; mutable caller/client identity is not used.
- The output selector recursively checks the known project, asset,
  generation, variant, object/digest, catalog, association, and version
  claims. Contradictions fail before proposal/native success, including old
  authored media claims.
- Runtime's exact five-field selection is required. Verified media must be
  `audio/wav` with positive integer size and finite positive intrinsic
  duration; the same normal WorkspaceClient reads the object bytes and checks
  exact size and SHA-256.
- The initial admitted revision/publication pair is retained and checked
  before and after synthesis. The proposal's outer producer/fence and
  admitted target are host-owned and distinct from the inner speech task.
- Changed output is the existing exact six-key proposal with its digest,
  written through the standard manifest. `planned` and `unchanged` retain
  successful report results. The public 22-positive behavior and publication
  path remain intact.
- Managed preparation cannot publish. The action returns a proposal/report
  for the requester; no worker publication, parallel writer, or outbox claim
  is introduced.

The approved normal pin remains the parent context. `runtime.lock.json` and
the frozen schema are unchanged from that parent; the schema digest remains
`84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`, and the
lock points at Runtime producer `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`.
The only new WorkspaceClient wire names are the two operations already present
in that C3d generated client.

## Evidence

All commands ran against this candidate with dependency-only shared
environments read-only and test temporary roots under `/tmp`.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-private15-combined-review-246 tests/core/execution/test_python_action_context.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_draft_voiceover.py tests/packs/video_editing/test_draft_voiceover_managed.py tests/editing_conformance/test_recipe_native_voiceover.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py tests/sdk/test_workspace_client_timeline_commit.py tests/test_artifact_manifest.py tests/test_tool_catalog_v3.py
246 passed in 25.81s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-private15-combined-review-public /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private15-combined-executable-source/test_public_baseline.py
22 passed in 0.13s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-private15-combined-review-action tests/packs/video_editing/test_sync_draft_voiceover_action.py
21 passed in 3.01s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567:/home/user/work/wt/rt-pin-c3d26567/tests" /home/user/work/venv-agent/bin/python -B -m pytest -q -s -p no:cacheprovider --basetemp=/tmp/agt-private15-combined-review-real-c3d /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private15-combined-executable-source/test_actual_runtime_readers.py
1 passed in 0.74s
real C3d trace reached media-selection, verified-media, and object-read; WAV was 64,044 bytes and Runtime intrinsic duration was 4.0 seconds.

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-c3d26567
ok runtime.lock.json (matches producer manifest)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567:/home/user/work/wt/rt-pin-c3d26567/packages/python" /home/user/work/venv-agent/bin/python -B -m scripts.reshape.compare_structure_baseline
Structure violations: current=13 new=0 fixed=0

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m ruff check --no-cache astrid/core/execution/executor/_action_context.py astrid/packs/video_editing/actions/sync_draft_voiceover/run.py astrid/packs/video_editing/shared/draft_voiceover.py tests/core/execution/test_python_action_context.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_draft_voiceover_managed.py --output-format=concise
All checks passed!

git diff --check 8444290337e2f7cb22e39b995834a80cb1cc1ef2 6a8dfb2286659dd67c108a230d24f14ba4599344
passed
```

No full suite, live/localhost workflow, browser, renderer, native requester,
TimelineSession outbox/retry/restart, accepted publication, or guarded undo
was run or claimed. The next step is exactly one centrally managed native
requester proof using this Agent commit and the reviewed C3d Runtime tuple,
with the existing requester queue/flush/retry/undo path and real credential
scope; do not broaden permissions or relabel this in-process reader proof.
