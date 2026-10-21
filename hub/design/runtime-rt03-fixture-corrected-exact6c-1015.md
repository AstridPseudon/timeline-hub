# RT03 fixture-corrected exact6c execution

Date: 2026-10-21 UTC

## Result

The single authorized corrected RT03 node reached the semantic test body, but
failed at its first dependency-manifest ordering assertion. RT03 is therefore
**not qualified**. The fixture correction is effective, but this run does not
establish the requested original unplaced owned-raw contract.

No retry, ordered sibling, fixture repair, product repair, assertion change,
marker, merge, adoption, or activation was performed after the failure.

## Exact identities

- Runtime under test: commit `ecdab2b4a10c4e9fbc4deb572f0382e54f3e6f00`,
  tree `176558a5abda7f53ee786e86f22a935f4e54b463`.
- Exact Agent consumer: commit
  `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`, at
  `/home/user/work/wt/agt-pin-6c1989ad`.
- Exact producer used for the lock check: commit
  `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`.
- Runtime, Agent, and producer checkouts were clean.

The Runtime tree contains only the already-prepared fixture-registration
commit relative to `aa0c26e`; the target import is the existing shared fixture
registration:

```python
from test_timeline_commit_integration import agent, film  # noqa: F401 (shared fixtures)
```

The target body and assertions were not changed in this task.

## Fresh preflight

All required checks passed with the exact normal tuple:

- `contract/schemas/edit-command.json`: raw SHA-256
  `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`;
  canonical SHA-256 `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`;
  65 definitions and 37 `EditCommand.allOf` clauses.
- `scripts/artifact_manifest.py --check`: current; 76 producer artifacts;
  manifest SHA-256 `0c0e3379302f5ded0bef96d9a5c7d7e72a29962d83bbb5b1500c0cfd7344e06f`;
  producer version `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Agent `vendor_lock.py check ... --producer /home/user/work/wt/rt-pin-42a7203f`:
  passed; 15 locked files matched the exact producer bytes and source commit.
- Client metadata: version `0.2.17`, schema/health digest
  `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`.
  Imports resolved to this Runtime worktree, the exact Agent checkout, and
  Agent-vendored `astrid_runtime_client`. The loaded `astrid` profile reported
  provider `astrid-v1`, interface `1`, and the matching digest.
- `pytest`, `jsonschema`, `referencing`, `yaml`, `filelock`, and `PIL` all
  resolved from `/home/user/work/venv-agent`.
- A private mode-0700 temporary directory was created and removed. Shared
  realpaths were `/home/user/work/venv-agent` and
  `/home/user/work/app/node_modules`; neither was modified. Available disk was
  `10,578,564 KiB` on both `/home/user/work` and `/tmp`.
- The exact selector collected one test. The no-body setup plan resolved the
  complete corrected closure:

  ```text
  tmp_path_factory -> tmp_path -> film
  monkeypatch -> astrid_importable
  film, astrid_importable, monkeypatch -> agent
  ```

The preflight used `PYTHONDONTWRITEBYTECODE=1`, Python `-B`, and
`-p no:cacheprovider`; no bytecode or pytest cache was written.

## Authorized execution

The one central request was:

```text
rt-m2-rt03-fixture-corrected-exact6c-1015-private017-agent6c-integration-1021101714-1635
```

It ran exactly:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
```

Result: exit 1, `1 failed in 1.25s`.

Fixture setup succeeded and the body entered the normal direct
Runtime/provider path. Existing assertions through accepted status, receipt
identity/result equality, projected reference identity/role, and empty parent
occurrences/clips passed. The first actual failure was
`tests/test_timeline_owned_reference_integration.py:160`:

```text
assert document["dependency_manifest"]["media"] == [unrelated_pin, exact_pin]
```

Observed actual order was `[exact_pin, unrelated_pin]`, with media IDs:

```text
actual first:   sha256:6e2ea6a28550bd8e44021d028e97191f3ef94e06e7b1b0b185d95c7643018b10
expected first: sha256:9b6dd332e72cde4e15dd61662c430434cc97bf61d231724f4066d02c9cffdbee
```

The unchanged test expects the unrelated media pin first, then the exact
media pin. The central log is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-rt03-fixture-corrected-exact6c-1015-private017-agent6c-integration-1021101714-1635/log.txt`

Because execution stopped at this first assertion, the later raw ownership,
role/id, exact retry, restart, no-duplicate, occupied-destination, foreign
no-write, and inverse assertions were not executed by this run. No
qualification claim is made for them.

## Disposition

The fixture import correction is proven by collection/setup and by the target
body reaching its semantic assertions. The remaining blocker is the observed
media dependency ordering mismatch, which requires the Runtime/Agent manager
to decide whether the existing expectation or the current provider behavior
is authoritative. This worker made no speculative change and did not rerun.

No full, browser, renderer, HTTP, install, generation, old44/186, live, or
ordered-sibling suite was run.
