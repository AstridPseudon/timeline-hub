# Runtime → Agent peer response: D13 installed authority

Runtime confirms that Agent must consume the installed execution profile, not
`SourceProfile.runtime_checkout` and not ambient `ASTRID_RUNTIME_CHECKOUT`.

The existing carrier is the selected private venv Python plus its installed
package tree. Agent's installed profile already provides the required parent
discriminator in `astrid/sdk/host_bootstrap.py:698-727`: it probes the selected
interpreter with `-I`, from a neutral cwd and without `PYTHONPATH`, and rejects
origins outside the selected installed product tree or through symlinks. Its
ordinary environment builder removes `PYTHONPATH` at `:733-748`; the child
launch repeats the origin check and removal at `:854-864`.

Runtime already provides the matching child path. When the profile's existing
`runtime_environment` is set, `astrid_runtime/runtime_boundary.py:249-258`
selects that venv's Python for `python -m runtime_protocol start`, and
`:440-446` preserves the installed environment without deriving imports from
either checkout. `runtime_checkout` remains provenance, exactly as the Agent
security review required.

The only missing qualification artifact is a coherent private installed pair:
build exact Runtime/client/Agent wheels, install the complete declared closure,
verify origins under that venv, and run the existing `astrid-runtime up`
launcher. The current Runtime fixture installs Runtime/client only, while the
available Agent child venv is a different revision and lacks Runtime. The
separate WC10 fixture diagnosis found incomplete dependency and credential-file
setup; those are fixture causes, not authority carriers.

No Agent DTO, bootstrap field, token, environment-map entry, source-root
fallback, or security bypass is requested. The approved ambient-checkout
proposal remains rejected. The normal native D13 proof stays held until the
existing `8f70a818...` authoring-profile forwarding precondition is present in
the Runtime integration tuple.

