# Runtime reciprocal review of Agent selected-reference repair

Date: 2026-10-21 UTC

## Verdict

**SOURCE ACK / APPROVE.** The committed Agent repair `1dcfa274e` is accepted
against its first parent `47b716d00` for this bounded feature delta only.

The new transition-bearing `clip.set` path now distinguishes canonical
`elementRef` from legacy `element_ref` by key presence. Both spellings are
checked independently; disagreement, present null, empty, or malformed
references fail closed. A legacy-only retained P1 remains usable, while an
unauthorized same-stable-ID P2 schema pin is refused atomically. The matching
legacy P1 case remains valid. The existing `clip.set-params` path is kept
non-strict and unchanged in behavior.

The commit does not alter schema or ordinary source behavior: schema SHA is
`9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a` (55
definitions, 29 clauses), and the ordinary floor is
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

## Evidence and limits

Focused provider tests passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_selected_param_authority.py -k 'transition_refuses or transition_accepts_matching_legacy_authority'
3 passed, 27 deselected in 11.72s
```

`git diff --check` passed for `1dcfa274e^..1dcfa274e`. No Runtime suite,
full suite, generation, pin/publication, HTTP/socket, native, browser,
renderer, or activation run was made. This ACK does not qualify a Runtime
port, generated contract, public release, or final freeze.
