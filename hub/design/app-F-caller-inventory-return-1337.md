Implemented the exact wire inventory closure.

- Updated only [caller-publication.py](/home/user/work/wt/app-F-caller-inventory-return-1337/caller-publication.py) and [caller-custody.json](/home/user/work/wt/app-F-caller-inventory-return-1337/caller-custody.json).
- Derived closures from current Runtime/App generated types:
  - Request: 22 types, 51 properties.
  - Reply/history: 53 types, 133 properties.
- Added missing/extra equality enforcement and separate header/enum metadata.
- Existing custody/security controls remain unchanged and passing.

Verification:

- Normal and `-O` preparation: PASS.
- All 20 negative controls in both modes: PASS.
- Missing/extra inventory negatives in both modes: PASS.
- Python compile, JSON validation, shell syntax, wrapped argv/export/failure checks: PASS.
- `git diff --check`: PASS.
- No full suite run; not requested.

Current tuple: App `971a29e…`, Agent `47b744d…`, Runtime `becfe6d…`.

No blockers. Commit message written; `DONE` marker created.