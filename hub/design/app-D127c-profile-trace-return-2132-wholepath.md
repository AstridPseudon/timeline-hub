# D127c bounded source trace

Result: `NO_GO_ORIGINAL_ELEMENT` remains unchanged. The safe verdict records one completed HTTP 200 request, but provider, App response, caller receipt, and browser outcome are unknown. The published profile artifacts remain `EXACTMISSING` / `PARTIAL_EXACTMISSING`.

## First seam

The retained run fact is qualified as: the actual completed request did not cross the helper cProfile eligibility gate. In `tests/helpers/p2_commit_phase_capture.py:542-564`, `_start_profile` first requires dispatch/prefetch provenance, then `_has_element_command`, then `_is_element_request`; only after those checks does it set `request["profile_eligible"] = True`. The summary path at `:1133-1134` adds the safe `cprofile` projection only when that flag is true.

The exact failing selector predicate is `UNKNOWN`. The safe packet deliberately omits the actual command operand and private payload fields, so this trace does not name or reconstruct which `_is_element_request` predicate failed. The failed browser assertion is not treated as that selector predicate.

## Raw pstats distinction and limits

Raw pstats is optional, not required by the safe projection. The helper constructor at `tests/helpers/p2_commit_phase_capture.py:131-150,173-177` accepts `raw_pstats_sink` but defaults it to `None`; `_raw_profile_path` at `:661-693` returns no path when it is absent and otherwise applies private temporary-path checks. The normal bootstrap’s `_watchdog_options` at `scripts/testing/sitecustomize.py:20-30` returns only `watchdog_seconds`, and `_start_capture` at `:45-60` passes those options. D66 sets the helper path/hash and watchdog at `scripts/testing/d66-plain-stack.mjs:377-384,748-750`; it supplies no raw-pstats destination. Therefore the bootstrap has no raw-pstats destination, independently of the missing safe cProfile projection.

The finite safe limits are 40 functions and 1600 edges, matching the helper constants and the safe schema. No raw payload, stack, key, URL, header, args, locals, or private identifier is included here.

## Source tuple and retained hashes

The safe source manifest fixes App `b5c9eadfa1950f46feac50d7d6a89c47f27f4881` (tree `8e10af0976b012205f27a18a432c750a27de0725`), Runtime `ab1e4f6141987706132916e2da16477f5a019464` (tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`), Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` (tree `6056414359ae9fce08d999d54cbecf719fda33c3`), and helper SHA-256 `095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`. The retained source-check hashes include `sitecustomize.py` `83c28b437417753a221e0fec36047dd6bb267256366dd4acacb8ef8d8137615e` and `d66-plain-stack.mjs` `56668b2a02abffd947a9045d081e4fdc2d56c226b656c43b1e823fb182ad4def`.
