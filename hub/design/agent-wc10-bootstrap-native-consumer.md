# WC10 bootstrap native consumer report

Status: blocked; no repository changes were retained.

## Caller list and cut

- `astrid/sdk/remote.py:482-551` remains the only Agent product caller in
  scope.
- The direct legacy call remains at `astrid/sdk/remote.py:536`.
- No caller was cut: the attempted native migration was reverted after the
  required real-daemon qualification failed, so the original behavior is not
  left red in the worktree.

## Qualification result

Requested named suite:

```text
main95bd-real-fixture-qualification
```

It ran the six existing normal95 qualification nodes plus:

```text
tests/stage1/test_runtime_client_cutover.py::test_empty_timeline_opens_as_composition_on_real_daemon
tests/editing_conformance/test_commit_runtime_first_clip.py::test_empty_bootstrap_first_clip_client_commit_exact_reload_inverse_redo
```

Result: `1 failed, 13 passed in 59.00s`.

The failing node was `test_empty_timeline_opens_as_composition_on_real_daemon`.
The attempted native consumer returned a validation error while opening the
new timeline: `could not open timeline 'main-timeline' ... composition
revision`. The first-clip native positive passed in the same run.

Local targeted evidence after reverting the attempt:

```text
PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/v10/test_timelines_create.py tests/editing_conformance/test_pristine_initialize.py tests/sdk/test_timeline_sync_native.py
66 passed in 2.53s
```

The worktree is clean and `git diff --check` is clean.

## Precise seam

`TimelineSession.open` resolves the timeline through the canonical read path
before `timeline.init` can be captured. Its bundle read goes through native
inspection and the immutable parent-revision read. Runtime's `create_timeline`
only installs the authenticated bootstrap when its timeline commit provider is
registered (`runtime_protocol/service.py`'s provider-gated bootstrap branch).
The failing stage1 daemon uses the default `real_runtime()` setup, while the
passing first-clip node explicitly starts with `authoring_profile='astrid'`.

Therefore the default normal95 daemon leaves this create consumer with a
headless shell and no native bootstrap authority. A client-side synthetic
bundle, a recursive open, or a legacy/whole-document fallback would violate
the WC10 constraints and would not preserve canonical source/CAS/history
authority. The existing foundation needs provider-backed bootstrap authority
in the daemon (or an existing authoritative bootstrap read seam) before this
consumer can be migrated.

## Recommended next step

Qualify the default normal95 daemon with the native timeline commit provider
and authoritative bootstrap read enabled, then rerun only the two named
bootstrap positives and add the direct/no-legacy proof. Once that seam is
available, migrate `remote.py:482-551` through `TimelineSession` and
`timeline.init`, retaining the existing shell/head idempotency and receipt
contract. No generated clients, schema, pin, or Runtime writer changes were
made here.
