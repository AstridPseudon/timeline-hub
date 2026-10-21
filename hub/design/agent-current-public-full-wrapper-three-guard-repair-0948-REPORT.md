# Current public full wrapper — three-guard repair

## Result

Repaired `scripts/full_coherent_public_current_integration.sh` on the Agent
worker branch. The wrapper now:

Wrapper Git blob SHA: `233e115294b9db7b72792f9c2528fb2c99de5dcd`.
Wrapper SHA-256: `de8b93c85d27e658902635017430cecaebc424efb8a7d3bd8d2be52cdce2c669`.

- replaces the central runner's ambient `PYTHONPATH` with an explicit
  bootstrap path; source `astrid` is loaded from the public c4b checkout while
  Runtime/client/schema packages are preloaded from the selected private site
  for the parent and xdist children, with post-schema origin checks;
- validates the settled 164-entry carrier (`478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`),
  exact 166-distribution/RECORD closure, all installed files, all product
  wheel RECORD/source bytes, c4b Agent source payload, b92 Runtime payload,
  public95 client payload, and Agent-wheel/client-wheel parity;
- retains the original `pytest -q -n 3` invocation, no marker, no cache or
  basetemp override, and ordinary pytest temporary-directory behavior;
- retains the 13 GiB admission threshold and refuses a new profile build until
  real headroom exists.

No product source, tests, shared dependencies, test-run implementation, or
other suite definition was changed. No install, profile build, pytest body,
collection, full request, Runtime/socket, browser, or renderer run was made.

## Wrapper registration / lease

The stable ORCH wrapper is the committed script at
`scripts/full_coherent_public_current_integration.sh`, named
`full-coherent-public-current-integration`. This report plus the adjacent
lease file are the ORCH registration handoff; the central allow-list remains
untouched as directed. The manager should register the named command against a
recreated snapshot of this worker branch, with the exact private c4b profile,
wheel, and `metadata/venv-agent-child-s2.txt` supplied as environment inputs,
then retire the lease after the one bounded decision.

Registration command shape (manager supplies the real profile paths only after
the storage gate clears):

```text
env -i HOME=/root LANG=C.UTF-8 PATH=<pinned-node-and-system-path> \
  SOURCE_ROOT=/home/user/work/agent \
  FULL_COHERENT_PUBLIC_PROFILE_ROOT=<private-c4b-profile> \
  FULL_COHERENT_PUBLIC_AGENT_WHEEL=<private-c4b-profile>/wheelhouse/astrid-0.1.0-py3-none-any.whl \
  FULL_COHERENT_PUBLIC_PINS=<private-c4b-profile>/metadata/venv-agent-child-s2.txt \
  bash scripts/full_coherent_public_current_integration.sh
```

The wrapper itself remains the only suite command artifact; no `suites.conf`
or test-run edit is part of this worker change.

## Bounded evidence

- `bash -n scripts/full_coherent_public_current_integration.sh` — PASS.
- `git diff --check` — PASS.
- Missing-profile/wheel preflight — exit 2; no pytest path reached; exact
  c4b/b92/95/C13/tool positives remained visible; storage refusal remained
  active (current observed gap 2.267 GiB to the 13 GiB threshold; prior
  independent review observed 2.880 GiB).
- Planted child seam — exit 37 propagated.
- Planted SIGTERM seam — exit 143 propagated.
- Planted zero-collection seam — exit 5 propagated, with effective argv
  `-m pytest -q -n 3 --collect-only`.
- Read-only historical/staging profile probe — refused at the strengthened
  closure guard (`182` RECORDs rather than `166`); the old Agent payload was
  not accepted as current c4b evidence.

No claim is made for a successful profile preflight or full suite until the
manager supplies a newly built c4b profile after the storage gate clears.

