# Report

## Changes

- No source, test, fixture, profile, or harness files changed.
- Worktree remains clean.
- Wrote the required commit message and `DONE` marker.

## Findings

| Case | Cause | Qualified input / status |
|---|---|---|
| `test_d13_installed_native_preflight` | Test requires explicit D13 environment bindings; it does not provision Node, Remotion, browser, FFmpeg, or profile inputs. | Existing retained D13 preflight passed once: `1 passed in 4.43s` under Agent `ef851b22`. Carrier: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D13-inputs-1017/d13-bindings.json`, SHA256 `c3f0191f336d50ab86b729cecd449aad72cea050b452505703bebe57f780e239`. Profile SHA256 `8339f657...`; Agent wheel SHA256 `fcccab4d...`. Regular 819acf inputs remain available: Composition archive SHA256 `819acf6b...`, lock SHA256 `f4fc0a32...`, Node SHA256 `43d6cf63...`, Chromium SHA256 `85918a99...`, FFmpeg SHA256 `ed16af62...`, FFprobe SHA256 `272f6ebc...`. Native/render qualification remains unverified. |
| Installer `[False-0]` | Test self-provisions its temporary service/profile, but `Backend.runtime()` invokes `python -I -m astrid_runtime`; the old source venv lacks the installed Runtime package. | Already qualified by retained D18 run: `1 passed` using `/home/user/work/venv-agent-child-f1012-installed/venv/bin/python` and its installed site-packages. |
| Installer `[True-1]` | Same missing installed-Runtime input. Repair branch was not reached in the old failing run. | Missing qualification. Smallest next runner is the same supported installed invocation as `[False-0]`, selecting only `[True-1]`. |
| Bootstrap environment | The test deliberately launches a clean child with `PYTHONPATH` set to the Agent repository only. That child cannot import `runtime_protocol` when using the old source venv. | Missing qualification for this exact node. Smallest supported fixture is the existing installed c886 interpreter, whose site-packages contain `astrid`, `runtime_protocol`, `astrid_runtime`, and `astrid_runtime_client`; leave the test’s clean child environment unchanged. |

## Durable carriers

The existing managed c886 bench is at:

`/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e`

It has Agent `c36ca8c9`, Runtime `abd47e68`, a passed `.provision-report` (SHA256 `5b2e75c9...`), and recorded import origins. It was not used to claim qualification for these four exact nodes.

## Tests

No pytest, service, installer, build, provisioning, or full-suite commands were run by this worker, per task restrictions.

Retained evidence:

- D13 preflight: `1 passed in 4.43s`.
- Installer `[False-0]`: passed in the retained D18 central run.
- Installer `[True-1]`: unverified.
- Bootstrap node: unverified.

No blockers; the remaining items are bounded qualification gaps, not source changes or product conclusions.