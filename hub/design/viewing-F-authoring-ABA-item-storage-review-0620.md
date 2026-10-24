# Independent review: FAIL

The bounded Agent patch at `1a983fa7c` is not safe to merge independently. It passes all local item identity/storage/inverse controls, but the exact two-occurrence materialized transformation still fails Runtime strict native-write membership.

Evidence:

- Required targeted acceptance: **245 passed**
- Ruff: pass
- Mypy: pass
- Vendor lock: pass
- Artifact manifest: pass
- `git diff --check`: pass
- Original media test blob unchanged: SHA-256 `0c23fc68...fbc487`
- Original ABA function retains all **59 assertions**
- Agent SHA: `1a983fa7c22aec5bc1b6db98d46d8aaed1e6fe03`
- Runtime SHA: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`

The exact recorded scratch transformation—removing only the single-occurrence slice—reproduced:

```text
2 failed, 59 deselected
```

Both fail at Runtime [`timeline_commit_auth.py:1160`](/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:1160):

```text
inverse stage native write membership differs from its authenticated stage
```

The Agent path is correctly wired through:

- `timeline_document.py:80-115` — `emit_document_publish_commands`
- `native_occurrence_media_commands.py:287-293` — `capture_occurrence_swap_media`
- `native_occurrence_media_commands.py:75-82` — identity-qualified item writes
- `_command_state.py:290-407, 583-619` — authenticated mapping and local-ID storage projection
- `inverse.py:31-76, 272-337, 982-1135` — inverse resolution, folding, and stage recording

The bounded controls cover bijective mapping validation, owner/revision/digest checks, missing/duplicate/foreign/local-alias refusal, colon IDs, aggregate/leaf/root folding, stored local IDs, and equal-byte retarget refusal.

Remaining seam: Agent inverse/materialization record emission does not produce native membership matching Runtime’s authenticated `source_stage["native_sites"]` or effect sites when both shared occurrences are retained. Runtime’s strict guard should not be relaxed; the Agent inverse-stage normalization/capture seam needs owner coordination.

`assets` and `audio_bindings` remain numeric-index paths at `native_occurrence_media_commands.py:84-107`; they are explicitly outside this bounded correction. No original/live/HTTP/full/browser/SDK4 runs were performed.