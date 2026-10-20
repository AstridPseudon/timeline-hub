# Default transition SET on normal013: native contract gate blocks port

2026-10-20. Source audit complete; **no App code changed**. The requested default SET cannot be implemented under FINAL Agent d874 / Runtime 2c4 / S2: native `clip.set@1` explicitly excludes transition authoring. This is a reproduced contract mismatch with the proposed slice, not a change to PLAN's settled incoming-transition decision. No writer activation, retirement, current-browser qualification or acceptance claim follows.

## Exact sources and current root

| Source | Identity / finding |
| --- | --- |
| Assigned App root | `/home/user/work/wt/app-m2-default-transition-set013-seam`, HEAD `b1ef4b9b910ba72375c34cf319692f90d22edc25`, tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`; clean before/after |
| Fixed native Agent | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed` |
| Fixed Runtime | `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`; official contract `0.2.13` |
| Native EditCommand schema | `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`, `astrid/core/timeline/schema/edit-command.schema.json:1716` at d874 |
| App Runtime pin | All **13/13** locked files match both lock hashes and exact `git show 2c4:<producer path>` bytes; includes current generated `ClipSetArgs` |
| App CLI surface lock | All **7/7** entries match their recorded hashes; root's source pin is `5dec5dc6a4eb6683cd8a9a7e7f2048fbb18d9681`, unchanged; this is not a claim of d874 CLI-lock adoption |
| Retained SET candidate | `686198313f35b4e918ec74af23beb9fcb3af5948`; schema SHA256 `4b12260791657ed6bc143992e2acf734c6b833489ca3538d7a8a4f81ec8dd4fc` differs from d874 |

Read PLAN first, including canonical incoming semantics, then `design/app-transition-set-seam.md`, `design/app-native-none013-source-compose.md`, `design/app-native-none013-independent-review.md` and `design/app-public12-native-none-source.md`. The retained SET report is authority for its distinct 6861983 candidate only; it is not evidence of registration at d874.

**Current-root qualification remains FIRST and UNRUN.** The assigned b1 root does not contain `commands/clipScalarCapture.ts` or `hooks/useClipScalarControl.ts`; its session has move/track-label capture, and `ClipTransitionSection` has no scalar submit prop. The separately retained normal013 None source is therefore not present on this assigned root. It was not imported as incidental dependency work. App labels/recovery, pins/package locks/public12/Main17/server/cold4/7M1 sources are unchanged. No shared dependency, cache, venv or runtime was modified; Node and dependency caches were never invoked.

## API and exact counterexample

At d874, `commands.operations()` registers `clip.set` with the native `ClipSetArgs` schema, and `validate_command` checks that schema before running its handler (`astrid/sdk/timeline/commands.py:62,86-102`). The current API is:

```python
capture_clip_set(bundle, select, *, values=None, clear=())
```

`_clip_scalar_commands.py:113` documents source hold SET/clear and raw asset/transition removal. `values` admits **only** positive `hold`; `clear` admits `hold`, `asset`, `transition`. Both objects are closed. Its schema says “transition authoring is outside v1.” There is no transition SET, paired `values.elementRef`, or `schema_source` argument. App's generated `timeline-commit-types.ts:109-118` agrees: SET values contain only hold. A built-in renderer being listed in App's catalog does not authorize that field in the command.

Using the exact d874 scalar fixture bundle, both native capture and direct native execution reject this smallest default SET:

```json
{"schema_version":1,"op":"clip.set","version":"1","select":"parent/clip:f2-transition-clip","args":{"values":{"transition":{"type":"crossfade","duration":0.5}},"clear":[]}}
```

Exact result: `CommandError`, kind `invalid_edit_command`, message `Additional properties are not allowed ('transition' was unexpected)`.

The same request against explicit raw owner `occurrence:f2-occurrence/clip:f2-agent-clip` produces the same error. Parent/occurrence targets each also refuse a duration-0.75 transition with original revision, nulls, ordered arrays, empty/dotted/`__proto__`/`constructor`/`prototype` keys. All **four capture cases and four direct executions** leave the entire original bundle unchanged. These are atomic refusal proofs, not proof of SET preservation or acceptance. No display-ID ownership heuristic, selected-pack schema inference, incoming predecessor recording, invented binding, App transition policy/math or fallback was added.

Full exact inputs and errors: [native-counterexample.json](../workers/app-m2-default-transition-set013-seam/notes/native-counterexample.json). Reproducer: [native-counterexample.py](../workers/app-m2-default-transition-set013-seam/notes/native-counterexample.py). Source/pin results: [source-audit.json](../workers/app-m2-default-transition-set013-seam/notes/source-audit.json).

## Golden and App ingress

The retained `6861983` golden `tests/editing_conformance/fixtures/recipe_m2_app_transition_set.json` has SHA256 `ce250ab38b5c7a681bddf618ad2fb55d5fba57290a337d474d1b6b5134e8d747`, verified against immutable Git bytes. **That file is absent from d874.** No current transition SET commands/records/after/inverse can be matched, because native validation refuses SET before capture.

The actual d874 `recipe_m2_app_clip_scalar_fields.json` golden contains precisely `{values:{hold:4},clear:[]}`, `{values:{},clear:['asset']}` and `{values:{},clear:['transition']}`. Its compact stored SHA256 is `52dac614ac1b13efda13de9b79ecd3a1713939fd7e6f5f7d07d57ca8ec500348`; the fixture loader restores factored records. The prior App report's `8bb75e23...` identifies its expanded App fixture, not these compact bytes. Fresh proof matches every original capture, complete command, record, after-bundle and inverse/redo against current d874. Original input remains exact.

Current App `components/PropertiesPanel/ClipTransitionSection.tsx:132-147` routes selection to `onChange` with type, old duration/default 0.5 and optional defaults. Duration at 251-259 spreads the displayed transition; parameter and Reset callbacks at 283-317 spread its envelope and params (Reset overlays declared defaults). None/Remove also use the existing callback here. This task does not rewrite those existing behaviors or assert that display state is raw capture authority. No tests were changed, weakened, skipped or marked expected-to-fail.

## Exact validation commands and results

Commands ran with dependencies read-only, bytecode/cache disabled. Native code came from an exact private `git archive d8749a9ce12a699672faf3ad96b4e4cbea9245c2` extracted under this worker's notes, never from moving integration code. Archive setup is retained in `notes/prepare-native.py`.

From the assigned App worktree:

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-default-transition-set013-seam/notes/prepare-native.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-default-transition-set013-seam/notes/agent-d874 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-default-transition-set013-seam/notes/native-counterexample.py
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-default-transition-set013-seam/notes/audit-source.py
```

Results: archive extraction succeeded; exact supported golden parity plus four SET refusals passed; source/pin/clean-tree audit passed. All exit 0. The archive preparation was initially executed inline with the identical saved script body. Counterexample output is retained in `notes/native-counterexample.log`.

From the private `notes/agent-d874` archive:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-default-transition-set013-seam/notes/agent-d874 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py
```

Result: **95 passed in 8.92s**, exit 0, unchanged main conformance tests. This includes the existing explicit transition SET refusal case; no behavior test was rewritten to produce it. No App suite ran because no App code changed and the prerequisite native schema gate failed. No full suite/central request, build, browser, socket, tsc or install ran.

## Blocker, owner question and remaining gate

**Implementation blocked by missing native registration on the required frozen tuple.** Per the brief's explicit stop condition, no speculative App port/framework was created and no alternative candidate was adopted.

Owner question for Agent/Runtime/orchestrator: **Which official future paired source/schema release will carry transition SET and its exact native golden?** The retained 6861983 candidate has it, but FINAL d874/2c4/S2 does not. Recommended next action: Agent owner ports/reviews the missing native SET contract and predecessor/read/selection/inverse coverage; Runtime owner publishes the matching generated artifacts; orchestrator authorizes that exact new tuple before App resumes. This report requests no unapproved pin change.

After that contract exists, qualify the current App root first, then implement only the bounded default SET capture/session/control slice against complete native commands/records/after/inverse. Original raw revision/opaque/null/prototype keys/order and parent/occurrence identity must survive; unsupported custom/unknown/mixed drafts must remain atomic visible refusals without fallback. Real matching-pair acceptance, immutable reload, other-author guarded undo, unknown-ACK/dependent suffix/process-restart/exact retry, real revision/publication identity and representative zero-legacy traffic remain the actual central gate. Prior source tests and this audit establish none of those live claims.

Private Agent archive removed after checks. No build output/temp file or product/test change remains in the assigned worktree. Worker report and conventional commit message are retained; BLOCKED records the implementation gate. No KEEP is needed because there is no code for review. No Git commit/merge/rebase/checkout/push/ref mutation was performed.
