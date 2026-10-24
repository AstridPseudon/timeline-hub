# F-ABA managed-row request

The candidate row is staged only. Its later execution target is the existing
`tl/agt-F-final-source-join-0816` checkout at commit `0c2c28da4f9733a1becc134f95219ae3079fc50e`
and tree `4ce9de35768c75d38db16882423313fb5047eb5f` (`/home/user/work/wt/agt-pin-0c2c28da`),
not this artifact branch. The manager should request the single original selector
`tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
only after independent source review and source-proof PASS.

Canonical later manager operation:
`request-test agt-F-final-source-join-0816 authoring-current-becfe-nodes --files tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`

F-ABA-row-env repairs the command scope only. Service packet
`agt-F-final-source-join-0816-authoring-current-becfe-nodes-1024083505-26998`
passed preflight, then exited 4 before collection: the old row's `env -i`
qualified only preflight, while pytest inherited the service snapshot's
`PYTHONPATH` and could not import `runtime_protocol` in conftest.

The staged row now uses the service-supported
`env -i ... /bin/bash --noprofile --norc -c`
serialization. The unchanged preflight and `exec ... -m pytest` share that
environment. The suite name supplies shell `$0`; the service appends the exact
selector as `$1`, and the inner command's quoted `"$@"` passes it to pytest.
The preflight's 23 assertions, all environment assignments, fixed working
directory, Python `-P`, pytest options and original selector are preserved.
Preflight failure stops the command before pytest and retains its exit status.
The startup-file flags prevent this host's Bash initialization from prepending
Nix paths to the qualified PATH; the synthetic control checks every assignment.

This matters before the test body: conftest imports `runtime_protocol.platform`
through Agent's `atomic_io`, so pytest must start with becfe on `PYTHONPATH`.
The unchanged body later sets the locator to 8ea and exposes that checkout;
already-imported Runtime modules remain becfe. Its explicit a0 fixture archive
still supplies fixture data. No module-cache replacement, user-site override,
fixture/body change or emitter change is introduced. Same-user execution and
the authenticated becfe authority guards remain intact.

The live registry is unchanged. Independent read-only review must PASS before
the manager installs this staged row and requests the operation above. The
controls below establish serialization and static identity only; they do not
claim collection, body, realm, child or actual Runtime execution succeeded.

Retained finite control (standard library only; no repository modules imported).
Run from this artifact checkout:
`python3 -I -c 'from pathlib import Path; p=Path("tests/suites.conf.candidate.request.md"); exec(compile(p.read_text().split("```python\n",1)[1].split("```",1)[0],str(p),"exec"))'`

```python
import ast
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

SUITE = "authoring-current-becfe-nodes"
SELECTOR = (
    "tests/timeline/test_authoring_media.py::"
    "test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba"
)
PYTHON = "/home/user/work/venv-agent/bin/python"
BASE = "bd635de857953282651ba5d541ab50bfe8f0f659"


def run(argv, **kwargs):
    return subprocess.run(argv, capture_output=True, text=True, check=True, **kwargs).stdout


def command(row):
    # Exact production test-run awk extraction, including whitespace rebuilding.
    return run([
        "/usr/bin/awk", "-v", "r=agent", "-v", "s=" + SUITE,
        '$1==r && $2==s {$1=$2=""; sub(/^ +/,""); print; exit}',
    ], input=row).rstrip("\n")


old_row = run(["git", "show", BASE + ":tests/suites.conf.candidate"])
new_row = Path("tests/suites.conf.candidate").read_text()
assert new_row.split(None, 2)[:2] == ["agent", SUITE]
assert len(new_row.splitlines()) == 1
old = command(old_row)
new = command(new_row)
old_head, old_pytest = old.rsplit(" && ", 1)
old_tokens = shlex.split(old_head)
python_index = old_tokens.index(PYTHON)
preflight = old_tokens[python_index:]
assert preflight[:3] == [PYTHON, "-P", "-c"]
new_tokens = shlex.split(new)
bash_index = new_tokens.index("/bin/bash")
assert new_tokens[:bash_index] == old_tokens[:python_index]
assert new_tokens[bash_index + 1:bash_index + 4] == ["--noprofile", "--norc", "-c"]
assert new_tokens[bash_index + 5:] == [SUITE]
inner = new_tokens[bash_index + 4]
assert shlex.split(inner) == preflight + ["&&", "exec"] + shlex.split(old_pytest) + ["$@"]
assert inner.endswith(' "$@"')
assert shlex.split(old_pytest) == [
    PYTHON, "-P", "-m", "pytest", "-q", "-o", "addopts=", "-p",
    "no:cacheprovider", "--timeout=45", "-m", "integration",
]
# Compare raw preflight bytes too, before the service's whitespace normalization.
raw_old = shlex.split(old_row.split(None, 2)[2])
raw_new = shlex.split(new_row.split(None, 2)[2])
assert shlex.split(raw_new[raw_new.index("/bin/bash") + 4])[3] == raw_old[raw_old.index(PYTHON) + 3]
assert sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(preflight[3]))) == 23
compile(preflight[3], "<preflight-source-only>", "exec")

env_index = new_tokens.index("env")
assert new_tokens[env_index + 1] == "-i"
qualified = dict(item.split("=", 1) for item in new_tokens[env_index + 2:bash_index])
assert qualified["PYTHONPATH"] == (
    "/home/user/work/wt/agt-pin-0c2c28da:/home/user/work/wt/rt-pin-becfe6db"
)
assert "PYTHONNOUSERSITE" not in qualified
source = Path(qualified["ASTRID_AGENT_SOURCE_ROOT"])
runtime = Path(qualified["ASTRID_RUNTIME_CHECKOUT"])
for root, commit, tree in [
    (source, "0c2c28da4f9733a1becc134f95219ae3079fc50e", "4ce9de35768c75d38db16882423313fb5047eb5f"),
    (runtime, "becfe6db88b2cc034dba3fafa6c050117cdf2b06", "7edc08e3fe94edcbc8ef695c479f4de301789b89"),
]:
    assert run(["git", "-C", str(root), "rev-parse", "HEAD"]).strip() == commit
    assert run(["git", "-C", str(root), "rev-parse", "HEAD^{tree}"]).strip() == tree
    assert run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"]) == ""
test_path = Path("tests/timeline/test_authoring_media.py")
body = (source / test_path).read_bytes()
assert test_path.read_bytes() == body
assert hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest() == "e55be12f88d23fddba3dd36614eb91745c1f8adf"
test = next(n for n in ast.parse(body).body if isinstance(n, ast.FunctionDef) and n.name == SELECTOR.split("::")[1])
assert sum(isinstance(n, ast.Assert) for n in ast.walk(test)) == 59
assert hashlib.sha256((runtime / "runtime_protocol/timeline_commit_auth.py").read_bytes()).hexdigest() == "e172f8c56d81e8039570ba5a07fc7121fba623b305e7c7a0b529d90c5dcccb70"
assert run(["git", "-C", str(runtime), "rev-parse", "HEAD:runtime_protocol/timeline_commit_auth.py"]).strip() == "979225ab8fdf7f6de1fcea4e7576b60b49b8b5f1"
assert run(["git", "-C", str(runtime), "rev-parse", "HEAD:tests/test_timeline_shared_inverse_authority.py"]).strip() == "e9827aa49e3ca59f58335c60a1e8483390d0a0e1"
run(["git", "-C", str(runtime), "cat-file", "-e", "a0dca16975dfe8f5e762703b99d9791a16cf7fd7^{commit}"])
profile = Path(qualified["ASTRID_REMOTION_PROJECT_DIR"])
package = json.loads((profile / "package.json").read_text())
archive = profile / package["dependencies"]["@banodoco/timeline-composition"].removeprefix("file:")
assert hashlib.sha256((profile / "package-lock.json").read_bytes()).hexdigest() == "f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d"
assert hashlib.sha256(archive.read_bytes()).hexdigest() == "819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234"
assert json.loads((profile / "node_modules/@banodoco/timeline-composition/package.json").read_text())["version"] == "0.0.14"
assert qualified["ASTRID_NODE_EXECUTABLE"] == "/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node"

# Only these benign stdio echo programs execute: neither payload imports product code.
def echo(phase, exit_code=0):
    code = (
        "import json,os,sys; "
        "print(json.dumps(dict(phase=" + repr(phase) + ",env=dict(os.environ),argv=sys.argv[1:],cwd=os.getcwd()))); "
        "sys.exit(" + str(exit_code) + ")"
    )
    return shlex.join(["/usr/bin/python3", "-I", "-c", code])


def synthetic(repaired, exit_code=0):
    if not repaired:
        return old.replace(shlex.join(preflight), echo("preflight", exit_code), 1).replace(old_pytest, echo("pytest"), 1)
    replaced = inner.replace(shlex.join(preflight), echo("preflight", exit_code), 1).replace(old_pytest, echo("pytest"), 1)
    wrapper = " /bin/bash --noprofile --norc -c "
    return new.split(wrapper, 1)[0] + wrapper + shlex.quote(replaced) + " " + SUITE


outer = {"PATH": "/usr/bin:/bin", "PYTHONPATH": "/service-snapshot", "F_ABA_OUTER_ONLY": "sentinel"}
for text in (old, new):
    run(["/bin/bash", "-n", "-c", text + " " + SELECTOR])
for repaired in (False, True):
    # Exact service suffix: CMD+=" $f" followed by bash -c "$CMD".
    shell = synthetic(repaired) + " " + SELECTOR
    records = [json.loads(line) for line in run(["/bin/bash", "-c", shell], env=outer).splitlines()]
    assert [r["phase"] for r in records] == ["preflight", "pytest"]
    for record in records[:2 if repaired else 1]:
        assert all(record["env"].get(k) == v for k, v in qualified.items())
        assert "F_ABA_OUTER_ONLY" not in record["env"]
        assert record["cwd"] == str(source)
    assert records[1]["argv"] == [SELECTOR]
    if not repaired:
        assert records[1]["env"]["PYTHONPATH"] == "/service-snapshot"
        assert "ASTRID_RUNTIME_CHECKOUT" not in records[1]["env"]
    print(("NEW" if repaired else "OLD") + ": environment scope and exact selector PASS")
failed = subprocess.run(["/bin/bash", "-c", synthetic(True, 7) + " " + SELECTOR], env=outer, capture_output=True, text=True)
assert failed.returncode == 7
assert [json.loads(line)["phase"] for line in failed.stdout.splitlines()] == ["preflight"]
print("PASS: bash syntax, service serialization, 23 unchanged guards, source/oracle hashes, 59 body assertions, failure propagation")
```
