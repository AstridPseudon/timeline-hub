# Runtime PUBLIC018 normal consumer handoff

**Operational status: HOLD.** The independent final generator/release review
is complete and records **APPROVE**, but this note does not authorize a pin,
publication, merge, or App activation. The Runtime manager makes that
coordinated decision.

## Exact candidate tuple

| Field | Value |
| --- | --- |
| Runtime producer commit / tree | `8ed79a31e66d02e2e2e7062b9a368e3266cea9db` / `f52aa1456fc6b65a7c634d4876aa4d6adfd9f822` |
| Candidate parent | `d6d21d8d305549c9b0f8540be994bba974e93204` |
| Contract/client version | `0.2.18` (Python and TypeScript client metadata agree) |
| Health/handshake schema digest | `sha256:1ee82d1d95d9b5006786180560c8b9cc4feab2221e72252a2b14c2043d957c03` |
| Canonical Agent command schema | `contract/schemas/edit-command.json`, `sha256:9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a`; 55 definitions / 29 clauses |
| Raw Runtime commit bundle | `runtime_protocol/schemas/timeline-commit-bundle.json`, `sha256:5eb9775e2c46ab08a41d1e3044632854354f021efd0f48ea960f082524c0bb4c` |
| Artifact manifest | 76 artifacts; manifest version/digest `sha256:afd65ccf54aa1c27fac95840235d50fa93da0e951b2b03adceaf47d391cd996c` |
| `contract/artifacts.json` file digest | `sha256:84f93ced825c6384c55e7c29611e44451dc9e7719c19108c36a9c68509bd0174` |

The generation source is the exact ordinary Agent producer
`0cfa4ad14664cec9df430637d8f68f2d1f2b487f`, tree
`01561fcefb61db6ad70b3cf2f31a778701f8db5e`, and
`astrid/core/timeline/schema/edit-command.schema.json` has the canonical schema
digest above. Private017 is not an input.

## Existing evidence

No tests are repeated for this handoff. The existing records are:

- The pre-repair targeted command in
  `tests/rt-m2-public018-normal-generate-interim-1153-targeted-1021115709-2858/summary`
  ran the documented contract/client/door/Document selection and retained
  `140 passed, 2 deselected, 3 errors`; the errors were the known generator
  crash and are historical, not a current qualification claim. Its exact
  command was:

  ```text
  /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_client_release.py tests/test_client_parity.py tests/test_timeline_commit_contract.py tests/test_timeline_current_union_contract.py tests/test_timeline_commit_provider.py tests/test_timeline_ordinary_http.py::test_ordinary_http_empty_bootstrap_must_be_reachable tests/test_timeline_fresh_bootstrap_scope.py::test_real_provider_fresh_create_uses_normal_bootstrap tests/test_transcript_documents.py tests/test_timeline_document_object_contract.py
  ```
- The author generator-fix report at
  `workers/rt-m2-public018-boolean-schema-generator-fix-1200/report.md`
  records the focused generator regression command below with **6 passed**,
  normal generation/conformance/manifest checks and `git diff --check`
  passing. The corrected Document-object command below had **22 passed**. The
  central command/result is retained at
  `tests/rt-m2-public018-boolean-schema-generator-fix-1200-targeted-1021120308-17185/summary`.

  ```text
  /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_type_generator.py
  /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_document_object_contract.py
  ```
- The completed independent review at
  `design/runtime-public018-final-generator-release-review-1206.md` records
  **APPROVE** after checking the exact candidate, generator `--check`,
  TypeScript conformance `--check`, artifact-manifest `--check`, 76-artifact
  reproducibility, generated-client checks, and `git diff --check`. It did not
  run full, HTTP, browser, live-socket, renderer, native, keeper, or real
  journey suites.

The generator repair only makes JSON-Schema boolean subschemas render as
impossible (`Never`/`never`) or unconstrained (`Any`/`unknown`); it does not
change the canonical schema bytes.

## Consumer-visible boundary

PUBLIC018 carries the existing `clip.set` transition values and the optional,
derived `Document.content_digest`. The digest is produced by Runtime’s
canonical document-content path. Consumers must accept that old accepted
results and old ledger-first replays can omit it; no consumer may compute or
substitute its own authority digest. No live App adapter activates from this
handoff. Public014 and Private017 remain immutable.

The handoff contains no keeper or frozen packet as an interim merge gate.

## Normal updater/checker inputs

After the manager supplies a clean Runtime producer checkout, use the real
producer HEAD below. The normal updater requires each consumer lock’s
`source_commit` selector to be set to the exact Runtime commit first; the
updater does not select a different commit.

```sh
RUNTIME_PRODUCER=/path/to/clean/runtime-checkout
test "$(git -C "$RUNTIME_PRODUCER" rev-parse HEAD)" = 8ed79a31e66d02e2e2e7062b9a368e3266cea9db
test "$(git -C "$RUNTIME_PRODUCER" rev-parse HEAD^{tree})" = f52aa1456fc6b65a7c634d4876aa4d6adfd9f822
```

Agent, from its checkout after the normal lock selector is coordinated:

```sh
cd /home/user/work/agent
python scripts/vendor_lock.py update runtime.lock.json --producer "$RUNTIME_PRODUCER"
python scripts/vendor_lock.py check runtime.lock.json --producer "$RUNTIME_PRODUCER"
```

App, from its checkout after the normal lock selector is coordinated:

```sh
cd /home/user/work/app
node scripts/vendor-lock.mjs update runtime.lock.json --producer "$RUNTIME_PRODUCER"
node scripts/vendor-lock.mjs check runtime.lock.json --producer "$RUNTIME_PRODUCER"
```

These are updater/checker inputs only. They do not activate a live App adapter
or authorize publication. The manager requests an exact producer checkout only
if one of the normal tools needs it.
