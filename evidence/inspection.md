# F-render-timeout-path-0522 inspection

Read-only inspection of the retained qualification and current source. No
original body or support probe was rerun.

## Identity

- Current integration head: `2007cf7aaf`; relevant source parent: `9cd3dbe865`.
- Installed managed child: `child-3b5cb98c4f2dfc20ce8747f68bf2e1124ff47b9dd5f04dabaada3a22278fdfc9`, Agent `ba8f0bc8be`, Runtime `f3208b26`.
- Installed-only production imports were recorded; no Agent source was injected through `PYTHONPATH`.
- Current source equals the installed child for `astrid/sdk/rendering.py`, `astrid/core/rendering/transport.py`, `astrid/core/rendering/registry.py`, the Three.js launcher, and its manifest. Their SHA-256 values are retained in the qualification `evidence/preflight.json`.
- Target body is unchanged: 9 assertions, file `9efe493c...`, function `ca54f2d5...`, assertions `087c80d0...`; function hash matches `ba8f0bc8be`.
- Runtime profile custody: Node `v20.19.4`, profile/archive identity `819acf6b...`; no browser, Remotion render, raster, MP4, or Node path was reached.

## Actual retained result

- The first attempt failed before collection because `-P` hid repository `tests`/`scripts`; this was a harness import failure, not a body result.
- The corrected run collected exactly one node and invoked the original body exactly once.
- Result: `pytest_exit=1`, `1 failed in 45.65s` with pytest-timeout at 45 seconds.
- Trace: `astrid.sdk.rendering.support` -> `_support_report` -> `CommandTransport.run` -> `process.communicate`; the failing call is the transition case at test line 229.
- The support temporary directory was cleaned during timeout. No result JSON, child exit code, child PID/process state, request/result bytes, or structured renderer error was retained; stdout/stderr were empty in the retained outer trace.

## Bounded source facts

- The production caller writes a request, dispatches the manifest command
  `python3 rendering/renderers/threejs/run.py support --request ... --result ...`,
  and parses the child result before returning.
- The target body makes ten `reasons_for` support invocations (four loop cases
  plus six direct cases). Each public support call creates a fresh temporary
  request/result directory and a fresh transport. The parent resolves its
  registries, while the child launcher loads the request and enters its local
  Three.js support function. This proves repeated work, not its elapsed time
  or causal responsibility for the timeout.
- Existing SDK6 wire proof `27934` passed six exact conformance selectors in
  41.48 seconds under its separately qualified c36/Runtime8ea environment.
  It proves the generic request/result wire path for those fixtures, not this
  Three.js ten-probe body or this ba8/f320 child.

## Missing finite evidence

One future, explicitly authorized run needs per-probe timestamps for parent
entry/child spawn/child exit/communicate return, exact child argv/cwd, PID and
process-tree state at timeout, return code, result-path existence/size/hash,
and captured child stdout/stderr bytes before cleanup. Until then, startup
cost, a live child, pipe ownership, and child-side failure are all possible;
none is proved and no registry attribution is made.
