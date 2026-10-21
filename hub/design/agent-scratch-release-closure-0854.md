# Agent scratch release closure

Date: 2026-10-21 UTC  
Scope: lossless release of the two finished scratch records named by the
08:50 lead note. No scratch directory was deleted, compacted, recycled, or
mutated by this task.

## Release result

**RELEASED — private311 typing scratch**

Exact path:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-gate7-private311-mypy-once/gate7-private311-source8afe`

Predicates:

- Finished record: yes. The historical source8afe run is retained as
  **UNKNOWN**, with no child exit/status or diagnostic; it is not a prerequisite.
  The later current-source proof is durable: source `de36e302`, tree
  `3cafb945`, unchanged `make ... mypy`, exit 2, 2075 findings versus the
  1979 baseline (+96). Configuration, baseline, Python 3.11 environment,
  Runtime95 lock, stubs, imports, wheels, and disk checks passed.
- Consumers: no queued/running test, suite, or process names this exact path.
  The obsolete `gate7-private311-mypy-capture-current` suite registration
  was retired after its recorded fail result; no result was discarded.
- Durable evidence: the failed current result, historical UNKNOWN status,
  exact source/result classification, and the private311 dependency/wheel
  inventory are retained in the prior Gate7 reports and this closure.
- Private311 inventory retained for reconstruction/diagnosis: historical
  source `8afe5a87dfe093ac5efd017106acb03cc597509c`, tree
  `9eac28e8ac1d24d2020c9b3700ea54ddef5812cd`; Runtime95
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`; Agent runtime-lock SHA-256
  `7a05eb67ba9aa2efbcb81ba57225351abf0456e63b67110e5fe75cec16732cb5`;
  64 hashed Runtime-lock wheels; NumPy 2.4.6 wheel SHA-256
  `89cd468399cfd2504718f0ba50e410dca55a170b61a02ad92bb18c8a65186e93`;
  Agent wheel `585a10fb33821f5babf71089086e847a869ac8d9eca59fd76c18bc82ea1f0751`;
  Runtime wheel `5236bc9dadb51190403b1a61b7e3ea2467f7d221f8532844197dad9c01e4ec78`;
  client wheel `837ce7218ea177eccd036373c900e5f2f27ad0f60f05d945e4feafb3f11add28`;
  test-only `types-PyYAML 6.0.12.20260906` wheel SHA-256
  `bca893ff0d51df5c9053137d5d0e6ccd36e939a196356f1d5c16372422f5137b`.
- Safe finished path: the current coherent `f4edcb4b` profile below; no
  future task should use source8afe as an active prerequisite.

**RELEASED — coherent-pair staging scratch**

Exact path:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-private-coherent-pair-staging/profile-staging`

Predicates:

- Finished record: yes. The prior staged wrapper evidence remains preserved:
  lifecycle wrapper 7 passed, and two-network wrapper 2 passed, against Agent
  tree `698ae4df`. These wrappers were historical evidence, not a current
  prerequisite.
- Current consumer: the final builder
  `agt-m4-d13-final-current-wheel-profile-build-0851` reached `ended`,
  `DONE`, exit 0 at 08:58:27 UTC. Its final source/profile is the new
  `f4edcb4b` path; no active builder/test/process now reads
  `profile-staging`. A /proc command-line scan after worker termination
  found no actual process containing `profile-staging`,
  `private-profile-f4edcb4b`, or `gate7-private311-source8afe`.
- Consumers: no queued/running test request remains for either old coherent
  wrapper. Both dormant suite registrations were retired after preserving
  their exact pass summaries.
- Ancestry: pin `6efc8150` remains untouched; read-only Git verification shows
  it is an ancestor of current source `f4edcb4b). No pin/tree was deleted.
- Safe finished path: the final private profile below. Do not treat the old
  installed `6f2d8c` profile as current source authority.

## Durable final profile / inventories

Final source authority is commit
`f4edcb4bce531be3ea8c6389069429175b048c2a`, tree
`1cbd18011b56c41a5ef31f155c15bd373c1208e6`, with exact parents
`5be2918c45909abcf0c91b79b53a2ce73eed83b1` and
`566307478f43672db23f84fda2a478bb6116a008`. The nine approved D13 paths
match the 5be blobs and all other paths match current 566. The stopped 0844
builder/old Agent wheel is not source authority.

Final private root:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-final-current-wheel-profile-build-0851/private-profile-f4edcb4b`

Interpreter:
`.../private-profile-f4edcb4b/venv/bin/python`, CPython 3.13.16.

Wheel inventory (final profile):

- Agent 0.1.0:
  `astrid-0.1.0-py3-none-any.whl`,
  SHA-256 `7455220aa1d3f8c67c7c9cee0f7a6571fb4f51882eca2543ead25943eebd185a`.
- Runtime 0.1.0, compatible b92:
  SHA-256 `12df54644e1acac46b9c396135ef345808a98515965f1f12f479f32adf3c9b0a`.
- Runtime client 0.2.14, published 95/all76:
  SHA-256 `567605b13254f88ddeddad7b570553a2c50b5092908e6c4153553f9867e37254`.

Exact 164-entry dependency constraint inventory (unchanged; SHA-256
`478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`):

```text
agent-detector==2.0.0
aiodns==4.0.4
aiofiles==25.1.0
aiohappyeyeballs==2.7.1
aiohttp==3.14.5
aiohttp-retry==2.9.1
aioquic==1.7.0
aiosignal==1.4.0
annotated-doc==0.0.5
annotated-types==0.8.0
anthropic==1.0.0
anyio==4.14.2
astrid @ file:///home/user/work/wt/.orch-astrid-d8749a9c
asyncstdlib==3.14.0
attrs==26.1.0
backoff==2.2.1
backports.zstd==1.8.0
banodoco-timeline-schema @ git+https://github.com/banodoco/ArtAgents.git@242f9c4306bf3b501222cb041a9eb246ef47bc85#subdirectory=packages/timeline-schema/python
bcrypt==5.0.0
boto3==1.43.114
botocore==1.43.114
brotli==1.2.0
build==1.4.0
certifi==2026.7.22
cffi==2.1.1
charset-normalizer==3.5.1
click==8.4.2
colorama==0.4.6
coverage==7.16.2
cryptography==50.0.0
detect-installer==0.2.1
distro==1.9.0
dnspython==2.9.0
docstring_parser==0.18.0
email-validator==2.3.0
execnet==2.1.2
fal_client==1.0.1
fastapi==0.149.0
fastapi-cli==0.0.32
fastapi-cloud-cli==0.26.0
fastar==0.12.0
filelock==3.32.4
fonttools==4.67.0
frozenlist==1.8.0
google-auth==2.56.3
google-genai==2.19.0
googleapis-common-protos==1.75.5
h11==0.16.0
httpcore==1.0.9
httpcore2==2.12.0
httptools==0.9.0
httpx==0.28.1
httpx-sse==0.4.3
httpx2==2.12.0
idna==3.19
iniconfig==2.3.1
inquirerpy==0.3.4
invoke==3.0.3
itsdangerous==2.2.0
jaraco.classes==3.4.0
jaraco.context==6.1.2
jaraco.functools==4.6.0
jeepney==0.9.0
Jinja2==3.1.6
jiter==0.16.0
jmespath==1.1.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
keyring==25.7.0
markdown-it-py==4.2.0
MarkupSafe==3.0.4
mdurl==0.1.2
more-itertools==11.1.0
msgpack==1.2.1
multidict==7.1.0
mypy==1.17.0
mypy_extensions==1.1.0
numpy==2.5.2
openai==2.54.0
opencv-python-headless==5.0.0.93
opentelemetry-api==1.45.1
opentelemetry-exporter-http-transport==0.66b1
opentelemetry-exporter-otlp-common==0.66b1
opentelemetry-exporter-otlp-proto-common==1.45.1
opentelemetry-exporter-otlp-proto-http==1.45.1
opentelemetry-proto==1.45.1
opentelemetry-sdk==1.45.1
opentelemetry-semantic-conventions==0.66b1
packaging==26.3
paramiko==5.1.0
pathspec==1.1.1
pfzy==0.3.4
pillow==12.3.0
pip==26.2.1
platformdirs==4.11.3
pluggy==1.7.0
prettytable==3.18.0
prompt_toolkit==3.0.53
propcache==0.5.4
protobuf==7.36.2
psutil==7.2.2
py-cpuinfo==9.0.0
pyasn1==0.6.4
pyasn1_modules==0.4.2
pycares==5.2.0
pycparser==3.0
pydantic==2.13.4
pydantic-extra-types==2.11.1
pydantic-settings==2.16.0
pydantic_core==2.46.4
Pygments==2.21.0
PyJWT==2.13.0
pylsqpack==1.0.0
PyNaCl==1.6.2
pyOpenSSL==26.4.0
pyproject_hooks==1.2.0
pytest==9.0.2
pytest-cov==7.1.0
pytest-split==0.11.0
pytest-timeout==2.4.0
pytest-xdist==3.8.0
python-dateutil==2.9.0.post0
python-dotenv==1.2.4
python-multipart==0.0.32
PyYAML==6.0.3
referencing==0.37.0
requests==2.34.2
rich==15.0.0
rich-toolkit==0.20.6
rignore==0.8.1
rpds-py==2026.6.3
ruff==0.12.0
runpod==1.12.0
runpod-lifecycle @ git+https://github.com/banodoco/runpod-lifecycle.git@db79345536985c701b7aff2eb5eec36667aae204
s3transfer==0.19.2
scenedetect==0.6.4
SecretStorage==3.5.0
sentry-sdk==2.72.0
service-identity==26.1.0
setuptools==80.9.0
shellingham==1.5.4
six==1.17.0
sniffio==1.3.1
starlette==1.9.0
tenacity==9.1.4
tomli==2.5.0
tomlkit==0.15.2
tqdm==4.70.0
tqdm-loggable==0.4.1
truststore==0.10.4
typer==0.27.3
typing-inspection==0.4.4
typing_extensions==4.16.0
urllib3==2.7.0
uvicorn==0.54.0
uvloop==0.23.0
watchdog==6.0.0
watchfiles==1.3.0
wcwidth==0.9.2
websockets==16.1.1
wheel==0.46.3
xxhash==4.0.1
yarl==1.25.1
zopfli==0.4.3
```

The final builder verified all 164 normalized names are installed (166 total
distributions including the three product distributions), no dependency was
downloaded/guessed/upgraded, and the copied private tree is symlink-free.
The final full RECORD audit passed: 166 records, 16,139 rows, contained and
hash-valid. Product wheel bytes and installed RECORD rows matched for Agent,
Runtime, and Runtime client; all eight required installed origins resolved
under private site-packages. No shared venv, Runtime checkout, node_modules,
or old profile file was written.

## Reconstruction recipe

1. Start from the exact two-parent source above; verify the nine approved D13
   blobs against 5be and every other path against current 566, with a clean
   worktree.
2. Materialize the unchanged 164-entry lock above; verify its SHA-256 before
   installing. Reuse only the recorded compatible Runtime b92 and client 95
   wheels/hashes. The prior staged wheel inventory was Runtime
   `12df5464...`, client `567605b1...`; do not substitute the old Agent
   `fa2f824d...` wheel.
3. Build the Agent wheel only in a private destination with
   `python -I -B -m pip wheel --no-index --no-build-isolation --no-deps`,
   using setuptools 80.9.0, wheel 0.46.3, and build 1.4.0.
4. Install only into that private venv with
   `python -I -B -m pip install --no-index --no-deps --force-reinstall`.
   Rewrite inherited launchers to the private interpreter and refresh their
   private RECORD rows; never symlink a shared venv or use checkout/PYTHONPATH
   authority.
5. Verify wheel/installed byte identity, all RECORD paths/hashes/containment,
   eight origins, isolated sys.path, source/profile hashes, disk, and the
   exact Runtime/client hashes. Native, socket, browser, render, credential,
   and full-suite qualification remain downstream and unclaimed.

The final builder's machine-readable preflight and audit outputs were at the
private profile's `preflight.txt` and `audit.txt` while the worker record
was live; this flat closure is the durable release record and does not rely on
retaining the large scratch trees.

## Preserved limitations

No product code changed. No new test body, install, shared dependency, native
run, browser run, render, socket, or full suite was run by this release task.
The final profile is a build/install handoff, not D13 qualification. The
private311 diagnostic remains a recorded +96 failure, and its earlier source8afe
attempt remains UNKNOWN.

