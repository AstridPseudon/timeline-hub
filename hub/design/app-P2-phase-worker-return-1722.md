## Report

Implemented P2-D21 wiring:

- Bootstrap activates only for normal `python -m runtime_protocol.cli start`.
- Replaced private observer calls with a genuine Runtime CLI startup and accepted Agent-authored HTTP commit.
- Verified actual handler phases: authorization, provider, receipt, and HTTP response.
- Preserved bounded/redacted capture and private `0700`/`0600` sink lifecycle.
- No Runtime source/helper or original journey specs changed.

Tests passed:

```text
Node 20 focused bootstrap/control smoke: PASS
python3 -m py_compile scripts/testing/sitecustomize.py: PASS
Scoped ESLint: PASS
tsc --noEmit -p tsconfig.node.json: PASS
git diff --check: PASS
Six protected journey-spec hashes: unchanged
Runtime helper identity: unchanged
```

No full/browser/P2 suite was run. Commit message written; `DONE` marker created.