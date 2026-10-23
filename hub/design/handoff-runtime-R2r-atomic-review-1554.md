# Runtime R2r atomic native-birth review — PASS

Independent Luna review completed 2026-10-23 against the settled PLAN/C0 scope and the orchestrator 15:44 Sol row.

## Reviewed identity and provenance

- Runtime base/current origin: `origin` is `https://github.com/banodoco/banodoco-workspace-runtime`; integration base `9ce4242bc01f100bab9efc51032a73985cefb2b2` (`tl/integration`).
- Cumulative reviewed range: `9ce4242bc01f100bab9efc51032a73985cefb2b2` → author WIP parent `b11f390a22404a8d330a800501c32b88aa78bf17` → reviewed author commit `53249509df12bc5b83e32d2c47830cc094e9054e`.
- Final reviewed tree: `3bd06dc517f347976541ae4dde3caf3d29d03419`.
- Executing Agent checkout: `/home/user/work/agent`, origin `https://github.com/peteromallet/astrid-agent`, clean `tl/integration` HEAD `d682c5977e0d5a7627ca04852980a2d65ca899d4`.
- Runtime review checkout ended clean at the reviewed author commit/tree. `b11f` was not treated as a separately approved landing; the cumulative 9ce→final diff was reviewed here.

## Finding

PASS. The production delta is correctly narrow in `runtime_protocol/timeline_commit_auth.py::validate`:

1. Each step reconstructs sequential command input images.
2. Atomic touched scopes are resolved against each command’s actual reconstructed input, after prior commands can establish a native birth/alias.
3. Boundary authentication and binding validation still run for every step.
4. The complete batch touched-scope union is checked against every accepted step after all steps have been processed.

This specifically closes the earlier-step subset hole for a scope first appearing in a later command. I found no birth-scope exception, foreign/future/ambiguous/wrong-owner escape, owner/allocation weakening, or atomic-to-fields fallback. The original rejection-before-persistence behavior and native/public commit caller remain intact.

The only changed files relative to 9ce are the auth module and additive authentication regression cases. No contract, schema, generated client, pin, Agent body, host/daemon, Git mutation, or response-shape carrier changed. The existing v2 request/reply/history/undo/preview fields therefore remain byte/source-preserved; this review did not claim a new full-suite qualification of every response variant.

## Evidence

- Exact portable old source: **2 passed, 2 failed**, exit 1; the two atomic grouped/separate birth cases fail at the old `provider occurrence alias is outside its boundary` guard.
- Exact portable corrected source: **4 passed**, exit 0.
- Current-tree additive birth regression: **18 passed**, exit 0. This covers fields/atomic and grouped/separate acceptance, seven atomic tamper classes in grouped/separate form, and unchanged DB/history/source after refusal. No skips, xfails, deselections, or weakened expectations.
- Central named service `v2-auth-current-integration`: **338 passed in 93.35s**, exit 0, exact final tree `3bd06dc517...`; the eight requested authentication/read-basis/input/port/inverse/source/raw-capture files ran with no skip/deselect count.
- Static/preservation: Ruff exit 0; Pyright current exit 0 with 0 diagnostics; `git diff --check` exit 0; audit reproduced 30 original auth definitions, 281 other test files, 77 frozen files, 63 frozen schema/client/generator files, and edit-command digest `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Final file SHA-256: auth `02bc94cd0a41e3ec3fd6d3011d03509588fdb50d459517932d43ce72533f9d15`; auth tests `10f4f9b53e9a39afa735e26543c29cdb620c776a364b61e0009591212059ad6e`.

## Held 44-test qualification boundary

The exact 85b2 archive plus only the durable atomic guard patch was reconstructed in private scratch. The sequential-verifier source was byte-identical to 85b2, and the compatibility snapshot passed **44/44** in 8.93s with no skips/deselections. The 9ce ancestry does not contain `tests/test_timeline_commit_sequential_verifier.py` or `validate_sequential_capture`; therefore this is supplementary compatibility evidence, not a current-9ce 44-test qualification and not a reason to import 85b2 production code. The actual 44-test run belongs after the separate sequential owner lands.

## Landing / next step

Manager should queue only the reviewed current commit `53249509df12bc5b83e32d2c47830cc094e9054e` for its own serial Runtime landing before merge. Do not hold this atomic fix or consumer seed on the unrelated historical 85b2 prerequisite. After the sequential owner is actually present, rerun the exact 44 tests on the integrated source and retain the explicit current-338 qualification boundary.

Durable author evidence remains in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-atomic-birth-sol-1546/evidence/`.
