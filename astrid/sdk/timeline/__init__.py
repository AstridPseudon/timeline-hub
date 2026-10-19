"""Modular API over the timeline working-copy implementation."""

# Main's intent namespace has no separate take discriminator; R4's timing
# evaluators treat that absence as one ordinary line. Keep the optional R4
# accessor compatible without changing the main intent/source-window schema.
from astrid.sdk import timeline_intent as _intent

if not hasattr(_intent, "line_take"):
    _intent.line_take = lambda _clip: None
if not hasattr(_intent, "loop"):
    _intent.loop = lambda _clip: None
if not hasattr(_intent, "fixed_start"):
    _intent.fixed_start = lambda _clip: False
if not hasattr(_intent, "until_film_end"):
    _intent.until_film_end = lambda _clip: None


__all__ = ["Checkout", "Clip", "Cut", "Word", "Voice", "TimelineEditError", "EDITABLE_NOTE",
           "EditCommand", "CommandError", "draft_path", "drafts_root", "find_draft", "resolve_ids"]


def __getattr__(name):
    if name in {"EditCommand", "CommandError"}:
        from astrid.sdk.timeline import commands
        return getattr(commands, name)
    if name in __all__:
        from astrid.sdk import timeline_checkout as legacy
        return getattr(legacy, name)
    raise AttributeError(name)
