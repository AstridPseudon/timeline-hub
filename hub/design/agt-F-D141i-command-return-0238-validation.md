# F/D141i corrected command validation

## Commands run

```text
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-command-return-0238/evidence/measurement-command.sh
=> PASS

/home/user/work/venv-agent/bin/python -P <stdlib validator over evidence>
=> PASS: JSON parsing, exact positive/poison one-field delta, source tuple
   commit/tree/origin/clean checks, physical source/hash readbacks, exact 22
   roots and preserved pytest settings, JUnit argv/path join, distinct input
   and launcher-output roots, and python shutil.disk_usage(...).free floor.

sha256sum measurement-command.sh positive.manifest poison.manifest source-manifest.json
=> PASS: command=87384df6e825af2e211b67135ec944aa51f855251e195bb955a8832c92ab0381;
   positive=94d8d5813c7f96259547bc273cad388d6fefe60126c33fc5faa68385c56f8707;
   poison=c1e9ae00cc7c4b94262b9277f3079e1234524d90610cbe807945961d5379fb4c;
   source=773d23da50a9212b137ec3a8f3228fea69b206f372e9fad9d25b4c720b70f0c1.

env P4_D73_EVIDENCE=/tmp/w-636cd0a924/d141i-command-return-0238-final/positive \
  P4_D73_REQUEST_ID=agent-core-full-positive-final \
  P4_STUB_COUNT=<fresh-control>/positive/stub.count \
  /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh \
  <this packet>/positive.manifest dry -- <retained positive stub>
=> PASS exit 17; launcher preflight exit 0; exactly one stub counter line.

env P4_D73_EVIDENCE=/tmp/w-636cd0a924/d141i-command-return-0238-final/poison \
  P4_D73_REQUEST_ID=agent-core-full-poison-final \
  P4_STUB_COUNT=<fresh-control>/poison/stub.count \
  /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh \
  <this packet>/poison.manifest dry -- <retained positive stub>
=> PASS expected refusal exit 1; `D73 launcher: agent SHA mismatch`; stub/counter 0.

<actual authored die()/available_bytes()/record_disk() helper controls>
=> PASS default refusal 78; explicit refusal 83; disk read failure 97;
   disk trace write failure 98. No pytest/import/provider/body was run.
```

## Not run

No measurement body, pytest, collection, provider/product body, request-test,
installation, suite registration, queue/admission operation, REG join, or ship
credit operation was run. The later normal service controller remains outside
this task.
