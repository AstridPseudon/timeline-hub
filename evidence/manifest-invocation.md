# D141 fresh manifest invocation (prepared, not run)

The exact tuple is Agent `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` / tree
`0a3691a49b63fd7b0c22fb3478e9cf1947f266ed`, Runtime
`fa9cd5464a8b37b02f971de375e56be846cd69e2` / tree
`124e10dbcd54fb90219e783ec11aa34f8c91590c`, App
`7ca61bb3280beca21d98a854af266a382f7ce5df` / tree
`974de7cd08900872eeb0bd6f6004d44323e01fab`, and Composition
`67b8aa3d0d6831d3e3504a340ff583c3da253707` / tree
`62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`.

The normal external manifest-maker source is the reviewed Agent manager recipe
`tests/suites.conf.candidate.request.md`, source commit
`91398e9de4500ce16c8e55741209ba3609cb1694`, Git blob
`fbde96168dca681a76cff1526c23b8d0b74001eb`, SHA-256
`782fb81cea67ce71b785dd5dbf891bb1d32df74c136425d83d53e938bdf8b51c`.
The normal external D73 launcher source is current Agent
`tools/p4-d73-pinned-launch.sh`, SHA-256
`9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`.
Neither source exists in frozen Agent upstream. The launcher also requires its
own path to be `<agent_path>/tools`, so it cannot be overlaid or invoked against
pristine by this preparation. The controller must provide a supported
pristine-compatible external route; no substitute is invented here.

The source-only Composition D73 candidate
`afda6c66a11608d8cb012df1a54bf2489d8c20b3` (`ops-d73-exact-nodes`) is a
reviewed admission/check source, but its own README says
`CANDIDATE_NOT_INSTALLED`/`NOT_READY`; it is not a runnable comparator route.

Once normal lead checkout receipts and that supported external route exist, the
fresh generation invocation is the source-owned tuple renderer with these
bindings (no historical manifest reuse):

```text
format=p4-d73-v1
agent_sha=8b6ed2116fd1803d24b2be5bc08bd9490407fe4a
runtime_sha=fa9cd5464a8b37b02f971de375e56be846cd69e2
app_sha=7ca61bb3280beca21d98a854af266a382f7ce5df
composition_sha=67b8aa3d0d6831d3e3504a340ff583c3da253707
agent_tree=0a3691a49b63fd7b0c22fb3478e9cf1947f266ed
runtime_tree=124e10dbcd54fb90219e783ec11aa34f8c91590c
app_tree=974de7cd08900872eeb0bd6f6004d44323e01fab
composition_tree=62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120
agent_path=$AGENT_CHECKOUT
runtime_path=$RUNTIME_CHECKOUT
app_path=$APP_CHECKOUT
composition_path=$COMPOSITION_CHECKOUT
python=/home/user/work/venv-agent/bin/python
node=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
profile=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
schema=/home/user/work/venv-agent/lib/python3.13/site-packages
```

The generator must complete the remaining launcher-required fields from the
receipt-backed normal settings and write a fresh positive manifest. It must
then create a byte-for-byte copy whose sole parsed difference is
`agent_sha=0000000000000000000000000000000000000000`. Use the retained 2234
stub at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-rehearsal-2234/evidence/positive-stub.sh`
only if its SHA-256 is exactly
`38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0`.

Expected later controls: positive launcher preflight `0`, stub `17`, exactly
one fresh counter line; poison nonzero (expected `1`), zero calls. This file
records the invocation inputs and expected result only; no controls, imports,
collection, pytest, or body was run.
