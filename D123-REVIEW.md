# D123 retained Agent patch resolution candidate

This is an F-final source candidate for ONE independent core/protected review. It is not final merged source or a qualification/adoption claim. Gating remains frozen.

## Custody and limits

- Exact base: `b742893426a46a99a2f30583a54faeebe2bd98b7` (tree `ccb2f286eae9419b95a3f54b11208f68c57b27cf`).
- Applied existing D108 patch `92443771676ef2bbb547d0a103d708fa8bec4c63` -> `d6294843286c18e57af3c1874cf1996be42212d2`, captured tree `6aeae30f0892a424104a4348bca6fd74ba1315d6`.
- Patch SHA256 `f5d49d5e63ddc0e7a0fb85966280024af70e498eb4f75bd6595bfb59a52a204a`; original manifest SHA256 `37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`.
- Ordinary `git apply --reject`, no Git state/ref mutations. The six named reject scratch files were individually removed after resolution.
- Historical D77 `523893` / `a522` remains a distinct source tuple. Later D122 `14c7ef05` is outside retained custody and absent from this reapplication. No render/gating retarget, new pin, acquisition, source profile, release, browser, P4 or D54a run.

## Six rejects: per-hunk purpose map

| Path / hunk | Retained purpose | Resolution / upstream purpose |
| --- | --- | --- |
| `astrid/chat/astrid-local-agents.test.ts`, retained line 363 | Add one EOF blank line | Keep upstream tests unchanged, including newly added local-agent discovery/sign-in coverage. No test body or predicate replacement. |
| `astrid/chat/astrid-project-chat.ts`, retained line 321 | Add one EOF blank line | Keep upstream project-session creation/Main-selection concurrency logic unchanged. |
| `astrid/chat/service.mjs`, line 1 | Historical generated bundle refresh | Keep upstream bundle unchanged: every overlapping chat source retained change is EOF whitespace only; exact current build check passes. No new bundle generation. |
| `astrid/installer/backend.py`, retained line 632 | Add one EOF blank line | Keep new upstream tail, skills synchronization and command-shim behavior. Three substantive retained hunks applied cleanly, detailed below. |
| `docs/install/OMP-LANDING.md`, retained line 64 | Add one EOF blank line | Keep upstream 18.12.6 full-fork landing instructions, producer and native pins, ledger, and deployment gate. |
| `tests/test_installer_omp_source.py`, retained line 383 | Add one EOF blank line | Keep upstream ABI/version predicates and added recipe-refresh tests unchanged. |

### Substantive overlapping retained hunks (exceptions to upstream)

- `backend.py` helper: verify the vendored canonical timeline schema is a regular file with the expected Runtime source pin/hash. Stage call: verify before creating/installing the candidate environment. Removed install: stop taking a transitive npm Python schema as canonical. These are the authentic retained local-schema/C0 contract selection, not an integrity relaxation. Upstream skills sync, shim safety, service retention and installer sequencing are preserved.
- `dispatch.py` doctor import: put `RuntimeCLIError` in scope before its exception handler, retaining the D108 diagnostic failure-path fix. New upstream skills gateway entries are preserved.
- Rendering `SKILL.md` hunks: retain existing native command/session/outbox and held detached-publication guidance required by the retained one-writer/C0 decision. Keep upstream's installed-Python wording. No skill instructions from this file were executed.
- All other 31 overlaps carry only retained EOF whitespace. The original patch's clean nonoverlap changes remain as delivered; no unrelated repair was added.

## OMP source behavior and pins

`tools.omp.source` accepts an exact npm package/version or exactly `{repo, sha}`. HTTPS GitHub input still resolves through `omp_source_url` to codeload. A supported absolute local path or local `file://` repository input returns no URL and uses `local_source`: commit-object check, regular tracked tree entries only, then `git archive` of that exact commit; dirty checkout files are ignored. Inherited Git redirects are removed. This route avoids codeload for OMP source only; native and dependency downloads remain. It predates the latest 14-commit upstream increment and requires an already available producer object. No endpoint was retried and no source was acquired.

Upstream producer documented in `OMP-LANDING.md`: `78f0e0960f471c2c62b943272a48c33366f239fe`, upstream v18.12.6 base `45c35e40c46166dc726ccc52f5d27f40f2449f99`. npm fallback `@oh-my-pi/pi-coding-agent@18.12.6`; native ABI 18.12.6; recipe Bun 1.3.14; lock SHA256 `6e330e18ca780dfccd6b6161818c204155f4c2cefce482bfead3e8315406a048`; Linux x64 native SHA256 `16c79fdc9783c7eb08ffd48867771eae792f6c0377a5eb5fc5ebb5e84ac5e931`. The recipe intentionally does not select a producer. All platforms' recipe pins and integrity checks remain upstream-equivalent. No new selection was made.

## All 35 overlaps

The 12 overlapping test files preserve the complete upstream contents modulo one EOF blank line; their retained changes also contain only EOF whitespace. Both sides' live test families/predicates survive. This is a source assertion, not behavioral qualification.

| Path | Resolution |
| --- | --- |
| `astrid/chat/acpProcessHost.test.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/acpProcessHost.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-acp-bridge.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-acp-models.test.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-agent-models.test.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-agent-models.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-local-agent-host.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-local-agents.test.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-local-agents.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-project-chat.test.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-project-chat.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-shared-acp-sessions.test.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/astrid-shared-acp-sessions.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/discoveryProbe.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/localAgents.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/modelCatalog.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/service.mjs` | Upstream bundle retained byte-for-byte; Bun 1.4.2 source check passes; retained bundle superseded. |
| `astrid/chat/service.test.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/chat/service.ts` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/core/gateway/dispatch.py` | Retained doctor exception import fix; upstream skills dispatch retained. |
| `astrid/installer/backend.py` | Retained local schema pin verification and no transitive Python schema install; upstream skills/shim/update behavior retained. |
| `astrid/installer/core.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/installer/launcher.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/installer/omp/recipe.json` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/installer/tools.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `astrid/packs/rendering/docs/SKILL.md` | Retained C0 command/outbox documentation; upstream installed-Python wording retained. |
| `docs/install/OMP-LANDING.md` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `docs/reference/services.md` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `docs/testing/TESTING.md` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `scripts/refresh_omp_recipe.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `tests/test_installer_acl.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `tests/test_installer_cleanup.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `tests/test_installer_lifecycle.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `tests/test_installer_omp_source.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |
| `tests/test_installer_wheel.py` | Upstream behavior and predicates retained; retained EOF whitespace only. |

## Verification and blocker

- Targeted installer command: `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/w-82d5f7486d/pytest-installer tests/test_installer_omp_source.py tests/test_installer_sources.py tests/test_installer_tools.py tests/test_installer_asset_checksums.py tests/test_installer_schema.py tests/test_installer_remotion.py tests/test_installer_lifecycle.py tests/test_installer_startup_stop.py tests/test_installer_update_recovery.py tests/test_installer_service_env.py tests/test_installer_acl.py tests/test_installer_cleanup.py`: **268 passed, 27 integration deselected, 13.06s**. Default lane selection was unchanged. No new tests, catches, retries, fake protocol shapes or authority widening were introduced by resolution.
- `NODE_PATH=/home/user/work/app/node_modules bun run scripts/build-chat.ts --check`: PASS, installed Bun 1.4.2. This is the repository's configured chat build gate; there is no standalone chat tsc/lint script. It does not establish TS typecheck success.
- `node --check astrid/chat/service.mjs`: PASS.
- Python `ast.parse` for backend/tools/OMP test/recipe-refresh: PASS.
- `/home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-82d5f7486d/mypy astrid/installer/backend.py astrid/installer/tools.py`: PASS, 2 source files.
- `/home/user/work/venv-agent/bin/python -m ruff check astrid/installer/backend.py astrid/installer/tools.py tests/test_installer_omp_source.py`: 2 upstream-existing backend findings (I001 import formatting, BLE001 existing shim handler). Compared directly with exact upstream stdin; no new finding. No unrelated lint repair.
- Plain `git diff --check`: 115 retained EOF-blank-line warnings. `git -c core.whitespace=-blank-at-eof diff --check`: PASS. Original retained whitespace hunks are intentionally kept; no behavioral check was changed.
- Central request: `request-test rt-F-D123-Agent-join-sol-1212 targeted --files '/tmp/w-82d5f7486d/test_d123_chat.py -s tests/test_installer_wheel.py'`. Result ID `rt-F-D123-Agent-join-sol-1212-targeted-1025121553-3707`: service ERROR, `bad file arg /tmp/w-82d5f7486d/test_d123_chat.py (relative path/glob/node-id, no ..)`. No test body ran, and the refusal was not retried/rerouted. No supported Agent Bun/chat named suite is registered. Intended existing suites: local-agents, project-chat, service, acpProcessHost, acp-models, agent-models, shared-acp-sessions; wheel remains unverified too.

Next owner: orchestrator/test-service owner must provide an allowed central route for the existing chat/socket tests, then commission ONE independent core/protected review of this source candidate and the inventory. Full/render/browser/P4/D54a qualification belongs to the separately authorized cut. No final merged-source claim is made.
