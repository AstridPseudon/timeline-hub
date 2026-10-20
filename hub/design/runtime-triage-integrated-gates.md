# Runtime M2 triage integrated gates

## Result

**GREEN / qualified on the actual Runtime integration snapshot.** The already-present
merge `2cb9bb62c88d91fdab03df230ef0b2a3bd81f513` (`Merge
tl/rt-m2-triage-s2-current-gate`) was qualified without changing this worker or the
shared checkout.

The qualification snapshot was frozen before the service requests:

- Runtime integration HEAD: `2cb9bb62c88d91fdab03df230ef0b2a3bd81f513`
- Runtime integration tree: `ec90ae8c6472316eea0101369314fcbef6907334`
- Agent HEAD/tree: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` /
  `75354d38c898729bac09619679f5421faba319ed`
- App HEAD/tree: `6ff21cac9deee3aae014e5c9e65d9871a3452f77` /
  `27d41c1b0e64ff9028f78576804f3b8cb3b9f1d5`
- Composition HEAD/tree: `e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab` /
  `23a994070b8e25aba18703af1c6a0c840df1ab62`

All four shared checkouts were clean at freeze and after the runs. The worker itself
started at `c1fb9ef2f7736459ceaaaaf85b5f9650e32c942d`, tree
`e0aa6fbeb28a771a121248c0879aa6831d16f5fd`; that stale worker tree was not used as
qualification evidence.

## Bounded source verification

The first-parent diff from the integration parent `c1fb9ef` to the merge is exactly:

- `runtime_protocol/store.py`
- `tests/test_render_historical_admission.py`
- `tests/test_spec_reference.py`
- `tests/test_timeline_pack_inputs.py`

It is 84 insertions and 27 deletions. The four actual integration files are
byte-identical to approved port commit `1051c4b8a5ec48a9688c3f0803256d8497e65edf`
(source `9abc5c65de784d8d04bc5af2284fbc365ca625fa`, as reviewed). A read-only diff
confirmed every other current capture/text/render-guard/client/main file is unchanged.
The port therefore retains the current S2 storage/seam behavior; the only
current-Agent compatibility additions are the two authentic capture-authority
identity fields (`project_id` and `timeline_id`) in the visualize fixture.

The `store.py` conversion remains narrow: only historical replay of the specific
retained snapshot-object error (`timeline snapshot reference object is missing or
corrupt`) becomes the established `ConflictError` with
`reason=render_revision_integrity` and the Runtime-built digest. The later replay
check applies the same exact-message restriction. Other reference, custody,
validation, archive, and conflict errors retain their original refusal behavior;
no repair or publication write is introduced.

The fixture diff keeps real behavior coverage: real startup-loaded Agent provider,
accepted publication boundary, real projection, isolated retained-row corruption,
and Runtime media ingestion. Positive A-after-C, restart, archive, corruption,
no-repair, current-C, and exact retry assertions remain present. No Agent overlay,
fake provider, xfail, skip, or weakened behavior expectation was added.

## Central service evidence

Every requested lane used the central service against `integration:runtime` with
`--files`; no full or broad suite was run.

1. Ordinary lane, result `runtime-targeted-1020121521-25698`:

   ```sh
   /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime targeted --files 'tests/test_render_historical_admission.py tests/test_spec_reference.py tests/test_timeline_pack_inputs.py'
   ```

   Service command: `python -m pytest -q` with those three files. Result:
   **76 passed, 59 deselected in 43.77s**, Runtime tree
   `ec90ae8c6472316eea0101369314fcbef6907334`.

2. Marked integration lane, result `runtime-marked-integration-1020121521-23758`:

   ```sh
   /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime marked-integration --files 'tests/test_render_historical_admission.py tests/test_spec_reference.py tests/test_timeline_pack_inputs.py tests/test_canonical_render_admission.py'
   ```

   Result: **59 passed in 37.24s**. This includes the three triage files plus
   canonical render admission. The service external span records Agent
   `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` and the frozen App/Composition
   heads above; all repeated span records agree.

3. Commit integration lane, result `runtime-commit-integration-1020121521-937`:

   ```sh
   /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime commit-integration --files 'tests/test_timeline_commit_integration.py'
   ```

   The named suite supplies that file and the explicit `--files` argument repeats
   it; pytest de-duplicated collection. Result: **9 passed in 13.29s**.

Read-only checks also passed:

```sh
git diff --check c1fb9ef2f7736459ceaaaaf85b5f9650e32c942d 2cb9bb62c88d91fdab03df230ef0b2a3bd81f513
```

The four actual integration files parsed with `ast.parse`; none contains xfail or
skip markers. The existing Runtime snapshot-authority neighbor result remains
**115 passed** (`rt-m2-triage-s2-current-gate-targeted-1020114812-20872`) on the
current triage port. It was not repeated: the new diff is confined to the narrow
historical replay conversion and its three bounded fixtures, while the new marked
lane already includes canonical render admission.

## Limits and remaining caller gaps

- Agent Linux activation/custody identity failures remain held separately (Darwin
  audit-token custody and parked-host process identity representation).
- The ordinary HTTP caller remains held on the Agent-vendored Runtime client
  metadata pin (`0.2.9` versus current Runtime `0.2.10`/schema metadata).
- `test_real_retained_legacy_publication_uses_verified_source` remains positive
  retained-publication coverage, but is not evidence that the retired legacy
  publication branch still runs.
- No full, broad, browser, or additional authority-neighbor run was performed.

No product edit, merge, pin, publish, dependency/cache mutation, or other
repository change was made by this worker. The shared integration merge was
already present when the qualification snapshot was frozen.
