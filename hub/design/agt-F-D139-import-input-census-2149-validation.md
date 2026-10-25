# D139 validation

{
  "checks": {
    "agent_source_ref_exists": true,
    "agent_source_tree_matches": true,
    "graph_membership": true,
    "json_serializable": true,
    "missing_membership": true,
    "parse_errors_absent": true,
    "root_count": true,
    "root_file_arithmetic": true,
    "runtime_lock_source": true,
    "runtime_object_exists": true,
    "source_hashes_present": true,
    "unfiltered_command": true
  },
  "counts": {
    "graph_edges": 17604,
    "graph_nodes": 1001,
    "imports": 1146,
    "missing": 17,
    "root_python_files": 431,
    "root_selectors": 22
  },
  "method": "stdlib AST, Git blob reads, SHA-256, and direct dist-info/RECORD/top_level reads only",
  "parse_errors": [],
  "schema": "timeline.d139.validation/v1",
  "source_hashes": {
    "command": "8cd8300a4d1e4f43dc7895907f858f6f2989e964ba38cc017a6a5fbe4cfd2637",
    "launcher": "9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd",
    "proof_lock": "6f6e3843fbb39d91e80d5be952cb3d589053503541b61202d341f9757902c110",
    "runtime_lock": "ad818e99cb0759d1742d9f67b5bb3367b03fd3e88d8f65846253169272b8b6ce"
  }
}
