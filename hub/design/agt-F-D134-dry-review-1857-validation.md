# F/D134 independent dry-review validation

## Result

PASS for readiness for the owner-authorized conditional 20:00Z measurement
only. This review grants no ship, behavior, full-body, or custody credit and
did not run a body.

## Read-only checks

- The four frozen checkouts independently matched the recorded SHA, tree,
  parents, official origin, and clean status.
- The normal maker and pinned launcher matched their recorded SHA-256 values
  and Git blob witnesses.
- Runtime lock, profile lock/archive/registry, schema copies, client/schema
  metadata, Python, Node, and Composition version matched the exact manifest
  bindings.
- `positive.manifest` and `poison.manifest` have 36 lines and differ only in
  `agent_sha`; their SHA-256 values are the required
  `b539c6bda83f...` and `f41fef0062e...` values.
- The existing 0811/2234 positive stub hash is the required full
  `38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0`.
- The retained positive counter parses to one line (`called`); the poison
  counter parses to zero lines.
- The retained structured preflight result records positive `0/17/1` and
  poison `1/0`, with the deliberate `D73 launcher: agent SHA mismatch` guard.
- The recipe retains 22 selector roots, `-n 3`, cleared `addopts`, disabled
  cache provider, and `--timeout=45`.

## Commands run

```text
bash -n evidence/measurement-command.sh evidence/preflight-command.sh
python3.13 -P -m json.tool evidence/review.json
python3.13 -P -m json.tool evidence/source-custody.json
python3.13 -P -m json.tool evidence/source-review.json
python3.13 -P -m json.tool evidence/source-manifest.json
python3.13 -P -m json.tool evidence/manifest-diff.json
python3.13 -P -m json.tool evidence/preflight.json
python3.13 -P -m json.tool evidence/readiness.json
python3.13 -P -m json.tool evidence/missing-inputs.json
git diff --check
```

All checks are source/evidence checks. No request-test, collection, pytest
body, provider, fixture, package acquisition, installation, child/profile
build, alternate environment, or full suite was run. The two DRY controls were
not rerun.

## Durability and bounded missing evidence

The usable scripts, manifests, counters, and structured results are tracked in
`evidence/` and are the durable receiving source for this review. The manager’s
byte-exact publication destination is the requested
`$ORCH/design/agt-F-D134-dry-review-1857-*` prefix. The prior private raw DRY
directories were recycled, so their raw stdout/stderr is unavailable; this is
bounded because the retained evidence includes the actual counter contents,
manifest hashes, receipt hashes, and guard/outcome fields.

The Agent-local design path named by the preparation brief is absent. The
available hub design copy was used only as a reference, while the normal maker
and launcher were verified directly from the frozen Agent checkout.

At 20:00Z, the manager must bind the recorded owner clock/verdict and check
the genuine D128 custody result, free-space start/stop limits, and ordinary
preflight acceptance. If custody is GREEN or any real safety/classifier/
permission guard refuses, the conditional measurement does not proceed and
there is no retry or alternate route.
