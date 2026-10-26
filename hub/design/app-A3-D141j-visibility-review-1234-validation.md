# Validation

- `sha256sum scripts/testing/check-d141j-visibility.mjs` and `git hash-object scripts/testing/check-d141j-visibility.mjs`: PASS; hash `49678b45252a5a1163a57ae990af57baf81e653cc300d70a1926ea84741f8fe7`, blob `9da3fbaeca584c9803b62e27865853831d9784b3`.
- Focused pinned Node/Vitest command with `D141J_VISIBILITY_ARTIFACT_PATH=.../review-retained-artifact.json`: selected test passed; process exit 1 because the repository wrapper reports 11 undeclared filtered skips.
- `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node scripts/testing/check-d141j-visibility.mjs .../review-retained-artifact.json`: PASS.
- Full touched `TimelineEditorCore.test.tsx` with pinned Node/Vitest and `--no-cache`: PASS, 12/12.
- Scoped ESLint command from author validation: PASS.
- Locked App typecheck (`tsconfig.app.json`): PASS.
- Locked Node typecheck (`tsconfig.node.json`): PASS.
- `git diff --check 82e9e13ddf1d7ec6c736521b2eb091dca9877598..HEAD; git diff --check`: PASS.
- Malformed control artifact with no events: checker refused it with `Error: missing accepted read event`, exit 1.

No full suite, browser/native journey, service, package install, diagnostic body,
or test-service request was run.
