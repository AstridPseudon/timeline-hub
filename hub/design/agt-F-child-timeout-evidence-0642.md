## Report

- Exported evidence packet: [evidence/packet.json](/home/user/work/wt/agt-F-child-timeout-evidence-0642/evidence/packet.json)
- Retained failed candidate receipt SHA-256: `4117623f…464b6cc`; stage `pinned-requirements`, `06:01:18–06:11:18Z`, 600s, rc `124`.
- Confirmed partial path and named provision/pip logs are absent; no cause inferred.
- Exported exact D40 child `3b5cb98c…` metadata, custody identity, markers, provision safe view, and both exact `RECORD` CSVs.
- Preserved tuple distinction: old child Agent `ba8f…` cannot qualify new Agent `bb50…`.

Validation:

```text
python3 -I ... — PASS final evidence packet validation
python3 -I -m json.tool ... — PASS
git diff --check — PASS
```

No product, kit, installed environment, network, package, test, or production-caller changes. The provision report omits `pip_freeze` under the allowlist while retaining its original hash and redaction disclosure.

Recommended next step: obtain a normal authenticated maker completion for the exact `(bb50, f320, client tuple)` candidate.