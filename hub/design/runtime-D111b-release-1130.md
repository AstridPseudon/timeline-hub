# Runtime D111b normal release

RELEASED at `2026-10-25T11:25:50Z` from normal Runtime `7070f1378d1917fcce69857ebd33cd2b3015568b` (`7070f1378`), tree `cd68015cb9fe85a6ecd2d15dd7e2eac69f67e2b1`.

The normal merge tree is exactly the independently reviewed `f0c4d6d2b66bb84e935b9008853fcb628746fe88` tree. The worktree was clean before and after qualification. The queue receipt is `merged tl/rt-D111b-closure-growth-sol-1115 into runtime tl/integration -> 7070f1378`.

The required actual-normal integrated smoke passed all 9 cases with exit 0 in 15.89s. Durable XML is at `workers/rt-D111b-normal-release-1130/evidence/integrated.xml` (SHA-256 `7cdbf4afb9550f527987c522c582efd72db5761ce46bbd8ed1eb6db8f5dbf9b3`); the only output warning is pytest's `record_property`/xunit2 compatibility warning. Compile and `git diff --check` passed. All 15 canonical client/schema paths are byte-equal to `42aad0e9`; the independent 1122 static review was reused and no typecheck was repeated.

Native scope is honest and bounded: the actual author result `10398` passed the one existing acceptance case at `1.448x` (`84.715ms -> 122.704ms`) under the unchanged `1.5x` gate. The prior `1.971x` failure and noisy `190.000671ms` middle interval remain retained. No broader source-bearing performance claim is made. The captured-transcript auth failure `[None-True]` was parent-identical and was not rerun or fixed.

Only the reviewed Runtime source/test delta is present relative to `42aad0e9`: the port, store, and the two reviewed ancestry/closure regression tests. No private diagnostic or evidence artifact was imported. This release does not claim full-suite, full-core, P2 GO, original-element, browser/live-socket, cut/build, or ZIP qualification.

See the machine-readable receipt in `runtime-D111b-release-1130.json` and the durable evidence under the worker directory.
