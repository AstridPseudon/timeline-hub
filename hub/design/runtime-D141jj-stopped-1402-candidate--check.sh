#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP_ROOT=$(mktemp -d "${TMPDIR:?worker TMPDIR required}/d141z-check.XXXXXX")
export D141Z_ROOT="$ROOT" D141Z_TMP="$TMP_ROOT" PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT${PYTHONPATH:+$PYTHONPATH}"
python3 - <<'PY'
import fcntl, hashlib, importlib.util, json, os, pathlib, signal, subprocess, sys, threading, time
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
    "row((4000000000 if mode=='equalbefore' else 3999999999) if mode in {'lowbefore','equalbefore'} else 5000000000,'first')\n"
    "if mode=='invalid': raise SystemExit(9)\n"
    "if mode in {'lowduring','equalduring'}: time.sleep(.08); row(4000000000 if mode=='equalduring' else 3999999999,'periodic'); time.sleep(2)\n"
    "elif mode=='stale': os.utime(fd,(time.time()-30,time.time()-30)); time.sleep(2)\n"
    "elif mode=='frozen': time.sleep(2)\n"
    "else: time.sleep(2 if mode=='normal' else 5.3)\n"
    "row(3999999999 if mode=='lowafter' else 5000000000,'final') if stopping else row(5000000000,'final'); os.close(fd)\n"
)
child = tmp / "child.py"
child.write_text("import os,signal,sys,time\nfrom pathlib import Path\np,m=sys.argv[1:]; signal.signal(signal.SIGTERM,signal.SIG_IGN if m=='ignore' else signal.SIG_DFL); Path(p).write_text(str(os.getpid())); time.sleep(30)\n")
tree_builder = tmp / "tree-builder.py"
tree_builder.write_text("import subprocess,sys,time\nc,p,m=sys.argv[1:]; cm='ignore' if m in {'ignore','leader-exit'} else m; q=subprocess.Popen([sys.executable,c,p,cm],start_new_session=True)\nif m=='normal': time.sleep(.15); q.terminate(); q.wait()\nelif m=='cadence': time.sleep(5.3); q.terminate(); q.wait()\nelif m=='leader-exit': raise SystemExit(0)\nelse: q.wait()\n")
wrapper = tmp / "wrapper.py"
wrapper.write_text("import subprocess,sys\nraise SystemExit(subprocess.call([sys.executable,sys.argv[1],*sys.argv[2:]],start_new_session=True))\n")

real_wrapper = root / "delivery_gate_build.py"
core = tmp / "run-final-services.py"; inventory = tmp / "core-inventory.json"; builder = tmp / "builder.py"
core.write_text("# controlled source fixture\n"); inventory.write_text('{"fixture":true}\n')
builder.write_text("import os,subprocess,sys,time\nfrom pathlib import Path\ndef main_with_args(args):\n mode=os.environ.get('D141Z_TREE_MODE'); q=None\n if mode:\n  q=subprocess.Popen([sys.executable,os.environ['D141Z_CHILD'],os.environ['D141Z_CHILD_PID'],'ignore'],start_new_session=True)\n  while not Path(os.environ['D141Z_CHILD_PID']).exists(): time.sleep(.01)\n p=os.environ.get('D141Z_BUILDER_MARK'); p and Path(p).write_text('called\\n')\n if mode=='leader-exit': return 0\n if q is not None: return q.wait()\n time.sleep(float(os.environ.get('D141Z_BUILDER_SLEEP','0'))); return 0\n")
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
candidate.APP_UPSTREAM_BASE, candidate.APP_UPSTREAM_TREE = repos["app"][1], repos["app"][2]
main_case=tmp/"actual-main"; main_case.mkdir(); mark=main_case/"builder-called"; os.environ["D141Z_BUILDER_MARK"]=str(mark); receipt=main_case/"receipt.json"
os.environ["TMPDIR"] = os.environ["TMP"] = os.environ["TEMP"] = str(main_case)
main_args=["--source-tuple",str(source),"--tuple-sha",sha(source),"--gate-tuple",str(gate),"--gate-tuple-sha",sha(gate),"--wrapper",str(real_wrapper),"--wrapper-sha",sha(real_wrapper),"--builder",str(builder),"--builder-sha",sha(builder),"--receipt",str(receipt),"--","--harmless"]
assert candidate.main(main_args) == 0
main_receipt = json.loads(receipt.read_text())
assert mark.is_file() and main_receipt["status"] == "PASS" and main_receipt["wrapper"]["receipt"]["status"] == "PASS"


def gone(pidfile):
    if not pidfile.exists(): return
    pid=int(pidfile.read_text())
    for _ in range(300):
        if not pathlib.Path(f"/proc/{pid}").exists(): return
        time.sleep(.02)
    raise AssertionError(f"descendant {pid} survived stop")


local_cases=[]
def case(name, mode, expected, timeout=1.0, sampler_path=None, stale=15.0):
    d=tmp/name; d.mkdir(); pid=d/"child.pid"; life.TRACE_SCRIPT=pathlib.Path(sampler_path or sampler); life.SAMPLER_STALE_SECONDS=stale; os.environ["D141Z_SAMPLER_MODE"]=mode
    assert candidate.run_delivery.__globals__["TRACE_SCRIPT"] == pathlib.Path(sampler_path or sampler), (name, candidate.run_delivery.__globals__["TRACE_SCRIPT"])
    code,_=candidate.run_wrapper([sys.executable,str(wrapper),str(tree_builder),str(child),str(pid),mode],d,timeout_seconds=timeout)
    record=json.loads((d/"timeline-delivery-KEEP"/"lifecycle.json").read_text()); assert code==expected,(name,code,record); assert (d/"timeline-delivery-KEEP"/"KEEP").is_file(), name
    if expected in {75,124,125,130,143}: assert record["status"] in {"stopped","unknown","refused"}, (name,record); gone(pid)
    local_cases.append(name)
    return record

case("normal","normal",0); case("early-leader-live-descendant","leader-exit",124,.3); case("low-before","lowbefore",75); case("low-during","lowduring",75)
for name,mode in (("equal-before","equalbefore"),("equal-during","equalduring")):
    result=case(name,mode,75)
    if name=="equal-before": assert not (tmp/name/"child.pid").exists(), result
fakebin=tmp/"bin"; fakebin.mkdir(); (fakebin/"df").write_text("#!/bin/sh\nif [ \"${D141Z_DF_MODE:-}\" = lowafter ]; then printf 'Avail\\n3999999999\\n'; else printf 'Avail\\n5000000000\\n'; fi\n"); (fakebin/"df").chmod(0o755)
old_path=os.environ["PATH"]; os.environ["PATH"]=str(fakebin)+os.pathsep+old_path; os.environ["D141Z_DF_MODE"]="lowafter"; case("low-after","normal",75)
(fakebin/"df").write_text("#!/bin/sh\nprintf 'Avail\\n4000000000\\n'\n"); case("equal-after","normal",75)
os.environ.pop("D141Z_DF_MODE"); os.environ["PATH"]=old_path
invalid_sampler=tmp/"invalid-sampler.py"; invalid_sampler.write_text(sampler.read_text().replace("if mode=='invalid': raise SystemExit(9)", "os.write(fd,b'bad\\n'); os.fsync(fd); time.sleep(2)"))
case("sampler-invalid","normal",125,sampler_path=invalid_sampler); case("sampler-frozen","ignore",125,stale=.1); case("sampler-stale","stale",125); case("sampler-missing","normal",125,sampler_path=tmp/"missing.py"); case("timeout","ignore",124,.15)
case("sampler-failed","invalid",125)
malformed_sampler=tmp/"malformed-sampler.py"; malformed_sampler.write_text("print('ready\\tbad',flush=True)\n")
case("sampler-malformed-binding","normal",125,sampler_path=malformed_sampler)
life.TRACE_SCRIPT=sampler
cancel=tmp/"cancel"; cancel_case=tmp/"cancel-case"; cancel_case.mkdir(); threading.Timer(.2,lambda:cancel.write_text("cancel\n")).start()
code,_=candidate.run_wrapper([sys.executable,str(wrapper),str(tree_builder),str(child),str(cancel_case/"child.pid"),"ignore"],cancel_case,cancel_path=cancel,timeout_seconds=10); assert code==130; gone(cancel_case/"child.pid")
for sig,expected,name in ((signal.SIGTERM,143,"sigterm"),(signal.SIGINT,130,"sigint")):
    d=tmp/name; d.mkdir(); threading.Timer(.2,lambda sig=sig:os.kill(os.getpid(),sig)).start(); code,_=candidate.run_wrapper([sys.executable,str(wrapper),str(tree_builder),str(child),str(d/"child.pid"),"ignore"],d,timeout_seconds=10); assert code==expected; gone(d/"child.pid")
record=case("actual-5s-trace","cadence",0,8,sampler_path=donor_sampler); rows=pathlib.Path(record["trace"]).read_text().splitlines(); assert rows[1].endswith("\tfirst") and rows[-1].endswith("\tfinal") and any(r.split("\t")[-1]=="periodic" for r in rows[1:]); assert record["trace_status"]=="PASS" and record["reaped_pids"]

custody=tmp/"custody-replacement"; custody.mkdir(); life.TRACE_SCRIPT=sampler; os.environ["D141Z_SAMPLER_MODE"]="normal"; trace=custody/"timeline-delivery-KEEP"/"disk-trace.tsv"
def replace():
    for _ in range(100):
        if trace.exists(): trace.unlink(); trace.symlink_to(tmp/"attacker-trace"); return
        time.sleep(.01)
threading.Thread(target=replace,daemon=True).start(); code,_=candidate.run_wrapper([sys.executable,str(wrapper),str(tree_builder),str(child),str(custody/"child.pid"),"ignore"],custody,timeout_seconds=10); assert code==125; gone(custody/"child.pid")
print("PASS local lifecycle controls: main/D68 stub, early leader/orphan, TERM/KILL/reap, low/equal disk before/during/after, sampler faults, timeout/signals/local cancel, donor 5s trace, descriptor custody")

# Run the qualified lease supervisor verbatim; no native supervision doubles,
# live dispatcher, snapshot, registration, admission, or heavy body is invoked.
donor=donor_sampler.parent/"test-run"
donor_text=donor.read_text()
assert sha(donor)=="f674569b4935ee03022fa209ec102f6323dce80b40be726f44b9698acbaf1300"
lease_source=donor_text.split("<<'BENCH_LEASE_PY'\n",1)[1].split("\nBENCH_LEASE_PY",1)[0]
lease_source=lease_source[:lease_source.index("\ndef main():")]
body_source=donor_text[donor_text.index('if [ -n "$BENCH_CONTROL_FD" ]; then'):donor_text.index('[ -n "$LEASED" ] && exit "$RC"')]+ '\nexit "$RC"\n'
body=tmp/"lease-body.sh"; body.write_text(body_source)
config=tmp/"main-config.json"
config.write_text(json.dumps({"args":main_args,"core":str(core),"inventory":str(inventory),"wrapper":str(real_wrapper),"builder":str(builder),"app_base":repos["app"][1],"app_tree":repos["app"][2]}))
driver=tmp/"main-driver.py"
driver.write_text('''import hashlib,importlib.util,json,os,sys
from pathlib import Path
sys.path.insert(0,os.environ["D141Z_ROOT"])
spec=importlib.util.spec_from_file_location("candidate",Path(os.environ["D141Z_ROOT"])/"run-final-delivery.py")
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
v=json.loads(Path(sys.argv[1]).read_text()); d=Path(os.environ["D141Z_CASE"])
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
c.APP_UPSTREAM_BASE=v["app_base"]; c.APP_UPSTREAM_TREE=v["app_tree"]
c.CORE_RUNNER=Path(v["core"]); c.CORE_RUNNER_SHA256=sha(v["core"]); c.CORE_INVENTORY_SHA256=sha(v["inventory"])
c.REVIEWED_WRAPPER_SHA256=sha(v["wrapper"]); c.REVIEWED_BUILDER_SHA256=sha(v["builder"])
args=v["args"]; args[args.index("--receipt")+1]=str(d/"receipt.json")
try: result=c.main(args)
except Exception as exc:
 print(str(exc),file=sys.stderr); result=125
raise SystemExit(result)
''')
supervisor=tmp/"lease-supervisor.py"
supervisor.write_text(lease_source+'''
orch,root,tests,case,body=sys.argv[1:]
spec=importlib.util.spec_from_file_location("bench_store",Path(orch)/"bench_store.py")
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
store=module.Store(Path(root),Path(tests)); d=Path(case)
result=supervise(store,"composition","controlled-delivery",os.environ["CMD"],["bash",body],d/"CANCELLED",os.getppid(),Path(tests))
(d/"lease-result").write_text(str(result))
raise SystemExit(result)
''')

store_spec=importlib.util.spec_from_file_location("bench_store_fixture",donor.parent/"bench_store.py")
store_module=importlib.util.module_from_spec(store_spec); store_spec.loader.exec_module(store_module)
tests=tmp/"lease-tests"; tests.mkdir(); store_root=tmp/"tiny-lease-fixture"
store=store_module.Store.initialize(store_root,tests)
identity={"remotion_tree":"0"*40}; key=store_module.key_for("runtime",identity); eid="runtime-"+key
entry_path=store_root/"entries"/eid; entry_path.mkdir(); lock=store_root/"locks"/eid; lock.touch(mode=0o600)
entry={"component":"runtime","key":key,"identity":identity,"path":str(entry_path),"seq":1,"lock":store_module.inode(lock),"node":store_module.inode(entry_path),"owner":store.owner["id"]}
(entry_path/".bench-owner.json").write_text(store_module.canonical({k:entry[k] for k in ("owner","component","key","identity")}))
command=" ".join([sys.executable,str(driver),str(config)])
reg={"env":"","suite":"composition controlled-delivery "+command+"\n","requires":[eid]}; reg["hash"]=store_module.digest(store_module.canonical(reg))
(tests/"suites.conf").write_text(reg["suite"])
index={"version":1,"seq":1,"entries":{eid:entry},"registrations":{"fixture":reg},"retired":[],"retired_suites":[]}
(store_root/"index.json").write_text(store_module.canonical(index))
assert store.names_for_suite("composition","controlled-delivery",command)==["fixture"]


def await_file(path, process=None):
    deadline=time.monotonic()+12
    while not path.exists():
        assert process is None or process.poll() is None, (path,process.returncode)
        assert time.monotonic()<deadline, path
        time.sleep(.02)


def lease_locked(expected):
    fd=os.open(lock,os.O_RDWR)
    try:
        try: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: assert expected; return
        assert not expected,"lease released while builder descendant was alive"
    finally: os.close(fd)


for mode in ("mounted-cancel","outer-parent-death","early-leader-mounted-cancel","normal-eof"):
    d=tmp/mode; d.mkdir(); pid=d/"child.pid"
    env=dict(os.environ,TMPDIR=str(d),TMP=str(d),TEMP=str(d),D141Z_CASE=str(d),D141Z_BUILDER_MARK=str(d/"builder-called"),D141Z_TREE_MODE="leader-exit" if mode.startswith("early") else "ignore",D141Z_CHILD=str(child),D141Z_CHILD_PID=str(pid),D=str(d),SNAP=str(d),CMD=command)
    if mode=="normal-eof": env.pop("D141Z_TREE_MODE")
    argv=[sys.executable,str(supervisor),str(donor.parent),str(store_root),str(tests),str(d),str(body)]
    log=(d/"control.log").open("w")
    if mode=="outer-parent-death":
        launcher=tmp/"parent.py"
        launcher.write_text("import subprocess,sys,time\nfrom pathlib import Path\np=subprocess.Popen(sys.argv[2:]); Path(sys.argv[1]).write_text(str(p.pid)); time.sleep(60)\n")
        parent=subprocess.Popen([sys.executable,str(launcher),str(d/"supervisor.pid"),*argv],env=env,stdout=log,stderr=subprocess.STDOUT)
        await_file(d/"supervisor.pid",parent)
        supervisor_pid=int((d/"supervisor.pid").read_text())
    else:
        parent=subprocess.Popen(argv,env=env,stdout=log,stderr=subprocess.STDOUT)
    try:
        await_file(d/"builder-called",parent)
        if mode!="normal-eof":
            await_file(pid,parent); lease_locked(True)
            if mode=="outer-parent-death": parent.kill(); parent.wait(timeout=3)
            else: (d/"CANCELLED").write_text("mounted dispatcher cancellation fixture\n")
        await_file(d/"lease-result")
        if mode=="outer-parent-death":
            waited,status=os.waitpid(supervisor_pid,0); assert waited==supervisor_pid and os.waitstatus_to_exitcode(status)==130
        else: assert parent.wait(timeout=10)==(0 if mode=="normal-eof" else 130), (mode,(d/"control.log").read_text())
        assert int((d/"lease-result").read_text())==(0 if mode=="normal-eof" else 130)
        gone(pid); lease_locked(False)
        lifecycle=list(d.rglob("lifecycle.json")); assert len(lifecycle)==1,(mode,lifecycle)
        value=json.loads(lifecycle[0].read_text()); assert value["trace_status"]=="PASS",value
        if mode!="normal-eof": assert value["status"]=="stopped" and value["reaped_pids"],value
        print("PASS",mode,"exact donor lease/CANCELLED/control-pipe/PDEATHSIG -> main -> D68 -> stub; lease held until reap")
    finally:
        if parent.poll() is None: parent.terminate(); parent.wait(timeout=12)
        log.close()

d=tmp/"caller-parent-death"; d.mkdir(); log=(d/"control.log").open("w")
env=dict(os.environ,TMPDIR=str(d),TMP=str(d),TEMP=str(d),D141Z_CASE=str(d),D141Z_BUILDER_MARK=str(d/"builder-called"),D141Z_TREE_MODE="ignore",D141Z_CHILD=str(child),D141Z_CHILD_PID=str(d/"child.pid"))
parent=subprocess.Popen([sys.executable,str(launcher),str(d/"caller.pid"),sys.executable,str(driver),str(config)],env=env,stdout=log,stderr=subprocess.STDOUT)
await_file(d/"caller.pid",parent); await_file(d/"builder-called",parent)
caller_pid=int((d/"caller.pid").read_text()); parent.kill(); parent.wait(timeout=3)
await_file(d/"receipt.json")
waited,status=os.waitpid(caller_pid,0); assert waited==caller_pid and os.waitstatus_to_exitcode(status)==130
gone(d/"child.pid"); value=json.loads(next(d.rglob("lifecycle.json")).read_text())
assert value["stop_reason"]=="parent_died" and value["trace_status"]=="PASS" and value["reaped_pids"],value
log.close(); print("PASS caller-parent-death PR_SET_PDEATHSIG and getppid -> D68/stub groups KILL/wait/reap")

# A still-open caller control writer advertises the actual D68 group; a reader
# closed before advertisement fails closed. EOF after the body advertisement is
# normal donor protocol and is covered by normal-eof above.
life.TRACE_SCRIPT=donor_sampler
for closed in (False,True):
    d=tmp/("control-reader-closed" if closed else "control-advertise"); d.mkdir()
    read_fd,write_fd=os.pipe2(os.O_CLOEXEC|os.O_NONBLOCK)
    if closed: os.close(read_fd)
    env=dict(os.environ,BENCH_CONTROL_FD=str(write_fd))
    try:
        code,_,value=life.run_delivery([sys.executable,"-c","import time;time.sleep(.2)"],d,env=env)
        assert code==(130 if closed else 0),(code,value)
        if not closed:
            advertised=int(os.read(read_fd,100).strip()); assert advertised in value["process_groups"]
        else: assert value["stop_reason"]=="control_pipe_closed"
    finally:
        os.close(write_fd)
        if not closed: os.close(read_fd)
    print("PASS",d.name,"actual inherited BENCH_CONTROL_FD")

guard_count=0
for path in (core,inventory,builder,source,gate):
    original=path.read_bytes(); path.write_bytes(original+b"\npoisoned\n")
    try:
        try: candidate.main(main_args)
        except ValueError: guard_count+=1
        else: raise AssertionError(("guard accepted poison",path))
    finally: path.write_bytes(original)
print("PASS",guard_count,"main source/inventory/builder/tuple/gate hash refusal controls")
print("D141z purpose counts:",json.dumps({"local_lifecycle":len(local_cases)+4,"mounted_donor_lease":4,"direct_parent_death":1,"inherited_control_pipe":2,"main_normal":1,"main_guard_refusals":guard_count},sort_keys=True))
print("D141z mounted acceptance PASS; genuine F1/dispatch admission/install remain unverified")
PY
