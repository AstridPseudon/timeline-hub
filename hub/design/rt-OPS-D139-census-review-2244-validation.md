# D139 validation

Candidate: `bae2ba5ec66e6fb4115c2f79299f82f535e68bb1`, parent
`4e0fa7afeeee5ee380c6e063c09bc1c63aa98aee`.

| Exact control | Result |
|---|---|
| `bash -n ops-child-custody/make-child-venv ops-child-custody/check-child-imports ops-child-custody/install-prep/apply-reviewed-maker.sh` | PASS |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ops-child-custody/tests -v` | PASS — 57/57, 12.730s |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/check-child-imports` | PASS — all checks passed |
| Seven embedded Python `compile()` controls for `STORE_PY`, `STORE_VERIFY`, `STAGING_INVENTORY`, `RELOCATE`, `PROVENANCE_SCRIPT`, `DIST_METADATA_SCRIPT`, `IDENTITY_SCRIPT` | PASS |
| `PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py` | PASS — private CAS, no-clobber, descriptor/identity, helper, symlink, hardlink controls |
| `python3 -m json.tool ops-child-custody/source-manifest.json` | PASS |
| `git diff --check` | PASS |

Exact canonical supporting-system command:

```sh
/usr/bin/python3.13 ops-child-custody/check-child-imports \
  --child /usr/bin/python3.13 \
  --launcher /home/user/work/agent/tools/p4-d73-pinned-launch.sh \
  --census-file /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-D139-import-input-census-2149-input-census.json \
  --output "$TMPDIR/d139-canonical-cli-2244.<private>/result.json"
```

Result: exit `1`; 1,146 census rows; 22 attempted modules; 0 missing
installed distributions; 12 missing-census modules; 12 failures; provenance
SHA-256 `be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30`.
The output is supporting system-probe evidence only and does not assert a
registered child, installation, Store state, or provider acceptance.

Read-only identity audit: maker `5b6bfa01...` / 93,300 bytes / 0755,
installer and protected source unchanged to `4e0fa7`, candidate manifest
binding correct, and protected helper hashes unchanged.

One non-acceptance diagnostic was also run with
`PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest
discover -s ops-child-custody/tests -v`; it failed only the synthetic
`typing_extensions` availability assertion because that shared venv does not
contain the external package. The system-Python lane above has the package and
passes all 57 controls. No full suite, package install, provider, child,
browser, socket, or body run was performed.
