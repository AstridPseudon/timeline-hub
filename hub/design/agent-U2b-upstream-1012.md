# Agent U2b upstream drift

The U2b worker integrated the upstream no-invisible-skips policy into the Agent integration merge-forward. It added the registry/guard/static-policy tests, exact lane-marker and reason custody, copied-reason/unregistered-node negatives, and zero-pass/deselection reporting. Existing behavior tests and protected schema/client/lock/Composition artifacts were preserved byte-for-byte.

See the worker report for exact commands, results, protected hashes, conflict resolutions, and the pending post-finalization ancestor check.

