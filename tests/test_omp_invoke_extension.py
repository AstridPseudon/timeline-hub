"""Optional real OMP loader/ABI test; no model request or Runtime admission."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def test_real_omp_registers_and_executes_packaged_admission_tool(tmp_path):
    omp_root = os.environ.get("ASTRID_OMP_TEST_PACKAGE_ROOT")
    bun = shutil.which("bun")
    if not omp_root or not bun or os.environ.get("ASTRID_OMP_TEST_RUNTIME") != "1":
        pytest.skip("Provide OMP, Bun and ASTRID_OMP_TEST_RUNTIME=1 with a scoped Runtime for integration")
    root = Path(__file__).parents[1]
    loader = Path(omp_root) / "src/extensibility/extensions/loader.ts"
    extension = root / "astrid/omp_extensions/astrid-invoke.ts"
    probe = tmp_path / "probe.ts"
    probe.write_text(
        f"import {{ loadExtensions }} from {json.dumps(str(loader))};\n"
        f"const loaded = await loadExtensions([{json.dumps(str(extension))}], {json.dumps(str(root))});\n"
        "if (loaded.errors.length) throw Error(JSON.stringify(loaded.errors));\n"
        "const definition = loaded.extensions[0].tools.get('astrid_invoke')?.definition;\n"
        "if (!definition || definition.loadMode !== 'essential') throw Error('Admission tool is not top-level');\n"
        "const result = await definition.execute('rejection-probe', {capability_id:'missing.test_capability',"
        "kind:'executor',project:'no-admission-project',inputs:{}}, new AbortController().signal, undefined,"
        f"{{cwd:{json.dumps(str(root))}}});\n"
        "const content = JSON.parse(result.content[0].text);\n"
        "if(content.ok!==false||result.details.astridTaskRefs.length) throw Error('Rejection created a ref');\n"
        "console.log(JSON.stringify({registered:definition.name,loadMode:definition.loadMode,ok:content.ok,refs:result.details.astridTaskRefs}));\n"
        "process.exit(0);\n"
    )
    env = {**os.environ, "ASTRID_OMP_PYTHON": sys.executable,
           "PYTHONPATH": str(root), "ASTRID_EXTRA_PACK_ROOTS": ""}
    result = subprocess.run([bun, str(probe)], cwd=root, env=env,
                            capture_output=True, text=True, timeout=45)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout.strip()) == {
        "registered": "astrid_invoke", "loadMode": "essential", "ok": False, "refs": [],
    }
