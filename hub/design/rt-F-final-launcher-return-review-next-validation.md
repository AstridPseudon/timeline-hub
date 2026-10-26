# Validation

## Exact acceptance script

The copied review script is byte-identical to the published author script:

```text
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-return-review-next/evidence/check-launcher.py
8c1a6ebbb1779a8d1c5e72d50196289bfb9d18ac69609963e16d57b4b17a5603
```

Command:

```text
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-return-review-next/evidence/check-launcher.py
```

Result: exit 0. It reported PASS for live-registry derivation, exact core row, mechanical three-row diff, complete argv, AST/JSON/private compile/Ruff F/shell syntax, original registered import failure, corrected final and dry-run lifecycle/D68 stub paths, tuple/hash/symlink refusal, and actual unchanged installer validation.

## Independent production-CLI reachability

Command:

```text
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-return-review-next/evidence/candidate/install-final-services.py --registry /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-return-review-next/evidence/tmp/private-cli-20261026/suites.conf --candidate /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-return-review-next/evidence/candidate/runtime-final-service-rows.txt --builder /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --source-tuple /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/candidate/final-source-tuple.json --gate-tuple /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/candidate/final-gate-tuple.json --backup /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-launcher-return-review-next/evidence/tmp/private-cli-20261026/suites.conf.backup --install
```

This is the unchanged CLI with `--install`, the exact existing source/gate tuple paths, the actual reviewed builder path, and a private copy of `tests/suites.conf` as registry; private backup only.

Result: exit 0. The backup hash equals the original live registry (`0495919f...`); the real registry remains the same hash. Both canonical tuple hashes remain `90b9da...` and `eec639...`. No canonical output or tuple was written.

## Independent runtime-cwd replay

With `cwd=/home/user/work/runtime` and `PYTHONPATH`, `PYTHONHOME`, and `NODE_PATH` unset:

- original final row: exit 1, `ModuleNotFoundError: delivery_lifecycle` (required original failure);
- corrected final row: exit 0, harmless stub reached D68 and wrote a PASS receipt;
- corrected dry-run row: exit 0, harmless stub reached D68 and wrote a PASS receipt using its own private temp directory.

An initial dry-run replay reused the final row's lifecycle trace directory and failed closed on the existing trace. It was rerun once with the required per-row private temp directory and passed; this was a harness setup collision, not a candidate finding.

## Disk/process controls

The review monitor recorded 5,122,301,952 available bytes against the 4,000,000,000-byte stop floor, child exit 0, and an explicit wait/reap. The acceptance lifecycle records also show normal exit 0 and reaped child PIDs for both harmless stub rows.

No full suite, real builder, canonical activation, service request, clone, or product test was run.
