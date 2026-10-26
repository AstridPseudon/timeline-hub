# F-final protected launcher review — FAIL

## Intrinsic finding

`runtime-final-service-rows.txt:3` (`runtime delivery-v2-dryrun`) is not an executable successor of the registered dry-run row. Its candidate command binds `--wrapper` to `candidate/delivery-v2-receipt.json` and omits `--wrapper-sha`, `--builder`, `--builder-sha`, and `--receipt`. The original row has the reviewed wrapper, wrapper hash, builder, builder hash, and receipt arguments. If installed, this row reaches the real caller with required arguments missing and an invalid wrapper path, so argparse refuses before the dry-run route can execute.

The row is nevertheless accepted by the author controls because `validate_registry` authenticates the row’s pinned bytes/hash but does not validate the dry-run command’s required argument shape. The author `check-launcher.py` exercises only `delivery-v2-final` (`launcher_argv()` selects that row), so its PASS does not cover this exact-three-row defect.

This is a blocking review finding. No repair was made, no dry-run was invoked, and no canonical registry was changed.

## Confirmed controls

- Same author script SHA256: `a850c28bb5872e9f8adad7ebb35730f5369078630e2cacf4094e5198c0338413`.
- Same acceptance script: PASS, including source closure, AST/JSON, private compile, Ruff F, bash syntax, original final-row import failure, candidate final-row startup/stub path, and private scoped-CAS controls.
- Independent concrete launch from `/home/user/work/runtime` with `PYTHONPATH`, `PYTHONHOME`, and `NODE_PATH` unset: original row FAIL exit 1 with `ModuleNotFoundError: delivery_lifecycle`; candidate final-row startup PASS exit 0 on `--help`.
- Candidate source closure hashes/modes and current registry preimage matched the supplied manifest. The private installer separately passed exact preimage, three selected old rows, backup/readback/fsync, drift, wrong-row, outside-byte, protected-row, and poisoned-caller checks.

## Limits

The lifecycle evidence is the required tiny stub control only; it is not whole-author monitor coverage. No real builder, delivery dry-run, staging clone, request-test, canonical installation, ZIP, product suite, or live service was run. The prior actual10589 exit1 / builderNOTRUN result remains unchanged.
