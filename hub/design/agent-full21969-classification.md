# Agent full21969 classification

Date: 2026-10-21 UTC

## Disposition

The retained run is red, but its terminal evidence does not support a single
all-environment conclusion and does not support “no owned product follow-up.”

The exact terminal partition is in
agent-full21969-exhaustive-failure-partition.md:

| partition | failed | errors | meaning |
|---|---:|---:|---|
| DIRECT | 73 | 0 | terminal trace directly names missing runtime_protocol |
| DERIVED | 34 | 3 | wrapper/child traceback identifies the same missing-module chain |
| UNCLASSIFIED | 31 | 1 | another observed cause; ownership remains open |
| **total** | **138** | **4** | exact retained terminal result |

Therefore the retained log proves the missing runtime_protocol cause for 73 of
138 failures directly. It identifies the same cause through a traceback chain
for a further 34 failures and three setup errors. The remaining 31 failures
are not classified as environment failures. The fourth error is the separate
fixture error native_host not found. In particular, the 65 non-DIRECT
failures cannot be collapsed into “no owned product follow-up.”

No product edit, test edit, dependency mutation, suite request, cancellation,
repeat, or source/test weakening was performed.

## Retained run

Result directory:

    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-venv-agent-child-published14-b9797941-full-1021045238-21969

Summary:

    138 failed, 15840 passed, 456 skipped, 4 xfailed, 85 warnings,
    4 errors, 565 subtests passed in 3351.03s (0:55:51); exit 1

The retained source snapshot is Agent tree
0698a30b3eb42d47db84ed5ed2e21221158795c4. The selected child is
venv-agent-child-published14-b9797941 with installed marker b97979411,
Python 3.13.16. The parent command supplied the Runtime checkout through
PYTHONPATH, while sanitized children did not retain that checkout.

## Evidence boundary

The repeated direct chain is:

    astrid/core/execution/__init__.py:2
      -> astrid/core/execution/persistent_supervisor.py:17
         from runtime_protocol import platform
         ModuleNotFoundError: No module named 'runtime_protocol'

Other direct traces name the same missing package at
astrid/core/foundation/atomic_io.py:16 or
astrid/packs/vibecomfy/production_engine.py:19.

The DERIVED rendering chain is not counted as DIRECT merely because its
payload contains the same text. Its retained chain is:

    astrid/core/rendering/transport.py:328
      -> astrid/core/rendering/errors.py:110
         RendererInternalError / RendererError payload
         -> child ModuleNotFoundError: runtime_protocol

The render-export node is similarly wrapped:

    astrid/packs/rendering/actions/render/task_adapter.py:466
      -> astrid/packs/rendering/actions/render/run.py:9
         -> astrid/core/execution/persistent_supervisor.py:17

The timeline child-import node records:

    tests/sdk/test_timeline_commit_provider.py:101
      -> astrid/sdk/timeline/commit.py:1017
         -> astrid/core/element/project_packs.py:27
            -> astrid/sdk/documents.py:19
               ImportError: cannot import name 'platform' from runtime_protocol

The managed-scene and bootstrap nodes surface the child probe failure as
RemotionValidationError at astrid/core/rendering/remotion_runtime.py:632.
The retained probe evidence identifies the underlying import at
astrid/core/rendering/remotion_runtime.py:26, with
original_wait_exit_code=1 and phase=registry_discovery.

The separate collection/setup error is explicit:

    tests/sdk/test_scene_real_public_summary_rle.py:51
    fixture 'native_host' not found

No coherent rerun is required to recognize that this is a fixture/setup error,
but it must not be folded into the missing-module result.

## Historical fact kept separate

The old full5664 result had six absent terminal nodes. That is a separate
historical comparison, not a classification of this current run. The current
qualification has the exact 142 terminal nodes listed in the exhaustive
partition, and the old six-node absence does not replace any of them.

## Ownership boundary and next steps

The child-environment worker owns its installed-profile map. The Viewing
handoff worker owns its scoped rendering/managed-scene map. The exhaustive
report records the unclassified nodes and their actual sourcefile:line
locations without assigning ownership or proposing a fix.

No suite or fix is requested by this report.
