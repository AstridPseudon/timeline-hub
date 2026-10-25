# D77 complete source/input handback recipe

Status: `NOT_READY`. This is a source-only handback. It is not an instruction to
start Farm, install packages, fetch a browser/OMP source, create a child, stage,
preflight, render, or run a provider.

## Authoritative tuple rule

The D139 final merged tuple is the only current source authority:

```text
Agent   4c4ee35d5687c4cd40a0e5395efda53aa56f939d  tree d50fd98f7d1bc6860de810f38e8a0b3a55ca224e
Runtime ab1e4f6141987706132916e2da16477f5a019464  tree 7d8e77b2f5a4af79305c9212ce5174d3ea9fd657
```

The older D77 applied tuple remains preserved, but is not relabelled:

```text
Agent   91398e9de4500ce16c8e55741209ba3609cb1694  tree 523893dcf54dbe756db8fe2915d14055b1da660b
Runtime 1daca2a33f6d7b10053e07c539a54843e3984e19  tree a522511414947e48e317a5e5c2103483b121a750
```

Its child `717e53d7` and related Farm receipts describe the historical D77
tuple only. They do not qualify the D139 tuple.

## Supported acquisition and delivery route

The complete route, once the owner clears the current blockers, is:

```text
independent guard receipt
  -> Farm source admission and finite peak bound
  -> normal request-checkout for current D139 Agent and Runtime
  -> normal request-runtime with current source identities and exact Remotion lock
  -> normal request-child-venv for that same tuple
  -> authenticated INSTALL_MANIFEST and normal ASTRID_RUN launcher
  -> Installer.run -> Backend.stage
  -> private profile/service/bindings/tool receipts
  -> D13 installed native preflight
  -> daemon-backed authoring and final render
  -> private durable result receipt
```

The installer command shape is the existing normal operational path:

```text
ASTRID_RUN install --root PROGRAM_ROOT --data-root DATA_ROOT \
  --manifest INSTALL_MANIFEST --uv UV
```

`validate_manifest` requires schema version 1, full Agent/Runtime (and optional
VibeComfy) source SHAs, exact versions for uv/Python/Bun/Node/FFmpeg, HTTPS
asset URLs and checksums, and an exact OMP source selection. `Backend.stage`
then materializes source trees, creates the uv environment, installs the locked
Python closure, installs tools, runs the OMP route, runs frozen Remotion `npm ci
--no-audit --no-fund`, writes the service declaration and computes `profile.json`
with `source_checkout`, `source_digest`, `runtime_environment` and
`service_declaration`.

The consumer route is the installed profile only:

```text
generic_host --service
  -> run_pack_host_foreground / ensure_pack_host
  -> tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight
  -> tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

No direct `python -m astrid.installer.cli`, direct `Backend` call, copied
checkout, shared venv/node_modules/runtime/cache, guessed profile, guessed
seven-key carrier, or old D77 child is an equivalent route.

## Current missing gates

Farm's read-only inventory found exact historical checkouts, Node, Remotion
lock, VibeComfy fixture, guard source, and free disk, but no installed
`ASTRID_RUN`, authenticated manifest, verified uv, browser, current D139
runtime/child receipt, seven-key carrier, installed profile, or render receipt.
FFmpeg/FFprobe were not hash-verifiable in that inventory. The source census
also reports 17,604 graph edges versus 17,642 import occurrences; the 38
exclusions must be declared before D139 source publication is unconditional.

The footprint result is deliberately `UNKNOWN_UNBOUNDED`. The retained
1,168,669,468-byte observation is not a peak, the 4.6 GB source admission and
4 GB stop rules are not peak bounds, and archive/unpack, uv/wheel, Bun/OMP,
Remotion, cache, backup and render overlap quantities remain unbounded.

## Private receipt requirements

Farm may retain, but must not export here, the actual values for:

```text
ASTRID_RUN INSTALL_MANIFEST UV PROGRAM_ROOT DATA_ROOT RUN_ROOT RESULT_ROOT
PROFILE BINDINGS PY SITE RUNTIME REMOTION NODE BROWSER FFMPEG FFPROBE ASTRID_PACKS_PATH
```

The `BINDINGS` JSON must contain exactly:

```text
agent_commit agent_tree agent_wheel agent_wheel_sha256
source_checkout source_digest runtime_environment
```

All values must be tied to the current D139 tuple and preserved in private
Farm receipts. Only the public source/tree/tool hashes in `source-manifest.json`
may be transported in the ordinary handback.

## V2 contract carry-forward

The production caller remains unchanged: `api_version`, `project_id`,
`timeline_id`, `base_revision_id`, `base_publication_id`,
`commands[{schema_version,op,version,select,args}]`, `label`,
`steps[{id,label,intent,tags,command_ordinals,patch,optional reads}]`,
`merge` (`fields|atomic`), `reads`, `Idempotency-Key`, `dry_run`, `source`,
`rationale`, and `group_id`. Replies retain accepted/merged canonical/base/
landing/merge_mode/receipt/records/bindings/effects/dependencies/history/
undo_steps, conflict reason/head, invalid code/path/hint/suggested_command,
and preview `would_status` with null-or-receipt. No schema or product change is
proposed by this bundle.
