# P4 D141l CLI selector source-only validation

Status: `PASS_SOURCE_AND_TINY_CONTROLS; PRODUCTION_PROFILE_INPUT_MISSING`.

- The live five-second disk trace started before source reads/edits, stayed above the 4,000,000,000-byte stop, and recorded 4,801,536,000 bytes at its minimum sample.
- `check-source.py prepare` generated the production input manifest from current Git/source and environment facts; it did not handwrite product pins.
- `check-source.py check` passed current Agent/Runtime/App/Composition SHA, tree, parent and clean-state checks. App is the qualified `82e9e13d` catch-up head; the expected `8585ed9c` App metadata pointer is retained as D141v documentary metadata only.
- The target test and launcher/installer bytes are unchanged. No product, test, pin, registry, kit, shared environment, Git or service file was changed.
- The candidate row contains exactly one selector, retains `run -- -m pytest`, the later `-m integration`, original timeout/profile environment, disabled cache provider, and all unchanged test predicates. It is a candidate row only; no CAS installation occurred.
- The new input manifest, future run materialization, and actual JUnit destination all name `operational inputs/body-evidence/p4-d141l-cli-selector.xml`. This corrects the historical 0055/10086 stale JUnit-path metadata only in new inputs; historical files remain untouched.
- The unchanged production launcher was exercised in `run` mode against the private tiny profile control: original stub SHA `38afc8a5...` returned 17 and recorded one call. The Agent-SHA-only poison returned nonzero with zero calls. The controls ran no pytest, import collection, service, request-test, row installation or body.
- Product typecheck/lint are not applicable: this worker authored no executable product source.

Finite supported-input gap, recorded exactly: `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.astrid-registry-state.json` is absent. The historical `/home/user/work/runtimes/agent-remotion-v3-819acf-1110` profile is also absent. No receiving problem or future profile was assumed.

Author and reviewer must invoke the same owned check:

```text
/home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P4-D141l-cli-source-host-0825/evidence/check-source.py check
```
