# Owner-film scan

This is static delivery guidance, not an owner-film result. Apply the four
repositories using [README.md](README.md), including its pinned `origin/main`
checks and Runtime history prerequisite. The source gate status is in
[README.md#gate-results](README.md#gate-results). The owner-difference list is
[`extras/owner-film-differences.md`](extras/owner-film-differences.md).

## Prepare the scanner

The delivery extra `extras/owner_film_cliplook_scan-v1.0.8.zip` is the reviewed
scanner (SHA-256
`204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`). Unpack
it into its own subdirectory. It contains a `README.md`; keeping it below a
dedicated scanner directory prevents that file from overwriting the delivery
README and its apply instructions.

The companion instructions extra
`extras/owner-film-differences.md` is the exact reviewed payload (SHA-256
`969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`).

Use the scanner's existing qualified setup and command exactly:

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

`OWNER_FILM_INPUT` is one regular JSON file containing the read-only duplicate
Runtime canonical closure: `parent_revision.payload`, pinned
`shot_revisions`, pinned `internal_timeline_revisions`, and
`dependency_manifest`. Keep the duplicate, film, and report local. Do not use
credentials, a database/table dump, media, or a production upload. The input
is not modified; `--json-out` is optional and the report is also printed to
stdout. The scanner does not search for projects, open a database, fetch media,
render, or use a credential.

The scan is not a render, pixel or audio parity check, and never establishes a
completed-owner-film claim: `clean_claim` is always `false`, and missing or
unsupported closure data remains `incomplete` or `unknown`. The reviewed
scanner was exercised on Linux only; no macOS run or qualification is claimed.

## Current open viewing differences

The owner must review these on the duplicate film at the hard stop; the static
scan does not close them:

- explicit audio `curve=` behavior;
- element/custom-effect clip look and overlapping fades;
- continuous source-time audio fade sampling;
- implicit-theme preview appearance (explicit film themes are preserved).

See [`extras/owner-film-differences.md`](extras/owner-film-differences.md) for
the settled descriptions and current evidence limits.
