# F-D86 inverse-stage7 protected source handoff

Verdict: PASS_SOURCE. Normal merge is pending; the orchestrator still owes the MAIN7 functional proof.

Candidate: `tl/agt-F-inverse7-return-0242`
Candidate commit: `a07e9eb283a203ae054b627a5e681398f09e53e3`
Changed test blob (git): `b97bd6a6b6da650cd60b48f78a31fabd7471f26b`
Changed test SHA-256: `6c02629fded13bbd97a2cd62d5954083c04cbead04a67e6b30df500f2a4fc1f1`

MAIN7 exact selectors:

- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-4-two-step-clips-before]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-16-two-step-clips-after]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-28-two-step-config-clips-before]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-40-two-step-config-clips-after]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_whole_inverse_authenticates_forward_history_and_exact_redo[case-49-native-whole]`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_inverse_refuses_forged_source_publication_and_step_without_writes`
- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py::test_known_inverse_refuses_native_write_and_aba_without_writes`

Pinned custody:

- Agent `bd3c95b1cebe3bf27c4a82919e5839efb37519db`; `commit.py` SHA-256 `eec60cd2520730e5ccfa8ebde6ad6a1fa986df62520c57d6575f5512c79b9cf7`; `inverse.py` SHA-256 `06bd41f404a40c17a1ec06b49c8443e0e755f622134822ede55fb3ca79234cee`.
- Runtime `6634a17f3ffd885567ba3c91b6c7a560df7375a4`; `timeline_commit_auth.py` SHA-256 `4ac2b8792fe0389afb6eb710a348c35fa196131a13cab175bd3646f7d2cc0aeb`; `timeline_commit_store.py` SHA-256 `2a68990b180326585b7f0abaf1ee54c8ff9340e83663f17cd1efff1b2bd78a5c`.
- Current Agent production worktree HEAD `a836baa3b11208d66bf8d23d6abfb1c8e59257e2`; current Runtime production worktree HEAD `6634a17f3ffd885567ba3c91b6c7a560df7375a4`; all relevant source fingerprints match.

Already-joined source hashes on `tl/integration`:

- D91 `b003f3799b`, `tests/editing_conformance/test_commit_runtime_shared_inverse.py`: Git blob `00c1ccc5949ca987b51af9c8cdc741c05ecfb1ec`; SHA-256 `8f920cae425ac3b4bfaaaf1409f0c7a77e18f45e6dafb742590e845560db16d4`.
- D83 core-element `f643a5e12a`, `tests/core/test_timeline_element_publication_runtime.py`: Git blob `a46bb9e8ab9e4065064017f674cfd848a30d6265`; SHA-256 `f03e19caa0b6505a42d17fc0eaca77a4794fafb863619bdc4876b14bd63b0357`.
- Occurrence48 `095177db79`, `tests/editing_conformance/test_commit_runtime_occurrence_media.py`: Git blob `b42079e3b350212109b63aa86bd0eb145444843b`; SHA-256 `e177f56a9a26b07e4d074961e5fa78d8941b379b4c3efb241aaca5a03c0c9537`.
- Net-zero `f32a890e3b`, `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py`: Git blob `a6056ae9ee33dbffef7bfec7c2f078135d22543c`; SHA-256 `b0e8bfb466fd12f1d4ccbd6b065f8cffc78e41c6a33dfe94245119e16b7434e9`.

Functional qualification is intentionally not claimed here.
