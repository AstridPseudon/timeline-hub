# Validation

- Checker hash first: `sha256sum scripts/testing/check-d141j-visibility.mjs` = `bd5feadba07f6cdec3afa4d12baa3008cfd9bd012fdb9db6895d34e3db5baa27`; `git hash-object` = `9f99bf3de96a5885fd419324e7709061bf98b692`.
- Full touched file, pinned Node 20.19.4, private `--no-cache`: `.../node --max-old-space-size=6144 node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx`; exit 0, 1 file, 13/13 passed.
- Independent retained artifact: `.../node scripts/testing/check-d141j-visibility.mjs .../evidence/visibility-proof.json`; exit 0, status PASS, readCount 2, heads `timeline-rev-2` then `timeline-rev-3`.
- Independent stale artifact: same checker against `.../evidence/stale-artifact.json`; exit 1, `active occurrences is not uniquely correlated to accepted-read-2`.
- Focused control: selected test passed, but exit 1 because the repository skip guard reported 12 undeclared filtered skips; not used as acceptance evidence.
- Scoped ESLint over the six changed source/checker paths with `--report-unused-disable-directives --max-warnings 0`: exit 0.
- Locked App TypeScript check with `flock -w 600 /home/user/work/.app-tsc.lock ... tsc --noEmit --incremental false -p tsconfig.app.json --pretty false`: exit 0.
- Locked Node TypeScript check with the same flock and `tsconfig.node.json`: exit 0.
- `git diff --check 82e9e13ddf1d7ec6c736521b2eb091dca9877598..HEAD`: exit 0.

Warnings observed in the full test are existing React `act(...)` warnings and
the stale-control checker stack printed by the deliberate refusal assertion;
the test still passed. No full suite, browser/native journey, service,
package installation, test-service request, diagnostic body, or historical
27026 replay was run.
