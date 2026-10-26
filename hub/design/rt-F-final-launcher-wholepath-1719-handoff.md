# F-final handoff

The real 10589 service is a pre-builder startup failure, not a build result.
The exact installed row reaches the hash-checked `python3 -c` exec, but the
test-run shell has changed cwd to the detached Runtime snapshot and supplied
only `PYTHONPATH=$SNAP`. Because the exec wrapper does not add the caller's
parent, `run-final-delivery.py:23` cannot import its sibling lifecycle helper.

The passing `check_jj` and `installer.load_runner` controls are source/in-process
loads with an explicit candidate-directory `sys.path` insertion. They explain
the false positive and are not real-entry acceptance.

Recommended next step for the author: repair only the reviewed production
loader seam, preserving all existing hash, argv, source/gate, lifecycle, D68,
disk, ownership, and no-install purposes. Then run one fresh
`request-test integration:runtime delivery-v2-final --no-cache` and require
the actual lifecycle → D68 → builder-entry chain. Do not claim success from
worker exit 0, import availability, or the historical positive harness.
