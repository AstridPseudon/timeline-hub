# AP2-M2 selected canonical resolver review

## Decision

**APPROVE** the exact candidate for one next central selected-fixture gate.

- Commit: `f490c60a11015c6bf1a80e167c3d7bea63aaed81`
- Tree: `5b9ec99d9670c5262b04c35bc9475379f9ef43be`
- Parent: `1d9299867020b64fd80afae0ea5a951601d4dc8d`

The next gate should be the one central real selected DEV journey covering P1/P2, source removal, refusal, exact retry after lost acknowledgement, reload, and undo. This review does not claim that browser/live-socket journey passed.

## Source and custody review

The candidate changes only the selected fixture harness and its offline control:

```text
tests/e2e/local/support/harness.ts
tests/e2e/local/support/selected-param-credential.test.ts
```

The new helper returns the fixed argv prefix:

```text
[python, "-m", "astrid.core.element.cli", "project-pack", "resolve"]
```

The existing Vite host appends only the scoped values from the current request and selected Runtime identity: `--realm` from the expected realm, `--project` from the admission request's project ID, and `--pack`, `--element`, `--kind`, and `--revision` from the exact requested ref. `config/vite/vite.config.ts` invokes the array with Node `execFile`; no shell interpolation or `shell` option was added. The existing `projectElementSelection` checks the project/ref identity, Runtime document binding/version/content digest, and retained snapshot digest before accepting the resolver record.

The normal document read remains the existing Runtime client `getDocument`, whose generated operation is `GET /v1/projects/{project}/documents/{document}`. No new endpoint, DTO, write path, source-pin fabrication, fallback catalog, or authority bypass is present.

The protected four-line bridge change from `1d9299867`, issuer context from `eee191c1`, and seed from `24165cb` are all unchanged ancestors of the candidate. The candidate does not add a credential file, actor, scope, profile override, or browser credential carrier. Existing P1/P2 and refusal/retry/reload/undo assertions are unchanged.

## Frozen Agent check

Frozen Agent `8130a401bf44a518d5a40ae274d398b8c560be55` contains both:

```text
astrid/core/element/cli.py
astrid/core/element/project_packs.py
```

Using a private temporary extraction of that exact tree, the real entrypoint was invoked with `project-pack resolve --help`. It parsed successfully and exposed the closed required flags:

```text
--realm REALM
--project PROJECT
--pack PACK
--element ELEMENT
--kind {effects,effect,animations,animation,transitions,transition}
--revision REVISION
```

This confirms that the repaired fixture prefix matches the frozen Agent producer; it is not a guessed command.

## Evidence

Passed:

- `node --import tsx tests/e2e/local/support/selected-param-credential.test.ts` — 4/4 controls passed: fixed argv, credential path-versus-token, issuer/realm/actor rebinding after restart, and cleanup.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/support/selected-param-credential.test.ts` — passed.
- `git diff --check HEAD^ HEAD` — passed.
- Private extraction of frozen Agent `8130a401...` followed by `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-extraction> python3 -m astrid.core.element.cli project-pack resolve --help` — passed; exact flags above were printed.
- Protected ancestor checks for `1d9299867`, `eee191c1`, and `24165cb` — all passed.

Not run by instruction: browser, localhost/live sockets, central request-test, full suite, or product edits.

