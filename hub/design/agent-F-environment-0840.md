# Agent F environment repair

Status: bounded repair PASS; final full suite remains FAIL and was intentionally not rerun.

The existing Agent farm metadata now projects the read-only Runtime checkout into sanitized children through a private `/tmp/w-5829dd9212/site-packages` dependency root, and binds the existing qualified renderer runtime `agent-remotion-composition14-255b6856` with explicit Node v20.19.4. The existing startup/security guards remain active; `PYTHONNOUSERSITE` was tested and removed because the renderer guard rejects it.

Central targeted request `agt-F-environment-0840-targeted-1023084256-4579` passed the four exact representative nodes: generic host ownership, scene answers `[start-dip]`, normal audio `[full-compiled-normal_profile0]`, and normal audio sources `[30-0.06666666666666667]`; result `4 passed in 13.30s`.

The original final full result `agent-full-1023072419-4249` remains `16388 passed, 240 failed, 140 errors, 40 skipped, 5 xfailed`, exit 1. Its remaining concrete environment blocker includes three D09 tests requiring absent `/home/user/work/runtimes/agent-remotion-0013`. This worker did not create a shared alias or mutate shared runtime dependencies. The runtime owner must restore that fixture via the sanctioned route, independently verify the install, and then launch the single final full run.
