Implemented WC5 real speech seam proof in `tests/packs/video_editing/test_runtime_publication_chain.py`.

- Added deterministic managed-WAV fixture through normal SDK admission and `GenericPackHost` settlement.
- Added positive five-field media-selection and verified-media assertions.
- Added malformed provenance negative case.
- No Runtime/API/client/generated changes.
- Preserved existing speech/RIPPLE tests.

Tests:

- `pytest -q tests/packs/video_editing/test_draft_voiceover.py tests/sdk/test_projectless_admission.py` — 42 passed.
- `py_compile`, `git diff --check` — passed.
- Named integration suite — blocked by Runtime/SDK schema mismatch (`8de823…` expected, `ce3781…` served); 4 failures including two pre-existing tests.

Remaining requester-authority qualification is honest: the outer authoring target remains a bounded test double.

Commit message written and `DONE` created.