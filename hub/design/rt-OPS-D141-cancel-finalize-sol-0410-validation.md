# OPS D141h cancellation validation

Final bounded result: PASS, 49 common author/reviewer control checks, exit 0. All seven trace attacks ran after cancellation. This is isolated installed→published→received-bin evidence, with no controls sibling; it is not production qualification.

Commands executed from `/home/user/work/wt/rt-OPS-D141-cancel-finalize-sol-0410`:

- `TMPDIR=/tmp/w-f47dcb2045 PYTHONDONTWRITEBYTECODE=1 python3 -I privateops-d141-measured-floor/controls/real-controls.py > /tmp/w-f47dcb2045/controls-verified.json 2> /tmp/w-f47dcb2045/controls-verified.stderr` — PASS, 49 checks, exit 0, empty harness stderr.
- `TMPDIR=/tmp/w-f47dcb2045 python3 -I /tmp/w-f47dcb2045/startup-regression.py > /tmp/w-f47dcb2045/startup-verified.json` — PASS, exit 0; signal at first trace visibility; validation `trace PASS: 2 actual samples`; sampler reaped in 0.196s after signal.
- `python3 -I /tmp/w-f47dcb2045/validate-source.py` — PASS, exit 0; AST 5 Python files, five manifest hashes/modes, exact live 0be17b preimage/four absent helpers, parent unchanged, no untracked files.
- `bash -n privateops-d141-measured-floor/bin/test-run` — PASS, exit 0.
- `ruff check --no-cache privateops-d141-measured-floor/bin/*.py privateops-d141-measured-floor/controls/real-controls.py` — PASS, exit 0, all checks passed.
- `python3 -m json.tool privateops-d141-measured-floor/install-manifest.json > /tmp/w-f47dcb2045/manifest-formatted.json` — PASS, exit 0.
- `git diff --check` — PASS, exit 0.

The complete controls were repeated only after source changes: intermediate 47 PASS; intermediate 49 PASS exposed an unset-rc diagnostic through the new frozen-sampler case; final 49 PASS includes its correction. No full suite was requested or run. No tests were removed, disabled, weakened, or redefined as refusal.

Before-fix narrow isolated reproduction at `/tmp/w-f47dcb2045/d141-controls-160j0dxm` reproduced the first-only trace and no validation after 32 seconds, with runner and sampler gone. The earlier diagnostic at `d141-controls-g4ld3geq` showed the normal foreground timeout in a separate process group, explaining why direct killpg(runner) is distinct from production stop-test's session-child enumeration. Those diagnostics used inline `TMPDIR=/tmp/w-f47dcb2045 python3 -I -` and did not touch live processes.

The original retained 0402 evidence cannot distinguish cancellation before trap installation from cancellation during readiness acquisition; both adjacent source windows are repaired. The independent readonly 0410 report corroborates those windows and was consumed without duplicating broad investigation.

No live dispatcher, queue, request, service, body, installation/CAS, registry, Store mutation, package/environment installation, network, child/product test, build/ZIP, credential action, Git write, or release gate was performed. Fixture Git/snapshot activity remained entirely in the prescribed isolated controls under TMPDIR.
