# P4 show readback: Agent product blocker

Report-only classification completed. No repository changes or test correction.
Exact Agent SHA `98190338b33124668048d0acafb705290ebcada5`, tree
`9c7ea32f8500bbac8d3f411936da661fd06802be`, Runtime pin
`34eac0041b0891e9011966b39bcbd26053fde5bc`.

Service `ap2-P4-runtime-cache-sol-0455-p4-v2-http-nodes-1023050653-17279`
reached the unchanged show predicate after accepted CLI/sheet/canonical/cache/
request/receipt/steps and show success/revision checks. Its retained database
contains actual parent clips `a: 0→5.0`, `b: 0→0`, with placements `[]` and
shots `{}`. The actual accepted revision is
`authoring-parent-revision-3be21afa6e9999e25991ba6664a3b1e9a97dea681e706c7294e3724df544909a`,
canonical digest `sha256:c9945c7370d5f6284286ba8379d4f5f8d9fa5e78a3d1565d1d73205355408d46`.

Offline real CLI handler projection from that saved accepted document yields
`ok: true`, the same revision, `complete: true`, two counted clips, zero cuts,
duration `0.0`, **`rows: []`**. No row representation change can prove `a` at 5.

**Owner Agent:** `astrid/core/timeline/cuts.py:287`
(`occurrences_from_bundle`) ignores `parent.clips`, traversing only placements
and shot internal timelines. Ordinary show selects this cut table at
`astrid/packs/timeline/cli.py:984`; `cli_native.show_native` does not intercept
ordinary show. `cli_show.print_cut_table` loads the exact immutable revision
then `timeline_cuts.build_cut_table` consumes the empty occurrences. Bounded
Runtime inspection is a separate selector/`--layers` path, not the original
command's representation.

Exact-one-node collection, scoped Ruff, private-cache mypy, diff checks and
the minimal offline actual-canonical shape witness all exit 0. The original
positive predicate remains false; this is **not** passing P4 acceptance.
History/publisher/history steps/records and final stored readback after the
failing assertion were not reached in service 17279 and remain unverified.
No HTTP/service/sockets/browser/test body/full suite was run here.

All original positive/production/fixture/request/cache/wrapper/receipt/history/
steps/full physical closure expectations are unchanged. No helper/schema/pin/
generated/lock/launcher/suite/other tests, deletes, dependency writes, Git
mutations, pushes, or delegation. Repo remains clean at the exact base tree.

Agent owner should restore parent-native ordinary show readback, obtain
independent review, then have the manager retry the same single original
central node. Do not rerun the unchanged tree or rewrite the positive test.

Full report, exact commands, outputs and limits:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P4-show-cause-sol-0509/report.md`.
Witness `/tmp/w-b77990b1a4/readback_shape_witness.py`, output
`/tmp/w-b77990b1a4/readback-shape.log`.
