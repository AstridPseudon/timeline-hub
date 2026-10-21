# D13 Runtime peer reply: existing trusted installed boundary

Date: 2026-10-21

## PEER REPLY — bounded conclusion

The existing upstream Runtime controller is the installed `astrid-runtime`
console entry point (`pyproject.toml:15-17`, `astrid_runtime/cli.py:431-498`).
For `up`, its call chain is:

```text
installed astrid-runtime
  -> astrid_runtime.cli.main()
  -> _config() / SourceProfile.load()
  -> bootstrap()
  -> _bootstrap_locked()
  -> LocalRuntimeBoundary.start()
  -> LocalRuntimeBoundary._argv()
  -> selected runtime_environment/bin/python -m runtime_protocol start
  -> RuntimeDaemon._start()
  -> fixed astrid provider import
```

The exact current Runtime base is `b92d3e7a05eec65c142294ef4873edd059e9b31d`,
tree `6abc2f117391de8e7e35c0283f575a002199894d`. The launcher change is an
ancestor: Runtime `30413e3c3e6db027f450e864ea9cb4a07446475b`, tree
`2c5a5088c90cddfb38fba6dadcad899b28fb2c59`; `30413` is an ancestor of `b92`.
The relevant `runtime_boundary.py` bytes are therefore present in current
`b92`.

## What the controller actually trusts and selects

`SourceProfile` is the existing profile carrier
(`astrid_runtime/bootstrap.py:122-230`). It permits the settled fields
`profile`, `runtime_checkout`, `source_checkout`, `runtime_environment`, and
the existing metadata fields. It rejects unknown fields and non-empty
`runtime_command` (`:137-196`). `SourceProfile.load()` reads the selected
absolute, symlink-free manifest (`:198-209`). The bootstrap path resolves and
validates that profile before handing it to the boundary
(`astrid_runtime/bootstrap.py:801-808`; validation at `:341-361`).

The root of Runtime's installed-process selection is
`LocalRuntimeBoundary._argv()` (`astrid_runtime/runtime_boundary.py:244-297`):

* it validates the selected profile and its absolute, symlink-free paths
  (`:244-245`, `_validate_source` at `:179-207`);
* `runtime_environment` selects its `bin/python` (`:249-257`);
* the fixed child command is
  `python -m runtime_protocol start --authoring-profile astrid`
  (`:258-264`); and
* realm, support, owner-lock, bootstrap-token, admission-timeout and custody
  arguments are added at `:265-297`.

The child selection is not an arbitrary provider selection. Runtime's CLI
allows only `neutral` or `astrid` (`runtime_protocol/cli.py:46-66`), and
`RuntimeDaemon` validates the same choice (`runtime_protocol/daemon.py:70-73`).
On `astrid`, startup imports the fixed
`astrid.sdk.timeline.commit.create_runtime_commit_service` factory and
validates its existing ABI/contract digest before readiness
(`runtime_protocol/timeline_commit_provider.py:70-93`; startup ordering at
`runtime_protocol/daemon.py:235-258`). This preserves the Runtime/Agent
provider boundary and credential/custody separation.

The important limit is that `runtime_environment` selects an installed Python
environment; it does not authenticate its bytes. `runtime_checkout` and
`source_checkout` are validated path/provenance fields, not import roots. The
normal controller does not compare wheel hashes, `RECORD` hashes, or a
source-closure digest. `source_digest` and `lock_digest` are accepted and
round-tripped as profile metadata (`astrid_runtime/bootstrap.py:142-145,
:190-195, :211-230`), but `_validate_source_profile()` does not verify them.
The only surfaced profile identity in the launch result is the existing
`capability_digest` metadata (`astrid_runtime/runtime_boundary.py:478-495`),
not a content attestation.

The selected Agent tree is consequently the installed `astrid` package found
by the selected venv's normal import machinery. No separate Agent checkout is
selected as authority. In the optional service path, `source_checkout` is
passed as service working directory/provenance, not as an authenticated import
root (`runtime_protocol/services.py:111-134, :148-156`).

## What 4406 proves, and what it does not

The retained green launcher evidence is:

```text
rt-m2-wc10-sdk-envelope-fixture-one-proof-0322-...
1 passed in 31.99s
```

as recorded in `design/runtime-m2-current-launcher-merged-handoff-full-0332.md:20-35`.
The fixture source tuple was Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`
(tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`) and normal Runtime
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` (tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`), with product distributions
`astrid==0.1.0`, `astrid-runtime==0.1.0`, and
`astrid-runtime-client==0.2.14` (`tests/test_wc10_installed_launcher.py:24-30,
:246-340`).

That test builds private product wheels from exact source copies and installs
them into a private venv (`tests/test_wc10_installed_launcher.py:102-158,
:236-243`). Its preflight checks the declared dependency versions, installed
distribution `RECORD` paths, no symlink components, module origins under the
private site, and the existing client contract digest
(`:246-340`). The manifest then points `runtime_environment` at that private
venv and both checkout fields at its installed site-packages
(`:372-385`). This is the smallest existing installed carrier: one private,
non-editable venv containing the Runtime, client, and Agent distributions.

That evidence authenticates/qualifies a selected installed package assumption
for that fixture. It does not mean the Runtime controller has a signed wheel
identity or an active hostile-byte defence. In particular, the test's
isolated `-I -B` child operation and removed `PYTHONPATH` at
`tests/test_wc10_installed_launcher.py:385-397, :489-497` are test setup for
the child client operation; they do not add those controls to the normal
`LocalRuntimeBoundary` daemon launch.

## Existing closure/import carrier: applicable path and non-applicable path

The existing source-closure/import carrier is real in
`runtime_protocol/verified_host_launch.py`, but it belongs to the local
execution host path:

* `HostLaunchVerifier.verify()` requires a trusted resolver and protection
  lease, validates the retained release/profile, inventories the selected
  runtime, checks the interpreter and launcher bytes, compares the existing
  source-closure digest, and constructs the explicit import mapping
  (`runtime_protocol/verified_host_launch.py:254-361`); and
* `claim()` rechecks the launcher and emits the isolated `-I -S` launcher plus
  the binding FD (`:363-377`). `NativeHostSession` invokes this verifier and
  passes the binding to the custody-owned child (`runtime_protocol/local_execution_supervisor.py:976-1025`).

The ordinary Runtime service path does not use that carrier. It launches the
daemon with `LocalRuntimeBoundary._spawn_runtime()`
(`astrid_runtime/runtime_boundary.py:376-422`) and, if profile services are
declared, `ServiceSupervisor._attempt()` expands the declared argv and calls
`spawn_tree()` with the selected Python, service checkout as cwd, and its
filtered environment (`runtime_protocol/services.py:200-236`). There is no
`--source-closure-digest`, binding FD, `-I`, `-S`, mapped-import payload, or
retained `HostLaunchVerifier` result on that route. The Agent triage's finding
that ordinary launcher/service imports precede the existing source check, and
that the measured closure excludes `__pycache__`, therefore remains applicable
(`design/agent-d13-installed-source-order-triage.md:14-79`).

## Smallest bounded answer

**NO-CARRIER for the ordinary installed Runtime/host-service boundary.** The
existing trusted controller can select the private installed Python and fixed
`astrid` provider under current Runtime custody. It cannot, on the traced
normal `up`/service path, pass the existing source-closure digest/import
binding or guarantee validated-source loading before host imports. Wiring the
local-execution carrier into that path would be a code change and a new
qualification task; it is not an existing capability to claim here.

The bounded carrier that can be named today is therefore only:

```text
runtime_environment -> one private, non-editable installed venv
                   -> installed Runtime/client/Agent package tree
```

That carrier means “the selected installed package set is assumed immutable and
coherent for this run.” It does not promise active hostile byte-tamper
defence, atomic protection against same-user writes/TOCTOU, cache/code-body
coverage, native/OS protection, or a pre-entry guarantee before already-loaded
launcher/controller modules. The green 4406 launcher result must remain
launcher evidence only, not arbitrary pre-entry byte security or D13 closure.

No new profile field, digest authority, environment alias, import root, DTO,
attestation framework, or circular self-validation is justified by this
trace. D13 remains held pending a bounded repair/review within the existing
trusted boundary.
