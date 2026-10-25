# D136c original-nine command results

## Source and admission

- Agent source: exact d133 checkout/tree `f87d59a9deb3b64efddd4707d2c8eb8a52e31bf5`.
- Runtime source: receiving carrier `777f203885ba66d89439d45d584aadd41487119f`, tree `2c022e367128da7c556d94613fb0a4b2d1915a09`, immutable ab1e parent.
- Production loader precheck: Agent modules resolved from the d133 source; Runtime auth/store/provider/service resolved from the carrier; the registered loader returned `RuntimeCommitService`.
- Python: `/home/user/work/venv-agent/bin/python`, version 3.13.16.
- Admission: 5,339,742,208 bytes free, no concurrent heavy body, 5,000,000,000-byte floor passed. The 4,000,000,000-byte stop floor was not reached.

## Sole original-nine command

The one command used the exact prescribed environment, interpreter, options, and nine selectors from `predicate-map.json`; concrete private paths are retained only in private run metadata.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<Agent-d133-source>:<Runtime-carrier-source> ASTRID_RUNTIME_CHECKOUT=<Runtime-carrier-source> /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=<private>/own9.xml <the nine exact absolute Agent selectors>
```

Result: exit 1; 9 collected; 9 setup errors; 0 failures; 0 passes; 0 skips. Measured duration was 39.339905578 seconds. XML case times were 4.076, 2.348, 2.631, 2.555, 3.270, 2.696, 2.390, 2.449, and 2.502 seconds.

All nine reached the same first seam: `provider intermediate command lacks an authenticated physical observation`.

No retry, adaptation, alternate qualification, full/family/browser/tour/core suite, collector, acquisition, profile, or separate diagnostic body was run.

## Result handling

The XML, stdout, stderr, and run metadata remain private. Only counts, the bounded first-seam message, and allowlisted schema facts are exported. No raw refusal map, traceback, payload, image, key, URL, private path, or user content is published.
