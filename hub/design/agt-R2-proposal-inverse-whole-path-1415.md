## D30 report — source-cause PASS; integration behavior FAIL

- Base Agent: `512f83d8385e449c9020e5db2aa3fb02ff152848`, tree `9fce413c0335f2dca2bbb3ac2b20a58d2141acc6`.
- Runtime: `e68cf231641db98a72805a586b51ab5c4fae2c16`, parent `becfe6db88b2cc034dba3fafa6c050117cdf2b06`.
- Retained failing selector: `tests/sdk/test_timeline_producer_guard_runtime.py::test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes`.
- Failure remains: `invalid_records: provider inverse effect bindings do not cover its stage image`.

Cause is Agent-owned:

- `astrid/sdk/timeline/producer.py:47-63` emits a producer batch without `label`, `steps`, `merge`, or `reads`.
- `astrid/sdk/timeline/_commit_patch.py:262-263` therefore classifies the request as legacy (`v2=False`).
- `_commit_patch.py:595-610` emits no `commit.effect` bindings in that mode.
- The accepted inverse still contains an authenticated `inverse.stage` for `publication_id`, `step_id`, `command_ordinals`, and native/effect ranges, but has zero physical effect bindings.
- Runtime `runtime_protocol/timeline_commit_auth.py:1694-1708` correctly resolves the affected physical image as `parent` and requires one binding for each `effect_ordinal=0`, `side=before/after`, and path `["config", "tracks"]`.

The source-only `DetachedRealm` probe reproduced this exactly: legacy request → `inverse.stage` present, zero `commit.effect` bindings, Runtime validator rejection. Adding the normal v2 step metadata produced two authenticated `parent` bindings and passed the same validator.

Production reachability is confirmed: `astrid/sdk/timeline/sync.py:271-286` queues settled proposals through `build_producer_batch`; `sync.py:518-536` can flush that legacy-shaped body. `assembly.py:177-194` separately supplies full v2 metadata.

Four held fork failures are unrelated: those fail through `_CopiedShot` provenance loss across durable reload (`commands.execute → inverse.apply_inverse → _validate_inputs → State.shot_item_map`), whereas this case is a simple `parent` image with an omitted Agent binding. ABI ruling 1400 remains relevant only as a prohibition on inferring recorder mode or weakening Runtime validation.

Scoped unapplied Agent hunk:

```diff
-            if self.v2:
+            if self.v2 or any(self.inverse_stages.get(index)
+                              for index in step['command_ordinals']):
```

File: `astrid/sdk/timeline/_commit_patch.py:595`. Runtime changes, ABI changes, and test changes are not warranted.

Checks:

- `git status --short --branch`: clean.
- `git diff --check`: pass.
- No pytest/original body/full/live suite run, per task restrictions.
- Source hashes recorded: Agent `_commit_patch.py` `b5002547aae418431685b653ed0a077ff11b478c`; Runtime validator `979225ab8fdf7f6de1fcea4e7576b60b49b8b5f1`.

Commit message and `DONE` marker created.