# F D141l native whole-path second-failure investigation

Verdict: `FAIL_FINITE`, with five intrinsic native-route findings in
`findings.md`. The principal new failure is that `set -e` stops at a failed cut
before `dispatch_phase pristine`; direct controller `test-run` also races the
queued dispatcher. The required current Composition base is verified as
`6a2d1c2` / tree `57f68e1f`; the earlier 0820 packet’s `5ab5191a` Composition
tree is not used.

No source repair or semantic review round was performed. No request-test,
test-run, wait-test, dispatcher admission, CAS/registry write, service/body,
receipt admission, product import, install, or suite was run. The 45 private
historical/control inputs and pristine/toolchain paths are absent on App and
are reported as transport limits, not reconstructed.

The existing supported next route is: the owner/controller performs one
native `request-test` queue admission, lets the dispatcher own `test-run`,
waits with `wait-test`, captures the returned service directory and
authenticated terminal/launcher artifacts, then runs the pristine comparator
only after a terminal cut result (including a failed cut if the controller is
explicitly designed to retain both outcomes). No new schema, direct `--run`,
row-install interface, floor, guard, launcher, approval gate, or C0 change is
authorized by this report.

