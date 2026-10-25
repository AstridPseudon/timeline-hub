# Tiny whole-maker E2E inputs

This directory is the durable, source-only input for
`tests/e2e_inventory.py`. The four roles are intentionally private and tiny:
the Agent and Runtime source carriers, plus the two differently-spelled
dependency distributions. The `makers/` files are the exact parent `0857a5…`
and candidate `c3226b…` shell inputs, including their executable modes;
`tiny/manifest.json` pins every source and maker byte and the two locally-built
dependency wheel hashes. It contains no product data or caller privileges.

The receiving service must commit the emitted Agent and Runtime carriers in
dedicated fixture Git repositories through its normal receiving path. The
runner uses those committed checkouts for the maker's authenticated archive
and never expects the source archive itself to contain `.git`. The packaged
maker files and the protected Store/helper hashes are checked before any
Store or maker body starts.

Before `--write-inputs`, wheel building, venue preparation, or a run, the
receiving target can enumerate all prerequisites without mutation:

```sh
python ops-child-custody/tests/e2e_inventory.py --check-only \
  --helper "$TMPDIR/bench_store.py" \
  --bootstrap-artifact "$TMPDIR/bootstrap-wheel-input.tgz" \
  --wheelhouse "$TMPDIR/tiny-wheelhouse" \
  --agent "$TINY_AGENT_CHECKOUT" --runtime "$TINY_RUNTIME_CHECKOUT" \
  --orch-root "$TMPDIR/tiny-orch" \
  --parent-work "$TMPDIR/tiny-parent-work" \
  --candidate-work "$TMPDIR/tiny-candidate-work" \
  --result "$TMPDIR/check-only.json"
```

This mode checks the real Agent Python (`/home/user/work/venv-agent/bin/python`)
for Python/build/setuptools/wheel, the child `/usr/bin/python3.13`, required
commands, local wheel hashes, source Git heads/tree/modes, the numeric `df`
reserve and Store projection contract. It lists every missing item and exits
non-zero before Git mutation, Store initialization, maker execution, or body
setup. `--prepare-venue` then creates the empty `tests/suites.conf` projection
baseline before normal `Store.initialize`; this is private fixture state.

The commands below are lead/harness commands. The worker does not initialize a
Git repository or create a commit. The harness must materialize two clean,
dedicated fixture checkouts and commit exactly the source files emitted by the
writer:

```sh
export TMPDIR=/the-harness-owned-tmpdir
python ops-child-custody/tests/e2e_inventory.py \
  --write-inputs "$TMPDIR/tiny-inputs"

# In the harness-managed dedicated checkouts, copy only these files:
cp -a "$TMPDIR/tiny-inputs/agent/." "$TINY_AGENT_CHECKOUT/"
cp -a "$TMPDIR/tiny-inputs/runtime/." "$TINY_RUNTIME_CHECKOUT/"
git -C "$TINY_AGENT_CHECKOUT" add LICENSE astrid astrid_runtime_client pyproject.toml requirements/proof.lock
git -C "$TINY_AGENT_CHECKOUT" commit -m 'test: publish tiny Agent fixture'
git -C "$TINY_RUNTIME_CHECKOUT" add LICENSE astrid_runtime packages/python/astrid_runtime_client pyproject.toml runtime_protocol
git -C "$TINY_RUNTIME_CHECKOUT" commit -m 'test: publish tiny Runtime fixture'
```

The two resulting commit IDs are the only source identities accepted by the
venue preparer. `fixture_sources()` checks the exact file set and hashes again
before either commit is used.

Build the private dependency wheels offline with the already-installed build
tool. The command writes only below `TMPDIR`; it does not install anything or
use an index:

```sh
python ops-child-custody/tests/e2e_inventory.py \
  --build-wheels "$TMPDIR/tiny-wheel-build" \
  --build-python /home/user/work/venv-agent/bin/python
```

Stage the three already-qualified bootstrap wheels from the existing local
artifact into the same private wheelhouse. Verify the hashes shown in
`tiny/manifest.json` and in the bootstrap artifact's integrity manifest; do
not acquire another version:

```sh
mkdir -p "$TMPDIR/tiny-wheelhouse" "$TMPDIR/bootstrap-input"
tar -xzf /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz \
  -C "$TMPDIR/bootstrap-input"
cp "$TMPDIR/bootstrap-input"/timeline-bootstrap-wheel-input-0932/wheelhouse/pip-26.2.1-py3-none-any.whl "$TMPDIR/tiny-wheelhouse/"
cp "$TMPDIR/bootstrap-input"/timeline-bootstrap-wheel-input-0932/wheelhouse/setuptools-80.9.0-py3-none-any.whl "$TMPDIR/tiny-wheelhouse/"
cp "$TMPDIR/bootstrap-input"/timeline-bootstrap-wheel-input-0932/wheelhouse/wheel-0.46.3-py3-none-any.whl "$TMPDIR/tiny-wheelhouse/"
cp "$TMPDIR/tiny-wheel-build"/custody_b-0.1.0-py3-none-any.whl "$TMPDIR/tiny-wheelhouse/"
cp "$TMPDIR/tiny-wheel-build"/custody_a-0.1.0-py3-none-any.whl "$TMPDIR/tiny-wheelhouse/"
```

Prepare two empty, single-use Stores through the unchanged `Store.initialize`
API. This creates only private roots under `TMPDIR`; it does not touch the
production Store or change any admission, reserve, owner, or permission. The
preparer copies the protected helper into its private orchestration root only
after checking `bench_store.py` against `123bb93c…7adfe2`:

```sh
python ops-child-custody/tests/e2e_inventory.py \
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

Only after an admitted receiving venue has passed its unchanged reserve check,
run the genuine bounded make. It executes parent `0857a5…` first (expected
RED), candidate `c3226b…` second (expected GREEN), then the unchanged sealed
verifier and exact adversarial mutations. The runner records stage names and
hashes, never private command bodies or URLs:

```sh
python ops-child-custody/tests/e2e_inventory.py \
  --venue-manifest "$TMPDIR/tiny-venue.json" \
  --result "$TMPDIR/tiny-e2e-result.json"
```

Stop before this last command when free space is below the unchanged
`5905580032`-byte normal-child reserve, or stop immediately at the unchanged
4 GiB floor. Do not reuse either Store or its work root, and do not rerun a
failed make in the same venue. The result remains `NOTRUN` until this real
receiving execution occurs; source checks and wheel preparation are not E2E
credit.
