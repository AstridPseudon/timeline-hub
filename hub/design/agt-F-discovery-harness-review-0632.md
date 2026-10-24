## FAIL — independent first-return review

Reviewed cumulative source, prior FAIL0619/return0626, PLAN §3, commit-v2 §§1–5, and production path.

Findings:

- Harness self-invalidates: current `HEAD` is `060fab…`, but lines 383–389 require the same checkout to be Agent `bb50…`. The committed harness cannot qualify its own valid `bb50` source carrier.
- `--manager-run-gate` accepts any caller-selected file containing three matching text fields; authority is forgeable and path overrides weaken the gate.
- Public `--child` bypasses parent receipt resolution and durable parent evidence.
- Installed custody is incomplete: only selected client `RECORD` rows and six product files are compared. Runtime `RECORD`, full package contents, and several production imports (`contracts`, Remotion/shared renderer modules, render action) are not pinned.
- Required durable before/after evidence is incomplete: no complete safe environment, origins, JUnit/result artifact, and exit record on every setup-failure path. `EVIDENCE.mkdir()` occurs outside the guarded evidence path.
- No `tests/suites.conf`/normal test-service registration for this runner was found, so the claimed manager/test-service execution path is not wired.

Confirmed positives:

- Runner SHA: `03be7e7b…a0ada`.
- Exact selector/body hashes, 9 assertions, 10 support calls, transition invocation 6, and `--timeout=45` are preserved.
- Preflight returns before body launch; run requires reviewed SHA plus gate.
- Agent/Runtime SHA, dirty-tree, markers, Node20, profile, archive, and lock checks are present.
- No body, provisioning, host, Node, browser, or test-service run was performed.

Checks:

```text
python3 -m py_compile tools/run-discovery-original-0603.py — PASS
/home/user/work/venv-agent/bin/ruff check --no-cache tools/run-discovery-original-0603.py — PASS
bash -n wrapper — no wrapper present
git diff --check — PASS
```

Future target remains:

```text
tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons
```

No product changes made. Commit message and `DONE` marker recorded.