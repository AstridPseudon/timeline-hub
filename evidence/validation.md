# D140 Farm recipe validation

## Source and scope

The packet is source-only and contains no product, test, pin, kit, Store,
queue, provider, collection, acquisition, or global-registry change. The
existing D139a maker/checker/wrapper sources are consumed by hash; the new
operational receiver is isolated under `ops-d140-farm/`.

Verified read-only source objects:

- Agent `41ad656529fa8489829de9078b1b6e157c7433c8` / tree
  `d29e47fe7be6e55940b42fa1477a23e7925f62fa`;
- Runtime `f103bb46866999c961a8865636f2e66d544e0c9b` / tree
  `5d0cedf2e5134acf895e8d43191cc5fdc09f9883`;
- App `5696769dfca056676cde1ab46d8bc94354b3a44a` / tree
  `0748df404125114a0f68b701fa76f43abd3fc79a`;
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree
  `5ab5191a296980a0a6bcd1178ab6902d6478a148`.

The actual Main Agent checkout remains stale at `547e1045`; it was not
retargeted. The exact `41ad…` object is present and is recorded as a read-only
source identity, not as an exact checkout receipt.

## Commands and results

| Command | Result |
| --- | --- |
| `bash -n ops-d140-farm/receive-farm.sh` | PASS |
| `/home/user/work/venv-agent/bin/python - <<'PY' ... compile(test_recipe.py) ... PY` | PASS — in-memory compile |
| `/home/user/work/venv-agent/bin/python -m pytest -q ops-d140-farm/test_recipe.py` | PASS — 4 tests |
| `AGENT_CHECKOUT=/home/user/work/agent ... ops-d140-farm/receive-farm.sh --check-only` | PASS — complete JSON census; exit 1 because status is finite `NOT_READY` |
| `/home/user/work/venv-agent/bin/python -m json.tool <check-only-output>` | PASS |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-d140-farm/test_recipe.py` | PASS |
| `git diff --check` | PASS |

The check-only run reported `NOT_READY`, 94 checks, 66 non-PASS checks, and
named their owners. It confirmed the four source object identities,
D139a maker `fd83…`, normal wrapper `60d223…`, checker `8215…`, launcher
`9f668…`, client/schema/runtime-lock hashes and the supporting canonical
1146-row packet. It found no Farm schema RECORD closure, received maker,
registered child/interpreter/bootstrap, current D73 manifest/profile, central
service, retained-disk admission, output roots, fresh controls, or current
Farm receipts.

The D73 positive/poison controls, registered child import census, and the
22-root Agent core were not run. No full suite, browser, socket, Store,
installer, package acquisition, or body was run. The 57-source-control result
and the canonical `4c/ab1e` census are not a current `41ad/f103` Farm result.

Acceptance must use the exact Agent Python and Ruff paths above. No external
profile, alternate schema source, old tuple, prior failure, original9, D77
render, or D130 route is admitted.
