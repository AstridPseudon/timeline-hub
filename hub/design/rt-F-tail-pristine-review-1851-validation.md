# Independent preparation review

Verdict: **FAIL**.

This is a read-only preparation review. No core/full/body/P4/tour/provider/
browser/render/wheel/ZIP command was executed, and no private runner was
installed or invoked.

## Commands and results

- `python3 -m json.tool <prep>/inputs.json >/dev/null` — PASS.
- `python3 -m json.tool <prep>/selector-map.json >/dev/null` — PASS.
- `python3 -m json.tool <prep>/source-manifest.json >/dev/null` — PASS.
- `bash -n <(sed -n '14,42p' <prep>/commands.md)` — PASS; normal route only.
- `bash -n <(sed -n '46,87p' <prep>/commands.md)` — PASS; preflight only.
- Read-only route parser against `selector-map.json` — PASS: exact 22 roots and order.
- Read-only `git cat-file`/tree checks for named Agent, Runtime, App and Composition objects — PASS.
- Read-only `git rev-parse HEAD`/`HEAD^{tree}` checks against captured `tl/integration` receipts — PASS.
- Read-only SHA256 verification of the private 100 Python inventory against released Runtime `7070f1378d1917fcce69857ebd33cd2b3015568b` — PASS: 100/100.
- Read-only `git diff --check` on captured integration worktrees and prep worktree — PASS.

## Blocking findings

1. `commands.md` uses `optionalreads` in the C0 example, while the real
   `RequestedStep` schema and contract use `reads`.
2. `commands.md` places `Idempotency-Key` inside the JSON body; the real
   contract requires it as an HTTP header and the request schema rejects it as
   an additional body property.
3. Five missing upstream roots and the missing D73 launcher are recorded only
   as `missing`, not explicitly as `UNKNOWN_MISSING_UPSTREAM_SELECTOR`.
4. The manifest's `frozen_r4_ref` labels resolve locally to different objects
   than the exact named commits recorded beside them. The exact named objects
   are present, but the ref-to-object provenance is ambiguous and unsafe for a
   later cut.
5. The reported 41-file private matrix is not covered by a stable complete
   source manifest: the hash manifest lists 34 files, and its generated
   `run-final-matrix.pyc` hash currently differs from the recorded value.

## Preserved limitations

The five missing roots and launcher remain genuinely unavailable, so no
executable pristine-upstream gate can be claimed. D59 and the upstream census
remain pending. The 100 Python plus TypeScript inventory remains private
qualification evidence only; it was not imported as pristine upstream. No
D134 interim count or D130 action was used. Scoped lint/type checks are N/A for
this prose/evidence-only review. No livekit, hub, credentials, permissions,
generated/pin writes, package acquisition, clone, environment/provisioning,
Store write, or source/registry/git write was performed.
