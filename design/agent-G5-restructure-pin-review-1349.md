# G5 native restructure pin review — bounded PASS

Decision: PASS for the bounded `nativepin/publicforward` scope. This is still
G5 draft-only and P1 remains NO-GO, inherited from the solution and hydration
reviews. No integration merge is requested.

Reviewed source pairs:

- Candidate `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`, tree
  `ac1251cdc911b99d690d303cdd777fe14643bdb1`, against hydration-reviewed
  parent `052e148539828cdf44d36029074bab225e21de31`, tree
  `5fecdabcb0eff53a9329779073caf77772116f74`.
- Candidate changes are limited to
  `astrid/sdk/timeline/native_restructure.py` and
  `tests/sdk/test_timeline_restructure_guarded_runtime.py`.
- Native source SHA-256 is `800247535bbe034777fe84beb0612d96ea11992f8d77ad52ba7503dff56afb43`;
  focused test SHA-256 is
  `d7dc8942c49b4c464535280b8849520adfba4b67d4dc0560a5b68203abf7983b`.
- Runtime evidence pair is approved checkout `8592822fd11275540f596562f43c715676f2bc0f`,
  tree `ed9856f43a4e44a058bf2230badea2c4c7080050`; vendored client pin remains
  `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- The original inverse function remains byte-identical with SHA-256
  `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d` and
  was not executed.

Review findings:

- The native guard accepts exactly `{revision_id, content_digest}` or those two
  keys plus a nonempty string `publication_id`; it compares the exact revision
  and digest, checks project/timeline scope and source parent identity, and
  refuses unknown or malformed fields without mutation.
- The change does not make the pure preparer an opaque publication authority.
  The public exact-pair loader, Agent request/evaluated-head checks, and Runtime
  history/CAS/auth checks remain the authority. No ignored publication,
  current-head substitution, digest waiver, provenance drop, repaired cache, or
  caller-supplied source payload was found.
- The public fixture captures the actual request, evaluated head, public reads,
  native input, idempotency key, preview, accepted reply, lost ACK and exact
  retry. It verifies canonical document equality, one history publication,
  receipt/records/bindings/writes/dependencies, steps and patches, reads,
  authored opaque/null/list data, and no-write refusal controls for wrong
  revision/digest/publication/unknown/scope, stale same-byte history, and forged
  immutable payload. The narration failure is the deliberate original test seam
  and is disclosed as out of scope.
- The prior hydration review’s two-file `publish.py` source change is unchanged
  here; its exact-current-closure guard, local-authored value preservation and
  refusal behavior are inherited.

Durable authored evidence reviewed:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-pin-sol-1335/evidence/`
(`source-evidence.json`, `forward-summary.json`, `public-forward.json`, and
the final fixture logs). The evidence source hashes and tree identity match the
candidate in this worktree.

Exact verification commands and results:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -o tmp_path_retention_policy=all -p no:cacheprovider --timeout=40 -k fixture_ tests/sdk/test_timeline_restructure_guarded_runtime.py
10 passed, 1 deselected in 86.84s (0:01:26)

/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/native_restructure.py tests/sdk/test_timeline_restructure_guarded_runtime.py
All checks passed!

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-pin-review-1349/tmpdir/mypy-cache astrid/sdk/timeline/native_restructure.py tests/sdk/test_timeline_restructure_guarded_runtime.py
Success: no issues found in 2 source files

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
ok runtime.lock.json

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check
pass
```

Additional non-qualifying diagnostic: `scripts/vendor_lock.py check
runtime.lock.json --producer /home/user/work/wt/rt-pin-8592822f` reports the
expected producer mismatch (`expected 34eac004...`, `got 8592822...`). The
candidate's checked-in Agent artifacts pass the authoritative lock check above;
the separate Runtime checkout is the approved test authority, not the pinned
vendored-artifact producer.

The original inverse test was intentionally excluded by `-k fixture_`; no full,
P1/P4, HTTP/browser/native14/58, D17/54, live-socket, Runtime patch, or inverse
diagnosis suite was run. No product or test edits were made by this reviewer.
