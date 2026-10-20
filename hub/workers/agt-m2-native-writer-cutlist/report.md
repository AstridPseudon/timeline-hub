Implemented the read-only M2 cutlist in [agent-native-writer-cutlist.md](/home/user/work/wt/agt-m2-native-writer-cutlist/docs/design/agent-native-writer-cutlist.md).

- Mapped WC1–WC10 and live checkout/publish/narration/CLI/sheet/script callers.
- Documented exact native replacements, missing primitives, held unsupported behavior, timing gaps, and in-flight dependencies.
- Identified five next writer-removal source tasks with existing positive test paths.
- No product, test, ledger, branch, or shared dependency changes.

Tests:

```text
304 passed in 54.11s
```

Also ran `git diff --check`. No full suite was run.

Created the external report, conventional commit message, and `DONE` marker.