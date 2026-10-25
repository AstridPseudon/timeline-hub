# D140 Farm receiving packet

This is a source-only, portable receiving recipe. `receive-farm.sh` has one
supported mode, `--check-only`; it performs a read-only census and emits a
complete JSON result. It does not create a child, import a module, invoke
pytest, run an installer, touch a Store or queue, acquire packages, or use a
fallback profile/interpreter.

The Farm owner must bind every path through the environment. Paths in the
packet are receipt bindings, not portable assumptions. In particular,
`AGENT_CHECKOUT` must be a clean checkout at Agent `41ad6565…`, not Main's
stale `tl/integration` `547e1045…` home. The Agent commit object may be
verified read-only in that object store, but a stale checkout is not accepted.

The schema route is the D139a installed-distribution route. It requires the
authentic `banodoco-timeline-schema==0.0.2` dist-info directory, its exact
18-row RECORD closure (12 hashed rows and the six named unhashed rows), the
pinned PEP 610 direct URL, and the trusted schema manifest. A missing Farm
venue is `EXACTMISSING`; the old shared venv, arbitrary old child, alternate
mirror, package acquisition, source invention, and `--farm-schema-source`
substitution are not substitutes.

Receipt trust starts with the Farm owner's independently authenticated handoff:
bind `FARM_ORCH_ROOT` and the SHA-256 of each original artifact as
`<receipt binding>_SHA256`. This includes the four `FARM_CURRENT_*_RECEIPT`
bindings, `FARM_D139A_KIT_RECEIPT`, and, after the request, `CHILD_RECEIPT`,
`P4_D73_MANIFEST`, and `FARM_D73_RECEIPT`. Do not derive trusted digests from
untrusted files during the census. Missing trust bindings give `NOT_READY`.
These are receiving inputs, not a new receipt format or a signature scheme;
an operator who controls the trusted handoff controls this authority boundary.

The checker reads existing producer artifacts only:

- Source receipts are the original `queue/done/checkout-<repo>-<full SHA>`
  dispatcher results, with exact `created ... (detached at ..., KEEP)` or
  `exists: ... at ...` text. They close to the normal worker `meta` and `KEEP`
  records and the clean checkout/tree. `make-checkout` and `dispatcher-daemon`
  must have the reviewed bytes. Arbitrary JSON cannot replace these results.
- The kit receipt uses the existing `timeline.ops.d137.installed-kit/v1`
  lead summary and the `installer1826` `PASS_INSTALL` installation JSON.
  Bind `FARM_KIT_INSTALLATION` and its independently supplied
  `FARM_KIT_INSTALLATION_SHA256`, plus `KIT_SOURCE_CHECKOUT`. The latter is
  the reviewed **Composition OPS source**, whose maker/wrapper/checker bytes
  must match D139a. It is distinct from the four film source checkouts.
  The original D137 capture has the wrong maker bytes and cannot qualify D139a.
  No new D139a receipt is asserted to exist. The installed maker and protected
  helpers must match the summary and source; child/Store component key/value
  receipts are not installed-kit receipts.
- The child receipt is the original normal queue result for
  `venv-agent-child-d140`. The maker's final `created`/`reused child venv`
  line must include the registered key, actual/requested tuple, provision-report
  path and digest, and installed-schema identity digest. The original report
  under `tests/provision/` must match the child's `.provision-report`, source
  markers, generated-client identity, schema identity and inventory sections.
  Redacted `allowlisted_fields` JSON and legacy success text are insufficient.
  This reads retained evidence; it does not open or validate a live Store.
- D73 uses the manager-rendered `p4-d73-v1` manifest, independently bound by
  digest. The receipt must be byte-identical to it and contain all launcher
  required fields, exact four-source paths/trees/parents, and bound interpreter,
  Node and profile. The launcher must be the reviewed file in the pinned Agent
  checkout. A manifest copy alone does not authenticate its producer.

Each failure remains in the complete census; a valid checkout never upgrades
an unauthenticated receipt. No producer, request, or D73 body is run by these
checks. A changed producer requires a new reviewed handoff, with no fallback.

Run the sequence in [commands.md](commands.md) only after the pre-child census
is `READY`; the post-child census is a separate admission after the normal
request returns its registered child receipt. The command file preserves the
normal request wrapper, registered-child import checker, D134
positive/poison accounting, and the unfiltered D124 22-root core selector.
The existing reviewed D73 launcher remains the sole launcher. `CORE_ROUTE`
must be the existing D73-compatible Farm route and is invoked with
the launcher’s exact manifest/`run` argv; no wrapper or alternate launcher is
defined here. Its outer command binds the exact JUnit path, raw log,
start/stop, disk witness, and retained KEEP root before cleanup.

The handoff names the f103 C0 request/reply fields literally. Request `reads`
are not `optionalreads`; accepted output uses `canonical_document`, explicit
base/previous/accepted IDs and `rebased_onto`, while conflict details use
`current` and `conflicts`. Record nesting, `receipt`, and the separate
history/head shapes remain the Runtime schema’s shapes.
