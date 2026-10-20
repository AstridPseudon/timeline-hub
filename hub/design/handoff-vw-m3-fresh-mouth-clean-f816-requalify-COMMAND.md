# Exact commands

The own proof wrapper is:

```sh
/home/user/work/venv-agent/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-fresh-mouth-clean-f816-requalify/run-clean-f816-qualification.py
```

It selects only the four real public-Node tests, points at the retained Node
and `/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules`, unsets Node
injection variables for the child pytest process, and performs the full
peer/public12 before-and-after checks.

The direct crop neighbor was run with the same wrapper in its own local-only
mode:

```sh
/home/user/work/venv-agent/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-fresh-mouth-clean-f816-requalify/run-clean-f816-qualification.py crop
```

The single central request used the new named suite
`integration-viewing-mouth-clean-f816-requalify`; no existing suite entry was
edited:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  vw-m3-fresh-mouth-clean-f816-requalify integration-viewing-mouth-clean-f816-requalify)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```
