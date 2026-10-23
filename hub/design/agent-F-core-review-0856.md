# F-core review — PASS

Independent review of `tl/agt-F-core-0847` commit
`e1aff378381ef55629944a913859334864346f89` against base
`e837e18c5156e762eca05e6d9bb15779cf847b60` passed.

The commit contains only the three authorized production files. The live
Remotion generator carrier uses `_effect_registry.main()`, which now enters the
server-owned `remotion_render_lock` boundary. The boundary preserves inherited
direct-child lock handling while the underlying lock remains non-recursive.
Attempt-root ownership uses Runtime `platform.current_user()`. No allowlist,
raw `os.getuid`, source/test/fixture/baseline/contract/pin, or unrelated lock
escape was introduced. C0/fullv2 request and reply surfaces are outside the
diff and remain untouched.

Evidence: exact targeted acceptance `16 passed in 24.95s`; Ruff
`2149/2149`; mypy baseline `1912/1912`; vendor lock, artifact manifest, and
`git diff --check` all passed. Scoped Ruff reports six pre-existing findings
only at unchanged lines of `remotion_runtime.py`. No full/browser/render
suite was run.
