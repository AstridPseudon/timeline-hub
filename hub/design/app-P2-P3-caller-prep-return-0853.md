## PASS — PREPARED only

Changed only:

- `caller-publication.py`
- `caller-custody.json`

Fixes:

- Rebinds actual mounted `P2APP/P3APP=663…`, `P2TREE/P3TREE=9a…`, parent, and all decoded row fingerprints.
- Requires dispatcher worker metadata, branch/base identity, clean proof-worker checkout, and hashed source receipt.
- Preserves accurate C0 v2 request/reply wire inventory.
- Removed trailing EOF blank line.

Checks passed:

- `python3 -m py_compile caller-publication.py`
- `python3 -m json.tool caller-custody.json`
- `git diff --check HEAD`
- `git diff --check b5fc832b78a3ce6702543d064c5bbefe61df3fc3`
- Decoded P2/P3 `bash -n`
- 60 P2 and 106 P3 fingerprint guards decoded and modeled-rebound
- 248 outsider rows preserved
- Missing/forged final-source inputs refused
- Modeled preparation successfully removed stale mounted identities

No browser, backend, HTTP, build, provision, service, or full-suite execution performed. Final authorized source tuple, receipt, and integrated P2/P3 execution remain pending.