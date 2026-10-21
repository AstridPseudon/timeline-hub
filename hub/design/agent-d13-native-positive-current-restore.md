# D13 native positive current-tree restore

## Result

Restored the registered native D13 positive on Agent `0963d9452ec2a5720ffed834017b28b0a5413c8e` by porting the active assertion/helper path from approved `65c87dd5`/`7b3e1205` into `tests/packs/video_editing/test_runtime_publication_chain.py`.

The positive is active (no new xfail) and retains the complete custody chain:

- immutable admitted target, ordered association/media reads, and settled native proposal;
- `producer.guard` in the requester outbox;
- lost commit acknowledgement, durable flight key, restart, exact retry, and receipt/publication identity;
- revision-pinned ordinary historical render admission;
- decodable MP4 with `ffprobe`; and
- guarded undo of the accepted publication.

The existing legacy hook xfail and legacy admission refusal remain unchanged. The separate explicit Runtime publication test remains adjacent legacy coverage and is not used as the native positive. No Runtime/client/pin/scope/generated-client changes were made.

## Minimal current-source bootstrap port

The current rendering bootstrap imports `runtime_protocol` in child registry processes, while the validated child environment only carried the supported `ASTRID_RUNTIME_CHECKOUT` selector implicitly. The smallest current-source correction retains the exact checkout and explicit Node executable in the Remotion registry context and propagates the checkout selector to children; the import resolves only that configured checkout when the module is not already importable. This does not add authority, bypass validation, or alter Runtime semantics.

## Tests

Passed locally:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  -m 'not integration' tests/packs/video_editing/test_runtime_publication_chain.py \
  tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py \
  tests/core/rendering/test_remotion_registry_context_key.py
79 passed, 2 deselected, 1 xfailed in 6.44s
```

`git diff --check` passed. The selected Ruff command reports five pre-existing import diagnostics in the touched rendering/subprocess files (the same lint debt was present before this change); no new test-file diagnostics were reported.

Added central suite `d13-native-positive-render-integration` with Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, Main95bd Remotion/C13 profile, and pinned Node20. It selects only:

```text
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

Central requests, all one failed original-positive node (no full/browser/matrix suite):

- `...-1021010610-7279`: fixture failure before product execution, child `ModuleNotFoundError: runtime_protocol` during registry discovery.
- `...-1021010705-19889` and `...-1021010844-28726`: the same discovery failure after private environment corrections.
- `...-1021010947-32473`, `...-1021011035-28248`, and final `...-1021011225-30146`: discovery passed, but the guarded registry-generator subprocess exited 1 before Runtime admission; the service did not retain generator stderr.

The final central result is therefore **unqualified/environment-blocked**: no native transport, Runtime admission, requester outbox, render, decode, or undo claim is made from central execution. D13 remains HOLD pending an independent custody/assertion review and coordinated adoption, as directed.

No full suite was requested or run.
