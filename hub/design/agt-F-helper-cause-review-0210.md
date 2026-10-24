# Causal review: FAIL for current Agent helper `[True]`

Owner is Agent core, not Runtime.

The retained capture is custody-valid:

- JSON: `4,879,737` bytes, SHA256 `ea99da6e6340d74627a12ea351b4bfd49208b0af55a0ec69d152af656157546f`
- gzip: SHA256 `d20b22981bdef983b5952952154ab3f102fc55266594f4067567d8594830777a`
- Agent `415181d983`, tree `f49cae445`
- Runtime `8ea0766f`, tree `6047ac303`
- Captured source hashes match the current Agent and pinned Runtime sources.
- Refusal caused no database write; before/after DB SHA256 remained `d2247888…`.

## Exact cause

Agent emits 14 unique replay-map entries:

- 2 patch entries
- 3 changed internal-image reads
- 9 extra unchanged-physical `parent` reads:
  - 3 `batch-read`
  - 6 `input`

Runtime computes exactly 5 required entries. All 5 are present in Agent’s map; the first unexpected entry is:

```text
(0, read, parent, [config, theme_overrides], batch-read)
```

Runtime rejects it at `timeline_commit_auth.py:2195`. This is over-emission, not a duplicate key and not a missing changed-child mapping.

Runtime’s rule at `:2139–2141` adds a read replay coordinate only when original and landing `physical_ref` differ. The changed internal child reads correctly rebind through `occurrence:occ-film/shot`; patch entries remain required.

The parent’s revision/digest does change across head movement, but its physical owner remains `parent`:

- original command-0 input: revision `bb8353…`, digest `c0cfd8…`
- landing command-0 input: revision `c32278…`, digest `aa0a3a…`
- original command-1 input: revision `dd4980…`, digest `9de0de…`
- landing command-1 input: revision `36ccd8…`, digest `bb1b0b…`

Those facts are already authenticated by the binding image checks at Runtime `:482–492`; they do not justify fabricating a physical replay successor.

## Minimal owner/hunk

Agent core, `astrid/sdk/timeline/_commit_patch.py:839–853`, in `rebase_patch`.

Only add a read replay-map entry when the rebased value differs from the original `binding["physical_ref"]`. Keep:

- all declared reads;
- all original/landing envelopes;
- all revision, digest, owner, dependency, effect and binding metadata;
- all patch entries;
- the existing six-field private carrier.

No Runtime change, waiver, alias retargeting, byte-equality shortcut, or metadata removal is justified.

## Validation

Offline validation through the unchanged pinned Runtime validator:

```text
CommitRejected
sequential replay binding is duplicated or omitted from the authenticated map
replay_bindings=14
failure_map_key=[0, 'read', 'parent', ['config', 'theme_overrides'], 'batch-read']
expected_map=[five entries]
```

Also passed:

```text
git diff --check
```

No production source or test files were changed. No pytest/full/browser/original-body rerun was performed, per task limits.

Recommended next step: apply the bounded Agent map-index correction, add focused positive/negative controls for unchanged-parent reads versus changed physical reads, then rerun the original helper `[True]` and relevant `[False]` targeted controls.