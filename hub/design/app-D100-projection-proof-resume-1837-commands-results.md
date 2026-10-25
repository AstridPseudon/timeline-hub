# D100 projection proof commands and results

## Source and capacity

- git rev-parse HEAD — PASS, 9486cbb06e2ab53402086772e6c2bc18bc4849fc.
- Candidate product/test SHA-256 checks — PASS against required values.
- Runtime custody — PASS, clean ab1e4f6141987706132916e2da16477f5a019464, tree 7d8e77b2f5a4af79305c9212ce5174d3ea9fd657.
- Projection fixture before/after — PASS unchanged at 90c4625a7481fdcd570ec8b85bbe95325f4d3c57f0a3a26017dd405b8269b638; reviewed donor retained at 6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436.
- Capacity checks: initial 5030436864, after private source prep 5068406784, after parentRED 5066850304, after candidate 5066809344 bytes. No capacity-only wait was needed.
- Worktree remained clean; no product, fixture, generated, pin, or schema changes were made.

## ParentRED

Exact command:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-5cbf575783/app-D100-projection-proof-resume-1837-parent-d4ba9916:/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D100-projection-proof-resume-1837/evidence/parent.xml tests/sdk/test_d100_item_birth_boundary.py

Result: exit 1; 23 passed, 4 failed, 4.99s. The first physical-birth assertions fail at the old shot item correspondence changed guard. The Runtime test reaches the genuine registered provider and returns the same old public refusal. This is meaningful parentRED, not setup failure.

## CandidateGREEN

Exact command:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-D100-projection-proof-resume-1837:/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D100-projection-proof-resume-1837/evidence/candidate.xml tests/sdk/test_d100_item_birth_boundary.py

Result: exit 1; 24 passed, 3 failed, 3.65s. First failed frame: test_first_physical_item_preserves_custody_and_opaque_fields[False], line 49. The repaired execution reaches the assertion that plan.bundle['source_mapping'] is unchanged, but the bundle contains an extra _doc_patch_images entry. The second aggregate variant has the same failure. The shared-owner test still fails with UnsupportedAuthoringEditError on the existing placement source offset. No speculative repair was attempted.

## Stopped work

- App projection9 / exact D118d receiving fixture — NOTRUN.
- Own nine node selectors — NOTRUN.
- No full, browser, socket, native, family, tour, alternate, or retry run.

