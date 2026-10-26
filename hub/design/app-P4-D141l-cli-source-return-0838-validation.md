# P4 D141l CLI source-coordinate return

Verdict: `SOURCE_PASS / PRODUCTION_PROFILE_INPUT_MISSING`.

- Stable detached source pins were verified clean with exact full commit, tree, and parent tuples: Agent `ecdc242e`, Runtime `95d98f03`, App `82e9e13d`, Composition `635f4de0`.
- The new owned checker was run exactly as requested:
  `/home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P4-D141l-cli-source-return-0838/evidence/check-source.py prepare`
  and then `.../check-source.py check`; both exited `0`.
- Checker output: current tuple/clean/detached/target unchanged PASS; positive harmless launcher control exit `17`, stub calls `1`; Agent-SHA poison nonzero (exit `1`), stub calls `0`.
- Static checks passed: Python AST, shell syntax for the stub and launcher, and `git diff --check` for this and all four stable source worktrees.
- The candidate row has one unchanged selector and retains the normal launcher, restricted environment, `run -- -m pytest`, integration marker, timeout `45`, disabled cache provider, and one durable prospective JUnit path.
- The production source manifest is separate from future body evidence. The supported production registry state is absent at `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.astrid-registry-state.json`; the historical profile `/home/user/work/runtimes/agent-remotion-v3-819acf-1110` is also absent. No profile, registry, body, JUnit, pytest collection, service request, install, CAS, queue, or permission bypass was attempted.
- The tiny stub exits `17` by design and does not emit JUnit; this is not a pytest pass and no behavioral P4 credit is claimed.
- Product typecheck/lint are not applicable: this return changes operational metadata/checker source only, with no product source, tests, pins, or profiles changed.

The only repaired dependency is the source coordinate: NEW manifests/row/checker use the four stable pin paths. Historical author/reviewer originals remain immutable.
