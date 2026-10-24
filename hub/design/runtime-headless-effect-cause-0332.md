**Classified: Agent authoritative-effect recorder defect. No fixture correction is supported.** Runtime worktree unchanged.

The first mismatch is in step `headless-probe`, command 0, effect 2:

| Boundary | Exact value |
|---|---|
| Authoritative effect path | `parent/config/clips` |
| Resolved storage path | `parent/clips` |
| Effect’s claimed before | `{"state":"absent"}` |
| Runtime’s observed before | `{"state":"present","value":[]}` |

The accepted bootstrap payload is:

```json
{"clips":[],"config":{"clips":[],"tracks":[]},"occurrences":[],"registry":{}}
```

Replacing config genuinely removes its synchronized root `clips` mirror. Native command writes record that removal, and change 0’s binding covers both writes (`write_range: [0,2]`). The authoritative step patch omits the removal.

Agent `_commit_patch.py` computes a complete `effect_diff()`, then its all-parent `doc.patch` shortcut replaces those effects with normalized submitted changes. Offline, the complete diff produces one whole-parent effect; Runtime’s existing `step_output()` projects it to the **exact genuine command output**. This locates the defect independently of the exception text.

Additional findings:

- `picture`, `a`, and `edited` are genuinely new at this base; all three created declarations match recorded allocations.
- Accepted history contains one bootstrap entry, with `records: null`. Line 322 is the first authored patch against that bootstrap, not a repeat over accepted authored content.
- Genuine CAS media verified: 2,329 bytes, digest `sha256:8ea859676fb0dc68b5f5ba4921b80758e3fe9f65c8540ebd35de2c2c902b471e`.
- Public head/history remained unchanged after interception.
- Agent advanced from `8f5c7329c8` to `7aa96ae614` during investigation. The relevant shortcut matches historical `622b30a8`; `commit.py`, `_doc_patch.py`, and `_commit_preview.py` are byte-identical to that historical source.

Verification:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python "$TMPDIR/effect_capture.py"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python "$TMPDIR/classify_effect.py"
git diff --check
git status --porcelain
```

Capture and offline comparisons passed; diff check passed; status clean. An initial setup-only attempt encountered unsupported `RuntimeService` context-manager syntax, corrected before capture. Ruff/Pyright: N/A, classification only. Original tests, assertions, requests, and guards remain untouched; no family, final acceptance, HTTP, browser, or full-suite rerun.

**Next:** independently repair Agent effect recording to retain complete mirror-topology effects, then qualify the unchanged positive body. No classification blocker remains. Wrote `commit-msg` and `DONE`; no committable changes.