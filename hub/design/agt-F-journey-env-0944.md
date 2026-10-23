# F journey environment isolation handoff

The eight service-8962 journey failures were caused by the targeted runner's
ambient `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime` conflicting with the
two fixtures' temporary `runtime_checkout_path()` results. The smallest fix is
test-only: each fixture uses `monkeypatch.setenv` to declare its own temporary
Runtime path.

The real mismatch guard remains in `astrid/core/dev/journey.py`. A focused
negative control confirms a mismatched declaration refuses before Runner phases
and leaves the source probe unchanged.

Qualification: central request `agent-targeted-1023094559-13611`, source snapshot
tree `61f8df72f486845746f8874326a15cb1b3311b57`, exact eight nodes plus the
negative control, **9 passed in 0.38s**. Local touched-file run: **16 passed in
0.45s**. Ruff and diff checks pass. Base commit is
`543d133c85de16ab800c4df0e9ff504ca077fcbf`.
