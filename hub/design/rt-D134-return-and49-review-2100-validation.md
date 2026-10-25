# D134 independent protected review

## Verdicts

- A inverse7: PASS.
- B history5: PASS, with M1 behavior still UNKNOWN.
- C Runtime49 source assessment: PASS; 27 FIXTURE_SETUP, 22 UNKNOWN, 0 proved product gaps.

The original 2045 packets and independent 2046 `FAIL_AUTHORITY_CLAIMS` packet
were read and preserved. They were not overwritten and their prior errors were
not converted into functional qualification.

## Source and scope checks

Commands/results:

```text
git diff --check a30e74e901a28b39c28facba3deb00d76f186e23..tl/rt-D134-inverse7-return-2053 --
PASS
git diff --check a30e74e901a28b39c28facba3deb00d76f186e23..tl/rt-D134-history5-return-2053 --
PASS
```

A finalized commit `9a7c9e38cf` changes only
`test_inverse_stage_runtime_regressions.py`. B’s review scope covers Gate1,
prepared-video, and M1; finalized commit `9e85402544` changes only the first
two, while M1’s source SHA-256 is identical before and after:
`838c77332683358877059f1357267a49cd130a985be4e4755a9655ec3f930d01`.

The reviewed A source tuple is Agent `a30e74e901` plus historical Runtime
`6634a17f3f`; A’s `use_runtime(commit=RUNTIME_COMMIT)` selects that exact
immutable Runtime object. The reviewed B tuple is current Agent `a30e74e901`
plus Runtime `ab1e4f6141`; Gate1’s `use_runtime(commit=NORMAL_RUNTIME)` agrees
with `runtime.lock.json`, and prepared-video’s vendored pin, `use_runtime`,
HEAD, and tree checks agree with the same Runtime tuple. Identity equality is
strict in both parts.

Read-only object/hash checks passed:

```text
Agent a30e commit.py SHA-256 = 2b81e46ac0f3553d1de812cf0533be2a9aecbd8cdfcaab118ac671eff75107b3
Agent a30e inverse.py SHA-256 = 6c794734cb763c21cec386f764bc63b94f3a74b4dd9f8464136a285c628d0423
Runtime 6634 auth/store SHA-256 = 4ac2b8792fe0389afb6eb710a348c35fa196131a13cab175bd3646f7d2cc0aeb / 2a68990b180326585b7f0abaf1ee54c8ff9340e83663f17cd1efff1b2bd78a5c
C per-ID source blob matches against frozen Agent a4e tree: PASS (49/49)
C first-frame source lines readable/nonblank: PASS (49/49)
```

The AST check compared the finalized branches with Agent a30:

```text
A whole-inverse assertions/raises: 45/45 and 0/0; forged: 7/7 and 2/2; native ABA: 4/4 and 1/1
B Gate1 parameter values: python, cli, sheet; roundtrip helper assertions: 15 conserved
B prepared assertions: 24 conserved; raises: 2 conserved
B M1 file SHA-256: identical; M1 assertions: 22 conserved; raises: 0
```

Ruff, private `py_compile`, and scoped mypy were reused from the finalized
workers against these exact after-file hashes (A
`c578ec36e41ec2d68fe6de8a7d3a443aab8477cbb8492f7cbd786abb9e48ddd3`; B Gate1
`3a29ab2fd37e940c4d8fd88a17f9621b188bd307774c05b69ed06411393f33cf`, prepared
`a10d730edb293def6c6a40e9852fbe68f94ae4ad5db5375bdffca82dd4453864`, M1
unchanged). All reported PASS. No broad new test lane was run.

## C source assessment

The C TSV has 49 unique rows, exact root-cluster membership (35 root-048 and
14 root-022), zero duplicate or extra IDs, zero source-blob mismatches, and
the exact frozen first-frame pairs:

```text
root-048: Agent astrid/sdk/timeline/validation.py:650 -> Runtime runtime_protocol/service.py:2546
root-022: Agent astrid/sdk/timeline/commit.py:1331 -> Runtime runtime_protocol/service.py:2546
```

Frozen sources were inspected with `git show` at Agent
`a4e016b6a9f9` / Runtime `5e9ad1c6f74`. Root-048’s 27 M1 setup rows author
`word:word-1` without the source/binding needed by the legacy lookup, so they
are fixture/setup. The eight retained-input rows and all 14 selected-PARAM
rows remain UNKNOWN because the authenticated request body, hydrated
authority/source state, accepted record, and exact failing command are absent.
The Runtime service boundary delegates to the registered provider at
`service.py:2546`; the guard location alone was not treated as causality.
D14/D23 are not blanket explanations.

Missing raw XML, full disk witness, raw runner receipt, accepted records, and
complete legitimate caller traces were preserved as missing, not reconstructed.
No product/test/fixture/media/transcript/source or protocol change was made.

## Functional boundary

Functional tests were **NOTRUN**. The mandated disk admission floor was below
5 GB, so no provider/body/collection/full/family/native/socket/browser test
was run. No product behavior or M1 closure is claimed from source review.
