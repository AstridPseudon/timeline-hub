# Runtime handoff: OPS-retire-runtime-1753

Private evidence packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-runtime-1753`.

The packet layers runtime retirement onto the reviewed v2 request route:

```text
request-retire-venv agent-remotion-<lowercase-suffix>
  -> queue/pending/retire-venv-agent-remotion-<...>
  -> RETIREVENV agent-remotion-<...>
  -> retire-child-venv <...>
```

The runtime grammar is the maker grammar `agent-remotion-[0-9a-z][0-9a-z-]*`. The target must be a stale direct canonical child of `$WORK_ROOT/runtimes`; `agent-remotion-current` is protected. Known make-runtime immutable markers are validated when present, package/lock layout is required, and `.partial.XXXXXXXX` failed-staging leftovers are considered only as exact associated components. Existing v2 child-venv/source behavior is retained.

The installed dispatcher is byte-identical (`f18bc20b...`). Worker packet hashes and installed comparisons are in `evidence/hashmanifest.txt`; exact executable exports and installed diffs are in `evidence/*.{sh,patch}`. Fresh private evidence is recorded in `report.md` and the per-command logs: v2 17/17, adapted 37/37 and 7/7, runtime 13/13, extra 8/8, and venv/runtime FIFO request→dispatcher→handler smoke 5/5 under normal and `env -i` environments.

No host install, production cleanup, actual main/remote runtime deletion, or Runtime repository change was performed. Required next step is independent HOST idle/smoke/UTC-backup/atomic-install/normal-publication qualification before Proof uses the syntax above.
