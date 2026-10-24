## Result

Updated only:

- [caller-publication.py](/home/user/work/wt/app-P3-solo-caller-0955/caller-publication.py)
- [caller-custody.json](/home/user/work/wt/app-P3-solo-caller-0955/caller-custody.json)

Implemented P3-only rebinding to source `82cb…`, preserving its exact two-parent list; P2 remains byte-identical. Added authenticated single-parent service-snapshot validation and fail-closed custody/proof-release checks.

## Verification

- `python3 -m py_compile caller-publication.py` — PASS
- `python3 -m json.tool caller-custody.json` — PASS
- `git diff --check 1d92503b4c` — PASS
- Decoded P3 controls: 106 fingerprints, `bash -n` — PASS
- Exact outsiders: 249 rows / 509969 bytes — PASS
- P2 row SHA preserved: `1fe552…01fd1` — PASS
- Retained Agent/Runtime custody: 4 clients, 78 backend files, 80 graph files — PASS
- Missing source manifest refusal — PASS

## Blocked / limits

The recorded `app-P3-current-integrated-0900` checkout and authenticated service snapshot receipt are absent. Therefore no reviewable row candidate or custody receipt was generated; status remains `PREPARED`.

No browser, backend, HTTP, build, provisioning, original, full-suite, or new-bench run was performed.

Commit message and `DONE` marker were created.