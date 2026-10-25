{
  "checks": [
    {
      "detail": "Current C0 commit-v2.md SHA256 4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7 and lead19:16 peer allocation SHA256 9ff7d26d5af941016a209a64972ef8175a70204374eee239f001a055d5854577 recorded.",
      "name": "c0_and_lead_allocation",
      "result": "PASS"
    },
    {
      "detail": "Named 1844 census artifacts and independent 1850 review/report hashed exactly.",
      "name": "immutable_input_hashes",
      "result": "PASS"
    },
    {
      "detail": "Captured full BASE/OURS/UP SHA and tree IDs used; no prefix/current-ref substitution.",
      "name": "exact_object_tuple",
      "result": "PASS"
    },
    {
      "detail": "Captured commits, trees, and every assigned base/ours/upstream blob exist; git cat-file checks only.",
      "name": "read_only_git_objects",
      "result": "PASS"
    },
    {
      "detail": "20 assigned paths, 20 remaining census paths, empty intersection.",
      "name": "exact_path_slice",
      "result": "PASS"
    },
    {
      "detail": "45 of 45 captured merge-tree headers classified with side hunk lists.",
      "name": "source_hunk_partition",
      "result": "PASS"
    },
    {
      "detail": "Evidence JSON parses; captured Python blobs AST-parse; recipe/environment JSON blobs parse.",
      "name": "json_ast_source_checks",
      "result": "PASS"
    },
    {
      "detail": "One SKILL.md patch bound to exact ours/upstream blobs and census header; no semantic patch.",
      "name": "trivial_patch_binding",
      "result": "PASS"
    },
    {
      "detail": "Temporary-index git apply --cached --check --whitespace=error-all against exact OURS object.",
      "name": "read_only_git_apply_check",
      "result": "PASS"
    },
    {
      "detail": "git diff --check after artifact-only worktree state.",
      "name": "own_git_diff_check",
      "result": "PASS"
    },
    {
      "detail": "No supported gitam/gitapply delivery script located; no whitespace proposal made.",
      "name": "delivery_script_whitespace_flag",
      "result": "NOT_FOUND"
    },
    {
      "detail": "No authorized supported route exists in task scope.",
      "name": "actual_clone_apply_service",
      "result": "NOT_RUN"
    }
  ],
  "prohibited_actions_not_done": [
    "merge",
    "checkout",
    "rebase",
    "reset",
    "fetch",
    "push",
    "commit",
    "product-file-write",
    "tests",
    "tsc",
    "lint",
    "build",
    "render",
    "installer",
    "ZIP",
    "live-service"
  ],
  "schema_version": 1,
  "status": "source-only provisional",
  "task": "agt-F-Agent-conflicts-B-1936"
}
