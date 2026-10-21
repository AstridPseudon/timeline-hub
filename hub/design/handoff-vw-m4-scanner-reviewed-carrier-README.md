# Owner-film scanner delivery payload

This is the bounded Runtime-owner handoff for the M4 delivery build. It does
not change a product repository, run the scanner, or make an owner-film,
macOS, whole-ZIP, renderer, or audio/pixel-parity claim.

## Frozen inputs

Use these existing durable files; do not rebuild or replace them.

| Input | Exact path | Bytes | SHA-256 |
|---|---|---:|---|
| Scanner ZIP 1.0.8 | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip` | 12,221 | `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee` |
| Owner instructions | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md` | 10,519 | `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220` |
| Reviewed carrier | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build` | 24,834 | `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990` |

The scanner ZIP contains exactly `README.md` and
`owner_film_cliplook_scan.py`. It is read-only, credential-free, and uses the
one qualified Agent projector. The prior 124-test approval is reused evidence;
do not replay it in this handoff. The owner instructions are the existing
append-only film-differences document, not a new policy.

## Composition e7 evidence to retain

The current Composition source is commit
`e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332`, tree
`408633d6b73dde63f683eaf9d13a132bb34a3bd7`, from `origin/main`
`67b8aa3d0d6831d3e3504a340ff583c3da253707` (tree
`62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`). The existing exact delivery
inputs and proof are:

- Patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-composition-e7-delivery-refresh/delivery/composition-origin-main-to-e7ef7a072.patch`
  — 467,845 bytes, SHA-256 `12f8361a3f4d6f1c1edcf684600bc5e0fcf2276f5136a27c4b93d0095c71a440`.
- Bundle: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-composition-e7-delivery-refresh/delivery/composition-origin-main-to-e7ef7a072.bundle`
  — 221,307 bytes, SHA-256 `46de26e1082485028a915d8693ec0484326e78c13a67c6d1ee03fb22702b8af3`.
- Manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-composition-e7-delivery-refresh-manifest.json`.
- Proof: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-composition-e7-delivery-refresh-REPORT.md`.

The existing proof records bundle verification, binary patch application to a
fresh main archive, exact 113/113 path/mode/blob equality, `git diff --check`,
and the central Composition result of 78 passed, 0 failed, 0 skipped. It does
not prove a final four-repository ZIP or owner-film viewing.

## Runtime owner action

Run the single command recorded in `COMMAND` after supplying the missing
delivery metadata inputs. It invokes all four current `tl/integration` repos,
so the normal builder emits the canonical Agent, Runtime, App, and Composition
patch/bundle outputs. It also carries the exact scanner, owner instructions,
and the reviewed Composition e7 patch, bundle, manifest, and proof under an
`extras/` subtree for traceability. The extra copies do not replace the normal
per-repository outputs.

The following are not present now and must be resolved by the Runtime owner:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/README.template.md` — required by the installed builder.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/gate-results.md` — required for truthful gate text; without it the builder emits an unrecorded-gates placeholder.
- The final owner-film canonical closure, a qualified Agent Python environment,
  and a matching extracted Agent checkout — required only for the owner's
  later local scan, and intentionally not supplied here.

The owner must also refresh/check the four repo refs and current `origin/main`
before running the builder. No result from that future run is asserted here.

## Owner hard-stop scan

After the delivery ZIP is extracted, the owner supplies an already-qualified
Agent Python environment, a matching extracted Agent checkout, and their own
immutable Runtime canonical-closure JSON. The scanner is not standalone and
does not install dependencies. From the extracted scanner directory, run:

```sh
OWNER_AGENT_PYTHON=/path/to/qualified/Agentenv/bin/python
AGENT_ROOT=/path/to/extracted/astrid-agent
OWNER_FILM_INPUT=/path/to/owner-provided/canonical_document.json
OWNER_SCAN_OUTPUT=/path/to/local/owner-film-cliplook-scan.json
PYTHONPATH="$AGENT_ROOT" "$OWNER_AGENT_PYTHON" -B owner_film_cliplook_scan.py \
  --agent-root "$AGENT_ROOT" \
  --input "$OWNER_FILM_INPUT" \
  --json-out "$OWNER_SCAN_OUTPUT"
```

Keep the film and closure local. The closure must contain the Runtime
`parent_revision.payload`, pinned shot and internal-timeline revisions, and
`dependency_manifest`; it is not a database dump or media upload. Review
`status`, `closure_errors`, every `unknown`/incomplete finding, and the
explicit `not_covered` list. `clean_claim` is always `false`; an absent owner
closure is not a clean result.
