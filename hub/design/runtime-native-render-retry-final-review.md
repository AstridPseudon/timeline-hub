# RT07/D13 native historical render admission — independent review

## Verdict

**APPROVE** `37c4304d56486b16e0c02090971315508f942c89` (test-only; Runtime
tree `c431abc5025bcadae5355da8229289af797187ec`). The new marked test is a
valid bounded proof of native historical `rendering.render` admission replay
after a lost acknowledgement, head advancement, and Runtime restart.

## Marked qualification tuple

The required central node was run as:

```text
env ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONPATH=$PWD:/home/user/work/agent \
/home/user/work/venv-runtime/bin/python -m pytest -q -m integration \
tests/test_render_native_historical_retry.py
```

Result: **1 passed in 11.66s** (central run
`rt-m2-native-render-retry-independent-review-occupancy-integration-1020144357-5229`).

Actual source tuple for that run:

- Runtime test tree: `c431abc5025bcadae5355da8229289af797187ec`
- Runtime commit under review: `37c4304d56486b16e0c02090971315508f942c89`
- External Agent commit: `acc17162dd57b2cafc966098e44625ea25bfe461`
- External Agent tree: `553ced9239bf063b3b94d4614795ac52a6d47aa9`

The frozen ordinary Agent reference requested for comparison is commit
`310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, tree
`c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`. Its
`astrid/core/dev/journey.py:352-377` builder is byte-identical to the current
external checkout’s builder: it supplies the normal `rendering.render` body,
capability digest/storage estimate, empty input IDs, and the key
`astrid.render:v1:{timeline_id}:head:download:{output_name}`. No source override
was used in the central qualification.

## What the test proves

- `astrid_importable` is used before importing `capture_move`,
  `bundle_from_document`, and `build_app_render_admission`; the test asserts the
  loaded capture implementation is inside that external Agent checkout.
- A is accepted through the real Agent commit provider (`capture_move`,
  `bundle_from_document`, and `load_timeline_commit_provider("astrid")`). The
  normal Agent builder creates the request; the test adds only Runtime’s
  existing closed five-field `spec.params.canonical_revision` selector.
- The selected A revision, publication receipt, and parent content digest are
  asserted in Runtime-owned `timeline_authority`; the retained A snapshot bytes
  are read from the admitted CAS reference.
- C is then committed through the same real provider after the admission
  response is intentionally discarded. After reopening Runtime, submitting the
  exact original body and idempotency key must return the byte-equal original
  admission result, including the original task, run, and receipt. The retained
  snapshot bytes remain A, the durable head is C, and the database has exactly
  one task and one run.

The Runtime implementation independently matches these claims: it validates
the closed selector and rejects caller-owned snapshot/provenance fields
(`runtime_protocol/store.py:1716-1758`), resolves the selected publication and
revision closure (`:1848-1901`), creates Runtime-owned authority/snapshot data
(`:2091-2122`, `:2414-2454`), and compares keyed replay against the persisted
normalized admission before returning the original result (`:2497-2542`,
`:2591-2639`).

## Bounds and open items

This is a direct Runtime service admission/replay test. Its discarded response
models a lost acknowledgement at the service boundary; it does not prove a TCP
connection drop, HTTP/outbox integration, worker claim, restart-safe client
outbox behavior, actual render execution, decoded pixels/PCM, export/decoder
behavior, or registered-completion restoration. It does not forge an inline
snapshot, provenance, or renderer-worker authority field, and it uses the real
Agent provider; negative forged-input refusal is covered by the neighbouring
historical-admission suite rather than this new positive test.

The prior central summary of **33 passed, 47 deselected** must not be
attributed to this new test: that run did not collect this newly added
integration-marked node. The direct focused run below and the marked central
run are the evidence for this review.

Existing old-render safety denial/legacy strong-completion positives, plus the
remaining RenderRequest propagation, builder/requester, decoder, and export
gaps, remain open as directed. No full or broad suite was run.

## Additional local check

```text
env ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=$PWD:/home/user/work/agent \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
-m integration tests/test_render_native_historical_retry.py
```

Result: **1 passed in 1.78s**. `git diff --check 16acbb6..37c4304` also passed.
No product code, fixture, schema, dependency, shared worktree, branch, merge,
or publication was changed.
