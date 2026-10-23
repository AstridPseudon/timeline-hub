# F-D22 manifest child qualification

**PASS — one original node only.**

Central run
`agt-F-D22-manifest-child-1550-d22-manifest-child-1550-rerun-1023155311-18159`
collected exactly one node and passed it in **10.46s**:

```text
tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root
```

Qualified pair: installed Agent
`8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`; exact Runtime
`9ce4242bc01f100bab9efc51032a73985cefb2b2` (tree
`92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`); child interpreter
`/home/user/work/venv-agent-child-d22-8c3b926e/bin/python`; Node `v20.19.4`;
approved profile `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`.

Profile lock SHA-256:
`f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`.
Composition archive SHA-256:
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, version
`0.0.14`. Runtime protocol SHA-256:
`4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`.
`PYTHONNOUSERSITE` was absent. PEP 610 URLs, parent/current-worktree imports,
isolated child/site-package imports, profile identity, and exact manifest
command `['python3', 'run.py']` resolving to the owning pack's
`astrid/packs/rendering/run.py` were checked before and after.

Current execution/renderer source matched installed 8c byte-for-byte:

```text
remotion_runtime.py  84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e
transport.py         58a7aaa59ff744876be1eccd9ef94b16304d3270c02163d0829894f86f6ff4af
run.py               5d2cfd30e69ddbe921e670dd9e1b345040de890cc859839e251fa468fbc647d2
renderer.yaml        1b433765b59ad3b42fbce147d7672a82284635daebadfb2601e026cc4f47164d
```

The original test function body is byte-equal to 8c, SHA-256
`e4274df23a48f4dc0a52f0bc6d91d987599c2741cc24687cc3deb17f2491dc71`. The only
full-file support drift is the pre-existing Composition expectation `0.0.14`
current versus `0.0.13` in 8c. No test or product source was changed.

Custody bytes were unchanged before/after; the worktree was clean and
`git diff --check` passed. No full suite, old 3b pair, wider D22 census,
browser, native14, schema/client/pin/archive/dependency, or production changes
were performed. The first central attempt exposed only a snapshot-HEAD
assumption in the harness; the corrected rerun is the reported result.
