# `astrid dev journey`: real-film merge gate

Run on a machine allowed to start the Runtime, Remotion and process groups, with the reference stack stopped.
It adopts a private clone of the reference realm into a disposable data root (the reference is never written),
brings the Runtime up there, and reaps or reports any leftover process group at the end.

```sh
python -m astrid dev journey --tier smoke \
  --reference <stopped data root> --timeline almost-ready/<TIMELINE> --summary /private/tmp/journey.json
```

`--tier smoke` (about 4 min, before every push): first client open starts the pack host, doctor must be healthy with a
usable renderer Node, render the excerpt (`--range 144 152` by default), append a comment to `astrid/core/dev/journey.py`
(inside the host's source closure; restored in `finally`), then:

1. the next client open, run inside an `otto-heavy` job, replaces the outdated idle host by itself and the new host
   outlives the job (`OTTO_HEAVY_LEASE` is stripped for the host);
2. a second excerpt renders on the new host;
3. a client with a duplicated PATH reuses the host (neither refused nor replaced);
4. kill -9 of the idle host: the next open recovers with a new host;
5. kill -9 of the host mid-render: the next host start reaps the orphaned render processes
   (`generic-host.task-scopes.json`), then a render succeeds.

`--tier full` (about 20 min) adds a Codex image (`generation.generate_image`, flux-dev t2i), `pixel.sprites`
(chroma, scale 5), `timelines checkout --fresh`, `edit --replace-asset SLOT=run:<sprites>/sprites#0`
(`--replace-slot`, default `BUGNET`), `check --no-sweep`, `publish`, and a full-film `render --review --wait`,
whose duration is checked (`--expect-duration` for an exact value). All of it happens in the private clone.

Time is never a verdict: each phase's duration and the machine load are recorded in the summary for
information. A command is stopped only when it is genuinely hung (no exit within `HANG_SECONDS`, many times
its usual duration on a loaded Mac), and that is reported as hung. Resource growth is asserted: 4 GiB disk,
20 MiB receipts, 100 MiB logs, and no rooted process left behind. On failure the tails of the Runtime and host
logs are kept beside the summary, and a failed command reports both its stderr and stdout.

Plumbing tests (no Runtime): `python -m pytest -q tests/journeys`.
