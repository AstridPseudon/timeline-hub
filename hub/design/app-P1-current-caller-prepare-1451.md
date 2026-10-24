## Result

Prepared:

- [p1-current-caller.py](/home/user/work/wt/app-P1-current-caller-prepare-1451/p1-current-caller.py)
- [p1-current-caller-facts.json](/home/user/work/wt/app-P1-current-caller-prepare-1451/p1-current-caller-facts.json)

Bound App `be98aac…`/`2839c7…`, current Agent `68e82c0…`/`aa62e9…`, and Runtime `e68cf23…`/`a2cbedd…`, including parents, locks, interpreter origins, Remotion graph, exact P1 body, and both cases. Historical `ap2-P1-chain-h6` is explicitly rejected.

Status remains `PREPARED`; no service, browser, HTTP, native, backend, or P1 submission occurred.

## Validation

Passed:

```text
python3 -m py_compile p1-current-caller.py
env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 p1-current-caller.py --dry-source
env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -O p1-current-caller.py --dry-source
bash -n generated shell
python3 -m json.tool p1-current-caller-facts.json
git diff --check
```

Negative controls refused: wrong source, tree, parent, lock, target, body, and poison inputs.

## Next step

After final shared launch review:

```bash
python3 p1-current-caller.py --dry-source >/tmp/p1-current-caller.sh
bash /tmp/p1-current-caller.sh
```

Commit message and `DONE` marker were written for the harness.