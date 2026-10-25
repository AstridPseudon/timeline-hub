# D108/D77 final review — namesD108render

## Candidate identity

- Candidate: `d108_render_rehearsal.py`
- SHA-256: `c4efb9547415ed0d6f877c4f2466a113296f8d2cbaa2401f352ec14588958312`
- Private controls: `check_candidate.py`, SHA-256 `406ffd19c77021388c86f38bdf0f80ff19bacefe38d7141437ff19e6f1d2f938`
- Exact corrected candidate delta was reviewed against the return-0820 candidate; no Runtime worktree changes.

## Review controls

- Private controls, run from a private scratch copy with this Runtime worktree on `PYTHONPATH`: **16 passed in 2.192s**.
  - Includes wrong applied Agent commit with retained tree, duplicate/trailing `--source-checkout`, every requested argv addition/substitution family, profile/carrier/schema/source/environment mismatch refusal, duplicate JSON keys, binary substitution refusal, canonical service/profile structural positives, and normal CLI `NOTRUN`/`UNPROVED` behavior.
- Additional argv sweep: **8/8 token substitutions refused; 9/9 insertion positions refused**.
- Compile command: `python -B -c ... compile(candidate, check_candidate)` — **exit 0**.
- Ruff: `ruff check --no-cache candidate check_candidate.py` — **exit 0, All checks passed**.
- Pyright: `pyright candidate check_candidate.py` — **0 errors, 0 warnings, 0 informations**.
- Worktree whitespace: `git diff --check` — **exit 0**.
- Candidate-vs-return whitespace: `git diff --no-index --check ...` — **exit 1 as expected for differing files; no whitespace diagnostics**.
- Sol’s exact existing Runtime parser evidence was hash-exact and not rerun: `32 passed in 1.86s` in `validation.json`; its candidate/check hashes match the reviewed files above.

## Decision and limits

**PASS for the private candidate controls, with readiness still UNPROVED and render NOTRUN.**

The corrected candidate pins the retained applied Agent commit `cd3f5480350d1ca68c9d8ec16aeae2863501c2a4`, authenticates the retained trees/manifest/patches, uses the canonical `SourceProfile` and service parser, and requires the exact `generic_host --service --source-checkout ... --support-root ...` argv. It does not contain the rejected historical `f4ed`, `0013`, or `819acf` identities or undefined shell-variable fallbacks.

The normal production route remains `Backend.stage -> service_declaration -> Runtime ServiceSupervisor -> generic_host -> run_pack_host_foreground -> ensure_pack_host`; the candidate does not replace that route or change D13. Its preparation receipt remains `status=NOTRUN`, `canonical_installed_preflight=UNPROVED`, `installed_render=NOTRUN`, `service_registration=NOTREGISTERED`, and `zip_publish=NOTRUN`.

The authentic applied Agent/Runtime objects, seven-key D13 carrier, installed profile/site/wheel/environment, and current Remotion closure are absent. The existing normal-installer/D13 seam is concrete: `Backend.stage` emits distinct `a/`, `r/`, and `py/` paths plus `source_digest` and `service_declaration`, while canonical D13's existing positive requires the four-field profile and `runtime_checkout == source_checkout`. This is documented as an input conflict; no private replacement deployment validator, broadened D13 shape, fabricated receipt, near-match substitution, install, build, service, browser, render, ZIP, or full suite was used.

The C0 request/reply contract remains unchanged, including the §1 request fields and §4 accepted/merged/conflict/invalid/dry-run envelopes.

