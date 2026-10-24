## Report

Read-only whole-path investigation completed. No product or packet files changed; worktree remains clean.

Findings:

- Farm preflight failed before pytest at the row import line: `banodoco_timeline_schema` was missing. The peer also reports `astrid_runtime` absent, but this conflicts with the same import statement reaching the later schema error; that absence is not independently provable because the retained child directory is no longer present locally. Evidence: peer report lines 3–11; Farm board line 11.
- `banodoco_timeline_schema` is a real external distribution. Agent 9cd declares it only under `[project.optional-dependencies].dev` (`pyproject.toml:43–57`), while `astrid/core/timeline/banodoco_schema.py:2–9,40–68` imports it and refuses validation without it.
- The distribution/import names differ: installed metadata is `banodoco-timeline-schema`, providing `banodoco_timeline_schema`; the genuine passing Agent environment has it at `/home/user/work/venv-agent/lib/python3.13/site-packages`.
- Runtime 1d9 genuinely packages `astrid_runtime*` and exposes `astrid-runtime` (`pyproject.toml:15–17,30–35`). The normal maker installs Runtime source after requirements and explicitly verifies `astrid_runtime` (`make-child-venv:385–413`).
- The maker’s locked `requirements/proof.lock` contains pytest/runtime dependencies but no `banodoco-timeline-schema`. Thus the child can acquire Agent, Runtime protocol, client, pytest and xdist while still lacking the shared schema.
- The passing Agent environment is not equivalent to the isolated child: it uses `PYTHONPATH` for Agent/Runtime source and `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` pointing to the shared venv (`agent-farm-env-snapshot-0626.json:21–27`; passing recipe lines 5–7). It is genuine qualification evidence, but not proof that the new child contains those distributions.
- The minimal correct owner seam is Sol0853’s normal child maker/verifier path: supply and authenticate the shared schema distribution in the child, and reconcile any `astrid_runtime` absence against the maker’s installed origins, `RECORD`, `direct_url`, source snapshots and receipt. Farm must not remove row imports, add overlays, `.pth`, or `PYTHONPATH`.

Preserved obligations: schema/canonical identity, actor and Store custody, client tuple, `RECORD`/`direct_url`/source provenance, Node20/Remotion profile peers, lease guards, atomic registry update and outside-byte identity.

Tests/evidence:

- Companion packet validation: `59 passed in 11.06s` via `pytest ... ops-handoff/farm-agent-full-v3`; installer/row/manifest follow-up was interrupted by a command-extraction typo, not a product failure.
- This worker ran `git diff --check HEAD`: PASS; worktree clean.
- No full suite, checkpoint, install, network, Store, registry, or process action was performed.