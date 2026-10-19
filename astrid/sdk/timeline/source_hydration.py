"""Exact source hydration shared by saved replay and the semantic receiver.

Only command declarations reach the request-bound COMMIT port. Journal
attachments are refetched separately and never extend that capability.
"""
import copy


def _runtime_transcript_resolver(request, closure, history, *, document_reader, object_reader):
    """Internal adapter for Runtime-owned exact reads, never caller receipts.

    Runtime supplies the authenticated immutable base/history and restricted
    readers. The existing resolver remains the sole private capture minter and
    record codec; no serialized value crosses this boundary as authority.
    """
    from types import SimpleNamespace
    from astrid.sdk.timeline.commit import RuntimeCommitService
    from astrid.sdk.timeline.transcripts import RequestBoundTranscriptResolver, verify_pinned_entries

    port = SimpleNamespace(revision_closure=lambda revision: copy.deepcopy(closure))
    base = RuntimeCommitService._load_revision(port, request, request["base_revision_id"])
    references = []
    for entries in history:
        references.extend(entry["selection"] for entry in
                          verify_pinned_entries(request["project_id"], entries).values())
    return RequestBoundTranscriptResolver(request,
        SimpleNamespace(get_document=document_reader), SimpleNamespace(get_object=object_reader),
        accepted_base=base, accepted_history=references)


def hydrate_sources(port, request, base, calls, *, parent_loader=None, include_base=True):
    from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
    from astrid.sdk.timeline.graph_commands import request_sources
    refs = request_sources(calls)
    imports, shots = {}, {}
    for ref in refs:
        if "timeline_id" in ref:
            imports[ref["parent_revision_id"]] = RuntimeCommitService._load_duplicate_source(port, request, ref)
        elif "parent_revision_id" in ref:
            rid = ref["parent_revision_id"]
            if include_base and request["base_revision_id"] not in imports:
                imports[request["base_revision_id"]] = copy.deepcopy(base)
            if rid == request["base_revision_id"]:
                continue
            if rid not in imports:
                imports[rid] = (parent_loader(rid) if parent_loader else
                                RuntimeCommitService._load_revision(port, request, rid))
        else:
            shots[_digest(ref)] = RuntimeCommitService._load_shot_source(port, request, ref)
    if imports:
        base["source_mapping"]["imports"] = copy.deepcopy(imports)
    if shots:
        base["source_mapping"]["pinned_shots"] = copy.deepcopy(shots)
    hydrate_transcript_sources(port, request, base, calls)
    return imports, shots


def journal_sources(workspace, request, base, row):
    from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
    from astrid.sdk.timeline.saved_intent import SavedIntentError
    from astrid.sdk.timeline.saved_publish import _ClosurePort, _exact
    entries = [e for e in row.get("evidence", []) if e.get("kind") == "immutable-source-imports-v1"]
    if not entries:
        return
    if len(entries) != 1:
        raise SavedIntentError("ambiguous immutable source provenance")
    entry = entries[0]
    imports, shots = {}, {}
    port = _ClosurePort(workspace, request["project_id"], request["timeline_id"])
    for rid, evidence in entry["documents"].items():
        if evidence.get("project_id") != request["project_id"] or evidence.get("base_parent", {}).get("revision_id") != rid:
            raise SavedIntentError("source provenance has wrong exact scope")
        if evidence.get("timeline_id") != request["timeline_id"]:
            ref = evidence.get("source_mapping", {}).get("duplicate_source")
            fetched = RuntimeCommitService._load_duplicate_source(port, request, ref)
        else:
            fetched = _exact(workspace, request, rid, base_document=evidence)
        # Journal bytes select only locators. Authenticated closures must
        # reconstruct them exactly before they can participate in replay.
        if fetched != evidence:
            raise SavedIntentError("journal source differs from authenticated exact closure")
        imports[rid] = fetched
    for token, evidence in entry.get("shots", {}).items():
        ref = evidence.get("selection")
        fetched = RuntimeCommitService._load_shot_source(port, request, ref)
        if _digest(ref) != token or fetched != evidence:
            raise SavedIntentError("journal shot differs from authenticated exact closure")
        shots[token] = fetched
    transcripts = entry.get("transcripts", {})
    if transcripts:
        from astrid.sdk.timeline.transcripts import verify_pinned_entries
        verify_pinned_entries(request["project_id"], transcripts)
        # Re-capture only command/base declarations. An unaccepted journal is
        # a locator; even hash-correct bytes never authorize an old revision.
        fetched = hydrate_transcript_sources(port, request, base, request["change"]["commands"])
        if any(fetched.get(key) != value for key, value in transcripts.items()):
            raise SavedIntentError("journal transcript differs from authenticated exact capture")
    if imports:
        base["source_mapping"]["imports"] = imports
    if shots:
        base["source_mapping"]["pinned_shots"] = shots


def hydrate_transcript_sources(port, request, base, calls):
    """Capture only declared new sources and authenticated accepted dependencies."""
    from astrid.sdk.timeline._common import TimelineEditError
    from astrid.sdk.timeline.commit import _digest
    from astrid.sdk.timeline.transcripts import (
        FrozenTranscriptSource,
        base_selections,
        inverse_selections,
        request_selections,
    )
    selections = {**base_selections(request["project_id"], base), **request_selections(request, calls),
                  **inverse_selections(request["project_id"], calls)}
    if selections and hasattr(port, "bind_transcript_request"):
        port.bind_transcript_request(request, base)
    pinned = {}
    for key, selection in selections.items():
        capture = port.resolve_transcript_source(request, selection)
        if (not isinstance(capture, FrozenTranscriptSource) or capture.selection != selection
                or capture.request_digest != _digest(request)):
            raise TimelineEditError("transcript capture differs from this request/source")
        pinned[key] = capture.entry()
    if pinned:
        # Preserve accepted old sources through rebinding and inverse generation.
        base["source_mapping"].setdefault("pinned_transcripts", {}).update(copy.deepcopy(pinned))
    return copy.deepcopy(base["source_mapping"].get("pinned_transcripts", {}))
