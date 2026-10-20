REJECT.

Found a concrete bypass in proposal `613a124250e57a98ccb50e6bffca03555b00702b`: explicitly empty or whitespace-only `TIMELINE_VIEWING_APP_SOURCE` and `TIMELINE_VIEWING_APP_TREE` values fall back to historical `APP13` instead of refusing.

Current source reviewed: `20ea14c26526fe4924354f10a177aebbaf6002bc`, tree `83cfad527f8b2264085571316cede1c6ae482b5f`.

Evidence:

- Exact proposal probe reproduced the empty/whitespace bypass.
- Node 20 controller tests: PASS, 1/1.
- Proposal `git diff --check`: PASS.
- No product edits, grants, browser/render/full-suite runs.

Reports and `DONE` are written in the worker directory. Hub inbox was not modified because it is root-owned/read-only.