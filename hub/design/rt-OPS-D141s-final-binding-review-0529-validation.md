# Validation

- Terminal identity: `git rev-parse HEAD` = `2733c720c555c2853ce73b5b74d7896aa1fe8b38`; `HEAD^{tree}` = `eb04b6da47a320f0920ae7dd53d95b0ac85928a9`.
- Accepted base: b168dbb05d469941ee57c63190198bb4df852cd7/tree aa70f43234e26aa2cdb23031ca0683c3e81da0bd.
- `git diff --name-only b168dbb05d469941ee57c63190198bb4df852cd7 2733c720c555c2853ce73b5b74d7896aa1fe8b38` — PASS, exactly four authorized paths.
- `TMPDIR=/tmp/rt-OPS-D141s-final-binding-review-0529.a99S6n PYTHONDONTWRITEBYTECODE=1 python3 -I ops-d141-measured-floor/controls/real-controls.py` — PASS, exit 0, 74 cases; SEC001/SEC002 PASS; freeze2 NEEDS; release NOT_READY.
- `bash -n ops-d141-measured-floor/bin/test-run` — PASS. The literal brief path `ops-d141-measured-floor/test-run` does not exist (status 127); no alternate file was created.
- `PYTHONDONTWRITEBYTECODE=1 python3 -I` AST parse of four scoped bin Python files plus controls — PASS, 5 files.
- `python3 -I -m json.tool ops-d141-measured-floor/install-manifest.json` — PASS.
- Scoped manifest/hash/mode/direct-destination checks — PASS, all 5 files.
- Manifest preconditions — PASS against immutable donor 56f2d56e7d241d303be85df62166570d51602101/tree 744cca68, all five hashes and mode 0755.
- App packet mechanical check — PASS: binding SHA 53a145f2…, App/Agent/Runtime/Composition tuple exact; builder blob 59b65214…, SHA 2032f308…, 49,914 bytes; command files UTF-8 with no LF; exact one-LF row hashes; all 8 normal/preflight pairs present.
- `git diff --check b168dbb05d469941ee57c63190198bb4df852cd7 2733c720c555c2853ce73b5b74d7896aa1fe8b38` and `git diff --check` — PASS.
- Existing scoped Ruff: unavailable at `/home/user/work/venv-runtime/bin/ruff`; no installation attempted.
- Current worktree: clean; no source changes made by this review.

The 5344 packet remains `registration=false`, `execution=none`; no D66 registration or production body was run. Runtime 95d98/tree 78df31d6 is mechanically present but not represented by a genuine regenerated App packet.
