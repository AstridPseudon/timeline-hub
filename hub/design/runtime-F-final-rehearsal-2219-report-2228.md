## F-final/D59 rehearsal report — BLOCKED

Captured rehearsal tuple once:

- Agent `039ff2c…` / tree `4e40d897…`
- Runtime `732c48c…` / tree `7ed0559c…`
- App `bceb035…` / tree `46ad4dde…`
- Composition `635f4de…` / tree `5ab5191a…`

Fresh upstream refs matched required pins. All source worktrees remained clean and unchanged.

Invocation:

```sh
python3 run-final-delivery.py \
  --source-tuple source-tuple.json --tuple-sha <sha> \
  --gate-tuple gate-tuple.json --gate-tuple-sha <sha> \
  --builder delivery-build \
  --builder-sha f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708 \
  --receipt rehearsal-receipt.json \
  -- --repos 'agent runtime app composition'
```

Result: exit 2 after 31 seconds. D68 staging refused on the shallow App source because upload-pack could not traverse parent `e1d440723d7e75b07c7a60472c78b3f026ee6bbf` from commit `3f05489…`. No build, ZIP, or applied result was produced.

Prepared the supported private App source view in TMPDIR; it has the exact captured tip, `origin/main=3881e9440`, clean status, and zero missing objects. Disk then fell from 8.0 GB to 6.7 GB, below the mandated 8.5 GB minimum, so no heavy retry or alternate venue was attempted.

Agent conflict-relevant paths were preserved for follow-up:

- `astrid/installer/service.py`
- `tests/test_installer_platforms.py`
- `tests/test_installer_windows_tasks.py`

Targeted Agent tests were not run because no applied tree exists. Luna’s installer receipt was read; it likewise reports no applied tree yet.

Evidence:

- [rehearsal receipt](/tmp/w-92adca8fec/rt-F-final-rehearsal-2219/rehearsal-receipt.json)
- [captured tuple](/tmp/w-92adca8fec/rt-F-final-rehearsal-2219/captured-tuple.json)
- [rehearsal manifest](/tmp/w-92adca8fec/rt-F-final-rehearsal-2219/rehearsal-manifest.json)

No product, generated, schema, pin, registry, source-repo, or integration changes were made. Next step: restore disk above 8.5 GB, then rerun the exact callable using the prepared private App source view.