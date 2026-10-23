# Runtime handoff — OPS-child-provision-0955

Candidate-only operational handoff. The Runtime product repository, dispatcher,
request wrapper, queue, daemon, tests, generated files, schemas, pins, and
configs were not changed.

## Inputs captured

Live main ORCH/bin/make-child-venv:

- mode 755
- SHA-256 ea4a1f53722ddd9f943b217021b6b4ed4828f34d10de76bae7ddc71fa470d6bc
- existing per-pip timeout 600 and freeze timeout 120 preserved

Candidate evidence:

- worker evidence directory:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-provision-0955/evidence
- candidate SHA-256:
  526e16145c3b014fb613618c27fe6d1a007857d769f31bfe5169ce423c71b52a
- candidate mode 755
- offline harness passes all required stub scenarios

## What the candidate stages

It retains the existing make-child-venv NAME AGENT_SHA [BASE_SUITE RUNTIME]
API and existing dispatcher -> make-child-venv -> request-child-venv route.
RUNTIME continues to mean the Remotion graph substitution. Runtime protocol
source is obtained separately from the current local Runtime integration
checkout at /home/user/work/runtime, archived at its exact HEAD SHA, and
installed noneditably with --no-deps. Agent remains an exact requested SHA
archive and also has a separate source marker.

The candidate adds a finite overall build budget, finite git/pip network
timeouts and retries, UTC stage progress, unique partial/failure identity,
actual python -I import-origin checks for astrid, astrid_runtime,
runtime_protocol, and astrid_runtime_client, CLI checks, freeze identity,
prepublish shebang relocation/read-only validation, and atomic final publish.
Failed partials do not occupy the immutable final destination; an exact same
name can be retried.

## Qualification boundary

The only executed qualification was offline fake Python/pip/git/timeout/filesystem
testing. It covered success, prompt timeout, failing Runtime install, missing
isolated import, immutable existing destination, no incomplete publish, and
same-name recovery. No real child venv body, package install, HTTP/socket,
full suite, D09, daemon, or heavy graph run was performed.

## Ready install

Independent review must approve the candidate before host publication. The
host-side install should replace only the existing main ORCH/bin/make-child-venv
file, preserving mode 755:

    install -m 755 <worker-evidence>/candidate/make-child-venv <ORCH>/bin/make-child-venv

Then the independent owner may run the representative child provision and
Runtime/D09 checks. No new launcher or dispatcher/process rule is required.
