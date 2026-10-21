# App2 M2 selected final custody one-case review

## Verdict

**HOLD.** The final runner delta and bounded launch controls passed, but the
single authorized central run failed during selected-fixture setup at the
first Runtime handshake. No selected behavior qualification is claimed and no
retry was submitted.

## Independent final-delta review

Reviewed the immutable runner
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-artifact-version-literal-0724/artifacts/run-owned-selected-final95.sh`
(`dcda1b820fa2feb68db6ae99b56cdc8cd4277016c3eaf939a5ded423c9b25ee0`) against
the four-fault runner (`a92fded8e01ce622060113d1296ac74e9ccff6a8770a8dcac08e331a0d901964`).
The only delta is artifact-version custody: the value is derived from
Runtime95 `contract/artifacts.json` at initial binding, tuple restoration, and
immediately before launch; the planted wrong-version refusal is retained.

Recomputed from Runtime95 `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`:

- valid manifest JSON, producer `astrid-runtime`, 76 artifacts;
- manifest SHA `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`;
- artifact version `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.

The unchanged final95 source/object, App source, lock, schema, graph, helper,
origin/proxy/credential, argv, selected-contract, cleanup and list-1 evidence
was independently reused only after the final-delta comparison. The offline
preflight passed all ten checks, including exact one-test collection.

The actual dispatch was exercised to a `/bin/true` launch-only stub with
`NORMAL014_USE_BASE_PYTHON=1`, hostile inherited `NODE_PATH`/`NODE_OPTIONS`,
the frozen keeper, and a clean service-root stand-in. It exited 0 and traced:
`source_refs artifacts locked_graph scripts_scope selected_contract
service_source protected_keeper keep_and_normal_link node_graph list1
artifact_version launch`. The private root and trace were removed. The
preflight planted wrong-artifact-version guard also passed. The initial local
attempt without `NORMAL014_USE_BASE_PYTHON=1` was stopped at the runner's
forbidden pip-install branch; it did not reach launch and was not a central
submission.

## Central registration and result

Registered exactly one immutable suite line in
`scratchpad/orch/tests/suites.conf`:
`ap2-m2-selected-final-custody-one-case-0730-run`. It binds the runner hash,
`SELECTED_FINAL95_MODE=run`,
`APP_KEEPER_ROOT=/home/user/work/wt/ap2-m2-selected-normal-dev-frozen-source-0651`,
and requires the exact frozen source HEAD/tree and clean status. The request
target was the frozen source worker
`ap2-m2-selected-normal-dev-frozen-source-0651`, never this checkout,
prior013, or moving integration. The source worker's `KEEP` marker remained
present; the runner hash and graph/source guards supplied the exact tool
binding for the one active central lease.

Exact request:

```text
request-test ap2-m2-selected-normal-dev-frozen-source-0651 ap2-m2-selected-final-custody-one-case-0730-run --no-cache
```

Result:

```text
TestID: ap2-m2-selected-normal-dev-frozen-source-0651-ap2-m2-selected-final-custody-one-case-0730-run-1021073218-8082
tree: 7fe8c15b56da9944ae31e8273d41d3ceb21b3677
exit: 1, 84s
counts: 1 failed
```

The runner passed source/artifact/graph setup, built the hosted App, collected
and executed exactly one test, then failed first at:

```text
tests/e2e/local/three-products.selected-param-dev.spec.ts:39:1
DirectHarness.seedSelectedParamDev -> harness.ts:589
project-pack init -> Runtime handshake
astrid.sdk.exceptions.ServiceUnavailableError: runtime request failed
(unauthorized: invalid bearer credential)
```

Reached: hosted build, one-test collection, test launch, fixture setup,
Runtime handshake attempt. Unreached: original 20-second mount assertion,
semantic budget, P1/P2 admission, source removal, P1 refusal with draft,
lost-ACK exact retry body/key, restart/reload recovery, inverse/undo, and
zero-legacy POST assertion. Central snapshot and runner temporary root were
cleaned after failure.

## Checks and limits

Passed:

```text
sh -n <dcda1b82 runner>
Runtime95 manifest/version recomputation and JSON parse
SELECTED_FINAL95_MODE=preflight ... <frozen source path>  PASS, all ten checks
bounded run-mode dispatch with launch-only stub                 PASS, exit 0
central exact one-test collection                                  PASS
```

No source, helper, spec, pin, dependency, lock, generated file, or worktree
change was made. No retry, second central submission, local browser/socket,
full suite, install, or writer cut was performed.

## Next step

Resolve the central credential/Runtime handshake custody boundary on the exact
frozen source/tool cohort, then schedule a separately authorized run only
after review. Preserve the registered suite's source and runner guards; do
not treat this result as behavioral qualification.
