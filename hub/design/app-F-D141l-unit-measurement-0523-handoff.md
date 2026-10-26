# D141l handoff

## Decision

`NOT_QUALIFIED`. Keep the default heavy App full-suite floor at `5,200,000,000` available bytes and the stop at `4,000,000,000` bytes. Keep the ordinary source-only floor at `4,600,000,000` bytes. No historical full-run behavior credit is changed.

## Why

The named normal and pristine App full runs are authentic same-kind bodies, and the manager streams preserve exact observed table rows and chronology. The maximum disclosed in-body bracket is `216,776,704` bytes on `app-full-1026004326-12174`; the pristine bracket is smaller. This is not promoted to `X` because the retained format is a multi-line `df -B1` table, not the exact two-line `Avail` witness consumed by the installed validator, and there are unobserved gaps before the first sample and after the minimum. The 5433016320-byte controller admission is source-only and is excluded from body consumption.

## Current headroom

The retained source-only admission record reports `4600090624` bytes at `2026-10-26T05:28:09.988639Z`. It meets the `4600000000`-byte source-only floor by `90624` bytes and does not meet the selected `5200000000`-byte heavy floor. This is not a new measurement.

## Future route

For a future authorized heavy job, the normal request-test/test-run caller must receive a manager-owned receipt at `tests/<actual-job-id>/recorded-measured-floor.json`, bound to that job's actual HEAD, snapshot tree, repo, suite, and registered command. Use the installed `timeline.d89d.measured-floor.v1` shape with exact start/stop witness files containing the original two-line `Avail` bytes. No ID or receipt is supplied here; no attachment or kit edit was made.

## Limits and next steps

The two retained full-run `KEEP` records and all originals remain untouched. D130, D141 stop, owner-gated hub state, and the pending paired App kit are unchanged. Runtime owns any future reviewed measured-floor kit seam; a future App body may consume only an authentic receipt.
