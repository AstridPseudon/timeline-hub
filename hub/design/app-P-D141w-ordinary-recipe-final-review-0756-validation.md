# D141w final validation

## Results

Binding: **PASS**. Prospective ordinary controller recipe: **PASS**. Actual body: **NOTRUN**. No product, test, generated-file, pin, registry, queue, hub, checkout, request, or Git-metadata mutation was made.

## Read-only commands and results

- `sed -n '1,520p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md` — PASS; plan read first and used as the decision source.
- `git -C /home/user/work/{app,agent,runtime,composition} status --porcelain=v1 --branch; git -C ... rev-parse HEAD HEAD^{tree}` — PASS; all four `tl/integration` worktrees are clean and equal to the packet tuple.
- `git -C /home/user/work/composition show --stat --oneline a8d94948d73c09a8ad7687d464a6e7cac815295f` — PASS; recovered commit contains exactly the nine 0747 evidence files.
- Python blob/SHA-256 verification against `app-D141w-ordinary-return-evidence-recovery-0754.json` — PASS; all nine recovered files match the recorded committed blobs and byte counts. This is byte-exact recovery, not an artifact rewrite.
- `sha256sum /home/user/work/app/scripts/testing/d66-plain-stack.mjs; git -C /home/user/work/app rev-parse HEAD:scripts/testing/d66-plain-stack.mjs; git -C /home/user/work/app cat-file -s 59b65214bc74c1ca118b097bc3b13c0ffe480a93` — PASS; blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, 49,914 bytes; no source change was found.
- Pure import from App root with Node v20.19.4 and only `serviceRecipe` — PASS; 8 selectors, 16 commands, 16 rows, zero body/row byte or SHA-256 mismatches.
- `cmp` of recovered 0747 normal/preflight command files against 0736 — PASS; both command bodies are byte-identical.
- Python comparison of all 16 0747 command body hashes against all 16 0736 hashes — PASS; zero mismatches.
- `python3 -m json.tool` over the four packet JSON files and recovery receipt — PASS.
- Source-spec SHA-256 comparison against the eight manifest entries — PASS; all eight source blobs match, with placement-first and popup/no-SWAP/no-Element/no-duplicate guards retained.
- `sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf` and prospective-name scan — PASS; registry preimage is unchanged and no prospective or historical 0545 rows are present.
- `git -C /home/user/work/app diff --check 5344c53e3063001bb3255bd0c9cd32cc5e77967f 82e9e13ddf1d7ec6c736521b2eb091dca9877598`; Composition diff check; assigned-worktree diff check — PASS.
- Read-only source inspection of builder lines 187–209, 345–395, 624–701; `test-run` lines 19–58 and 95–120; `request-test`, `wait-test`, `request-stop-test`, and `d141-disk-trace.py` — PASS; confirms exact pin handling, submit ownership, full-heavy classification, strict 5.2-GB admission, 4.5-GB initial refusal, five-second tracing, and the existing cancellation route.
- `df -B1 --output=avail /home/user` — read-only observation `5,250,732,032` bytes. This is before approximately `0.28 GB` preparation and does not qualify post-preparation dispatch.

An initial pure-builder probe launched from the Composition worktree could not resolve the App-local `tsx` package; it made no changes. Re-running the identical probe from `/home/user/work/app` passed. An exploratory C0 token probe was over-strict about display spellings (`id_map`/accepted IDs); direct contract review and the packet’s complete C0 field arrays passed. Neither was a product or recipe failure.

## Not run

No product tests, unit tests, typecheck, lint, browser, localhost/live socket, registration, checkout materialization, `request-test`, `wait-test`, controller body, full suite, collector, or provider execution was performed. No test request was submitted.
