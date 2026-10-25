# F/D134 validation and disposition

## Source checks

- Frozen tuple, trees, parents, origins, and clean worktrees: PASS (read-only
  `git -C ... rev-parse`, `rev-list`, `remote get-url`, and `status`).
- Runtime lock source commit: PASS static; `runtime.lock.json` SHA-256 is
  `4a3d51004d022b4c4adc77a15ac919f9716e7c01b37e30eba7d16031aa51d0be` and
  records Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`.
- Schema source/copy equality: PASS static; both timeline schema files hash to
  `4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`.
- Profile package lock, composition archive, registry state, and composition
  version: PASS read-only static checks (`f4fc...be18d`, `819acf...40234`,
  `d609...aac96`, `0.0.14`).
- Node: PASS read-only `node --version` = `v20.19.4`.
- Existing venv module origins: NOT RUN; executing `/home/user/work/venv-agent`
  Python is allowed only after MAIN's ordinary preflight accepts the exact
  bindings. Expected origins are recorded in `source-manifest.json`.
- D73: EXACTMISSING for the frozen tuple. The only available manifest is stale
  and is explicitly rejected; no normal-head substitution was made.

## Required local validation commands

These are source/evidence validations only and do not invoke the measurement
or preflight recipes:

```text
bash -n evidence/measurement-command.sh evidence/preflight-command.sh
python3.11 -m py_compile --check-hash-based-pycs=never <own Python source, if any>
python3.11 -m json.tool evidence/readiness.json
python3.11 -m json.tool evidence/source-manifest.json
python3.11 -m json.tool evidence/missing-inputs.json
git diff --check
```

No own Python source was added, so the isolated compile lane is not applicable.
Ruff and TypeScript typecheck are not applicable to this evidence-only change.

## Gate disposition

The first refusal is deterministic: if custody E2E is GREEN at 20:00Z, refuse
the measurement with no alternate route. If it is NOT GREEN, any missing exact
binding or any ordinary preflight/guard refusal stops the action and is
reported; there is no retry, child build, profile change, or bypass. D128's
existing child-maker custody refusal remains immutable and receives priority.
