# Agent WC8 literal text current landing

## Decision

The WC8 literal text slice is ready for the harness's two-parent merge
preparation. The intended parents are:

- first: `c723cbbd8ee51dde0a507cefd5a61ff62c957107`
- merge parent: `345085a511d05bc136672de1ff7236f2284bfb84`

Their common ancestor is `18a89a0d29766bd3cec31391042836ba7c951fa1`.

The current-forward resolution applies only the hub's upstream delta: the
five-line `tests/sdk/test_timeline_commit_provider.py` Runtime-platform test
harness change. The exact three WC8 c723 blobs are preserved:

```text
d1763a047ed88318c490bfd714784ea7df7713be  astrid/sdk/timeline_sheet.py
3a32036821f707eddf49b6a522e02d6fa928db5d  tests/editing_conformance/test_native_sheet_ordinary_runtime.py
4f14e3cab5424bf84edab5fd1cd8377bf0894c14  tests/sdk/test_timeline_sheet_native.py
```

The provider blob is exact hub345:

```text
55c082c2547dfd1da306c1a0d32a506d2f3faf82  tests/sdk/test_timeline_commit_provider.py
```

Thus f4dd's detached-text translator and c723's literal callback remain
together. No schema/op/pin/lock/release/native/render/body delta is present;
caption39dd, private016, whole-mixed, and new-source work are not included.

## Safety and preservation

The manager independent review approved c723/tree1bb8 at
`design/agent-review-wc8-text-independent-review-0648.md`. It found no
data-loss, retry, scope, authority, or unsupported-edit counterexample and
approved the retained basis, literal escaping, sibling isolation, restart,
inverse/redo, and mixed-grammar refusal behavior.

The exact central current014 HTTP proof on c723/tree1bb8 remains valid and was
not duplicated: **1 passed in 4.37s**. The current duration 142 and HTTP3
assertions remain through the exact hub provider blob; all other current hub
content (including kernel/custody/cache/document adapter/source origins,
published95, all76, and C13) is inherited byte-for-byte.

## Verification

```text
114 passed in 13.15s
  tests/sdk/test_timeline_sheet_native.py
  tests/editing_conformance/test_native_sheet_current.py
  tests/editing_conformance/test_native_sheet_ordinary.py

111 passed in 21.17s
  tests/sdk/test_timeline_commit_provider.py
  (with ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime)

ruff check tests/sdk/test_timeline_commit_provider.py: All checks passed!
git diff --check: PASS
```

No full/browser/render/install/native-socket/duplicate-HTTP20600 run was made.
The harness still needs to create the actual merge commit; this worker did not
perform Git mutation.
