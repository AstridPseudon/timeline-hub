# Runtime carrier compatibility proof repair

The five reported failures are conservative false negatives for exact Agent
`3730d0bd51686a1692450359482205df64dcc839`, schema SHA-256
`f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`.
Normal generation and both artifact checks now succeed without bypasses.
Independent review remains required; this report does not authorize composition
or public adoption.

Runtime base: `7f6dd8920e1ceec41b137358df5e7fecc304888d`.
Worker: `/home/user/work/wt/rt-m2-carrier-compatibility-proof-repair`.
Only `generators/command_schema_compatibility.py` and
`tests/test_command_schema_compatibility.py` change.

The proof uses transitivity. Let A be the digest-checked public 0.2.2 floor.
Construct B by adding precisely the existing five historical alternatives to A:
`asset` alongside `clip|track`, the standalone shot alternative at the four
identity definitions, and occurrence tracks alongside parent tracks for
`track.set`. These additions preserve every old alternative. The changed
definitions occur positively in this exact floor; the unaffected `oneOf` and
conditional predicates do not depend on those definitions. Thus A is contained
in B. The existing conservative checker then proves the *complete* B is
contained in f802. Its four patterns retain the exact historical pattern as a
regex alternative; its `track.set` union retains the complete historical v1
clause. The same generic checker independently proves all newer floors.

The helper first attempts the ordinary direct proof, preserving acceptance of
an unchanged 0.2.2 schema. It never rewrites the candidate. No error allowlist,
new regex inference, sample-based proof, new frozen snapshot, fixture-file
change, or generator bypass is introduced. The helper remains specialized to
the exact historical floor whose digest the generator checks.

One related strictness defect was repaired: equality of `.get()` results used
to equate an absent keyword with an explicit null keyword. Equal keyword values
now short-circuit only when the keyword exists on both sides. Unknown keyword
addition/removal with null therefore requires review. Existing annotations
retain their established treatment.

Focused tests cover all five complete floors, input immutability, all four
pattern branches removed/narrowed or constrained by a sibling, v1 clause
removal/version narrowing/select narrowing/args-ref narrowing, closed argument
property removal, unknown null siblings, operation removal, and modified
0.2.2/0.2.3/S2 floors refused before any write in generation and check modes.

Validation (all Python commands use the read-only shared Runtime venv):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-carrier-proof-pytest-final-focused tests/test_command_schema_compatibility.py tests/test_artifact_manifest.py tests/test_generated_client.py::test_generator_is_reproducible tests/test_generated_client.py::test_python_client_source_is_tracked_and_generated_check_is_not_self_referential
```

Result: **169 passed in 148.23s (2:28)**; exit 0, no skips or xfails.

Public 0.2.13 worktree checks:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B generators/generate.py --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B scripts/artifact_manifest.py --check
git diff --check
```

All exit 0. The normal-generation byte-preservation tests also remain ordinary
passing assertions. Public schema SHA-256 stays
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`;
public artifact-manifest SHA-256 stays
`129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`.
Release metadata remains 0.2.13.

Exact private evidence lives outside the repository in:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-carrier-compatibility-proof-repair`.
For the commands below, set `PROOF_WORKER` to that directory and `PROOF_ROOT`
to the worker worktree above. The isolated `private-f802` directory was built
with `git archive HEAD`, overlaid with the repaired helper and the exact Agent
schema read using:

```bash
git -C /home/user/peteromallet/astrid-agent show 3730d0bd51686a1692450359482205df64dcc839:astrid/core/timeline/schema/edit-command.schema.json > /tmp/carrier-proof-f802.json
```

Inside `private-f802`, these commands all exit 0:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B generators/generate.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B generators/generate.py --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B scripts/artifact_manifest.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B scripts/artifact_manifest.py --check
```

The manifest command records genuinely generated outputs. No renderer was
called directly. Final normal generation/check were also rerun using the
absolute archived script paths; `private-generation.log` records the outputs.
Generated bundle SHA-256 is
`3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425`,
matching the peer's reported bundle. Its packaged command schema equals exact
f802 as JSON.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PROOF_ROOT" /home/user/work/venv-runtime/bin/python -B "$PROOF_WORKER/check_exact_f802.py" "$PROOF_ROOT" "$PROOF_WORKER/private-f802"
```

Exit 0: zero errors against all five floors; four exact historical pattern
alternatives and all twelve complete S2 v1 clauses retained; **32 exact-carrier
removal/narrowing negatives rejected**. This script checks structure and the
same containment proof, not sampled instances. Output is retained in
`exact-f802-results.txt`.

`ruff check --no-cache generators/command_schema_compatibility.py tests/test_command_schema_compatibility.py`
exits 1 with six SIM114 findings and one I001. Running Ruff on each original
file via `git show HEAD:<path> | ruff check --no-cache --stdin-filename <path> --output-format concise -`
reproduces exactly those seven pre-existing findings. No unrelated formatting
rewrite was made.

The first focused run had 166 passes and one new-test typo failure (a
nonexistent `muted` property); it was corrected to remove the actual nested
`values.label` property. A subsequent selection including the whole generated
client file was interrupted (exit 130, at 30%, still in compatibility tests)
after inspection found later tests start localhost daemons. The final command
above selects only the two generator nodes. No localhost test was run, no full,
broad, or matrix suite was requested, and no shared dependencies were written.

Exact patch: `proof-repair.patch` in the worker evidence directory, SHA-256
`c7b03ebd748a42a8677aa0d8dad9e0f8c7bf4889520396088ae76ea4b8cb7be6`.
Patched helper SHA-256:
`57cfb2e5c8cf50be2d5c47ec815e7e0f5d1109dc41bfb405402889a4dd11b90b`.
Patched focused test SHA-256:
`bcb43bded5a4813b73c0bf0baeeeb5f27b38f36c5b6978b3087beb02ed029f04`.
Commit text is supplied as both `commit-msg` and `commit-msg.txt`.

No task blocker remains. Next: independently review this proof repair, then
compose it with carrier peer commit
`5f22672153253ea11cf35f92590c408ea7bba556` (tree
`e40f0108feea6c681b10d607ae4b1ed198c4e908`) under manager ownership.
The peer worktree was not modified. Its four xfail cases remain rejected:
restore the two normal-generation cases and the legacy-floor case to ordinary
assertions using this repair; separately resolve the public-013 typed-claim
refusal control against its actual public artifact while qualifying private
acceptance. Do not treat any of those xfails as approval. Exact paired native
qualification and counterpart review remain outside this bounded proof task.
No release, pin, merge, push, commit, or ref change was performed.
