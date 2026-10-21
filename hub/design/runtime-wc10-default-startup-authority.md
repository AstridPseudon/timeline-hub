# Runtime WC10 default-startup authority

Status: source investigation on Runtime `95bd3c5`; no Runtime source change made.

## Finding

The existing Astrid provider and Runtime bootstrap transaction are correct, but
the normal installed launcher currently drops the authoring profile at the
process boundary. This is a real integration regression for the WC10 default
bootstrap positive.

The normal user command is:

```text
astrid-runtime up --profile astrid --data-root <support-root> --json
```

`astrid/setup.py:286-294` emits that command and records
`runtime_profile: "astrid"` at `astrid/setup.py:570`. The SDK cold-start path
builds the same command at `astrid/sdk/autobootstrap.py:426,445-472`, and
`astrid/runtime_cli.py:183-208` forces `--profile astrid` at line 200.

The product launcher accepts that profile (`astrid_runtime/cli.py:177-184`),
builds `BootstrapConfig` with it (`:232-239`), and calls `bootstrap` for `up`
(`:481-487`). `BootstrapConfig` resolves the validated Astrid source profile
(`astrid_runtime/bootstrap.py:242-257`; `bootstrap`:738-760). However,
`astrid_runtime/runtime_boundary.py:244-258` falls back to:

```text
python -m runtime_protocol start
```

when the source profile has no custom command. The boundary appends roots and
custody arguments (`:268-287`) but not `--authoring-profile`. The source
profile's custom `runtime_command` is explicitly rejected by
`astrid_runtime/bootstrap.py:341-359`, so normal configuration cannot supply
that missing flag indirectly.

Consequently `runtime_protocol/cli.py:62` selects its deliberate low-level
default `authoring_profile="neutral"`, and `:376-394` passes that value to
`RuntimeDaemon`. No normal production caller currently selects
`authoring_profile="astrid"`.

## What the authoritative seam already does

When the profile is explicitly selected, the Runtime seam is complete:

- `runtime_protocol/daemon.py:235-256` loads/registers the provider before
  readiness.
- `runtime_protocol/timeline_commit_provider.py:70-93` maps `astrid` to the
  existing Agent factory
  `astrid.sdk.timeline.commit.create_runtime_commit_service` (factory at
  `astrid/sdk/timeline/commit.py:967-972`).
- `runtime_protocol/service.py:1698-1743` creates the timeline and calls
  `commits.bootstrap(...)` at `:1730-1741`, establishing the authoritative
  empty canonical head in the Runtime-owned commit store.

That is why the explicit native test setup
`real_runtime(authoring_profile="astrid")` supports the first-clip positive.
The old `real_runtime()` setup in Agent
`tests/conftest.py:43-63` passes no profile and is intentionally a generic
neutral Runtime. Its empty timeline is only a headless shell; it cannot provide
the canonical composition history that `TimelineSession.open` reads first at
`astrid/sdk/timeline/sync.py:131-168` (or the bundle that checkout reads at
`astrid/sdk/timeline/checkout.py:89-97`). The refusal is therefore correct for
that generic daemon, but it is not evidence that Astrid production startup is
healthy.

## Smallest source-owned fix and owner

Runtime should make the product boundary forward the already validated source
profile in the default child argv: in
`astrid_runtime/runtime_boundary.py:_argv` (currently `:244-291`), extend the
default `runtime_protocol start` argv with
`--authoring-profile <source.profile>` (the validated production value is
`astrid`). Keep `runtime_protocol/cli.py`'s neutral default and direct
`RuntimeDaemon` default unchanged; generic no-provider Runtime behavior must
remain neutral. Do not add a provider fallback, synthetic head, writer, route,
fixture bundle, generated change, or pin.

After that Runtime-owned fix, Agent should rerun only the two WC10 positives
named in the handoff, using the normal Astrid startup seam, and add the direct
no-legacy proof. Agent still owns the `astrid/sdk/remote.py:482-551` consumer
migration. D04/WC10 route retirement remains held until that qualification.
