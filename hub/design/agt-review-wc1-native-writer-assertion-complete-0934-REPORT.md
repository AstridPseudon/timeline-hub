# WC1 native-writer assertion/data-safety review

Date: 2026-10-21 UTC

## Verdict

**APPROVE unchanged bounded candidate**

- Candidate: `c7e392f19b6e6b186c632ed050d8ea6e73b55a34`
- Candidate tree: `d6aba756208419b9bdfa17e11c7b08710ad5399c`
- Parent: `8cad2a95b705862e4d8c6578780cf92a5ed1cc2b`
- Parent tree: `d0d0edc5e72a081ef5dc4676ad8130c470b98ccc`

This is a one-file test-only repair. It does not change product code,
fixture authority, Runtime pins, transport, or the native command path.

## Source/data-safety review

The diagnosis inventory records 39 requests per HTTP scope, for both
`parent` and `occurrence:occ-a`:

| Requests per scope | Method/path class | Disposition |
|---:|---|---|
| 2 | `GET /v1/health` | transport control read |
| 2 | `POST /v1/handshake` | authentication control |
| 12 | `GET /v1/projects/{p}/timelines?limit=50` | canonical timeline reads |
| 3 | `GET .../commits?...` | accepted-history reads |
| 6 | `POST .../inspect` | canonical inspection reads |
| 3 | `GET .../composition-revisions/{revision}` | legitimate immutable revision reads |
| 3 | `GET .../shots/{id}/revisions/{revision}` | legitimate immutable child reads |
| 3 | `GET .../timelines/{id}/revisions/{revision}` | legitimate immutable child reads |
| 2 | `GET .../media-selection/verified?...` | legitimate immutable media reads |
| 3 | `POST .../commit` | native product writes, including retry and inverse |
| **39** |  | **no legacy composition/publish write** |

The fixture's `publish_parent_composition` runs before the HTTP observer
records product traffic. The corrected phase field preserves that boundary;
it does not relabel a fixture request as product traffic.

The helper uses the actual method and path from each recorded tuple. It does
not normalize methods, rewrite paths, or drop rows. Its method set is exactly
`POST`, `PUT`, `PATCH`, and `DELETE`; its path test is limited to the two
legacy writer suffixes; and its phase test is exactly `product`. The added
positive assertion requires the concrete accepted immutable revision GET.

The planted negative invokes `legacy_composition_writes` itself and includes a
fixture-phase writer plus a product-phase immutable GET as controls. A
read-only AST probe loaded that exact helper from the candidate commit and
checked all eight mutating method/path combinations. It detected all eight,
left the input tuples byte-for-byte unchanged, and ignored the fixture write,
immutable GET, and native `/commit` control.

The c7 diff against 8cad is limited to the request observer, phase marking,
the exact immutable-GET positive, the write-only checker, and its planted
control. The original request key/body/base/media/guard assertions, outbox
flight identity, restart, receipt, reload, inverse/undo, opaque fields,
sibling/rebase, and both parent/occurrence parameter scopes remain unchanged.

The shared fixture caller remains covered. The restored OLD identity block in
8cad still applies to both `internal['payload']` and `parent`, and to
`internal['payload']['clips']`, `parent['clips']`, and
`parent['config']['clips']`; it preserves the old asset alias,
`generationId`, and `variantId`. No fixture caller or scope was removed by
c7.

## Checks and evidence

Passed:

- `git diff --check c7e392f19^ c7e392f19`
- Exact-candidate compact checker probe via `git show c7e392f19:<path>` and
  `/home/user/work/venv-agent/bin/python -B`: **8 forbidden product rows
  detected unchanged; immutable GET/commit/fixture controls ignored**.
- Candidate diff shape: **34 additions, 3 removals**, one test file.

Prior worker evidence, retained but not used as exact-candidate qualification:

- Central named HTTP lane: **2 passed in 9.16s**.
- Its snapshot was requested before c7 was committed and reported a different
  source tree (`444e09d77f...`), so this review does not relabel it as a run of
  exact tree `d6aba756...`. No duplicate HTTP/body/native/full/render/browser
  or install run was made.

## Recommendation / limits

Accept the unchanged candidate into the review chain. Keep the prior central
run labeled unqualified for exact-c7 provenance; the source review and compact
checker are the evidence for this approval. No blockers found in the assigned
assertion/data-safety scope.
