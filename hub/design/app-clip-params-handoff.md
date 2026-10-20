# clip.set-params capture qualification

Branch `tl/app-m2-clip-params-parity`, based on `5e7dabedc`; standalone M2 capture only. No integration merge or wiring. Agent authority: `ceb2ab67bf97d342c5af7392bee1f24cabc2ea2e`.

Removed the hand-built `expectedRecord()` oracle. `recipe_m2_clip_params_native.json` contains complete unmodified `execute(...).records`: four companion original exports and seven additional cases. All original four fixture files were compared byte-for-byte with the Agent commit and remain unchanged. Native execution verifies 11 command/bundle/full-record cases plus the original disjoint replay (12 results), including input immutability and replay of captured commands.

Added the existing `ctx.compile()` invocation after scalar writes. Before this fix, the new tests produced 11 failures: stale parent config mirrors and omitted retained compiler dependencies. Product changes are that one call and a stable local `clear` binding to preserve TypeScript narrowing across the argument-validation callback; imported M1 primitives are unchanged. No second recorder/compiler or Runtime DTO was introduced.

Additional native cases cover parent params object/absence/null/empty object with initially equal nonempty `parent.clips` / `parent.config.clips`, opaque sibling rows and parent/config/shot fields, retained transcript + source pins (unretained versions excluded), occurrence empty object, and an unchanged leaf write. All compare complete native command, bundle and record after freeze/JSON roundtrip. Original clears, empty/literal keys, null values, disjoint leaf replay, forged/incomplete claims and original identity/value refusal checks remain.

Scope: raw finite JSON capture and local preview only. Element parameter schemas, unknown-field/admission policy, authoritative accepted execution, inverse/redo, and registry validation remain Agent responsibilities. This helper is not a local schema bypass or an accepted Runtime command path. No UI/session/provider/pin changes. Initial divergent mirrors, first-add/last-delete and media selection aliases belong to `app-m2-recorder-primitives`; this qualification uses equal nonempty clip arrays and does not duplicate or claim that worker's wider fixes. No dependency blocks the cases qualified here; compose the shared recorder work before qualifying wider current-M2 behavior. M2 merge remains held until the orchestrator records M1.

Native export used installed dependencies without installation and read-only source extraction:

```bash
mkdir -p .native-clip-params/agent
set -o pipefail
git -C /home/user/peteromallet/astrid-agent archive ceb2ab67 astrid astrid_runtime_client schemas | tar -x -C .native-clip-params/agent
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/.native-clip-params/agent" /home/user/work/venv-agent/bin/python .native-clip-params/export.py
```

The temporary exporter passed fixture bundles/requests directly to native `execute`, exported its complete records/commands/bundles, checked originals against the frozen git bytes, and replayed the captured commands. A separate native Python stdin verification reloaded the exported JSON and compared all 12 results with `execute`; no Agent source modifications. Temporary extraction/exporter removed after verification.

Fixture SHA256: `13f361f98c42a942ca3a4d75115dbb7d271bcaf8eb0a98c0ea67b2e0ae83af73`.
Original hashes: object `30f6ef768d52affc7ac511a1b01aa09910fd0deae37f366c26e7293a47c80918`; absent `20bc5467bdfca447363816e0c86cf31c383afb9515a1a154a46a42feda5415d5`; null `be191fce0fca6d92194e034f9de7fce1328ed6ad831227225b5bba1176e50b3a`; disjoint `63541a7c4b9c17663b577d0bed40681842ac944c3abe4699bfec74803036679b`.

Checks:

```bash
node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/authoringBundle.test.ts --pool=threads --maxWorkers=1
node_modules/.bin/eslint src/tools/video-editor/commands/clipParamsCapture.ts src/tools/video-editor/commands/clipParamsCapture.test.ts --max-warnings 0
node scripts/quality/check-known-failures.mjs
node scripts/quality/check-no-smoke-tests.mjs
git diff --check
```

Vitest: 137 passed / 3 files, including 36 params tests. ESLint: exit 0, no warnings. Known-failure audit: exactly 3 authorized original markers, 0 forbidden. No-smoke audit passed. Diff check passed. No full/browser/socket suites or installs.

Actual App typecheck (run once, serialized):

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false
```

Exit 2: four diagnostics. Baselines: `RuntimeConnectionProvider.tsx(90,53)` TS7053 and `AgentChatNewChatButton.tsx(80,23)` TS2550. Existing capture helper: `clipParamsCapture.ts(50,44)` TS18047 (`args.clear` possibly null) and `(50,55)` TS2339 (`includes` unavailable on JSON union). Replaced closure access through mutable `args.clear` with a validated local const; this addresses the reported narrowing issue without changing validation semantics. Focused tests/lint rerun after the fix. Per the one-project-typecheck task limit, no second App typecheck was run: the final source tree's typecheck is UNVERIFIED, not green or “only two baseline errors.” Manager composition needs a fresh serialized typecheck.

Correction to predecessor report: its “no diagnostics” / typecheck-pass claim is unsupported. The predecessor log shows repeated launches and an empty temporary log inspection, without a completed successful typecheck result; this task's completed App check exposes the two pre-existing helper diagnostics above. Empty output from an unfinished command is not a pass.
