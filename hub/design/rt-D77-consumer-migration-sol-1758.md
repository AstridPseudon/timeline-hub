Implemented the D77 consumer migration on exact baseline `2a1637a`. Bootstrap and strict Remotion validation now consume the selected Agent’s Runtime-pinned canonical JSON. Origin, ownership, digest, reference, closure, inventory and mutation checks remain enforced. Backend b4 behavior, schema `4d74…deb3`, contract `867f…708b`, commit/history code and artifacts are unchanged.

Validation:

- **Old RED:** staged-bootstrap control failed because no schema environment was supplied.
- **New GREEN:** **228 targeted cases passed**, zero failures/errors/skips.
- Ruff: 19 inherited findings before/after; **zero new**.
- Mypy: 24 inherited findings before/after; **zero new**.
- Compile and `git diff --check`: PASS.
- Final-run comparison: **197 shared dependency files unchanged**.

Exact commands, XML, logs, selected test memberships, protected-assertion mapping and source hashes are retained in [evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D77-consumer-migration-sol-1758/evidence/commands.txt>). Commit message and empty `DONE` were written. No Git mutations or heavy gates were run.

The historical environment variable now names the canonical JSON **file**. Model equivalence uses the existing canonical reader and standards validator; the external exports were TypedDicts. No replacement models were introduced.

**Required before merge:** independent security/core review. Both review-spawn attempts failed with `invalid thread-store request: no rollout found`; no independent PASS is claimed. Upstream runtime outcome remains **UNKNOWN**, and installed-render readiness remains unverified.

The next bounded seam is [the D13 fixture environment](/home/user/work/wt/rt-D77-consumer-migration-sol-1758/tests/packs/video_editing/test_runtime_publication_chain.py:619):

```diff
- "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": str(source),
+ "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": str(source / "astrid/core/timeline/schema/timeline-config.schema.json"),
```

After review and that protected-fixture adaptation, use these existing selectors through the central service:

```text
tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

They require the authentic installed source profile, exact seven-key expected-bindings JSON, and pinned Node/Remotion/browser/FFmpeg/ffprobe inputs plus node_modules. The unchanged service path is `Backend.stage → service_declaration → generic_host --service → services.main → run_pack_host_foreground → ensure_pack_host`; preflight and worker validation consume the migrated schema binding. Denied acquisition remains stopped.