# P2 review report

Verdict: PASS for source-causal claims and exact scope, with qualifications below.

- Confirmed A2’s `opaqueClip` loss in `rowsToConfig` allowlisting.
- Confirmed parent refusal at `timelineLocalSaveHandoff.ts:324–326`.
- Confirmed deferred interaction rescheduling drops `gestureBasis` at `useTimelinePersistence.ts:1329–1334`.
- Confirmed all five current P2 paths use real selectors and mounted callbacks. No current source defect from prior 0357 remains.
- Corrected wording: reproduction shows one owner record with `intents.length === 0`, not literally zero intent records.
- Original13583 internal ordering remains unknown.
- Source qualification does not establish live browser upload/POST/reload/Undo behavior.

Bounded reproduction used the retained trace and finite six-resource extraction. All SHA-1 checks passed:

- parent `d9a136733945bf0bd8ad622379e6e093f01358ab`
- shot `5bb6bed55e89f700da3d641ad8ce8e572713fefe`
- internal `3963b500da676e9b328546d93883ab0d7a3e1cb1`
- history `4fb745fbe558c85ad8b1472f4f2d523423408f24`
- inspection `558234f80972c964fd4a932fe9bf3b75920d2f07`
- timeline `ff8e7a23654008f673056ff24a45292cee86a233`

Fixture SHA-256: `26ad79804f43f81cfe5f786837935b28948991b7f80012dcaa59134b1498fa72`.

Test command:

```bash
A2_FIXTURE=/tmp/w-78b08ebd4a/a2-source-fixture.json \
/opt/node20/bin/node node_modules/vitest/vitest.mjs run \
--config /tmp/w-78b08ebd4a/a2-vitest.config.mts \
--configLoader runner --no-cache
```

Result: 2 failed, 1 passed. Expected RED fail-witness; no product fix or browser-cause proof.

Source checks:

```bash
git diff --check
git status --porcelain=v1 --untracked-files=all
```

Both passed; worktree clean. No full suite, types, lint, or live browser run performed. Commit message and `DONE` marker created.