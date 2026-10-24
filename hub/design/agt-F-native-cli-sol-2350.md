**BLOCKED — F-D85/G3 needs an approved CLI batch interface.** No product or test files changed from `b9f0140619736758b08f93f9353932b6db0af3ad`.

Source inspection confirms:

- `commit --file` accepts detached documents, emits `doc.patch`, and defaults provenance to Python.
- Ordinary native `edit` handles one move/trim.
- `apply` accepts sheets, rejects added rows, and regenerates commands.

None preserves the required arbitrary captured batch, claims, rationale, and exact retry request.

**Contract question:** May existing `commit --file` gain an explicit native-batch format carrying original pins/claims/metadata and durable CLI retries, or does G5 prohibit that as a retired `commands-file` alias? Scoped choices: approve that format, or specify another approved CLI batch interface.

Source-only validation:

- `python3 …/evidence/source_check.py`: exit 0; in-memory compile, full supplied-base test AST conservation, and real call-path inspection passed.
- Scoped baseline/candidate Ruff: exit 1 each; identical **15 diagnostics**.
- Scoped baseline/candidate mypy: exit 1 each; **81 errors in `cli.py`**. Initial runs also hit the same NumPy stub syntax blocker.
- `git diff --check`: exit 0.

[Exact commands and logs]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-native-cli-sol-2350/evidence/), [source hashes and conservation results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-native-cli-sol-2350/evidence/source-manifest.json), and [24 retained selectors](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-native-cli-sol-2350/evidence/later-main-selectors.txt) are recorded. No new selectors. The older ancestor’s parser-test rewrite is explicitly recorded as inherited.

Proposed behavior-log entry: “Native CLI batch preservation remains blocked: current detached commit cannot retain original command captures and CLI provenance.”

Independent review could not start because the agent service failed to load the thread. No pytest, service, build, or functional PASS; no merge. Wrote `commit-msg` and `BLOCKED`. After interface approval: implement, obtain protected review, then qualify once in the authorized MAIN batch.