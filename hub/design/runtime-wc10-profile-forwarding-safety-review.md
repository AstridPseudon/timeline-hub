# Runtime WC10 profile-forwarding safety review

## Disposition

**APPROVE — no executable finding in the reviewed change.**

Reviewed exact commit `8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a` on parent
`95bd3c5`. The commit is limited to:

- `astrid_runtime/runtime_boundary.py`: pass the validated product profile as
  `--authoring-profile astrid` on the fixed, default local child launch;
- `tests/test_runtime_boundary.py`: positive forwarding, unmapped-profile
  refusal, and neutral-default controls.

No Agent/source checkout, provider implementation, generated artifact, pin,
publication, or adoption change is part of this commit. The provider seam and
its Runtime infrastructure are pre-existing context, not changes made by this
fix.

## Authority and provider selection

The normal product bootstrap resolves the source manifest and validates it
before calling the boundary (`astrid_runtime/bootstrap.py:801-808`). The
validated Stage-1 source profile must be `astrid`, must use the pinned runtime
checkout, and rejects a non-empty `runtime_command`
(`astrid_runtime/bootstrap.py:138-178,341-361`). Therefore the new mapping at
`astrid_runtime/runtime_boundary.py:258-264` consumes existing source-profile
authority; it does not load a provider from a checkout, accept arbitrary
configuration, or bypass bootstrap validation. An unmapped value fails closed.

The selected Runtime option remains a constrained existing seam: the CLI
accepts only `neutral` or `astrid` and defaults to `neutral`
(`runtime_protocol/cli.py:62`), `RuntimeDaemon` validates the same set
(`runtime_protocol/daemon.py:71-73`), and the provider loader accepts only
the fixed `astrid` choice and imports the fixed
`astrid.sdk.timeline.commit.create_runtime_commit_service` factory
(`runtime_protocol/timeline_commit_provider.py:70-93`). There is no arbitrary
module/provider name in the forwarded argv.

The default branch emits the flag exactly once. Existing custom-command argv
behavior is not changed, and the production source-profile validation rejects
custom runtime commands before this boundary is reached. The existing
`runtime_environment` interpreter selection is retained.

## Roots, custody, activation, credentials, readiness

The change only alters the initial child argv. Before that argv is built,
`LocalRuntimeBoundary.start` still lexically validates and resolves the realm
root, support root, and owner lock, creates the owner-only bootstrap token, and
then invokes `_argv` (`astrid_runtime/runtime_boundary.py:424-452`). After
launch it still waits for the child’s own discovery/health, checks the process
birth identity, and publishes either native custody or the existing retained
macOS broker capability (`:459-477`). No custody wrapper, reaper, signal,
handoff, or cleanup path changed.

The existing Runtime startup loads and validates the selected provider before
Runtime admission, registers it before readiness, and closes the service on
registration failure (`runtime_protocol/daemon.py:235-258`). Credential
provisioning, catalog activation, discovery publication, and readiness remain
downstream of that same startup sequence. The new flag consequently selects
the provider without moving or duplicating any root, custody, activation, or
credential authority.

The direct Runtime CLI and direct `RuntimeDaemon` defaults remain neutral, as
required. This review does not broaden the claim to the separate foreground
`astrid-runtime run` path, which intentionally constructs `RuntimeDaemon`
directly; that path was not changed by this commit.

## Upstream Main comparison and evidence boundary

Compared with upstream Main, the pre-fix local boundary constructed
`python -m runtime_protocol start` without an authoring profile, so the CLI’s
deliberate neutral default dropped the already validated Astrid source
authority. The fix supplies only the missing selection at that process
boundary. The exact commit’s source/test-only scope is confirmed by
`git diff --name-status 95bd3c5..8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a`.

The previously reported qualification evidence was **126 central tests, 7
deselected, plus 3 new controls passing**. Per the review instruction, that
green suite was not repeated here; no full suite was run. The additional
static check `git diff --check 95bd3c5..8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a`
passed.

This is an independent process/custody safety approval only. An actual
production `astrid-runtime up` launch using the installed Agent provider,
followed by authoritative timeline create/read, remains a separate required
proof and is intentionally **not claimed here**. No broad WC10 migration or
legacy-route retirement claim follows from this review.

## Recommended next step

Run the separate normal-launcher provider-backed create/read qualification
against the installed Agent/Runtime pair, then report that evidence
independently before treating WC10 consumer migration or route retirement as
complete.
