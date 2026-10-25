# D115 Runtime pre-cut-v31 fixture purpose review

Result: all 27 failures are callers of one shared Runtime-owned fixture seam. The exact selector-level map is in [rt-D115-fixture-purpose-0934.exactsafeIDmap.json](rt-D115-fixture-purpose-0934.exactsafeIDmap.json).

The named `validation27-0926` flat handoff files were not present in the shared design directory. I used the available peerAgent0923 handoffs, service107 ownership handoff, actual D108b 2016-result manifest/outcomes, and the prior D107/M1 source/read-coverage records; this absence does not change the source conclusion below.

The source trace is:

- `tests/editing_conformance/test_commit_runtime_m1.py:21-84` loads Runtime `build_film_fixture`, opens the retained parent closure, and authors the legacy `word:word-1` declaration.
- Runtime `tests/timeline_commit_film_fixture.py:28-44` restores the committed `precut-v31` archive and keeps source/duplicate roots.
- Runtime `tests/precut_realm_fixture.py:46-176` verifies/restores the genuine archive and reads retained transcript, binding, publication, receipt, and media facts from SQLite.
- `tests/editing_conformance/test_m1_legacy_archive_read.py:91-93` proves the retained historical baseline has `dependency_manifest.documents == []`. The transcript and binding rows remain in the archive, but no authenticated timeline document pin existed in that baseline.
- The Agent current producer reference is `tests/editing_conformance/native_word_anchor_fixture.py:seed` and the retained-input route in `test_timing_retained_inputs.py`; it creates current Runtime documents/provider state and retains the exact pin through a real `clip.anchor` path. It is not a repair to the historical fixture.

Therefore the `legacy_binding` failure is an intentional historical unpinned author-input case. The setup generator does not drop a preexisting authenticated pin: the retained source has no baseline dependency pin to drop. No case is classified as an unknown setup cause, and no Runtime auth/legacy guard change is indicated.

Disposition:

- 10 exact D107-approved selectors (ordinals 1085–1138) retain their original legacy coverage and have the already approved current-equivalent route. This is an exact selector match, not a broad family match. D107 remains source-qualified/behavior-pending; this review makes no pass claim.
- 17 selectors (ordinals 1143–3654 outside the ten) remain legacy-only with `exact_missing` current producer baseline. Their native checkout, frontend, owned-move, parent-track, and scalar callers are downstream consumers of the same `m1.film` setup; nearby current primitives do not authorize an exact combined replacement. Do not broaden the D107 ten.
- If a manager later requires current success for those 17, the minimum proposal is a new selector-specific source review using the existing real current producer route and explicit current anchor choice, while preserving the original legacy read and leaving the shared pre-cut fixture unchanged. No authored input, retirement, pin, registry, kit, body, collector, replay, acquisition, or probe change is proposed here.

Acceptance evidence is recorded in `workers/rt-D115-fixture-purpose-0934/evidence/static-validation.txt`: 27-row outcome membership, JSON parse, AST parse, source/archive hashes, retained-output proof, and clean diff check. Tests/typecheck/lint were not run, per the read-only brief; the 27 and full suites were not rerun.
