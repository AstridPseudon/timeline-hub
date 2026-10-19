Implemented `authoringBundleFromDocument(document): Promise<AuthoringBundle>` in the three assigned files. Await it during load/ACK before capture. It matches Python’s full bundle/source mapping, preserves `_runtime_document`, and isolates repeated-shot owners with deterministic SHA256 IDs.

Validation passed:

- `npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/authoringBundle.test.ts` — **23 passed**
- `npx eslint src/tools/video-editor/commands/authoringBundle.ts src/tools/video-editor/commands/authoringBundle.test.ts` — passed
- `npx tsc --project /tmp/app-m1-authoring-basis-tsconfig.json --noEmit` — passed using temporary mappings to review-worker exports; config removed
- `git diff --check` — passed
- Python exact check — **5 complete closure/bundle goldens passed**

Recheck goldens from App root; append `--write` to regenerate:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-m1-provider /home/user/work/venv-agent/bin/python -c 'from pathlib import Path; exec(Path("src/tools/video-editor/commands/authoringBundle.test.ts").read_text().split("PYTHON_GOLDEN\n")[1].split("\nPYTHON_GOLDEN")[0])'
```

Preserved Python’s limitation: repeated legacy items using only `id` fail collision validation; Python remaps `item_id` fields only.

Commit message written to the requested path. No full/browser/install run. Next worker must wire and verify exact Runtime initial reads and browser capture integration.