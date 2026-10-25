# D118d FIRST RETURN

- Result: no additional diff on candidate `94ac9347b64e0aaf5fb71443cc500fd57e80aa72`.
- The candidate remains the prior six-line v2-envelope-only change in `tests/sdk/test_timeline_commit_graph_roots.py`; current bytes equal committed `94ac`.
- Conservation against normal `20177e665`: 33 assertions, 11 test functions, seven `pytest.mark.parametrize` decorators, and assertion/decorator ASTs unchanged. The only source delta is 6 insertions / 0 deletions.
- The failing value is authored at `tests/editing_conformance/test_recorded_graph_roots.py:46-51`: `root_values()[1]['value']['gain']` is explicitly `None`. It is not introduced by Runtime setup or by the v2 envelope caller.
- The live caller is `RuntimeService.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))` followed by `RuntimeService.commit_timeline(...)` at `tests/sdk/test_timeline_commit_graph_roots.py:60,65,129-133`.
- Runtime `5e9ad1c6` validates the prepared canonical document against `PreparedCommit`; its `Occurrence.gain` schema is `number`. The refusal is at `parent_revision.payload.occurrences[2].gain`: `None is not of type 'number'`.
- D104 does not apply because changing the explicit null would alter authored input. D120 authorizes the bounded source/static checks only. No behavior GO, retirement, validator weakening, or product edit is claimed.

