# Final portable owner-scanner review package

## Candidate result

Built from current Agent integration `4a75f68f32049a69fd86135c645fa64c51175c14`
with zero product/repository changes. The ORCH-owned delivery contains the unchanged predecessor scanner,
its preserved reports/JSON, and its 8 test functions (10 pytest cases after
the three-way curve parameterization). The corrected README now states that
the tool adds no install step but requires the normal qualified Agent Python
environment and a matching extracted Agent checkout.

The candidate includes two deterministic archives:

- `delivery/owner_film_cliplook_scan-v1.0.0.zip` — the requested ZIP filename,
  retained from the predecessor package.
- `delivery/owner-film-viewing-tools-v1.tgz` — flat transport candidate for
  the manager/hub handoff.

Adjacent bare SHA-256 files, archive sizes, exact member manifests and the
owner command are recorded in `artifact-metadata.json` and
`owner-command.txt`.

Artifact metadata:

| Archive | Size | SHA-256 |
| --- | ---: | --- |
| `owner_film_cliplook_scan-v1.0.0.zip` | 20,310 bytes | `16b37fad6f3953b547c8d9dbeec914b1dcbf684faa95a71143b5a918eca16656` |
| `owner-film-viewing-tools-v1.tgz` | 15,871 bytes | `fc9d90a4cf2019882ba3dbb6fd4cb38e6193770d14e2e9d1ad279dddd0517308` |

## Portable CLI evidence

The extracted delivery was run from a relocated temporary directory using
`/home/user/work/venv-agent/bin/python`, with an `env -i` stripped environment,
explicit `--agent-root`, and synthetic valid/unknown/incomplete closures.
The valid fixture exercises all three categories, rational FPS and an unknown
curve/asset; the incomplete fixture omits the dependency manifest and must
return `status: incomplete` and `clean_claim: false`. No owner-film data was
supplied or uploaded.

## Policy and safety review

The scanner retains immutable input handling, same-path/symlink/hardlink
output rejection, atomic output replacement, exact projector/clip-field/
registry/public-clock-related timing seams, and bounded output. It performs
no default search, credential lookup, database access, network/socket access,
render, media decode, or code/script execution. It emits no scripts, raw
payloads, captions or source media. Unsupported and incomplete input remains
unknown/incomplete; `clean_claim` remains false.

The exact Agent canonical-policy review file list is
`AGENT-CANONICAL-POLICY-REVIEW-FILELIST.md`. Review remains required before
final publication or any real owner-film run; this is a concrete candidate,
not a premature hard-stop gate.

## Verification

Exact commands and results:

```sh
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-owner-scanner-release-package/delivery \
/home/user/work/venv-agent/bin/python -m pytest -q \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-owner-scanner-release-package/delivery/tests/test_owner_film_cliplook_scan.py \
  --agent-root /home/user/work/wt/vw-m4-owner-scanner-release-package
# 10 passed in 5.53s

/home/user/work/venv-agent/bin/ruff check \
  delivery/owner_film_cliplook_scan.py \
  delivery/tests/test_owner_film_cliplook_scan.py \
  delivery/tests/conftest.py build-release.py
# All checks passed

/home/user/work/venv-agent/bin/python -B -m py_compile \
  delivery/owner_film_cliplook_scan.py \
  delivery/tests/test_owner_film_cliplook_scan.py \
  delivery/tests/conftest.py build-release.py
# passed
```

The relocated extracted CLI was run from both ZIP and TGZ extractions with
`env -i PATH=/usr/bin:/bin PYTHONNOUSERSITE=1`, the qualified venv Python,
explicit Agent root, and synthetic valid/unknown/incomplete closures. Results
were `complete`, all three categories plus `[30000, 1001]` and an explicit
unknown finding for the valid case; `incomplete` and `clean_claim: false` for
the incomplete case; and 10 relocated tests passed. Rebuilding twice produced
the byte-identical hashes above. Archive member order, zero timestamps,
uid/gid, size and path-safety manifest checks passed.

The exact owner command is in `owner-command.txt`; the Agent canonical-policy
review paths are in `AGENT-CANONICAL-POLICY-REVIEW-FILELIST.md`.
No full suite, browser, live socket, central service, network, install, hub
publication, or product-repository write was performed.
