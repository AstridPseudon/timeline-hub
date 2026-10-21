# Runtime WC10 installed-fixture landing review

## Disposition

**APPROVE** the installed-launcher prerequisite in candidate `e194c9ea97abd3a9fd0481b917fbf3009f88f9f6` (tree `3f6ddd17e4e264e24b8e780c9a62e70fcdbe412f`). I found no fixture, envelope, custody, isolation, or hidden-product-change concern. This approval qualifies only the launcher prerequisite; the broad WC10 consumer migration and D13 render remain open.

The candidate contains only the new `tests/test_wc10_installed_launcher.py` after the already reviewed `8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a` product change:

```text
git diff --name-status 8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a..e194c9ea97abd3a9fd0481b917fbf3009f88f9f6
A       tests/test_wc10_installed_launcher.py
```

The published normal Runtime/client source `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` and the retained `all76` artifacts were not modified. The pinned Agent source was read-only at `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`; the normal Runtime source was read-only at tree `d3a290b407fa61e6ab2d476f50c068073f70df00`.

## Review findings

- The fixture creates one private venv, copies the approved dependency bytes into that venv, builds Runtime, the normal Runtime client, and Agent from private source copies, then installs all three wheels non-editably with `--no-deps`. The 54 dependency names are explicit and version-pinned from the approved read-only inventory; no shared environment or symlink is used as the installed carrier.
- `_safe_copy` rejects source symlinks, source paths escaping `/home/user/work/venv-agent`, target symlinks, non-file collisions, and differing collision bytes. The isolated preflight checks every expected distribution record, exact product/contract versions, private-site containment, no symlink path components, and imported module origins. The child operation runs with `-I -B` and the child environment removes `PYTHONPATH`.
- The launcher path is the normal installed `astrid-runtime workspace create`, `astrid-runtime up --wait --door-port 0`, `status`, and `down` path. The profile manifest supplies only the installed site-packages carrier and private environment. There is no test-owned provider, monkeypatch, authority override, alternate route, copied credential, or source import override. Authentication reads Runtime's discovered credential JSON and passes its string `token` field to the installed `WorkspaceClient`.
- The operation is provider-backed and reaches the normal project/timeline mutations and canonical reads. It checks exact `{data, receipt}` mutation envelopes, receipt identity and idempotency keys, project/timeline identity, nonempty revision/publication heads, the bootstrap history head, canonical inspection, and the absence of `publish_parent_composition`. The final envelope repair strengthens the prior direct-resource assertions; it does not weaken or delete a behavior assertion.
- Cleanup uses the supported Runtime `down` command only after a successful-start result with a discovery file. It does not delete authority files or claim a false cleanup result; the central proof completed without a leaked daemon.

The new module had only a descriptive title for a deliberately large, non-editable installation fixture. I added a comment-only purpose header in the working descendant of `e194c9e` explaining the approved 54-distribution carrier and the no-checkout/no-shared-write boundary. No code, assertion, threshold, or test flow changed. The descendant is intentionally not presented as a separately executed proof tree.

## Evidence

Reused the orchestrator-provided central run for the exact candidate before the comment-only descendant:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration \
  tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap

1 passed in 31.99s
```

The source-matched central result is `rt-m2-wc10-sdk-envelope-fixture-one-proof-0322-wc10-installed-launcher-integration-1021032335-4406`, tree `3f6ddd17e4e264e24b8e780c9a62e70fcdbe412f`. It is the requested one real socket/process case. The read-only closure discriminator under the approved outer interpreter reported:

```text
declared=54, missing=[], escaped=[], symlinked=[]
```

No full suite, browser, render, unchanged 126-test lane, or second installed-process run was performed. No merge or pin request is made.

