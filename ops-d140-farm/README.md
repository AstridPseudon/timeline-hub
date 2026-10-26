# D140 Farm receiving packet

This is a source-only, portable receiving recipe. `receive-farm.sh` has one
supported mode, `--check-only`; it performs a read-only census and emits a
complete JSON result. It does not create a child, import child/product code, invoke
pytest, run an installer, touch a Store or queue, acquire packages, or use a
fallback profile/interpreter.

The Farm owner must bind every path through the environment. Paths in the
packet are receipt bindings, not portable assumptions. In particular,
`AGENT_CHECKOUT` must be a clean checkout at the frozen Agent
`28e56cac…`/tree `2ebe2ddf…`, not Main's stale integration home. The Agent commit object may be
verified read-only in that object store, but a stale checkout is not accepted.

The schema route is the D139a installed-distribution route. It requires the
authentic `banodoco-timeline-schema==0.0.2` dist-info directory, its exact
18-row RECORD closure (12 hashed rows and the six named unhashed rows), the
pinned PEP 610 direct URL, and the trusted schema manifest. A missing Farm
venue is `EXACTMISSING`; the old shared venv, arbitrary old child, alternate
mirror, package acquisition, source invention, and `--farm-schema-source`
substitution are not substitutes.

Receipt admission uses the OS custody of the recorded normal Farm installation.
`FARM_ORCH_ROOT` must equal the root embedded in the qualified dispatcher and
maker; it cannot register another installation. The checker pins executable
bytes/modes, physical paths, ownership and safe ancestry. It uses isolated
Python and a fixed Git executable/environment. `<binding>_SHA256` values remain
required consistency assertions, but matching a caller hash grants no authority.
The owner of the qualified installation is the authority boundary; this does
not authenticate against a malicious privileged owner.

The production caller is `receive-farm.sh:check_producer_receipt` ->
`receipts.py:main`. It invokes all of these checks:

- `source` accepts only the dispatcher's normal `queue/done/checkout-<repo>-<SHA>`
  result, exact `make-checkout` destination, worker `meta`/`KEEP`, clean source
  commit/tree and pinned producer. Arbitrary JSON or an arbitrary owned root
  with locally computed hashes cannot qualify a checkout.
- `normal_kit` binds maker/requester/import checker to their installed normal
  paths and reviewed bytes/modes. `installation` checks the historical
  `timeline.ops.d137.installed-kit/v1` summary and installation/source closure
  as **supporting installation evidence only**, through the separate
  `FARM_INSTALLED_KIT_SUMMARY` and `FARM_KIT_INSTALLATION` bindings. Neither
  summary is a Farm distribution receipt.
- `kit` selects the ordinary D139a installed-distribution route by default and
  checks the normal maker/requester custody before creation. After creation it
  checks the registered child and retained provision report through the normal
  formats. It does not require `FARM_DISTRIBUTION_SOURCE`, `farm_authority`,
  or `.farm-receipt.json`. When the existing `FARM_REQUIRED=1` selector is
  supplied, the strict special Farm branch instead loads only the pinned
  `verify_dependency_seed.py` and `verify_farm_distribution_inputs.py` source
  bytes, authenticates `farm_inputs`, and requires the registered child's exact
  mode-0400 `.farm-receipt.json` and retained `farm_authority` closure. There
  is no replacement receipt protocol.
- `child` accepts the normal queue result for `venv-agent-child-d140` and the
  maker's real final success line. `registered_child` checks retained normal
  owner/index/entry/registration metadata, key, source/client/schema/bootstrap
  identity and report bytes. It does not instantiate or operate a Store.
- `d73_input` checks the manager's complete `p4-d73-v1` input under the normal
  owner root, pinned launcher, four source tuples/paths/parents and tool inputs.
  `d73` additionally requires the exact
  `$P4_D73_EVIDENCE/$P4_D73_REQUEST_ID.manifest` path, request-id file and
  launcher-created runmanifest. Expected runmanifest bytes and SHA-256 derive
  from the same checked manifest fields; the launcher has no digest field to
  invent. Preflight/body exit and log/command paths belong to that same request.
  A detached valid manifest is refused. `post-child` checks inputs before the
  launcher; `post-launch` checks retained results after it. No future launcher
  output is required at either earlier phase.

**Route selection.** The ordinary D140 request below selects the approved D139a
installed-schema input and reaches the normal caller without Farm authority.
The existing requester/maker guard still refuses the same request when Farm
authority is selected alongside the installed schema. The strict special Farm
branch is selected only with `FARM_REQUIRED=1`; no command bypasses the guard
and no Farm source replaces the D139a installed carrier.

Producer path: `request-child-venv` serializes `CHILDVENV` ->
`dispatcher-daemon:prov` invokes `make-child-venv` -> its inline Farm gate calls
`verify_dependency_seed.farm_inputs` ->
`validate_farm_distribution_inputs` -> `validate_schema_source` and
`validate_wheel_inputs`. The maker binds `component_identity` as
`identity.farm_authority` before key selection; `prepare_farm` retains the exact
receipt and `_retained_farm` revalidates it. Installed-schema-only requests
cannot take that path. The receiver checks this actual caller constraint.

Each failure remains in the complete census; a valid checkout never upgrades
an unauthenticated receipt. Only the pinned read-only input verifier runs;
no maker, request or D73 body runs. A changed producer requires a new reviewed
handoff, with no fallback.

The sequence in [commands.md](commands.md) uses the ordinary normal-caller
route by default. The post-child census is a separate admission after a normal request;
post-launch retained-result admission follows launcher execution. The command file preserves the
normal request wrapper, registered-child import checker, D134
positive/poison accounting, and the unfiltered D124 22-root core selector.
The existing reviewed D73 launcher remains the sole launcher. `CORE_ROUTE`
must be the existing D73-compatible Farm route and is invoked with
the launcher’s exact manifest/`run` argv; no wrapper or alternate launcher is
defined here. Its outer command binds the exact JUnit path, raw log,
start/stop, disk witness, and retained KEEP root before cleanup.

The handoff names the frozen D141 Runtime `6a011d58…` C0 request/reply fields
literally; its C0 schema bytes are unchanged from the historical f103 source.
Request `reads`
are not `optionalreads`; accepted output uses `canonical_document`, explicit
base/previous/accepted IDs and `rebased_onto`, while conflict details use
`current` and `conflicts`. Record nesting, `receipt`, and the separate
history/head shapes remain the Runtime schema’s shapes.

The pinned D141 `28e56/6a011/867cb/635f` tuple is SOURCE_ONLY. This packet does
not claim venue readiness. The historical canonical census remains the
supporting-only `4c/ab1e` packet and is not relabelled as a D141 census. Missing
venue inputs remain: the qualified four
source checkouts and normal queue results; the compatible normal caller join;
authentic Farm selected schema source/original input and retained dependency
closure; the D139a installed carrier and installation evidence; a registered
child/result/report; fresh manager manifest, controls, request-scoped D73
results; profile/Node/service routes, admission and durable output roots.
These must be supplied and verified at the venue, without acquisition or a
substitute route.
