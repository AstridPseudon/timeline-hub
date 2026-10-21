# Agent private15 normal current-owned pin

## Result

Staged one normal owned private Agent consumer descendant from current Main
`6efc81500a0e0688c2bb41e736503f0fc3e04abb` (tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`) against immutable Runtime
`c3d26567ff6fe4e20a959476d40aff90ad23a0ca` (tree
`f3ae49d38454ce73a9c91a954bb530b3ce51c122`). The private Runtime package is
`0.2.15` and remains unpublished; this worktree is staging only.

The Agent schema is byte-identical to Runtime's
`contract/schemas/edit-command.json` at SHA-256
`84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5` and has
59 definitions, 33 closed operations, and 12 explicit v2 clauses. The
approved source floors are preserved by the reviewed ancestry:

- voiceover: `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e`
- groups: `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`
- project-data: `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
- carrier: `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- ordinary: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

The port includes only the frozen 4d semantic source needed for that union:
materialization, project-data, canonical groups, voiceover metadata/lowering,
and occurrence extent lowering, plus the test-only union inventory correction
and the existing private group-bootstrap donor. Current Main safety, restore,
read, Scene, PARAM, rational, and GenericHost changes remain on the current
descendant. Rejected voiceover-helper/outer-host work, future free-multi,
reference/remove/mute/opacity proposals, public/current tuple writes, release,
and integration adoption are excluded.

## Runtime pin proof

`runtime.lock.json` was updated and checked with the normal updater/checker
against `/home/user/work/wt/rt-pin-c3d26567`; it contains the exact full c3
source commit and 15 locked consumer files. Runtime's committed artifact
manifest contains 76 artifacts and version digest
`sha256:2df8ebf4fb17cae1b62e78a262b2b20b393770d045d0ef8748207ac7efacbfbb`.
The distinct Runtime identities are retained: contract metadata schema digest
`sha256:07c0668b2fb16226475429ec65637404c0b2e885e1b88e67f896e249089d6680`,
raw timeline bundle digest
`sha256:bbbae375837456b267d9f0c7de89b962966da79a24abe7c4720301423b333bcb`,
and artifact-manifest version digest above. All 15 consumer bytes match the
producer manifest and lock.

## Verification

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/vendor_lock.py update runtime.lock.json --producer /home/user/work/wt/rt-pin-c3d26567
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-c3d26567
```

The bounded schema/client/vendor lane passed 68 tests, including vendor-lock,
vendored-client parity, composed schema, and current-union checks. The
semantic carrier/provider lane passed 51 tests with 33 deselected, covering
materialization, groups, project-data, voiceover, occurrence resize, and
selected Runtime schema/provider controls. The broader semantic targeted lane
passed 270 tests except for one stale composed-schema fixture assertion; after
adding the required occurrence.resize golden, the focused rerun passed 51/51
and the 68-test vendor/schema rerun passed. `git diff --check` passed.

No full suite, old44/1492 lane, browser/render execution, outer voiceover
execution, release, integration adoption, or public tuple write was run.
