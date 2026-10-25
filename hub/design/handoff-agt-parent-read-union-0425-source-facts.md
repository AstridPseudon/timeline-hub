# F-D86/R1 parent read-union source facts

Scope: read-only comparison of Agent `HEAD=4dcb5a5e8a` (the same
`_commit_patch.py` blob as `b415a42775`) against `7e23790248`, with Runtime
source read from `/home/user/work/runtime`. No product, test, fixture, service,
or generated-file edits were made.

## Settled contract and failure

- C0 §2 says native captures stay in `records.commands`, while
  `records.steps[].dependencies` is the normalized union of request/step reads,
  captured semantic reads/selections/bindings, and conservative generated reads.
- C0 §3 says scope reads guard the complete addressed payload and fields are
  exact-value guards; the original captured read is not erased by a narrower
  derived dependency.
- The retained proof report `design/rt-Agent-candidate13-proof-0347-report.md`
  records b415 as NO-GO: six parent selectors fail with
  `provider dependency union omits a captured read`; two word setup errors are
  separate. The report does not retain the failed six cases' prepared
  dependency arrays.
- The six applicability set in `design/agt-F-parent-guard-six-0314.md` is:
  image-anchor, image-fallback, image-lane-end, video-anchor,
  video-fallback, and video-lane-end. Their native parent birth path reaches
  `_registry()`.

## Producer path and encodings

1. `native_occurrence_media_commands._registry()` reads
   `owner + '/collection:asset'` before parent registry creation. For the six
   parent cases this is exactly `ref="parent/collection:asset", path=[]`.
2. `Recording.read()` stores that read in `record["reads"]` as
   `{"ref":"parent/collection:asset", "path":[], "state": <captured shape>}`.
   This is the native command capture; it is distinct from the normalized
   step dependency index.
3. On the normal commit path, `commit.py` executes the original at the base.
   For a moved head it loads authenticated ancestry, calls `rebase_patch()`
   before replay, then executes the replay and calls `CommitPatch.finish()`.
   The provider then passes `prepared_records(plan)` to the request-scoped
   Runtime port's `preview()` or `accept()`.
4. Current candidate `canonical_site()` special-cases `/collection:asset` to
   `parent` plus logical path `['registry','assets']`; `normalized_path()`
   makes that `['config','registry','assets']` in the dependency object.
   Current `finish()` then walks that path and emits a `field` dependency at
   that logical path when the container exists, or backs up to an ancestor and
   can emit a scope only if all path levels are absent. The exact persisted
   b415 array is UNKNOWN because it was not retained.
5. `rebase_patch()` consumes `step.dependencies` as conflict guards. A
   `scope,parent,[]` dependency overlaps an unrelated parent clip field; the
   narrow field projection was introduced to avoid that broad rebase conflict.

## Runtime strict-union expectation

Runtime `timeline_commit_auth.py` normalizes the same raw read through
`native_site()`/`site()`. Its `/collection:asset` branch requires the parent
owner and returns the physical read site `{"ref":"parent","path":[]}`.
`validate_step()` then builds the captured-read assertion as:

```json
{"kind":"scope","ref":"parent","path":[]}
```

and requires `covers(records.steps[].dependencies, capture)`. A dependency at
`parent/config/registry/assets` cannot cover the parent-root scope: `covers()`
only accepts exact equality or a `scope` dependency whose path is a prefix of
the captured read path. This explains the retained strict-union failure as a
producer/consumer encoding mismatch, without attributing the defect to Runtime
or changing Runtime policy.

## Passing comparison

The qualified current public-provider control in
`tests/sdk/test_timeline_open_commit.py` exercises both a generic `doc.patch`
and a native `clip.move`. With omitted reads, the public facade adds a
`step.reads` whole-closure scope and uses effective `merge="atomic"`; the
provider's atomic fallback adds a `timeline` scope and authenticated atomic
bindings. Those paths cover their Runtime captures and do not exercise the
parent `/collection:asset` alias. Thus their pass does not validate the parent
asset-map encoding.

## Bounded seam / unresolved incompatibility

The exact source seam is Agent `_commit_patch.py` `canonical_site()` plus
`CommitPatch.finish()` for `/collection:asset`; no other producer or Runtime
path is implicated by this source trace. However, the current code uses the
same `step.dependencies` list both for `rebase_patch()` overlap guards and for
Runtime's strict captured-read union. Emitting the Runtime-required
`scope,parent,[]` fixes the strict union but restores the broad parent conflict
for the six disjoint-head cases. Emitting only the current narrow registry-map
dependency avoids that rebase overlap but fails Runtime's required captured
scope. Therefore a producer-only fix must preserve both semantics through an
already-approved representation/seam; inventing a new policy, weakening either
guard, or changing Runtime is outside this investigation. The sole author
should resolve that seam with the exact retained six-case prepared record
before implementation.

## Static evidence

- In-memory `compile()` passed for current, 4dcb, and 7e237 `_commit_patch.py`.
- Ruff passed for current and for 7e237/4dcb source via stdin.
- Current scoped mypy passed: `Success: no issues found in 1 source file`.
- `git diff --check` passed; worktree remained clean.
- No pytest, collection, helper/function execution, probe, service, browser, or
  full-suite run was performed.
