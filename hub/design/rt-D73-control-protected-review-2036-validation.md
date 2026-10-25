# D73 protected control review

## Verdict

`PASS_SOURCE_ONLY`. The revised focused tests independently cover the actual
production launcher script and the author source remains a two-line launcher
correction. No product source, dispatcher, installed entrypoint, host guard,
D130 path, or public protocol was changed.

## Source checks

- Review head: `375c773449b1c6b477f10c1daff1d9f4704208a2`, tree
  `11e5430502ff313f298522b1781811abd11ecd50`.
- Adoptable author source: `d70bb370f396f137933d3b8ae3b194588e96e2b1`, tree
  `574c11a605d5862d7458cbd49d1a1c59d995b325`.
- Launcher blob: `f1bde17ea107a8b669cb6924fbdbd2f3979da988`;
  SHA-256 `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`.
- Diff from pre-D73 base is exactly two `export PYTHONNOUSERSITE=1` to
  `unset PYTHONNOUSERSITE` replacements, one in each child shell.
- Diff from the author source to this review head contains only the focused
  test file. Existing launcher guards and old predicates are unchanged.

The real Remotion probe rejects an inherited `PYTHONNOUSERSITE` and accepts a
minimal supported clear environment with policy `clean-schema-env/v1`.

## Commands and results

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_p4_d73_pinned_launcher.py
2 passed in 0.53s

bash -n tools/p4-d73-pinned-launch.sh
PASS

/home/user/work/venv-agent/bin/ruff check tests/sdk/test_p4_d73_pinned_launcher.py
All checks passed!

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -c 'from pathlib import Path; compile(Path("tests/sdk/test_p4_d73_pinned_launcher.py").read_text(encoding="utf-8"), "tests/sdk/test_p4_d73_pinned_launcher.py", "exec"); print("private compile: PASS")'
private compile: PASS

git diff --check a30e74e901 375c773449
PASS

Minimal direct Remotion probe with HOME=/private/home and PATH=/usr/bin
poisoned override rejected: PASS
supported clear environment accepted: PASS
```

The first ad-hoc one-line probe wrapper had a shell quoting syntax error; it
did not run product code and was rerun as a heredoc with the results above.

## Boundaries and operational adoption

This is source/control evidence only. The frozen tuple body, provider,
browser, sockets, Remotion build, acquisition/install, full suite, and
production request were not run. The review therefore does not claim live
qualification.

After owner approval, adopt the author launcher through the existing
dispatcher and installed entrypoint, regenerate a manifest for the exact
four-repository tuple, and run the separately authorized live positive and
poisoned-manifest qualification. Do not silently retarget captured request
18455. No new D137 prerequisite is introduced; Product host guard and D130
remain untouched.
