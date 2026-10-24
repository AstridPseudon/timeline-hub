Completed **F-farm96-csv-custody**.

- Restored all 288 exact Farm tuple cells.
- Also restored 96 omitted source citations, proven identical in JSON and original `cf0218` CSV.
- Preserved every other CSV cell and all JSON bytes, including 96 IDs/order/proof references, offsets, hashes, 88+8 cohorts and 80/1/15 classifications.
- Updated source/limits documentation.

Validation:

- `python3 "$TMPDIR/validate_farm96_csv.py"` — PASS: all 2,976 mapped cells; zero blank required cells; exactly 384 changed cells; 96 qualified census memberships.
- `git diff --check` — PASS.
- No product execution, probes, suites, browser or gate runs.

Final SHA256:

```text
JSON  9b9bc96bc6309c8b98d5afa8c3582a88d38d2895f97438f407e1c5044668b896
CSV   d0dd5e799b1d18a6f051642e55077f650af068da6c5a4675b4e5e7c717913da4
MD    c3590bf62c168ae27ed5ec7cf9555c6e263ae1c32f6eadf7e33199a1c9711298
```

No blockers. Independent final review is next. Docs repair, future home qualification and v2 production-caller adoption remain unverified. Commit message and `DONE` are written; no Git mutation performed.