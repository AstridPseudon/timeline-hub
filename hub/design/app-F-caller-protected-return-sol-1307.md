Implemented the three assigned-file corrections:

- Authenticate candidate body/tail bytes against pinned templates, permitting only bounded source/ref/environment substitutions. Native assertions, encoded custody code and fixed expectations remain unchanged.
- Complete the C0 inventory: 51 request fields and 133 reply/history fields, preserving full envelopes.
- Compare all 14 App and 15 Agent mappings with actual Runtime producer blobs.
- Apply D59 authority and remove invented coordinator/future-receipt prerequisites.

Validation commands:

```bash
env PYTHONDONTWRITEBYTECODE=1 python3 caller-publication.py
env PYTHONDONTWRITEBYTECODE=1 python3 -O caller-publication.py
env PYTHONDONTWRITEBYTECODE=1 python3 "$TMPDIR/run-controls.py"
env PYTHONDONTWRITEBYTECODE=1 python3 "$TMPDIR/check-inventory.py"
env PYTHONPYCACHEPREFIX="$TMPDIR/pycache" python3 -m py_compile caller-publication.py caller-dry-preflight.py
env PYTHONPYCACHEPREFIX="$TMPDIR/pycache" python3 -O -m py_compile caller-publication.py caller-dry-preflight.py
python3 -m json.tool caller-custody.json > "$TMPDIR/caller-custody.formatted.json"
git diff --check
```

Results:

- Paired normal/`-O` preparation: PASS, **3.833s / 4.421s**. Includes decoded/wrapped `bash -n`, actual wrapper argv/export checks and safe failure propagation.
- All 20 controls passed in both modes: **40 command runs**, retaining the original 13 attacks. Control totals: **24.845s / 28.479s**.
- Every cross-source mapping mutation was refused with consumer bytes/digests unchanged.
- Inventory, compilation, JSON and diff checks passed.

Integration advanced after the paired run. A later normal preparation succeeded on App `971a29e198c3e384795731f79e39c096abd58845`, Agent `3db4af43ca4676584a53a9eaed93c02bb04a2ec5`, Runtime `becfe6db88b2cc034dba3fafa6c050117cdf2b06`; its P2/P3 source guards took **0.161s / 0.228s**. The outer comparison with the earlier snapshot exited **1** on that advancement. No retry or source chase followed; optimized qualification was not repeated for that later tuple.

Exact trees, parents, registry, candidate body/tail/native hashes and both observations are recorded in [caller-custody.json](/home/user/work/wt/app-F-caller-protected-return-sol-1307/caller-custody.json). Final caller SHA256: `97e36cb460f8a20676f28368e9788950e0b7a5b1e641dd57c0ebe43944b25adf`.

No implementation blocker. Live environment qualification remains unverified; no registry installation, full/browser/native/backend/HTTP/service/original execution occurred. Next: independent cumulative review, then final binding after complete joined App source using recipe1304. Commit message and `DONE` written.