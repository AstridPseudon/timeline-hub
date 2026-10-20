"""Read frozen Git objects; run pure codec tests in a removed private snapshot."""
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

PREFIX = Path(__file__).with_name("handoff-vw-m3-frame-retained-genesis-fixture-")
WORKER = PREFIX.parent.parent / "workers/vw-m3-frame-retained-genesis-fixture"
REPO = "/home/user/work/runtime"
REVISION = "2c4ac180c2220bdad966bc01e95ad230e99ce26a"
AGENT = "d8749a9ce12a699672faf3ad96b4e4cbea9245c2"
PYTHON = "/home/user/work/venv-runtime/bin/python"


def main():
    with tempfile.TemporaryDirectory(prefix="codec-", dir=WORKER) as temporary:
        source = Path(temporary)
        data = subprocess.check_output(["git", "-C", REPO, "archive", REVISION,
            "runtime_protocol", "packages/python", "tests/test_timeline_commit_validation.py"])
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            archive.extractall(source, filter="data")
        agent = subprocess.check_output(["git", "-C", "/home/user/work/agent", "archive", AGENT, "astrid", "pyproject.toml"])
        with tarfile.open(fileobj=io.BytesIO(agent)) as archive:
            archive.extractall(source, filter="data")
        env = dict(os.environ, PYTHONPATH=os.pathsep.join((str(source), str(source / "packages/python"))),
                   PYTHONDONTWRITEBYTECODE="1")
        tests = source / "tests/test_timeline_commit_validation.py"
        names = ["test_schema_owned_values_preserve_opaque_null_absence_and_defaults",
            "test_packaged_track_set_accepts_labels_and_clear_without_changing_input",
            "test_packaged_track_set_rejects_malformed_args",
            "test_bad_requests_use_the_authoritative_command_schema",
            "test_schema_rejects_invalid_record_ordinals_and_derived_causes",
            "test_non_json_is_rejected_even_inside_untyped_payloads", "test_cyclic_json_is_rejected",
            "test_transitive_config_schema_rejects_bool_as_number_without_inserting_defaults",
            "test_closed_prepared_failure_and_restore_envelopes"]
        command = [PYTHON, "-B", "-m", "pytest", "-q", "-o", "addopts=", "-p", "no:cacheprovider",
            "--basetemp=" + str(source / "pytest-temp"), str(PREFIX) + "fixture-test.py",
            *[str(tests) + "::" + name for name in names]]
        print("PYTHONPATH=" + str(source), flush=True)
        print(" ".join(command), flush=True)
        result = subprocess.run(command, cwd=source, env=env)
        if result.returncode:
            return result.returncode
        # Emit INPUT bytes only. This imports neither proposal nor any store instance.
        emit = """import importlib.util,json,sys
s=importlib.util.spec_from_file_location('fixture',sys.argv[1]); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
print(json.dumps(m.build_fixture(),indent=2))
"""
        output = subprocess.check_output([PYTHON, "-B", "-c", emit, str(PREFIX) + "fixture.py"], env=env)
        Path(str(PREFIX) + "fixture.json").write_bytes(output)
        print("INPUT ONLY: canonical fixture emitted; no realm/helper/provider/capture executed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
