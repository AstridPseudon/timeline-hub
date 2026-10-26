Final source validation: PASS in the private scope.

- `bash ops-d141z-build-stop/check.sh` — exit 0; 33 purposes (20 local lifecycle, 4 exact donor mounted lease, 1 direct parent death, 2 inherited control-pipe, 1 normal main, 5 main hash guard refusals). Same final script is for reviewer rerun. Final output: `../private-controls/check-final.log`.
- `ruff check --select F ops-d141z-build-stop` — exit 0, All checks passed.
- `bash -n ops-d141z-build-stop/check.sh` — exit 0.
- `git diff --check` and `git diff --check 32bc911afcb2648e54be4432c5aa96cbdacf4eae` — exit 0.
- `python3 -B -` with the following stdin — exit 0, AST and redirected bytecode compile PASS:

```python
import ast, os, py_compile
from pathlib import Path
out=Path(os.environ['TMPDIR'])/'d141z-pyc-final'; out.mkdir(exist_ok=True)
for p in sorted(Path('ops-d141z-build-stop').glob('*.py')):
    ast.parse(p.read_text(),filename=str(p))
    py_compile.compile(str(p),cfile=str(out/(p.name+'c')),doraise=True)
s=Path('ops-d141z-build-stop/check.sh').read_text().split("python3 - <<'PY'\n",1)[1].split('\nPY\n',1)[0]
ast.parse(s)
```

The final shell invocation redirected its output to this worker's `private-controls/check-final.log`. Earlier targeted iterations are retained/classified in controls.json; two acceptance fixture mistakes were corrected, and no failed expectation was weakened. No full suite was requested or run. No real build, dry-run, rehearsal, test-run service/admission, collection, install, socket/browser or ZIP run occurred. TypeScript N/A for ops-only source.

F2 donor append-final and validator are real; only disk observations and builder output are controlled fault fixtures. Mounted cases execute the exact donor `suite_lease` and `supervise` (source hash pinned), plus the exact shell body/control-pipe block, using an empty-payload tiny real Store entry and native acquired lease. No Store code, native prctl/pipe/process/signal/wait/flock primitive or validator is replaced. This does not execute admission or prove real production dispatch.
