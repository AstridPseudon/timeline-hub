# F environment remainder — bounded provisioning audit

Status: BLOCKED at sanctioned dispatcher execution; no product or test repair was applied.

## Scope and exact causes

The sole full run was `agent-full-1023072419-4249`, Agent source commit
`d24da4af0f1ca83880b4b9ef57559e28ebe52a2a`, tree
`fcc33e0eb964dd48d422673e8f692f195c88748c`. It ended with
`16,388 passed, 240 failed, 140 errors, 40 skipped, 5 xfailed` (exit 1).
The final classification counted 316 environment/resource/collection nodes.

The two causes in this bounded task are:

1. Seven original installed-guard nodes fail because an isolated `python -I`
   child cannot import the installed Agent package. The exact representative
   original node selected for later proof is:

   `tests/packs/h3_av/test_character_swap_cpu_boundary.py::test_cpu_host_readiness_identity_reaches_real_installed_guard[success]`

   Its full-run traceback is `ModuleNotFoundError: No module named 'astrid'`
   at the `python -I` child import (`agent-full.../log.txt:19053-19132`).

2. Three original D09 nodes fail during setup because the exact fixture path
   `/home/user/work/runtimes/agent-remotion-0013` is absent. The exact
   representative original node selected for later proof is:

   `tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result`

   The full-run traceback is `FileNotFoundError` from `shutil.copytree` at
   `test_d09_managed_scene_only.py:92`
   (`agent-full.../log.txt:473-526`).

## Authentic identities

The original D09 fixture is recoverable from the Agent repository object,
without aliasing the current Composition 0.0.14 environment:

- Agent source: commit `30da0a5e05d4529a2b97b3c1818cf9e15842d628`;
  full tree `0dacaabb6cbb42bebc09b6677983814ad2f4d237`;
  `remotion/` tree `08236aaf8c63e43dafba6baa4fe412343edd6a99`.
- `remotion/package-lock.json`: SHA-256
  `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.
- Package identity: Composition `0.0.13`, Remotion `4.0.509`.
- Required artifact: `remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz`,
  Git blob SHA `56df7e57522ff7431b987f6047db1288a2a10350`, content SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The existing `agent-remotion-composition14-255b6856` is not interchangeable:
its package lock is `b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`
and its package names Composition `0.0.14`.

## Sanctioned requests and disk evidence

Current Agent source is `2e21af300abbefc8afbad217189fa4715cf82616`.
The existing request routes were used exactly as follows:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-child-venv \
  venv-agent-child-f0905-current \
  2e21af300abbefc8afbad217189fa4715cf82616

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-runtime \
  agent-remotion-0013 \
  30da0a5e05d4529a2b97b3c1818cf9e15842d628 \
  c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24
```

Requests remain pending at:

- `queue/pending/childvenv-venv-agent-child-f0905-current`
- `queue/pending/runtime-agent-remotion-0013`

The dispatcher heartbeat is stale at `2026-10-23 09:06:36Z`; daemon recovery
could not retain a dispatcher in this worker sandbox. The private child staging
directory exists only as `venv-agent-child-f0905-current.partial` (~4 KiB at
the last check), so no qualified environment exists yet.

Disk checks:

- Available at the final verification: `15,961,731,072` bytes (~15.96 GB).
- Mandatory floor: 15 GB.
- Existing child venv comparator:
  `/home/user/work/venv-agent-child-s2` = `693,246,231` bytes.
- Existing qualified renderer comparator:
  `/home/user/work/runtimes/agent-remotion-composition14-255b6856` =
  `329,994,948` bytes.
- Expected combined final footprints are therefore under 1.1 GB before
  temporary build overhead, leaving materially more than the 15 GB floor.
  No resource reclamation was attempted.

## Preservation and next owner

The 0856 durable projection remains untouched:
`/home/user/work/agent-runtime-projection-0856/site-packages/runtime_protocol`
resolves to `/home/user/work/runtime/runtime_protocol`. Node 20.19.4 and the
Composition 0.0.14 environment were not edited. No shared dependency, pin,
fixture, runner, security guard, launcher, contract, or source file changed.

The farm/dispatcher owner must consume the two already queued requests, then
prove the installed module origins with the actual `venv-agent-child-f0905-current`
interpreter under `python -I -B`, and prove the D09 runtime manifest/lock/source
identity before requesting exactly the two representative original nodes above.
The original full status remains open until those nodes pass through the
authorized test service or net runner.

## Commands and results

The isolated negative preflight was run as:

```text
env -i HOME=/root PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin \
  PYTHONPATH=/home/user/work/wt/agt-F-environment-remainder-0905 \
  /home/user/work/venv-agent/bin/python -I -B -c 'import astrid'
```

It returned exit 1 with `ModuleNotFoundError: No module named 'astrid'`;
`python -I` ignored the supplied `PYTHONPATH`, so this was not an isolation
bypass. No acceptance test command was run because neither requested
environment qualified. The original full-run status remains open.
