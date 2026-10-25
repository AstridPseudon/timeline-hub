# D108/D77 ordinary stage continuation

- Invocation: `Installer.run("install", manifest)` through the retained Agent installer, which calls the unchanged `Backend.stage`.
- Outer timeout: 180 seconds. Elapsed: 23.594 seconds.
- Outcome: stopped at the first ordinary prerequisite failure; `HTTPError`, HTTP 403.
- Failure site: `Backend.stage` -> `install_tools` -> `_install_omp_source` -> `fetch_archive` -> `urllib.request.urlopen`.
- Missing/blocked artifact: the pinned OMP source archive for the locked source revision. The exact URL is retained only in the mode-0600 private run record; its SHA-256 is `ee8b3117370f6f2b3aa1a7f0f3ba8948113fb61fd1abc963b47cb82716c1bbdf`.
- No retry, alternate source, schema acquisition, pin change, registry change, or test weakening was performed.

## Applied source validation

The private immutable source overrides were clean and matched the required trees:

| source | local materialization commit | tree |
|---|---|---|
| Agent | `46f9c8fcf4e7168c15704438c23af97db836a603` | `523893dcf54dbe756db8fe2915d14055b1da660b` |
| Runtime | `01c0820fe802879b31548ede4b26c73707854f80` | `a522511414947e48e317a5e5c2103483b121a750` |
| VibeComfy | `31f90bb03d330283b76e7dbdda51197be787090d` | `101744f0d87eebe5ddf6752c10f01f52dc94e3e9` |

The first two local commits are private restorations of the retained applied source trees; their exact target tree hashes are the acceptance identity. All three source repositories were clean after materialization.

## Materialization evidence

- Manifest validation passed with unchanged locked tool versions and a manifest SHA-256 of `4f953f4f35c4c2924701b988da55f55315bbfadfa6e87aefb5e95f4a733c3b2b`.
- `uv --version` passed at the pinned version.
- Pinned Python venv creation passed.
- Hash-locked runtime dependency installation passed.
- Local Agent, Runtime, and VibeComfy package installation passed.
- Pinned Bun and Node version probes passed; system ffmpeg/ffprobe capability probes passed.
- The ordinary run recorded ten successful subprocess commands before the failure; the failure occurred in the archive download helper and therefore has no subprocess exit event.

## Stage outputs and controls

- Candidate stage did not return a `Version`.
- Generated `profile.json`, generated service declaration, generated `version.json`, and service argv: not produced.
- Only source-carried schema files were present; no external schema acquisition was attempted.
- Seven-key carrier: not produced, so completeness is not claimed.
- Readiness and 16/17 controls were not run because there was no actual staged candidate.

## Footprint

The failed private staging root reached `1,168,669,468` bytes, exceeding the requested 750 MB incremental bound. `/tmp` free space went from `5,957,188 KiB` before the run to `4,631,096 KiB` after it. No second attempt was made.

Raw command output, the exact URL, traceback, and manifest remain in private mode-0600 files under the scratch area, not in this evidence file.
