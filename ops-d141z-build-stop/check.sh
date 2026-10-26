#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP_ROOT=$(mktemp -d /tmp/d141z-check.XXXXXX)
export D141Z_ROOT="$ROOT" D141Z_TMP="$TMP_ROOT" PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT${PYTHONPATH:+$PYTHONPATH}"
python3 - <<'PY'
import hashlib, importlib.util, json, os, pathlib, signal, subprocess, sys, threading, time
root = pathlib.Path(os.environ["D141Z_ROOT"]); tmp = pathlib.Path(os.environ["D141Z_TMP"])
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("candidate", root / "run-final-delivery.py")
candidate = importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(candidate)
life = importlib.import_module("delivery_lifecycle")
donor_sampler = life.TRACE_SCRIPT


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def git(path, *args): return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()
def grun(path, *args): subprocess.run(["git", "-C", str(path), *args], check=True, stdout=subprocess.DEVNULL)


sampler = tmp / "sampler.py"
sampler.write_text(
    "import hashlib,os,signal,stat,sys,time\nfrom datetime import datetime,timezone\nfrom pathlib import Path\n"
    "trace,job,body,probe,ticks=sys.argv[1:]; mode=os.environ.get('D141Z_SAMPLER_MODE','normal'); stopping=False\n"
    "def stop(_s,_f):\n global stopping\n stopping=True\n"
    "signal.signal(signal.SIGTERM,stop); signal.signal(signal.SIGINT,stop); path=Path(trace); records=[]; current=Path('/')\n"
    "for component in path.parts[1:-1]:\n current/=component; item=current.stat(); records.append(f'{component}:{item.st_dev}:{item.st_ino}:{item.st_uid}:{stat.S_IMODE(item.st_mode):o}')\n"
    "parent=hashlib.sha256('|'.join(records).encode()).hexdigest(); fd=os.open(trace,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_CLOEXEC|getattr(os,'O_NOFOLLOW',0),0o600); item=os.fstat(fd)\n"
    "os.write(fd,b'timestamp_utc\\tmonotonic_ns\\tavailable_bytes\\tjob_id\\tbody_pid\\tkind\\n'); print(f'ready\\t{item.st_dev}\\t{item.st_ino}\\t{item.st_uid}\\t{stat.S_IMODE(item.st_mode):o}\\t{item.st_nlink}\\t{parent}',flush=True)\n"
    "def row(value,kind):\n stamp=time.monotonic_ns(); now=datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'); os.write(fd,f'{now}\\t{stamp}\\t{value}\\t{job}\\t{body}\\t{kind}\\n'.encode()); os.fsync(fd)\n"
    "row(3999999999 if mode=='lowbefore' else 5000000000,'first')\n"
    "if mode=='invalid': raise SystemExit(9)\n"
    "if mode=='lowduring': time.sleep(.08); row(3999999999,'periodic'); time.sleep(2)\n"
    "elif mode=='frozen': time.sleep(2)\n"
    "else: time.sleep(2 if mode=='normal' else 5.3)\n"
    "row(3999999999 if mode=='lowafter' else 5000000000,'final') if stopping else row(5000000000,'final'); os.close(fd)\n"
)
child = tmp / "child.py"
child.write_text("import os,signal,sys,time\nfrom pathlib import Path\np,m=sys.argv[1:]; Path(p).write_text(str(os.getpid())); signal.signal(signal.SIGTERM,signal.SIG_IGN if m=='ignore' else signal.SIG_DFL); time.sleep(30)\n")
tree_builder = tmp / "tree-builder.py"
tree_builder.write_text("import subprocess,sys,time\nc,p,m=sys.argv[1:]; cm='ignore' if m in {'ignore','leader-exit'} else m; q=subprocess.Popen([sys.executable,c,p,cm],start_new_session=True)\nif m=='normal': time.sleep(.15); q.terminate(); q.wait()\nelif m=='cadence': time.sleep(5.3); q.terminate(); q.wait()\nelif m=='leader-exit': raise SystemExit(0)\nelse: q.wait()\n")
wrapper = tmp / "wrapper.py"
wrapper.write_text("import subprocess,sys\nraise SystemExit(subprocess.call([sys.executable,sys.argv[1],*sys.argv[2:]],start_new_session=True))\n")

real_wrapper = pathlib.Path("/home/user/timeline-hub/hub/design/runtime-D141z-input-0812-delivery_gate_build.py")
core = tmp / "run-final-services.py"; inventory = tmp / "core-inventory.json"; builder = tmp / "builder.py"
core.write_text("# controlled source fixture\n"); inventory.write_text('{"fixture":true}\n')
builder.write_text("import os,time\ndef main_with_args(args):\n p=os.environ.get('D141Z_BUILDER_MARK'); p and open(p,'w').write('called\\n'); time.sleep(float(os.environ.get('D141Z_BUILDER_SLEEP','0'))); return 0\n")
candidate.CORE_RUNNER=core; candidate.CORE_RUNNER_SHA256=sha(core); candidate.CORE_INVENTORY_SHA256=sha(inventory); candidate.REVIEWED_WRAPPER_SHA256=sha(real_wrapper); candidate.REVIEWED_BUILDER_SHA256=sha(builder)

repos={}
for name in ("agent","runtime","app","composition"):
    repo=tmp/f"source-{name}"; repo.mkdir(); subprocess.run(["git","init","-q","--initial-branch=main",str(repo)],check=True)
    grun(repo,"config","user.name","D141z fixture"); grun(repo,"config","user.email","d141z@example.invalid")
    (repo/"fixture.txt").write_text(name+"\n"); grun(repo,"add","fixture.txt"); grun(repo,"commit","-q","-m","fixture")
    head=git(repo,"rev-parse","HEAD"); tree=git(repo,"rev-parse","HEAD^{tree}"); grun(repo,"branch","origin/main"); grun(repo,"branch","tl/integration"); repos[name]=(repo,head,tree)
source=tmp/"source.json"; gate=tmp/"gate.json"
source.write_text(json.dumps({n:{"root":str(r),"sha":h,"tree":t} for n,(r,h,t) in repos.items()},sort_keys=True)+"\n")
gate.write_text(json.dumps({"version":1,"repos":{n:{"root":str(r),"base_ref":"origin/main","gate_ref":"tl/integration","upstream_base":h,"upstream_base_tree":t,"gated_tip":h,"gated_tree":t} for n,(r,h,t) in repos.items()}},sort_keys=True)+"\n")
main_case=tmp/"actual-main"; main_case.mkdir(); mark=main_case/"builder-called"; os.environ["D141Z_BUILDER_MARK"]=str(mark); receipt=main_case/"receipt.json"
os.environ["TMPDIR"] = os.environ["TMP"] = os.environ["TEMP"] = str(main_case)
assert candidate.main(["--source-tuple",str(source),"--tuple-sha",sha(source),"--gate-tuple",str(gate),"--gate-tuple-sha",sha(gate),"--wrapper",str(real_wrapper),"--wrapper-sha",sha(real_wrapper),"--builder",str(builder),"--builder-sha",sha(builder),"--receipt",str(receipt),"--","--harmless"]) == 0
main_receipt = json.loads(receipt.read_text())
assert mark.is_file() and main_receipt["status"] == "PASS" and main_receipt["wrapper"]["receipt"]["status"] == "PASS"


def gone(pidfile):
    if not pidfile.exists(): return
    pid=int(pidfile.read_text())
    for _ in range(300):
        if not pathlib.Path(f"/proc/{pid}").exists(): return
        time.sleep(.02)
    raise AssertionError(f"descendant {pid} survived stop")


def case(name, mode, expected, timeout=1.0, sampler_path=None, stale=15.0):
    d=tmp/name; d.mkdir(); pid=d/"child.pid"; life.TRACE_SCRIPT=pathlib.Path(sampler_path or sampler); life.SAMPLER_STALE_SECONDS=stale; os.environ["D141Z_SAMPLER_MODE"]=mode
    assert candidate.run_delivery.__globals__["TRACE_SCRIPT"] == pathlib.Path(sampler_path or sampler), (name, candidate.run_delivery.__globals__["TRACE_SCRIPT"])
    code,_=candidate.run_wrapper([sys.executable,str(wrapper),str(tree_builder),str(child),str(pid),mode],d,timeout_seconds=timeout)
    record=json.loads((d/"timeline-delivery-KEEP"/"lifecycle.json").read_text()); assert code==expected,(name,code,record); assert (d/"timeline-delivery-KEEP"/"KEEP").is_file(), name
    if expected in {75,124,125,130,143}: assert record["status"] in {"stopped","unknown","refused"}, (name,record); gone(pid)
    return record

case("normal","normal",0); case("early-leader-live-descendant","leader-exit",124,.3); case("low-before","lowbefore",75); case("low-during","lowduring",75)
fakebin=tmp/"bin"; fakebin.mkdir(); (fakebin/"df").write_text("#!/bin/sh\nif [ \"${D141Z_DF_MODE:-}\" = lowafter ]; then printf 'Avail\\n3999999999\\n'; else printf 'Avail\\n5000000000\\n'; fi\n"); (fakebin/"df").chmod(0o755)
old_path=os.environ["PATH"]; os.environ["PATH"]=str(fakebin)+os.pathsep+old_path; os.environ["D141Z_DF_MODE"]="lowafter"; case("low-after","normal",75); os.environ.pop("D141Z_DF_MODE"); os.environ["PATH"]=old_path
invalid_sampler=tmp/"invalid-sampler.py"; invalid_sampler.write_text(sampler.read_text().replace("if mode=='invalid': raise SystemExit(9)", "os.write(fd,b'bad\\n'); os.fsync(fd); time.sleep(2)"))
case("sampler-invalid","normal",125,sampler_path=invalid_sampler); case("sampler-frozen","ignore",125,stale=.1); case("sampler-missing","normal",125,sampler_path=tmp/"missing.py"); case("timeout","ignore",124,.15)
cancel=tmp/"cancel"; cancel_case=tmp/"cancel-case"; cancel_case.mkdir(); threading.Timer(.2,lambda:cancel.write_text("cancel\n")).start()
code,_=candidate.run_wrapper([sys.executable,str(wrapper),str(tree_builder),str(child),str(cancel_case/"child.pid"),"ignore"],cancel_case,cancel_path=cancel,timeout_seconds=10); assert code==130; gone(cancel_case/"child.pid")
for sig,expected,name in ((signal.SIGTERM,143,"sigterm"),(signal.SIGINT,130,"sigint")):
    d=tmp/name; d.mkdir(); threading.Timer(.2,lambda sig=sig:os.kill(os.getpid(),sig)).start(); code,_=candidate.run_wrapper([sys.executable,str(wrapper),str(tree_builder),str(child),str(d/"child.pid"),"ignore"],d,timeout_seconds=10); assert code==expected; gone(d/"child.pid")
record=case("actual-5s-trace","cadence",0,8,sampler_path=donor_sampler); rows=pathlib.Path(record["trace"]).read_text().splitlines(); assert any(r.split("\t")[-1]=="periodic" for r in rows[1:]); assert record["trace_status"]=="PASS" and record["reaped_pids"]

custody=tmp/"custody-replacement"; custody.mkdir(); life.TRACE_SCRIPT=sampler; os.environ["D141Z_SAMPLER_MODE"]="normal"; trace=custody/"timeline-delivery-KEEP"/"disk-trace.tsv"
def replace():
    for _ in range(100):
        if trace.exists(): trace.unlink(); trace.symlink_to(tmp/"attacker-trace"); return
        time.sleep(.01)
threading.Thread(target=replace,daemon=True).start(); code,_=candidate.run_wrapper([sys.executable,str(wrapper),str(tree_builder),str(child),str(custody/"child.pid"),"ignore"],custody,timeout_seconds=10); assert code==125; gone(custody/"child.pid")
print("D141z acceptance PASS: actual main/D68 wrapper, dispatcher-owned caller, early leader/orphan, TERM/KILL/reap, low disk before/during/after, invalid/stale/missing sampler, timeout, signals/cancel, donor 5s trace, immutable binding, append-final --fd, KEEP, and source guards")
PY
