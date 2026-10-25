# U2 D108 protected Windows source review

Verdict: **PASS_SOURCE**.

This is an independent protected source review of
`tl/agt-U2-D108-windows-restore-0742` commit
`2efa4dccf9fd09f67617933a2f42e116290cf0b0`, against captured normal
`b943270a9ed42bb968dbaeace7b296d9898ea21b` and fresh upstream
`08e6b905114a3ee2b05c3e7980421f26b4abf15c`.

The author commit has the exact requested delta: only
`tests/test_installer_windows_tasks.py`, 40 insertions and no deletions. The
three added imports are `uuid`, `from astrid.installer import service`, and
`from astrid.installer.core import Version`. The incoming
`test_register_scheduled_task_accepts_rendered_xml_string` function is
source- and AST-identical to fresh upstream, with exact source SHA-256
`deb4ceb835cb0cfcc3ad596214293b7cdc68356cf35d5e4c2cf2b63a1f52797d` and AST
SHA-256 `6f0d6ccd52104dbad4df30a247aa1ab1b4bd4bcad7906dd2b4743b7be845de17`.
It has exact parameters `(tmp_path, monkeypatch)` and no decorators.

The existing `test_task_cleanup_preserves_powershell_success_and_failure`
function is source- and AST-identical to the captured parent, with exact source
SHA-256 `277c9825fd2c69ee415d6f16650ac92a4037472792fcd954feb978f35c239120`
and AST SHA-256
`1b58e4eff0c2251b12ad5767b471d43c254e38499c84a98333c6fcfecd2146ce`.
Its parameters and both parametrization decorators remain unchanged. The
module marker remains exactly `pytest.mark.windows_installer`; no skip claim or
scope guard was added.

The restored body matches the settled D108 proposal exactly: UTF-8 XML is
written and checked for `<Task ` with no XML declaration; two enabled elements
are replaced with `false`; the current `service.TASK` and filtered
`service.TASK_QUERY` are monkeypatched; the current `Service`/`Version`
constructors and `register`, `powershell`, and `unregister` callers are used;
the Task Scheduler query uses `-ErrorAction Stop`; cleanup is guaranteed in a
`finally` block. Static inspection found the current signatures and installer
data valid. Both the incoming registration and current cleanup test sets are
preserved. No production, pin, generated, ledger, or unrelated test/source
file changed; the captured full-core tuple is untouched.

Checks passed:

- in-memory AST parse and compile for author and fresh source;
- scoped venv-agent Ruff for parent and exact candidate source, no diagnostics;
- scoped venv-agent mypy for parent and exact candidate source, no diagnostics;
- `git diff --check 2efa4dccf9^ 2efa4dccf9`.

No pytest, import/collection, helper or fixture execution, installer service
execution, or actual Windows behavior was run. This is source qualification
only. It does not claim functional Windows PASS or installer coverage closure;
those remain pending normal merge and qualified F-final Windows proof.

Detailed command output and hashes are in
`workers/agt-U2-D108-windows-review-0745/evidence/static-source-review.md`.
