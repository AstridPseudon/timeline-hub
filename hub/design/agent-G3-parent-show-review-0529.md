# Agent G3/P4 parent-native ordinary-show review

**PASS** on exact `1f93b8b3057a7c2a611f7bdc186c943418b62bc6` vs `9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`.

The three-file delta is bounded to the shared cut projection, its cut-table helper, and one real `_print_cut_table` regression. The default ordinary CLI show path still uses `cli_show.print_cut_table`, which validates immutable `base_parent.revision_id` before calling `build_cut_table`; no alternate `--layers` path, selector, executor, fake chapter, history, or writer behavior was introduced.

Parent-native visual clips now use canonical frame edges and parent composition duration, yielding real picture rows and uncovered gap rows. Audio-only parents contribute duration but yield no picture rows or chapters. Existing placed-shot/mixed/legacy behavior passed unchanged.

Exact suite with author environment (`PYTHONPATH="$PWD:/home/user/work/runtime"`, Runtime checkout `/home/user/work/runtime`, Agent venv): **55 passed, 2 subtests passed**. Changed core/test Ruff passed; normal Ruff stayed **2149/2149**; vendor lock against Runtime `rt-pin-34eac004`, artifact manifest, and diff checks passed. SDK Ruff’s 10 findings and private mypy’s core-1/SDK-2 diagnostics match the parent exactly. Normal mypy remains environment-blocked by missing `types-PyYAML` and incompatible NumPy stubs; `/home/user/work/venv-agent-typecheck-v2` was not ready, so no shared dependency was touched. No full/browser/live-socket/HTTP Proof retry was run. See the worker report for exact commands, provenance, and limits.

