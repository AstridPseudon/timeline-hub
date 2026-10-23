# Agent F environment remainder — 2026-10-23

## Result

Bounded provisioning audit complete. Qualification is blocked at the
dispatcher, not by an unresolved source decision. The two sanctioned requests
are queued, but neither immutable environment exists and neither acceptance
node has been rerun; no pass is claimed.

## Evidence

The plan, final classification 0851, independent review 0858, and environment
reports 0840/0856 were read. The sole full run was
`agent-full-1023072419-4249` from Agent commit
`d24da4af0f1ca83880b4b9ef57559e28ebe52a2a`, tree
`fcc33e0eb964dd48d422673e8f692f195c88748c`, with 16,388 passed, 240 failed,
140 errors, 40 skipped, and 5 xfailed. The classification counted 316
environment/resource/collection nodes.

The exact original nodes selected for later acceptance are:

- `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[success]`
- `tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result`

The first currently fails in a `python -I` child with
`ModuleNotFoundError: No module named 'astrid'`. The second fails setup because
`/home/user/work/runtimes/agent-remotion-0013` is absent. A direct negative
preflight also returned exit 1 with that isolated `astrid` import failure; no
`PYTHONPATH` bypass was used for qualification.

## Exact D09 producer identity

The required original fixture is Agent commit
`30da0a5e05d4529a2b97b3c1818cf9e15842d628`, full tree
`0dacaabb6cbb42bebc09b6677983814ad2f4d237`, remotion tree
`08236aaf8c63e43dafba6baa4fe412343edd6a99`, and
`remotion/package-lock.json` SHA-256
`c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.
Its package identity is Composition 0.0.13 with Remotion 4.0.509, and the
required artifact is
`remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz` (Git blob
`56df7e57522ff7431b987f6047db1288a2a10350`, content SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`). The
current Composition 0.0.14 runtime and unrelated runtime sources were not
aliased or reused.

## Provisioning and limits

The existing routes were invoked with the exact current Agent commit
`2e21af300abbefc8afbad217189fa4715cf82616` for
`venv-agent-child-f0905-current`, and the exact A013 commit plus lock hash for
`agent-remotion-0013`. The request scripts were used read-only; their hashes
were `f9e5ea6f2ff577ebd25218a1eba751e17fafd474b1e1a3a3adbb8524a80c440e`
and `15b07daf4cd46a225ecc020c11e3ec8f3a62368c73d9ba6940ad3ce4ea8191ff`.

Available disk was `15,961,731,072` bytes (~15.96 GB), against the mandatory
15 GB floor. Existing comparators were 693,246,231 bytes for the child venv
and 329,994,948 bytes for the Composition14 runtime, so the expected final
footprints are under 1.1 GB before temporary build overhead. No resources were
reclaimed. The pending request files remain under the orchestrator queue, and
the private child staging directory was only about 4 KiB at the last check.

The dispatcher heartbeat was stale and `ensure-daemons` could not retain a
dispatcher after the worker command exited. The dispatcher-owned network
builders were therefore not run directly. This is an ordinary operational
blocker, not a request for invented approval or a reason to guess an artifact.

## Preservation and next step

The 0856 durable projection and Node20/Composition14 prerequisites remain
unchanged. No product, test, fixture, pin, dependency, shared install,
contract, runner, launcher, or security files were edited. The farm/dispatcher
owner should consume the queued requests, verify actual module origins from
the installed `python -I -B` child and exact D09 manifest/lock/source identity,
then run only the two original nodes above through the authorized test service
or net runner. No full, browser, heavy-render, P1, P4HTTP, native14, or crash24
suite was run. The original full failure remains open until those exercises
pass.

The exact negative preflight was:

```text
env -i HOME=/root PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin \
  PYTHONPATH=/home/user/work/wt/agt-F-environment-remainder-0905 \
  /home/user/work/venv-agent/bin/python -I -B -c 'import astrid'
```

It returned exit 1 with `ModuleNotFoundError: No module named 'astrid'`;
`python -I` ignored `PYTHONPATH`. No acceptance test command was run because
neither requested environment qualified.
