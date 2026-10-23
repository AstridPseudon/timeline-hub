# Runtime OPS-D21b Remotion reuse — first return

Status: private staged evidence packet; not installed, merged, published, or
qualified against a production dispatcher/daemon.

The flat packet is:

- `handoff-runtime-OPS-D21b-remotion-reuse-return-1811-make-runtime.sh`
- `handoff-runtime-OPS-D21b-remotion-reuse-return-1811-request-runtime.sh`
- the two matching `.patch` files;
- `handoff-runtime-OPS-D21b-remotion-reuse-return-1811-hashmanifest.txt`;
- `handoff-runtime-OPS-D21b-remotion-reuse-return-1811-cmp.txt`.

Fixes over the failed 1753 packet:

1. `make-runtime` requires explicit private ORCH/work roots and performs the
   exact Node `20.19.4` / npm `10.8.2` executable check before scanning any
   reusable graph. `/does/not/exist` is refused and cannot be registered.
2. A retained build-origin Agent SHA must be an actual commit in the supplied
   clean Agent checkout. Its committed `remotion/` tree and package source
   bytes must match the requested authenticated tree/lock; a regex-shaped
   marker such as `111...` is refused.
3. Reuse registration preserves `ASTRID_BUILD_ORIGIN_AGENT_COMMIT` while
   binding the selected Node executable, template/profile, requested Agent SHA,
   and requested Runtime SHA into the generated env and suite command.
4. Reuse remains keyed by the authenticated Remotion tree. A marker mutation
   that the authenticated origin proves belongs to the requested tree refuses;
   an actually different source tree takes the normal build branch. The private
   build mock stops that branch before installer/network work.
5. The fixture matrix covers tampered bytes, manifest, origin, tree, lock,
   engine, profile/template, writable/dirty graph, partial graph, ambiguity,
   missing executable, changed tree, root omission, and old 2/3/new 7 argument
   request forms under `env -i`.

Read-only real-layout inventory found `/home/user/work/runtimes/agent-remotion`,
`agent-remotion-0013`, and `agent-remotion-current`, plus two partial graphs.
They have the older registry/source layout and no authenticated D21b source,
receipt, or manifest markers. They remain future-only and were not upgraded,
rewritten, or treated as reusable.

Evidence is intentionally limited to private fixtures and staged scripts. No
production queue entry, host tool, daemon, provisioner, network build, package
install, Runtime product file, generated file, retirement/child file, or
integration worktree was changed. The general C0 v2 timeline request/reply
contract and frozen34e product behavior were not exercised by this builder-only
packet and remain unverified here.

One intermediate development run exposed a fixture bug in the tree-marker
guard and entered the normal build path in a private temporary directory; npm
failed before an install completed. The final guard and matrix prevent that
path for tampered same-tree markers; no shared or production path was used.
