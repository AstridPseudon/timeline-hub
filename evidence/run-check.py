import os, pathlib, shlex, subprocess, sys, time
name, *command = sys.argv[1:]
evidence = pathlib.Path(os.environ["POPUP_EVIDENCE"])
start = time.monotonic()
with (evidence / (name + ".log")).open("w") as output:
    result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT)
(evidence / (name + ".exit")).write_text(str(result.returncode) + "\n")
with (evidence / "commands.txt").open("a") as output:
    output.write(f"{name}: cwd={os.getcwd()}\n{shlex.join(command)}\nexit={result.returncode}, seconds={time.monotonic()-start:.2f}\n\n")
print(name, "exit", result.returncode, flush=True)
print((evidence / (name + ".log")).read_text()[-5000:])
sys.exit(result.returncode)
