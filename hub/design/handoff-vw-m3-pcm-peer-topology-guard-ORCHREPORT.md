# PCM peer-topology guard — ORCH report

## Result

Prepared a flat ORCH-only successor to the held served-PCM controller. The
controller now rejects the borrowed graph before qualification when it has a
directory symlink cycle or differs from the exact retained root-smoke graph
manifest. The check is not a current-graph-vs-current-graph comparison and
does not mutate or repair the graph.

The existing public-77 archive, native helper, Node, source cleanliness/tree,
preflight/postflight-finally, seven whole-scope tests, two phase tests, and
six historical Remotion/Player file checks were preserved. Agent/App consumer
profiles remain distinct; this guard does not require their six hashes to be
equal.

## Artifacts

```text
controller  7c38b3d1c383918fcd93b9f2230d50700a5fa2c54ced0a443b9538e6f89c4738
fixture     2298b10a512fe5b32a6ba20ed5b806a189ed4e6a065f125833bc91709b734ba8
regressions 78df5c48437088b92c0d57eb8c98718c14400f85a6a18cfe57002d2d2fe0fe6
```

## Evidence

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check <three flat artifacts>
  PASS — All checks passed

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q \
  -c /home/user/work/wt/vw-m3-pcm-peer-topology-guard/pyproject.toml \
  -p no:cacheprovider <guard-regressions.py>
  PASS — 8 passed in 0.40s

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B <bounded actual-graph probe>
  PASS — refused at the observed cycle:
  .../node_modules/@babel/code-frame/code-frame
```

The eight pure regressions include the four retained served-guard checks plus
synthetic added-directory-cycle, added-entry, changed-symlink-target, and
retained-manifest-anchor cases. They open no listener and perform no peer
repair. No browser, socket, full suite, install, central test request, grant,
or actual PCM qualification was run.

## Decision and limits

The retained root-smoke `prepare-pre.json` is the only topology baseline.
The current shared graph remains unqualified because the independent audit
found 106 added package-directory self-links. A lead must restore the exact
approved graph (or provide a separately reviewed equivalent) and reprepare a
new READY artifact before any manager grant. This worker did not create a new
baseline or change the held `handoff-vw-m3-pcm-served-whole-ready-*` artifacts.

