# Validation

## Exact candidate checks

All ran from composition worktree commit
`d7727b99fb9cb063d4c0ee73fdfa54d752666135`:

```text
/home/user/work/venv-agent/bin/python -m pytest -q ops-d140-farm/test_recipe.py
9 passed

/home/user/work/venv-agent/bin/ruff check --no-cache ops-d140-farm/test_recipe.py
All checks passed!

bash -n ops-d140-farm/receive-farm.sh
PASS

in-memory compile of ops-d140-farm/test_recipe.py
PASS

JSON parse smoke check for the committed evidence JSON files
PASS

git diff --check
PASS
```

## Independent private controls

No Farm, localhost, browser, live socket, child, import body, Store, queue,
installer, package acquisition, or core service was run.

```text
private real receiver, pre-child phase ordering/route marker
PASS: pre-child omitted child/post-child bindings and invoked no route

private real receiver, malformed/wrong source receipt
PASS: wrong receipt was MISMATCH

private real receiver with temporary git shim, forged producer-free receipt
FAIL: receipt.FARM_CURRENT_AGENT_RECEIPT was PASS

private real receiver, detached RECORD/direct_url paths
PASS: schema.bound-paths was MISMATCH

private execution of commands.md import gate with failing checker route
PASS: rc=9; checker ran; dry/core markers were absent

private execution of commands.md positive/poison control block
PASS: positive counter had one call and rc=17; poison counter stayed empty and rc was nonzero

private execution of commands.md durable core block with a private route
PASS: rc=0; exact JUnit/raw/start-stop/disk/KEEP/runmanifest files existed; 36 argv entries included --junitxml
```

The durable control proves the command block’s actual argv and retention
mechanics only. It is not a normal Farm-service receipt or readiness result.
