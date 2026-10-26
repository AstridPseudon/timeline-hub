# F D141jj handoff

The exact failed log is preserved by commit `ce9e0532a71489e39a0d339e0f9d399a12a39090`:
`evidence/tmp/check_jj-positive.log`. It shows positive caller/D68 PASS,
then `delivery trace already exists` at the stale-nonapp-upstream refusal and
the assertion at `check_jj.py:448`.

Author action: change only the private derivative checker. Allocate a fresh
service TMP root per caller invocation, preserving explicit stage fixtures;
also make the checker observe nonzero caller returns as refusals, otherwise
the stale guard remains unobservable after the collision is fixed. Preserve
all positive, SAME33, and negative assertions and do not rerun or modify
production source. This handoff is not a qualification verdict.

