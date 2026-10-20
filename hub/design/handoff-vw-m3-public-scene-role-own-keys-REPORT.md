# Public scene role lookup correction proposal

Status: owner-ready, unapplied. This is a bounded source/test proposal for Composition at product worktree `ff0536bb5`.

## Finding

`typescript/src/scene-evaluation.ts` currently evaluates public scene roles as:

```ts
scene.roles[clip.id] ?? (track.id === 'plate' ? 'picture' : 'content')
```

`roles` is typed as a record, but an ordinary empty object still inherits `Object.prototype`. Therefore valid clip IDs `__proto__`, `constructor`, and `toString` resolve inherited object/function values instead of the existing track fallback. JSON serialization can also omit those non-string inherited values. This is an actual public evaluator failure, independent of compiler/provider/source-certification behavior.

## Proposed delta

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-public-scene-role-own-keys-proposal.patch`

- Change only the evaluator's role dictionary read to check `Object.prototype.hasOwnProperty.call` before reading the clip ID.
- Keep the existing nullish track fallback, including for an own property whose value is undefined.
- Add one direct existing `prepareScene`/`querySceneFrame` test in `typescript/tests/scene-evaluation.test.ts`.
- Exercise an own `__proto__` override from `JSON.parse`, plus absent `__proto__`, `constructor`, and `toString` entries in an ordinary empty map.

No host workaround, role-policy duplication, ID restriction, refusal, API/dependency/version/theme/params change, artifact rebuild, or release-plan claim is included. Existing input host null-prototype sanitation is untouched. The proposal does not change known `CONTENT`/`EMPTY`/`UNKNOWN`, capabilities, or normal role classifications.

## Independent source repro

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-public-scene-role-own-keys-repro.mjs`

The repro imports the emitted public evaluator source from the ORCH-only offline copy and prints the role type/value for the three reserved IDs, then prints an own JSON-parsed `__proto__` override. It does not invoke a compiler, provider, renderer, browser, socket, or source-certification path.

## Red-before evidence

In the ORCH-only offline copy, after adding the ordinary regression test but before changing the source:

```text
npm run build:test
# exit 0
node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/scene-evaluation.test.js
# 5 passed, 1 failed, 0 skipped, 0 todo
# failure: expected 'content', actual [Object: null prototype] {}
```

The direct public-source repro at that same red point printed:

```json
{"id":"__proto__","roleType":"object","role":"[object Object]"}
{"id":"constructor","roleType":"function","role":"function Object() { [native code] }"}
{"id":"toString","roleType":"function","role":"function toString() { [native code] }"}
{"id":"__proto__","ownOverride":"background"}
```

## Green-after evidence

After applying only the source correction in the ORCH-only offline copy:

```text
npm run build:test
# exit 0
node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/scene-evaluation.test.js
# 6 passed, 0 failed, 0 skipped, 0 todo
node --import ./typescript/tests/register-extensionless.mjs typescript/test-dist/tests/scene-diagnostics.test.js
# 15 passed, 0 failed, 0 skipped, 0 todo
```

The same public-source repro then printed:

```json
{"id":"__proto__","roleType":"string","role":"content"}
{"id":"constructor","roleType":"string","role":"content"}
{"id":"toString","roleType":"string","role":"content"}
{"id":"__proto__","ownOverride":"background"}
```

Patch validation from the clean product worktree:

```text
git apply --check --whitespace=error-all /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-public-scene-role-own-keys-proposal.patch
# exit 0
```

The product worktree remains clean at `ff0536bb5`. No production package build, pack, publish, artifact, integration branch, browser, render, socket, full suite, install, or network operation was run; `build:test` only emitted the temporary ORCH offline test copy.

## Adoption boundary

This is a source-future-fix proposal only. The sealed 0.0.8/0.0.9/0.0.10/0.0.11 source/artifact state is unchanged. Apply and coordinate it only in the next authorized Composition release; do not infer adoption from this report or rebuild/publish 0.0.11 here.
