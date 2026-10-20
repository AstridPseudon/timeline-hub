# v1.0.3 scanner independent policy review

## Verdict

**HOLD for manager/Agent follow-up; do not publish or run on owner data.**

The immutable candidate is materially compliant with the preserve-clears and
output-boundary policy and with four of the five Agent section-3 requirements.
One real gap remains: the canonical Runtime fixture permits an incoming
transition mapping written as `{"type": "crossfade", "duration": 0.2}`, but
the candidate only accepts `transition["id"]`. It therefore silently omits a
valid incoming boundary from `transition_boundaries`. This is not a guessed
outgoing conversion; it is a missing canonical input shape in the inventory.

Evidence for the accepted shape is the Agent transition census, which records
the Runtime synthetic fixture as incoming with exactly that `type` form. The
candidate gap is at `scanner.py:443-447`, where non-mapping values and mappings
without `id` are dropped. The independent strict-xfail regression is kept in
the flat design handoff test; it must become a passing test with the manager’s
minimal patch.

## Candidate integrity and scope

- Candidate TGZ SHA-256: `82fedfc67daa043c77f12629ab08ad06a0ea5f247db95e2491e2d57b2acbfee9`.
- Archive has 12 regular, safe members; no absolute or parent-traversal names,
  symlinks, hardlinks, or special members.
- Extracted scanner, tests, conftest, and README are byte-identical to the
  supplied flat copies.
- The Agent worktree remained clean; no product source, release branch, or
  archive was changed.
- The candidate remains immutable. No second validator, new ID grammar,
  truncation, release repackage, owner data, database, network, media, render,
  browser, install, or full-suite run was performed.

## Section-3 and policy audit

| Requirement | Result |
| --- | --- |
| Absent/`linear` curves omitted; explicit non-linear curves classified | **Pass** — existing parameterized regression and relocated suite |
| Single look-bearing elements; cross-track overlap; no-look pairs omitted | **Pass** — existing regressions cover all three |
| `crop_*`, element `speed != 1`, media `entrance`/`exit` | **Pass** — inventory/source-path assertions pass; `speed == 1` is not emitted |
| Canonical incoming transition inventory, no projected-outgoing guess | **Partial/hold** — `id` mappings pass and output says `semantics: incoming`; `type` mappings are silently omitted (independent xfail) |
| Half-open interval boundaries | **Pass** — existing cross-track boundary regression passes |
| Duplicate internal revision source indexes and occurrence-prefixed paths | **Pass** — existing duplicate-position regression reports the original list index and projected occurrence identity; canonical projector still fails closed on duplicate closure IDs |
| Preserve explicit `asset = None` clear | **Pass** — projector/scanner regression passes and input JSON is byte-stable |
| Output-boundary redaction | **Pass** — malformed scope/source/caption/credential/opaque sentinels do not appear in output |
| Read-only/input/output protections | **Pass** — same-path, symlink, hardlink, temp-file/fsync/atomic-replace tests pass |

The candidate uses the Agent projector and clip-field/audio-curve helpers as
the semantic authorities, reports `clean_claim: false`, and keeps conversion,
media overlap, and renderer pixel/alpha coverage explicitly in `not_covered`.
The static source audit found no network, database, media-client, or credential
client imports.

## Commands and results

All commands used the qualified existing environment
`/home/user/work/venv-agent/bin/python` and the current Agent worktree as the
explicit `--agent-root`.

```text
safe tar/hash/member validation and flat equality
passed; sha256 82fedfc67daa043c77f12629ab08ad06a0ea5f247db95e2491e2d57b2acbfee9;
12 regular members; scanner/tests/conftest/README byte-identical

/home/user/work/venv-agent/bin/python -m pytest -q \
  <relocated>/tests/test_owner_film_cliplook_scan.py --agent-root <agent-root>
23 passed in 5.62s

/home/user/work/venv-agent/bin/ruff check \
  <relocated>/owner_film_cliplook_scan.py \
  <relocated>/tests/test_owner_film_cliplook_scan.py \
  <relocated>/tests/conftest.py
All checks passed

/home/user/work/venv-agent/bin/python -B -m py_compile \
  <relocated>/owner_film_cliplook_scan.py \
  <relocated>/tests/test_owner_film_cliplook_scan.py \
  <relocated>/tests/conftest.py
passed

SCANNER_CANDIDATE=<relocated>/owner_film_cliplook_scan.py \
SCANNER_AGENT_ROOT=<agent-root> \
/home/user/work/venv-agent/bin/python -m pytest -q \
  handoff-vw-m4-scanner-v103-independent-review-audit-tests.py
1 xfailed (strict; canonical incoming type= inventory gap)
```

The first command extracted only regular safe members into ORCH temporary
storage. No build output was left in the Agent worktree.

## Delivery bloat and next step

The TGZ contains 97,766 uncompressed bytes. The minimal operational payload
(scanner, README, tests, and conftest) is 55,142 bytes; the remaining 42,624
bytes are `ORCHREPORT.md`, `FILELIST.md`, `VERSION`, two historical report/
fixture pairs, and `semantic-policy.patch`. Keep this candidate immutable for
review, but a future manager-approved final package should contain only the
tool, README, tests, and required test conftest; keep the historical reports,
reference JSON, and semantic patch as external flat handoff artifacts.

Minimal future patch: make the transition inventory accept the canonical
mapping’s `type` fallback (and add the independent regression as a passing
case); only consider string-form aliases if the canonical closure contract
explicitly admits them. Then rerun the same relocated targeted suite and
re-review the package. No release is authorized by this audit.

