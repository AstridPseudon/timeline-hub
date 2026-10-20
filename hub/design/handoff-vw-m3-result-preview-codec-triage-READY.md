# Review required — one central native decoder calibration

Prepared, NOT run. No product source edits or new suite registration. Read REPORT.md before approval. Source freeze includes current App integration, diagnostic donors, installed executable directory bytes (Chromium141 and Chrome155), Node20, complete installed playwright-core tree and retained MP4. No automatic refreeze on source movement. Node source-only --verify-sources is allowed offline.

Proposed manager-only suites.conf line:

```text
app e2e-viewing-result-decoder-calibration env VIEWING_DECODER_CALIBRATION=same-managed-bytes-diagnostic-only VIEWING_BROWSER_FLOCK_HELD=1 flock -x /tmp/timeline-viewing-browser.lock bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-result-preview-codec-triage/setup-decoder-calibration.sh
```

After review, absent manager QUIET, approved freeze/source hold, and creating this unique grant file (worker has NOT created it):
`workers/vw-m3-result-preview-codec-triage/READY_GRANTED__decoder-calibration`.

One exact central command, only after manager registers the stanza and grants it:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-result-preview-codec-triage e2e-viewing-result-decoder-calibration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

If wait returns124, wait again on R, never resubmit. The script is foreground and must finish its postflight before central snapshot deletion. One-shot marker forbids a repeat. Observe `decoder-result.json`; exit0 means six observations completed and sources stayed frozen, **not a native positive**. Native positive requires `outcome=decoded-seek`, readyState≥2, error null, correct dimensions, currentTime0.5 in a case. All outcomes, including timeouts/errors, remain visible. No exception eligible from canPlayType or FFmpeg decode alone. Calibration routes complete immutable bodies; real HTTP stream/cancellation causality remains outside its claim.
