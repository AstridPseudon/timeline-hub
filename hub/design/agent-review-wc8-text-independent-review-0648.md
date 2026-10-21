# WC8 literal text independent review

**Verdict: APPROVE**

Reviewed exact Agent `c723cbbd8ee51dde0a507cefd5a61ff62c957107`, tree
`1bb8c44a8e93ae74ea8bef2771e553db351df5c3`, as the bounded combined WC8 delta
from hub base `18a89a0d29766bd3cec31391042836ba7c951fa1` through retained-basis
commit `f4ddce5cc204e6d4b0695fb4f869697be192320a` plus the literal callback fix.

The candidate changes exactly three existing files: `astrid/sdk/timeline_sheet.py`,
`tests/sdk/test_timeline_sheet_native.py`, and
`tests/editing_conformance/test_native_sheet_ordinary_runtime.py`. The
retained translator uses the exported artifact's row binding and bundle, keeps
the original basis, and refuses unsupported/mixed grammar before staging. The
fix changes `re.subn` to a literal callback, so JSON-encoded backslashes,
newline escapes, `\\1`, quotes, non-ASCII, and empty strings are preserved.

The current014 HTTP proof asserts exact command capture, retained revision and
publication basis, normal `{"via":"sheet"}` request source, exact value after
commit and restart, opaque-field and sibling preservation, and guarded inverse
/ redo. Existing offline neighbors cover target identity, unbound/mixed grammar
refusal, exact retry without recapture, and draft/outbox preservation.

Reused evidence: focused regression `2 passed, 1 failed` before the fix;
focused text lane **3 passed**; 114 neighboring tests **passed**; central exact
current014 node command
`env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-current ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-current/node_modules /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_text_literal_uses_native_http_and_guarded_inverse`
**passed in 4.37s** on tree `1bb8c44a8e93ae74ea8bef2771e553db351df5c3`; `git diff --check` passed. No
full/browser/render/install/native-socket/old-duration-matrix run is claimed.
No counterexample found; no tests removed/skipped/xfail-weakened, new
schema/pin/authority, or unrelated blob changes found.

