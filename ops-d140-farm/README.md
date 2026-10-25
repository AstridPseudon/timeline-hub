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

Run the sequence in [commands.md](commands.md) only after the census is
`READY`. The command file preserves the normal request wrapper, registered
child import checker, D134 positive/poison accounting, and the unfiltered D124
22-root core selector. The existing reviewed D73 launcher is the sole launcher.
