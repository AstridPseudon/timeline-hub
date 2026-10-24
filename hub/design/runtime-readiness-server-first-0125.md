Ask: server diagnosis / Owner: Runtime / By: 2026-10-24T02:30Z.

**UNKNOWN; blocked before reproduction.** No Runtime defect established, no fix authored, and no tracked files changed.

Source findings:

- Bootstrap first calls `GET /v1/projects/:project/timelines/:timeline/commits?limit=50`, following cursors before loading the canonical closure.
- Runtime creates request threads, but history and ordinary health requests share `store._mutex`. History authenticates the head and entries while holding it. This explains possible shared blocking, not its cause.
- Door OPTIONS/CORS preflight bypasses that mutex.
- The fixture awaits the native seed subprocess and acceptance reply before bootstrap. A concurrent seed writer during bootstrap is therefore not established by source.

Prepared a bounded scratch probe using the existing native fixture, production daemon and browser door, with completion timing and periodic server stacks. It covers concurrent seed activity, completed seed/no writer, and the P1 seed comparison. **None of these conditions ran.**

The central request:

```text
request-test rt-R-readiness-commits-hang-sol-0125 targeted --files /tmp/w-a6f8888df7/test_readiness_probe.py
```

Run `rt-R-readiness-commits-hang-sol-0125-targeted-1024012756-17839` returned:

```text
bad file arg /tmp/w-a6f8888df7/test_readiness_probe.py (relative path/glob/node-id, no ..)
```

Zero tests collected. No local sockets, browser journey or full suite ran.

Validation: Python AST parsing passed for 10 traced Runtime files and both scratch Python files; TypeScript parsing passed for four files. `git diff --check` passed.

Pinned Runtime HEAD/tree: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` / `f79a2355cfb39d9ada7721978bd20d5702105778`. Agent `079580ca46af77e0292d49dc34386b25c8391f99` was archived into scratch. The App fixture and P1 spec match App `804134d74782d40855146aa568ff289200b79142` byte-for-byte. Actual daemon module origins remain unverified because execution never started.

Current Runtime integration `db11ea82978fba1f78cd79aec9563ea0e3372574` retains the traced server/history/locking code; among the ten inspected files, only inverse occurrence-order authentication differs.

**Next bounded observation — test-service owner:** register a named Runtime suite running:

```bash
/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider /tmp/w-a6f8888df7/test_readiness_probe.py
```

The task’s scratch-only diagnostic restriction and the service’s relative-path requirement prevented execution. `BLOCKED` and the task-named conventional commit message were written; `DONE` was not. App Sol0113 retains client/loader ownership.