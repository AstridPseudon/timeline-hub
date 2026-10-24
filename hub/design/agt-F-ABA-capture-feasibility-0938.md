# F-ABA capture feasibility (unapplied)

## Result

No request-bound accepted provider record exists in the retained 20732 packet.
The packet is finite and present at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-F-final-source-join-0816-authoring-current-becfe-nodes-1024085217-20732/`

The six retained metadata/result files are `summary`, `request`, `status`,
`exit`, `snap`, and `ext`. Their SHA-256 values are, respectively:

```text
summary  7a7213fcf020e0f8ce06eda8833fdabce6f978aedab717ce78c578ddf277e7d5
request  7f6b583f7b4fd24065cefc07988256799a8d4079963cf89e071e6dc738f9c2c1
status   2056a28ea38a000f3a3328cb7fabe330638d3258affe1a869e3f92986222d997
exit     4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865
snap     28d3cdb7bdc544a5c967ef72a430d3772f065c3f06863e08f9b3553fedd49a0c
ext      4c17952b36d5f9931f5c735811e160bca7bcb4890b1d5a34058a05b820c7dd62
```

The retained `summary`/`log.txt` fact is one exact selector, exit 1, 1 failed
in 40.19s: assertion 42 received `transport_timeout` instead of the original
`transport_error`; assertions 43–59 did not run. No hook-state, provider
receipt, retry, restart, final lookup, or history result is retained. The
known original body remains Agent blob
`e55be12f88d23fddba3dd36614eb91745c1f8adf`; Agent tree is
`4ce9de35768c75d38db16882423313fb5047eb5f`; Runtime is
`becfe6db88b2cc034dba3fafa6c050117cdf2b06`, auth blob
`979225ab8fdf7f6de1fcea4e7576b60b49b8b5f1`.

## Existing seam

The existing test-local hook is
`tests/timeline/test_authoring_media.py:1057-1080`:

- `RuntimeHandler._send` is already intercepted only for POST `/commit` with
  `Idempotency-Key: wc6-undo` while `_defer_response` is true.
- Before raising `ConnectionError`, it has the exact request bytes in
  `handler._prefetched_body`, the request key, the deferred status/payload and
  receipt arguments, and `handler.server.server_port`.
- The production caller is unchanged: `timeline_document.py` opens the
  authenticated `AstridClient`, creates `TimelineSession`, and calls the
  ordinary commit/inverse path; the hook does not bypass acceptance.
- `RuntimeHandler.handle` catches `ConnectionError`/`TimeoutError` at
  `runtime_protocol/server.py:1218-1219`, which explains why the retained
  packet alone cannot distinguish durable acceptance from close classification.

The normal test-service row is the existing `agent authoring-current-becfe-nodes`
row at `ORCH/tests/suites.conf:173`; it retains the requested selector through
the normal `request-test`/`test-run` custody, with Agent/Runtime/profile/module
guards and `--timeout=45`. `test-run` retains `status`, `exit`, `summary`, and
`log.txt`; no new row, service request, or custody run was made.

## Smallest future proposal (not applied)

Agent test/harness owner should add an observer-only block immediately around
the existing `with pytest.raises(WorkspaceClientError)` and the existing
`lose_undo_ack` hook:

1. At the existing hook, append one bounded JSON record to a path below the
   test's existing `tmp_path`, keyed by `wc6-undo`, containing the server port,
   request byte length and SHA-256, status, idempotency key, full deferred
   provider `data`/`receipt` projection, and the caught provider close-error
   type/message. Do not alter the raise or client mapping.
2. Immediately after the existing `pytest.raises` context and before assertion
   42, use the already-authenticated `client` to perform the existing
   `timelines.history(project, 'film', limit=100)` lookup. Append only the
   non-secret handshake authorization fields plus the complete returned head,
   matching `wc6-undo` receipt/key/result, and history item to the same record.
   Re-raise/retain the original exception and all 59 assertions unchanged;
   this observer must not convert a timeout into a pass or skip later checks.
3. Extend the existing staged `tests/suites.conf.candidate` row only enough to
   retain that one known diagnostic path/hash alongside the service result. If
   the row is not extended, print its path and SHA-256 through pytest's
   captured output so normal `test-run` `log.txt` custody retains the finite
   record. Do not add a second backend, realm, process probe, credential dump,
   or raw-body copy; the outbox remains the source of the exact original
   request bytes.

This is meaningful because it establishes, on the same authenticated request,
whether Runtime accepted `timeline.inverse` before the response close, whether
the close error was saved, whether the final lookup was authorized, and whether
the durable key/receipt/history agree. It does not infer acceptance from a
timeout, and it retains the original request/body hash, full v2 canonical
provider result, receipt, undo/history, IDs/digests/records/steps/dependencies/
effects/bindings, and structured outcome fields when present. It preserves the
30-second client and 45-second test budgets, all source/module/pin/profile
guards, scope/authentication, and the original 59 assertions.

## Owner and acceptance

Owner: Agent test/harness author for the test-local observer and staged runner
artifact retention. Any Runtime product seam would be returned to Runtime;
this proposal does not request one.

Review the exact unapplied hunk against the original test blob and run:

```bash
git diff --check
python3 -m py_compile tests/timeline/test_authoring_media.py
python3 - <<'PY'
import ast, pathlib
p = pathlib.Path('tests/timeline/test_authoring_media.py')
tree = ast.parse(p.read_text())
fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
          and n.name == 'test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba')
assert sum(isinstance(n, ast.Assert) for n in ast.walk(fn)) == 59
PY
bash -n tests/suites.conf.candidate
request-test agt-F-final-source-join-0816 authoring-current-becfe-nodes \
  --files tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba
```

The final command is a future single-selector service acceptance only after
independent review; this worker did not submit or run it.
