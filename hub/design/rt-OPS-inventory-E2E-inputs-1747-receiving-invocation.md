# Receiving invocation

The harness must first publish the exact Agent and Runtime source files from
`ops-child-custody/e2e-fixtures/tiny` into clean dedicated checkouts and commit
them. It then stages the three pinned bootstrap wheels from the qualified
local artifact and builds the two private dependency wheels with the offline
command documented in `ops-child-custody/e2e-fixtures/README.md`.

Prepare the isolated venue with the protected helper through the normal API:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python \
  ops-child-custody/tests/e2e_inventory.py \
  --prepare-venue "$TMPDIR/tiny-venue.json" \
  --helper /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py \
  --orch-root "$TMPDIR/tiny-orch" \
  --python /usr/bin/python3.13 \
  --wheelhouse "$TMPDIR/tiny-wheelhouse" \
  --agent "$TINY_AGENT_CHECKOUT" \
  --runtime "$TINY_RUNTIME_CHECKOUT" \
  --parent-work "$TMPDIR/tiny-parent-work" \
  --candidate-work "$TMPDIR/tiny-candidate-work"
```

Only when the receiving filesystem reports at least `5905580032` free bytes,
and its final free-space check remains at least 4 GiB, run:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python \
  ops-child-custody/tests/e2e_inventory.py \
  --venue-manifest "$TMPDIR/tiny-venue.json" \
  --result "$TMPDIR/tiny-e2e-result.json"
```

This performs parent `0857a5e0…` RED, candidate `c3226b93…` GREEN, genuine
source-carrier installation, relocation, unchanged `STORE_VERIFY`, private
Store registration, and the exact adversarial metadata/source-marker
mutations. It must be one bounded run: stop on the first reserve/floor
failure, never reuse either Store, and never run against `/home/user/work` or
the production bench. No E2E result is claimed by this preparation worker.
