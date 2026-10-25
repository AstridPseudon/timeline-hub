# D127a diagnostic retention candidate

This is a worker-private candidate. It is not installed or invoked against a
live Farm root.

## Source-backed lifecycle correction

The installed production caller validates a writable build tree with the
existing verifier's `--staging` mode in its `verify-staging-inventory` stage
(`make-child-venv`, lines 673–680 in the installed preimage). The embedded
verifier sets `staging = sys.argv[-1] == '--staging'` and only permits writable
regular files in that explicitly selected mode. Diagnostic retention creates
the authenticated staging root as `0700` before `build(stage, final)`.

The candidate therefore appends `--staging` to the existing `STORE_VERIFY`
invocation used by diagnostic `verify(stage)`, and records that exact argv in
the receipt. The verifier source itself is unchanged. `seal(stage)` still runs
after verification (including after a verification failure), and the receipt
keeps the failure status and error rather than claiming validation.

## Exact future Farm command

```text
$ORCH/bin/make-child-venv venv-agent-child-d127a a4e016b6a9f91fbe372672bdcf382c630bf59186 OPS-farm-agent-full --retain-staging-no-register --source-carrier $AGENT_CHECKOUT $RUNTIME_CHECKOUT 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344 --farm-schema-source $FARM_SCHEMA_SOURCE --dependency-wheelhouse $DEPENDENCY_WHEELHOUSE
```

The placeholders must be supplied by the authorized Farm handoff. This task
did not acquire them, build, install, register, adopt, reuse, publish, or run
test bodies.

## Barriers retained

- Default mode still calls the existing `Store.ensure` path.
- Diagnostic mode checks authenticated source, ownership, lock, reserve,
  source/RECORD/license metadata, and dependency authority through the exact
  installed embedded blocks.
- Diagnostic mode writes only authenticated staging plus its bounded receipt;
  registration, adoption, reuse, final publication, READY state, and test-body
  execution remain statically and dynamically barred.
- Verification failures, cancellation, and seal failures remain refused;
  receipts retain their actual status and captured error.

## Contract shape carried for downstream review

The eventual Runtime request remains the C0 v2 shape: `api_version`, scope
IDs, base revision/publication IDs, commands, nonempty label and steps with
`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, optional reads,
`merge`, `reads`, `dry_run`, and `Idempotency-Key`. Success evidence is
`accepted`/`merged` with canonical document, receipt, head, effects, bindings,
and dependencies. Refusal evidence carries conflict head/reason or invalid
code/path/hint; dry-run has no writes. This maker does not implement or invoke
that Runtime API.
