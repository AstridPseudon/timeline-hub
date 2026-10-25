# D140 validation record

## Scope

This was a read-only source investigation. No tests, type checks, lint, full
suite, Farm admission/body, child/core/request/queue/Store action, package
installation, credential use, D130 access, or live input access was performed.

## Exact identity checks

- Composition review HEAD was verified as commit
  `d7727b99fb9cb063d4c0ee73fdfa54d752666135`, tree
  `222476a7f8eea57f46402ab4fefabce4e2b8a703`, clean.
- Read-only `git rev-parse HEAD`, `HEAD^{tree}`, `remote.origin.url`, and
  worktree status checks were run for `/home/user/work/{agent,runtime,app,composition}`.
  Result: App and Composition match the required tuple; Agent and Runtime are
  clean but stale relative to the required tuple. Origins match.
- Required commit objects and source blobs were checked with read-only `git
  cat-file`/`git show` and SHA-256 checks. The required Agent/Runtime objects
  exist, but object presence was not treated as a qualified current checkout.
- Frozen R4 reference branches were inspected with `git show`/identity checks;
  no checkout, ref mutation, merge, rebase, or push was performed.
- Installed kit scripts under `/home/user/timeline-hub/hub/kit/bin` and the
  matching orchestration bin paths were compared read-only to the Composition
  source hashes and modes. No shared dependency or kit file was modified.

## Format and source checks

- Python standard-library JSON parsing of the completed
  `findings.json` and `source-manifest.json`: pass.
- JSON parsing of the f103 `contract/schemas/timeline-commit.json`: pass.
- C0 request/reply shapes were read from the f103 schema and
  `design/commit-v2.md`; no wire/product change: pass.
- `p4-d73-pinned-launch.sh`, child request/maker, Farm kit validator, and
  D140 receiver were traced by source line ranges. Producer formats and
  receiver checks are recorded in `report.md` and `findings.json`.
- The producer-free synthetic receipt attack is reported from the prior
  final2332 private control; it was not rerun because this task forbids Farm
  admission/body and requires read-only source investigation.

## Result

The source and JSON evidence checks pass, but the D140 whole-path acceptance
does not: the current generic source receipt checker can accept a synthetic
producer-free object, the child and kit checks do not close over their genuine
producer paths/bytes, and the live Farm inputs required to qualify the path
are absent. Verdict remains `FAIL_SOURCE` / `NOT_READY`.
