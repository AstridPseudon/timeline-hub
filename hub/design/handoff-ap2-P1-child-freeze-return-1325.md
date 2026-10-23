# D21 child freeze identity packet

Status: packet PASS; production NOTREADY pending MAIN publication and a fresh
immutable child name.

The actual failure at `freeze-identity` was caused by the validator assuming
`pip freeze` emits `astrid==...` and `astrid-runtime==...`. The retained report
shows the real installed source distributions as PEP 610 direct references:
`astrid @ file:///.../agent` and `astrid-runtime @ file:///.../runtime`.

The complete maker packet is
`handoff-ap2-P1-child-freeze-return-1325-make-child-venv.sh`; the minimal
unified patch against the published/local maker is
`handoff-ap2-P1-child-freeze-return-1325.patch`.

The patch retains all existing bounded process-group/FIFO/stage/pip/overall
timeouts, isolated `-I` import and CLI checks, source markers and proof.lock
identity, shebang relocation, immutable publish, failed-partial retention, and
read-only finalization. It adds only:

1. installed distribution name/version checks from `importlib.metadata` and the
   archived `pyproject.toml`;
2. PEP 610 `direct_url.json` validation for the exact archived Agent and Runtime
   source directories, accepting directory provenance or a hashed wheel;
3. retained report metadata for the actual distribution/source provenance; and
4. exact report `pip freeze`/import-origin/Agent+Runtime tuple validation.

Immutable tuple:

```text
Agent       f6116e1b658514021cbbf08d5a6f16a240523f1a
Runtime     8592822fd11275540f596562f43c715676f2bc0f
proof.lock  236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778
```

Source and packet hashes:

```text
actual maker SHA-256  5d1ac4cf4bcf876a4407165672a62d7720cdc9b36ac06f5743828847becbe131
final maker SHA-256   7f66634058172ee3280d9a060d725da3c09a5408941bd383c56f5ae5ac607a7d
small patch SHA-256   ab7132c59e4098cb40cb365291e3b4ea259349839746116cf51053faabfdd35f
retained report SHA   4967689f4a783d0925f06faf159bab36c9b551105786fb86209ce37bea598faa
```

Evidence: `bash -n` PASS; exact old report fails the old grep and passes the
corrected validator; missing/wrong package, version, source, Agent identity,
and Runtime identity adversarial cases all refuse; PEP 610 metadata probe PASS;
`patch --dry-run --fuzz=0` PASS; packet whitespace check PASS. The App worktree
is clean. No real provisioning/install/download/network/service/socket/daemon/
dispatcher/full-suite command was run.

Original body guards remain byte-identical: P1 blob
`221d05890ba9f42d50520c9b655c21338aece782` (SHA-256
`f28334c1f52d145ae66792ef419ba8138a1ec013f82fd982c4633de7f3a64133`) and
Gate-5 blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1` (SHA-256
`0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`).

MAIN should apply the patch to the authoritative D21 kit and request one new
immutable child. Do not mark production ready from this packet alone.
