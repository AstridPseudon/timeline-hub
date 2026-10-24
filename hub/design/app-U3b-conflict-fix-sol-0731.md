Completed U3b: **two files changed, 69 lines deleted**.

- Removed dangling `renderingElements` aliases; renderer config inherits current Composition aliases.
- Deleted obsolete SetupStatusLine after confirming zero callers and an identical RuntimeConnection replacement.
- Kept TourChatPanel: upstream introduced it in `91849b8737`; upstream `2a288e62` retains its production BrowserTourEditor caller. It contains scripted presentation, no retired writer. The review’s name-based rejection was incorrect.

Validation commands and results:

| Command | Result |
|---|---|
| `bash "$TMPDIR/union.sh"` — exact 27-path command from the corrected freeze plan, documented Node20 preload | **695/695** |
| Node20 Vitest `run --config config/testing/vitest.config.ts --configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism` over AgentChat, BrowserTourEditor, WelcomeFlow, bootstrap, tour-host/gate and AstridStatusSection neighbors | **249/249**, 16 files |
| `ASTRID_CHECKOUT=/home/user/work/agent` with Node20 Vitest `list` and `run --config config/testing/vitest.astrid-renderer.config.ts --configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism` | Config loaded; **2 discovered, 2/2 passed** |
| `/opt/node20/bin/node --import tsx --test tests/e2e/local/support/gate5-reset-precondition.test.mjs` | **12/12** |
| Serialized `flock -w 600 /home/user/work/.app-tsc.lock … tsc --noEmit --incremental false -p` for root/app/node configs | All passed |
| Scoped ESLint `--max-warnings 0`; `npm run check:astrid-conformance`; `git diff --check` | Passed |
| Node20 Playwright `test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --list` | 15 discovered; exit 1 from NOT RUN reporter, no source-load failure |

Label healing, explicit labels, outbox, authority guards, commit request/reply handling, six D31/D37 blobs, and P1/P2/P3 bodies remain unchanged. Upstream `2a288e62` is an ancestor; held draft `7fc54e1f` is not.

Limitation: default bundled renderer discovery lacks `ThreeTimelineComposition.tsx`; the explicit Agent checkout passes. No vendor adoption or full/browser/backend/HTTP/build/provisioning run performed.

U3b commit message and `DONE` written. Recommend independent review; keep isolated until P2/P3 GO.