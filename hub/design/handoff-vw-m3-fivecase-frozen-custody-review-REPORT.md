# vw-m3-fivecase-frozen-custody-review

## Verdict: REJECT / fail closed

The seven-file test/process custody delta at `05de08cecabeaea2d0d955475e6190acc685111a` is test-green, but not custody-ready. The App source/tree override accepts any full SHA pair; `assertExactGraph` uses that selected source as the `merge-base` and leaf-diff base. Selecting the candidate itself (`05de08...` / `496e820b...`) makes the seven-file diff empty, bypassing proof that it is a leaf over approved current App `20ea14...` / `83cfad...`. Selecting approved current App correctly rejects because the candidate HEAD differs. This repeats the recorded owner/leaf blocker.

The other requested controls are present: absent-vs-blank App selection, exact source/tree checks, Runtime server `8f105c26...` versus producer `2c4ac180...` and 75 artifacts, Agent d0 lock/whole graph/six peers, Composition public13 with 77 regular members, Node20, Chrome155, fresh grant/one-shot marker wiring, and exactly-five discovery. Focused guard tests and discovery passed; no `--ready`, grant, capture, browser, render, install, or full suite ran. No owner handoff is issued from a rejected review.

See the worker report and file list:

- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-fivecase-frozen-custody-review/REPORT.md
- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-fivecase-frozen-custody-review/FILELIST.md

