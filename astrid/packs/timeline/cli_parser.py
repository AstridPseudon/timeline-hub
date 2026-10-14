"""The timelines parser: a positional after the flags still fills the verb's open positional."""
from __future__ import annotations

import argparse
from typing import Any


class TimelinesParser(argparse.ArgumentParser):
    """``show TL --project P c41.mink``: a positional after the flags fills the verb's open positional
    (address, word, query, sheet file, asset key) instead of failing with "unrecognized arguments"."""

    def parse_args(self, args: Any = None, namespace: Any = None) -> argparse.Namespace:
        parsed, extras = self.parse_known_args(args, namespace)
        loose = [e for e in extras if not e.startswith("-")]
        if extras and len(loose) == len(extras):
            for dest in ("address", "word", "query", "sheet", "sheet_file", "key", "steps"):
                if loose and getattr(parsed, dest, "absent") is None:
                    value = loose.pop(0)
                    if dest == "steps":
                        if not value.isdigit() or int(value) < 1:
                            self.error(f"steps must be a positive integer, got {value!r}")
                        value = int(value)
                    setattr(parsed, dest, value)
            if loose and getattr(parsed, "address", None) and getattr(parsed, "command", None) == "show":
                parsed.more_addresses, loose = list(loose), []  # show TL a b c: one record each
        if loose or len(extras) != len([e for e in extras if not e.startswith("-")]):
            self.error(f"unrecognized arguments: {' '.join(extras)}")
        return parsed
