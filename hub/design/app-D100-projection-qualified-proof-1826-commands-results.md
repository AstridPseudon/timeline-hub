# D100/App projection proof commands and results

## Source and custody checks

- `git status --porcelain` — PASS, empty.
- Candidate `9486cbb06e2ab53402086772e6c2bc18bc4849fc` — PASS; exact candidate tree `0919e511bd28b3d3af76bb18155efda12c3e94f6`.
- `sha256sum astrid/sdk/timeline/_command_state.py` — PASS, `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`.
- `sha256sum tests/sdk/test_d100_item_birth_boundary.py` — PASS, `be2c9d054d94fe741fa2c53552ec59de1510bf82dbf704018e0bc49f3218ec58`.
- Current projection fixture hash — PASS against base, `90c4625a7481fdcd570ec8b85bbe95325f4d3c57f0a3a26017dd405b8269b638`.
- Reviewed D118d donor hash from `f53b016900c99e46998268e36c7c431ac0eec61e` — PASS, `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`; not received because the gate was not reached.
- Runtime `ab1e4f6141987706132916e2da16477f5a019464` / tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657` — PASS; clean.
- Import-origin check with the supported Python and `PYTHONPATH` — PASS; Agent modules resolved from this candidate worktree and Runtime modules from `/home/user/work/wt/rt-pin-ab1e4f61`.

## Admission

- `df -B1 /tmp` — `4,929,978,368` free bytes on the final check.
- Required light floor — `5,000,000,000` bytes.
- Result — BLOCKED before pytest dispatch. No test subprocess, XML, log, fixture receive, or source/product edit was started.

## Required behavior command

The exact reviewed additive command was not started because admission was below the mandatory floor:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<exactAgentRoot>:/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=<ABSOLUTE own evidence file> tests/sdk/test_d100_item_birth_boundary.py
```

ParentRED: NOTRUN. CandidateGREEN: NOTRUN. App projection9: NOTRUN. No full, browser, socket, native, family, tour, or alternate qualification was run.
