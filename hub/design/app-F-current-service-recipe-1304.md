## Report

Implemented:

- [current-service-inputs.py](/home/user/work/wt/app-F-current-service-recipe-1304/current-service-inputs.py)
- [current-service-inputs.json](/home/user/work/wt/app-F-current-service-recipe-1304/current-service-inputs.json)

The recipe freezes and verifies:

- App `bbed290…` / tree `e683465…`
- Agent `cba425b…` / tree `d19ce2e…`
- Runtime `becfe6d…` / tree `7edc08e…`
- Normal Agent/Runtime venv import origins and versions
- Client contract `0.2.14`, schema digest, and matching source hashes
- Existing Remotion tree/bench and Composition graph digest
- Exact Runtime CLI, DataProvider, door, and Agent callable paths
- Complete C0 v2 request/reply shape metadata

Validation passed:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile current-service-inputs.py
python3 -m json.tool current-service-inputs.json
PYTHONDONTWRITEBYTECODE=1 python3 current-service-inputs.py
git diff --check
```

No service, HTTP, browser, backend, native, or full-suite execution was performed. No blockers.

Commit message written and `DONE` marker created.