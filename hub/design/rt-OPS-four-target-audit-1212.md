# Four-target host audit handoff

The read-only helper and receipt are in the worker evidence directory. The sandbox process namespace is not an authentic HOST view, so this is not a retirement authorization. Run the helper on the normal host; its exit-0 predicate requires all four exact targets to be directories, zero exact path/basename references in the operational scopes, zero process hits across argv/environ/cwd/exe/fds, no UNKNOWN process fields, and readable namespace coverage. It excludes only its own PID and genuine ancestor chain and retains an explicit known-process-limit field.

The existing guard grammar rejects unsuffixed `agent-remotion`; `agent-remotion-current` is protected. Existing guarded refusal records are preserved and no target was retired.
