"""Modular API over the timeline working-copy implementation."""
__all__ = ["Checkout", "Clip", "Cut", "Word", "Voice", "TimelineEditError", "EDITABLE_NOTE",
           "draft_path", "drafts_root", "find_draft", "resolve_ids", "build_producer_batch",
           "capture_assembled_media"]


def __getattr__(name):
    if name == 'capture_assembled_media':
        from .native_parent_media_commands import capture_assembled_media
        return capture_assembled_media
    if name == 'build_producer_batch':
        from .producer import build_producer_batch
        return build_producer_batch
    from astrid.sdk import timeline_checkout as legacy
    if name in __all__:
        return getattr(legacy, name)
    raise AttributeError(name)
