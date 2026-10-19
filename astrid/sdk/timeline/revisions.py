"""Composition revision refs and the immutable Runtime history read adapter.

The commit-history route records accepted publication edges separately from the
immutable content revision.  In particular, two accepted writes may reuse one
content revision, so publication identities must survive this adapter's read
model.  Older Runtime clients still get the parent-link fallback below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from astrid.sdk.timeline._common import TimelineEditError

_SOURCE_PREFIXES: tuple[tuple[str, str], ...] = (
    ("authoring-parent-revision-", "astrid"),
    ("astrid.editor.timeline.", "app"),
    ("reigh.editor.timeline.", "app"),
    ("restore-", "restore"),
)
# The prefix a revision id carries, so that a short id can match the part after it.
_ID_PREFIXES: tuple[str, ...] = tuple(prefix for prefix, _ in _SOURCE_PREFIXES)
CANNOT_LIST = (
    "this Runtime cannot list revisions (it serves a composition revision by id and names no parent, "
    "so history cannot walk back from the head)"
)
_UNREPORTED_PROVENANCE = object()


@dataclass(frozen=True)
class Revision:
    id: str
    source: str  # "astrid" (authoring-parent-revision-*), "app" (astrid.editor.timeline.*), "restore" (restore-*), "other"
    created_at: str | None
    parent: str | None
    message: str | None
    publication_id: str | None = None
    previous_publication_id: str | None = None
    restored_from_revision_id: str | None = None
    provenance: Mapping[str, Any] | None = None
    is_current_head: bool | None = None
    content_digest: str | None = None


def publisher_identity(provenance: Any) -> str | None:
    """Return accepted publisher identity from Runtime provenance, if present."""
    if not isinstance(provenance, Mapping):
        return None
    publisher = provenance.get("publisher")
    if isinstance(publisher, str) and publisher:
        return publisher
    if isinstance(publisher, Mapping):
        kind, identity = publisher.get("kind"), publisher.get("id")
        if kind in {"agent", "human"} and isinstance(identity, str) and identity:
            return f"{kind}:{identity}"
    return None


def revision_source(revision_id: str, provenance: Any = _UNREPORTED_PROVENANCE) -> str:
    """Classify a revision, preferring explicit accepted publication provenance."""
    if isinstance(provenance, Mapping):
        if _text(provenance.get("via")):
            return provenance["via"]
        source = provenance.get("source")
        if isinstance(source, Mapping) and _text(source.get("via")):
            return source["via"]
    if provenance is not _UNREPORTED_PROVENANCE:
        return "other"
    for prefix, source in _SOURCE_PREFIXES:
        if revision_id.startswith(prefix):
            return source
    return "other"


class RevisionStore(Protocol):
    """The adapter. ``list`` returns None when this store cannot list revisions."""

    def head(self, project: str, timeline: str) -> str: ...

    def get(self, project: str, timeline: str, revision_id: str) -> Revision: ...

    def list(self, project: str, timeline: str, *, limit: int = 50) -> list[Revision] | None: ...


def _text(value: Any) -> str | None:
    return str(value) if isinstance(value, str) and value else None


class RuntimeRevisions(RevisionStore):
    """Read immutable revisions and accepted history through the timelines client."""

    def __init__(self, client: Any):
        self._client = client

    def _open(self, project: str, timeline: str, revision_id: str | None) -> Mapping[str, Any]:
        opened = self._client.open_composition(project, timeline, revision_id=revision_id, limit=1)
        if not getattr(opened, "ok", False) or not isinstance(getattr(opened, "data", None), Mapping):
            error = getattr(opened, "error", None)
            detail = getattr(error, "message", None) or str(error or "no answer")
            if revision_id is None:
                raise TimelineEditError(f"could not read the head of {timeline!r} in {project!r}: {detail}")
            raise TimelineEditError(f"no revision {revision_id!r} on {timeline!r} in {project!r}: {detail}")
        return opened.data

    def head(self, project: str, timeline: str) -> str:
        commits = self._commit_reader(project, timeline)
        if commits is not None:
            page = self._result_data(commits(project, timeline, cursor=None, limit=1),
                                      timeline=timeline, operation="read")
            head_data = page.get("head") if page else None
            head = _text(head_data.get("revision_id")) if isinstance(head_data, Mapping) else None
            if head is not None:
                return head
        compact = getattr(self._client, "head_canonical", None) or getattr(self._client, "head", None)
        if callable(compact):
            result = compact(project, timeline)
            data = getattr(result, "data", result)
            if not getattr(result, "ok", True) or not isinstance(data, Mapping):
                raise TimelineEditError(f"could not read the head of {timeline!r} in {project!r}")
            head = _text(data.get("revision_id") or data.get("head_revision_id"))
        else:
            data = self._open(project, timeline, None)
            summary = data.get("summary") or {}
            head = _text(summary.get("head_revision_id") or summary.get("revision_id"))
        if head is None:
            raise TimelineEditError(f"{timeline!r} in {project!r} has no published head yet")
        return head

    def get(self, project: str, timeline: str, revision_id: str) -> Revision:
        data = self._open(project, timeline, revision_id)
        summary = data.get("summary") or {}
        provenance = summary.get("provenance", _UNREPORTED_PROVENANCE)
        actual_id = _text(summary.get("revision_id")) or revision_id
        head_id = _text(summary.get("head_revision_id"))
        current = summary.get("is_current_head") if isinstance(summary.get("is_current_head"), bool) else (
            actual_id == head_id if head_id is not None else None
        )
        return Revision(
            id=actual_id,
            source=revision_source(actual_id, provenance),
            created_at=_text(summary.get("created_at")) or _text(summary.get("accepted_at")),
            parent=_text(summary.get("previous_revision_id")) or _text(summary.get("parent_revision_id")),
            message=_text(summary.get("message")) or _text(summary.get("label")),
            publication_id=_text(summary.get("publication_id")),
            previous_publication_id=_text(summary.get("previous_publication_id")),
            restored_from_revision_id=_text(summary.get("restored_from_revision_id")),
            provenance=None if provenance is _UNREPORTED_PROVENANCE else provenance,
            is_current_head=current,
            content_digest=_text(summary.get("content_digest")),
        )

    def list(self, project: str, timeline: str, *, limit: int = 50) -> list[Revision] | None:
        commits = self._commit_reader(project, timeline)
        if commits is not None:
            return self._list_commits(project, timeline, limit=limit, reader=commits)
        head = self.get(project, timeline, self.head(project, timeline))
        if head.parent is None:
            return None  # no revision names its parent, so there is no walk to make
        out: list[Revision] = [head]
        seen = {head.id}
        current = head
        while current.parent is not None and len(out) < limit:
            if current.parent in seen:  # a cycle in stored data must not loop forever
                break
            current = self.get(project, timeline, current.parent)
            seen.add(current.id)
            out.append(current)
        return out

    def _commit_reader(self, project: str, timeline: str) -> Any | None:
        """Find the frozen commit-history read on direct or wrapped clients."""
        direct = getattr(self._client, "list_timeline_commits", None)
        if callable(direct):
            return direct

        # RemoteTimelines is the product adapter around WorkspaceClient. The
        # generated client is intentionally not edited in this repo; consume
        # its new read method when Runtime integration supplies it.
        workspace = getattr(self._client, "_client", None)
        generated = getattr(workspace, "_generated", None)
        generated_reader = getattr(generated, "list_timeline_commits", None)
        if not callable(generated_reader):
            return None
        project_id, timeline_id = project, timeline
        resolve_scope = getattr(self._client, "resolve_scope", None)
        if callable(resolve_scope):
            scope = resolve_scope(project, timeline)
            scope_data = self._result_data(scope, timeline=timeline, operation="resolve")
            if scope_data is not None:
                project_id = scope_data.get("project_id") or scope_data.get("project_ref") or project
                timeline_id = scope_data.get("timeline_id") or timeline

        def read(_project: str, _timeline: str, *, cursor: str | None = None, limit: int = 50) -> Any:
            return generated_reader(project_id, timeline_id, cursor=cursor, limit=limit)

        return read

    @staticmethod
    def _result_data(result: Any, *, timeline: str, operation: str) -> Mapping[str, Any] | None:
        """Unwrap DomainResult or generated-client mappings without guessing errors."""
        if isinstance(result, Mapping):
            return result
        if not getattr(result, "ok", False):
            error = getattr(result, "error", None)
            detail = getattr(error, "message", None) or str(error or "no answer")
            raise TimelineEditError(f"could not {operation} revisions of {timeline!r}: {detail}")
        data = getattr(result, "data", None)
        if isinstance(data, Mapping):
            return data
        if data is None:
            return None
        raise TimelineEditError(f"Runtime {operation} returned an invalid revision page")

    @classmethod
    def _history_revision(cls, row: Mapping[str, Any], *, head: Mapping[str, Any] | None) -> Revision:
        revision_id = _text(row.get("revision_id"))
        if revision_id is None:
            raise TimelineEditError("Runtime revision history omitted a revision id")
        previous = row.get("previous")
        if not isinstance(previous, Mapping):
            previous = {}
        receipt = row.get("receipt")
        if not isinstance(receipt, Mapping):
            receipt = {}
        source = row.get("source", _UNREPORTED_PROVENANCE)
        provenance = row.get("provenance", source)
        head_revision = _text((head or {}).get("revision_id"))
        head_publication = _text((head or {}).get("publication_id"))
        publication_id = _text(row.get("publication_id"))
        return Revision(
            id=revision_id,
            source=revision_source(revision_id, provenance),
            created_at=_text(row.get("created_at")) or _text(receipt.get("created_at")),
            parent=_text(previous.get("revision_id")) or _text(row.get("previous_revision_id")),
            message=_text(row.get("message")) or _text(row.get("label")),
            publication_id=publication_id,
            previous_publication_id=_text(previous.get("publication_id")) or _text(row.get("previous_publication_id")),
            restored_from_revision_id=_text(row.get("restored_from_revision_id")),
            provenance=None if provenance is _UNREPORTED_PROVENANCE else provenance,
            is_current_head=(publication_id == head_publication if head_publication is not None
                             else revision_id == head_revision if head_revision is not None else None),
            content_digest=_text(row.get("content_digest")),
        )

    @classmethod
    def _list_commits(cls, project: str, timeline: str, *, limit: int, reader: Any) -> list[Revision] | None:
        """Read all pages to reconstruct newest-first publication ancestry.

        The frozen history route is bounded by a fixed head and returns items
        in acceptance order. Fetching its cursor chain before reversing avoids
        treating a reused content revision as a duplicate or as a new parent.
        """
        if limit <= 0:
            return []
        rows: list[Mapping[str, Any]] = []
        head: Mapping[str, Any] | None = None
        cursor: str | None = None
        seen_cursors: set[str] = set()
        while True:
            page = cls._result_data(reader(project, timeline, cursor=cursor, limit=min(200, max(50, limit))),
                                     timeline=timeline, operation="list")
            if page is None:
                return None
            raw_items = page.get("items")
            if not isinstance(raw_items, list):
                raise TimelineEditError("Runtime revision history returned invalid items")
            rows.extend(row for row in raw_items if isinstance(row, Mapping))
            raw_head = page.get("head")
            if isinstance(raw_head, Mapping):
                head = raw_head
            next_cursor = page.get("next_cursor")
            if not isinstance(next_cursor, str) or not next_cursor or next_cursor in seen_cursors:
                break
            seen_cursors.add(next_cursor)
            cursor = next_cursor

        revisions = [cls._history_revision(row, head=head) for row in rows]
        by_publication = {revision.publication_id: revision for revision in revisions
                          if revision.publication_id is not None}
        head_publication = _text((head or {}).get("publication_id"))
        if head_publication is not None and head_publication in by_publication:
            ordered: list[Revision] = []
            seen: set[str] = set()
            current = by_publication[head_publication]
            while current.publication_id is not None and current.publication_id not in seen:
                seen.add(current.publication_id)
                ordered.append(current)
                previous = by_publication.get(current.previous_publication_id)
                if previous is None:
                    break
                current = previous
            revisions = ordered + [revision for revision in revisions
                                   if revision.publication_id not in seen]
        elif head is not None:
            # Legacy-shaped pages may mark the head without publication IDs.
            head_revision = _text(head.get("revision_id"))
            marked = next((revision for revision in revisions
                           if revision.id == head_revision or revision.is_current_head is True), None)
            if marked is not None:
                revisions = [marked, *[revision for revision in revisions if revision is not marked]]
        return revisions[:limit]


def split_ref(text: str) -> tuple[str, str | None]:
    """``TL@prev`` → ``("TL", "prev")``; ``TL`` → ``("TL", None)``. The last ``@`` splits."""
    name, sep, rev = text.rpartition("@")
    if not sep or not name or not rev:
        return text, None
    return name, rev


def _available(revisions: list[Revision] | None) -> str:
    if revisions is None:
        return "the Runtime cannot list them"
    return ", ".join(r.id for r in revisions[:10]) or "none"


def _matches(revision: Revision, text: str) -> bool:
    if revision.id.startswith(text):
        return True
    for prefix in _ID_PREFIXES:
        if revision.id.startswith(prefix) and revision.id[len(prefix):].startswith(text):
            return True
    return False


def resolve_revision_record(project: str, timeline: str, ref: str | None, *, store: RevisionStore) -> Revision | None:
    """Resolve a history ref while retaining its accepted publication edge."""
    if ref is None or ref == "head":
        return None
    if ref == "prev" or (ref.startswith("-") and ref[1:].isdigit() and int(ref[1:]) > 0):
        steps = 1 if ref == "prev" else int(ref[1:])
        revisions = store.list(project, timeline, limit=steps + 1)
        if revisions is None:
            raise TimelineEditError(
                f"{timeline}@{ref}: {CANNOT_LIST}; @{ref} needs a revision that names its parent"
            )
        if len(revisions) <= steps:
            raise TimelineEditError(
                f"{timeline}@{ref}: only {len(revisions)} revision(s) back from the head are available "
                f"({_available(revisions)})"
            )
        if revisions and revisions[0].publication_id is not None:
            by_publication = {r.publication_id: r for r in revisions if r.publication_id is not None}
            node = revisions[0]
            seen = {node.publication_id}
            for _ in range(steps):
                previous = by_publication.get(node.previous_publication_id)
                if previous is None or previous.publication_id in seen:
                    raise TimelineEditError(
                        f"{timeline}@{ref}: publication ancestry is unavailable; use an explicit revision id"
                    )
                seen.add(previous.publication_id)
                node = previous
            return node
        return revisions[steps]
    if ref.startswith("-"):
        raise TimelineEditError(f"{timeline}@{ref}: not a revision ref (use prev, -N with N>0, head, or an id prefix)")

    revisions = store.list(project, timeline, limit=200)
    if revisions is None:
        try:
            return store.get(project, timeline, ref)
        except TimelineEditError as exc:
            raise TimelineEditError(
                f"{timeline}@{ref}: {CANNOT_LIST}, so only a full revision id resolves here ({exc})"
            ) from None
    # One immutable revision may occur at several accepted publications. An
    # explicit revision ref names the content, so retain the newest matching
    # event rather than reporting a false ambiguity; history still exposes
    # every publication edge to undo callers.
    found_by_id: dict[str, Revision] = {}
    for revision in revisions:
        if _matches(revision, ref):
            found_by_id.setdefault(revision.id, revision)
    found = list(found_by_id.values())
    if len(found) == 1:
        return found[0]
    if not found:
        raise TimelineEditError(f"{timeline}@{ref}: no revision matches; available: {_available(revisions)}")
    raise TimelineEditError(
        f"{timeline}@{ref}: ambiguous, matches {', '.join(r.id for r in found[:5])}"
    )


def resolve_revision(project: str, timeline: str, ref: str | None, *, store: RevisionStore) -> str | None:
    """Resolve a ref to its immutable revision id; ``None`` means the head."""
    revision = resolve_revision_record(project, timeline, ref, store=store)
    return revision.id if revision is not None else None
