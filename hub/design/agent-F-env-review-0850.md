# Agent F environment review 0850

## Result: FAIL

The 0840 environment repair is not durable. `suites.conf` lines 18–19 still
point both Agent `full` and `targeted` at `/tmp/w-5829dd9212/site-packages`,
but that projection is missing after the worker exited. A post-exit sanitized
child startup test fails `1 failed` with
`ModuleNotFoundError: No module named 'runtime_protocol'`.

The live Runtime pointer is `/home/user/work/runtime` at
`eb13b2051d4d30a4d8b7df8878bb7451701eab5a` and is clean. The live renderer
runtime remains qualified: Node `v20.19.4`, Remotion `4.0.509`, esbuild
`0.28.1`, Composition `0.0.14`, React `18.3.1`, real node_modules, lock hash
`b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`, and the
reviewed normal Composition identity `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
The Node 22 negative guard still refuses correctly; no `PYTHONNOUSERSITE`
bypass is present. `/home/user/work/runtimes/agent-remotion-0013` is absent and
must not be faked or aliased.

No source, tests, pins, shared dependencies, process code, or launcher files
were changed. The original full result remains `16388 passed, 240 failed, 140
errors, 40 skipped, 5 xfailed` (exit 1); the 0840 `4 passed in 13.30s` targeted
run occurred before cleanup and does not establish durability. No full run was
requested.

Next: the Runtime/farm owner must provision the private `runtime_protocol`
projection through the sanctioned route at a durable path outside worker `/tmp`
cleanup, verify the child origin after worker exit, then rerun the four exact
representatives before the one final full run.
