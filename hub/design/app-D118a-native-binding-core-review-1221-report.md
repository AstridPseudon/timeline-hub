# D118a independent review — FAIL

The candidate preserves `binding_id`, `head`, and existing Runtime-derived `event_stream_id` for unchanged captures, without fabricating authority or leaking `_runtime_document`.

However, the requested real rebind is not repaired. Against immutable Runtime `42aad0e…`, tree `085a5be…`:

- Candidate genuine script/rebind node: **failed** at [native_text_binding.py:69](/home/user/work/wt/app-D118a-native-binding-core-review-1221/astrid/sdk/timeline/native_text_binding.py:69), refusing the changed text with `dependency_changed`.
- Parent implementation under the same provider: **1 passed**.
- Parent authority reproduction: **1 failed, 1 passed**, with the expected missing-`binding_id` assertion—not ImportError.
- Candidate additive tests: **4 passed**.
- Existing native/spike/script units: **52 passed, 2 deselected**.
- Ruff, mypy, compilation, diff check, source containment: **passed**.

Only the permitted production file and additive test changed. No emitter, auth guard, Runtime, route, schema, or private-source changes were made.

Candidate remains HELD. The author must resolve the conflict between changed-text rebind support and the new authenticated-pin mismatch refusal while preserving wrong-pair, incomplete-authority, no-write, and privacy guards.

Evidence and commit message were written under the assigned worker directory.