# Handoff — D141jj finite owner-fixture audit

Status: **FAIL_NOT_READY; protected independent review still required.**

The finite defect is the impossible UID65534 `chown` in a namespace with only
UID/GID 0 mapped. The next author may adapt only the private checker fixture:
an allowlisted per-path `lstat` metadata fixture or isolated module proxy. The
real `os.geteuid()` and production `require_directory` implementation must
remain unchanged. Source-owner and stage-owner fixtures must be distinct, and
stage-owner evidence must show real source identity passed before the stage
guard. Direct D68 stage controls and caller `run_wrapper` controls both remain
required.

The stale-upstream case is already corrected and must retain its exact
caller-return/FAIL-diagnostic contract: code 2, caller FAIL receipt, exact D68
reason, empty repos/stage, and unchanged builder marker. Do not replace it with
exception-only or no-receipt evidence.

Remaining unverified caller cases: wrong source owner, wrong source mode, wrong
stage mode, wrong stage owner, wrong App base, wrong App tree, dirty source,
symlink source, and source-ref drift; plus both direct stage controls and the
direct authorized App-tree control. No semantic PASS is inferred from the
prior stop. Installation and product merge remain out of scope.
