# D134 source assessment

## Result

`PASS_SOURCE_ASSESSMENT`

The new claim is confirmed: omitting `PYTHONNOUSERSITE` from the outer
environment is necessary but ineffective against the immutable current D73
launcher. `tools/p4-d73-pinned-launch.sh` at the frozen Agent commit
`a4e016b6a9f91fbe372672bdcf382c630bf59186` exports `PYTHONNOUSERSITE=1` at
line 128 in its preflight subshell and line 149 in its body subshell. Its
SHA-256 is the manifest value
`cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1`.

The source chain is also exact. The launcher sets
`ASTRID_REMOTION_PROJECT_DIR` at lines 132 and 153. `host_bootstrap.py:1651`
calls `_prepare_render_validation`; its `:813-814` branch only avoids the
Remotion path when that project variable is absent. The validation path builds
the worker environment, applies `build_child_subprocess_env`, calls
`probe_context`, and `remotion_runtime.py:214-216` includes
`PYTHONNOUSERSITE` in the unsupported startup set; `:234-236` rejects it.

The candidate retains the frozen four-repository tuple and the exact 22-root
pytest body, flags, timeout, JUnit path, and D73 request bindings. Its body is
byte-identical to the author measurement body and its shell syntax parses.

## Gate limits

This candidate is not a working fix and is not an approved launchable gate:
the current launcher reintroduces the rejected variable, and the candidate
also omits the author recipe's D134 dispatch checks and remote-origin checks.
No unreviewed recipe may be used for D137. D137 proceeds through the normal
real-child/current guarded route. No launcher, body, test, or runtime command
was executed by this review.
